# -*- coding: utf-8 -*-
"""
Dialog de configuration pour le plugin EPUB Workflow
Interface graphique pour sélectionner les actions à effectuer
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QCheckBox, QPushButton, QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt

from .translations import _


class WorkflowConfigDialog(QDialog):
    """Dialog pour configurer les actions du workflow"""

    def __init__(self, parent=None, default_actions=None):
        super().__init__(parent)
        self.setWindowTitle(_('config_title'))
        self.setMinimumWidth(400)
        
        self.actions = {
            "convert": False,
            "repair": False,
            "beautify": False,
            "css": False,
            "check": False,
            "fonts": False,
            "resize_images": False
        }
        
        # Restaurer les actions par défaut si fournies
        if default_actions:
            self.actions.update(default_actions)
        
        self.checkboxes = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Créer l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre et description
        title_label = QLabel(_('select_actions'))
        title_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title_label)
        
        # Groupe de checkboxes
        group = QGroupBox(_('available_actions'))
        group_layout = QVBoxLayout()
        
        # Créer les checkboxes
        actions_config = [
            ("convert", _('action_convert')),
            ("repair", _('action_repair')),
            ("beautify", _('action_beautify')),
            ("css", _('action_css')),
            ("check", _('action_check')),
            ("fonts", _('action_fonts')),
            ("resize_images", _('action_resize_images')),
        ]
        
        for action_key, action_label in actions_config:
            checkbox = QCheckBox(action_label)
            checkbox.setChecked(self.actions.get(action_key, False))
            self.checkboxes[action_key] = checkbox
            group_layout.addWidget(checkbox)
            
            # Avertissement spécial pour resize_images
            if action_key == "resize_images":
                warning_label = QLabel(_('resize_images_warning'))
                warning_label.setStyleSheet("color: #d9534f; font-size: 10pt; font-weight: bold; background-color: #fff3cd; padding: 8px; border: 1px solid #ffc107; border-radius: 4px;")
                warning_label.setWordWrap(True)
                group_layout.addWidget(warning_label)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Bouton "Workflow complet"
        full_workflow_btn = QPushButton(_('select_all'))
        full_workflow_btn.clicked.connect(self.select_all)
        layout.addWidget(full_workflow_btn)
        
        layout.addStretch()
        
        # Boutons OK/Cancel
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton(_('ok'))
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton(_('cancel'))
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def select_all(self):
        """Sélectionner toutes les actions"""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)
    
    def get_selected_actions(self):
        """Retourner la liste des actions sélectionnées"""
        selected = []
        for action_key, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected.append(action_key)
        return selected
    
    def accept(self):
        """Valider le dialog"""
        selected = self.get_selected_actions()
        if not selected:
            QMessageBox.warning(
                self,
                _('no_action_selected'),
                _('no_action_selected_msg')
            )
            return
        
        # Mettre à jour self.actions
        for action_key in self.actions:
            self.actions[action_key] = action_key in selected
        
        super().accept()

