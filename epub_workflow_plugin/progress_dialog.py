# -*- coding: utf-8 -*-
"""
Dialog de progression pour le traitement batch
Affiche la progression et les résultats du traitement
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QTextEdit, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
import os
from pathlib import Path
from typing import List, Dict

from .workflow_engine import process_epub_file
from .translations import _


class WorkflowThread(QThread):
    """Thread pour le traitement asynchrone"""
    
    progress_updated = pyqtSignal(int, str)  # pourcentage, message
    book_finished = pyqtSignal(str, bool, dict)  # nom, succès, stats
    finished_all = pyqtSignal(list)  # liste des résultats
    
    def __init__(self, epub_paths: List[Path], actions: List[str]):
        super().__init__()
        self.epub_paths = epub_paths
        self.actions = actions
        self.cancelled = False
        
    def run(self):
        """Exécuter le traitement"""
        results = []
        total = len(self.epub_paths)
        
        for i, epub_path in enumerate(self.epub_paths):
            if self.cancelled:
                break
                
            # Calculer le pourcentage
            progress = int((i / total) * 100) if total > 0 else 0
            
            # Message de progression
            from .translations import _
            self.progress_updated.emit(progress, _('processing_file', filename=epub_path.name))
            
            # Traiter le fichier
            def progress_callback(msg):
                self.progress_updated.emit(progress, msg)
            
            success, stats = process_epub_file(epub_path, self.actions, progress_callback)
            
            # Émettre le signal
            self.book_finished.emit(epub_path.name, success, stats)
            
            results.append({
                "file": epub_path.name,
                "path": epub_path,
                "success": success,
                "stats": stats
            })
        
        if not self.cancelled:
            from .translations import _
            self.progress_updated.emit(100, _('processing_complete'))
        
        self.finished_all.emit(results)
    
    def cancel(self):
        """Annuler le traitement"""
        self.cancelled = True


class ProgressDialog(QDialog):
    """Dialog de progression pour le traitement batch"""
    
    def __init__(self, parent=None, epub_paths: List[Path] = None, actions: List[str] = None):
        super().__init__(parent)
        self.setWindowTitle(_('progress_title'))
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        self.epub_paths = epub_paths or []
        self.actions = actions or []
        self.results = []
        
        self.setup_ui()
        self.start_processing()
        
    def setup_ui(self):
        """Créer l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Label du statut
        self.status_label = QLabel(_('initialization'))
        self.status_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # Barre de progression globale
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        
        # Zone de texte pour les détails
        group = QGroupBox(_('details_title'))
        group_layout = QVBoxLayout()
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(250)
        group_layout.addWidget(self.details_text)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton(_('cancel_processing'))
        self.cancel_btn.clicked.connect(self.cancel_processing)
        
        self.close_btn = QPushButton(_('closing'))
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setEnabled(False)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
    def start_processing(self):
        """Démarrer le traitement"""
        if not self.epub_paths:
            self.status_label.setText(_('no_book_selected'))
            self.close_btn.setEnabled(True)
            self.cancel_btn.setEnabled(False)
            return
        
        # Créer et démarrer le thread
        self.thread = WorkflowThread(self.epub_paths, self.actions)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.book_finished.connect(self.on_book_finished)
        self.thread.finished_all.connect(self.on_finished_all)
        self.thread.start()
        
        self.append_log(_('starting', count=len(self.epub_paths)))
        self.append_log(_('selected_actions', actions=', '.join(self.actions)))
        self.append_log("")
        
    def update_progress(self, percentage: int, message: str):
        """Mettre à jour la progression"""
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
        
    def on_book_finished(self, filename: str, success: bool, stats: dict):
        """Appelé lorsqu'un livre est terminé"""
        if success:
            self.append_log(_('success', filename=filename))
            # Afficher les statistiques si pertinentes
            if stats.get("check", {}).get("found", 0) > 0:
                self.append_log(_('errors_found', found=stats['check']['found'], fixed=stats['check']['fixed']))
            if stats.get("fonts", {}).get("removed", 0) > 0:
                self.append_log(_('fonts_removed', count=stats['fonts']['removed']))
            if stats.get("resize_images", {}).get("resized", 0) > 0:
                self.append_log(_('resize_images_success', count=stats['resize_images']['resized']))
        else:
            self.append_log(_('error', filename=filename))
        
    def on_finished_all(self, results: List[Dict]):
        """Appelé lorsque tous les livres sont traités"""
        self.results = results
        
        # Calculer les statistiques
        total = len(results)
        success_count = sum(1 for r in results if r["success"])
        fail_count = total - success_count
        
        self.append_log("")
        self.append_log("=" * 50)
        self.append_log(_('summary'))
        self.append_log("=" * 50)
        self.append_log(_('total_files', count=total))
        self.append_log(_('successful', count=success_count))
        if fail_count > 0:
            self.append_log(_('failed', count=fail_count))
        
        self.status_label.setText(_('finished', success=success_count, total=total))
        self.progress_bar.setValue(100)
        
        self.cancel_btn.setEnabled(False)
        self.close_btn.setEnabled(True)
        
    def append_log(self, message: str):
        """Ajouter un message au log"""
        self.details_text.append(message)
        # Auto-scroll vers le bas
        # append() fait déjà le scroll, mais on peut forcer avec moveCursor
        try:
            # Utiliser moveCursor qui est plus simple et compatible
            self.details_text.moveCursor(QTextCursor.MoveOperation.End)
        except AttributeError:
            # Fallback pour anciennes versions de PyQt5
            try:
                # Dans certaines versions, c'est directement dans QTextCursor
                self.details_text.moveCursor(QTextCursor.End)
            except:
                # Si tout échoue, append() a déjà fait le scroll
                pass
        
    def cancel_processing(self):
        """Annuler le traitement"""
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.cancel()
            self.append_log("\n" + _('cancelling'))
            self.status_label.setText(_('cancelling_status'))
            self.cancel_btn.setEnabled(False)

