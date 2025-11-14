# -*- coding: utf-8 -*-
"""
Plugin principal EPUB Workflow pour Calibre
Action Plugin qui permet de traiter les EPUBs sélectionnés dans Calibre
"""

# Utiliser InterfaceAction comme dans EpubMerge (pas InterfaceActionBase)
from calibre.gui2.actions import InterfaceAction
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from pathlib import Path
from typing import List
import os

# Charger les traductions comme dans EpubMerge
try:
    load_translations()
except NameError:
    pass  # load_translations() ajouté dans calibre 1.9
except:
    pass  # En cas d'erreur, continuer sans traductions

# Imports déplacés dans les méthodes pour éviter les problèmes au chargement
# from .config_dialog import WorkflowConfigDialog
# from .progress_dialog import ProgressDialog
# from .translations import _


class EPUBWorkflowPlugin(InterfaceAction):
    """
    Plugin d'automatisation pour le traitement d'EPUB
    """
    
    name = 'EPUB Workflow'
    # Description en anglais (les traductions ne sont pas encore chargées à ce stade)
    description = 'EPUB automation plugin with interactive menu, batch processing and recursive scanning. Author: u/iamkxrz on Reddit'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Florent Bertiaux (u/iamkxrz)'
    version = (1, 0, 0)
    minimum_calibre_version = (6, 0, 0)
    
    # Type de plugin : action globale (comme EpubMerge)
    # 'global' = disponible partout, 'current' = seulement avec sélection
    action_type = 'current'
    
    # Définir action_spec selon le format EpubMerge
    # Format: (nom, chemin_icône, tooltip, raccourci_clavier)
    # Utiliser None pour l'icône et le raccourci (comme dans EpubMerge)
    # L'icône sera chargée dans genesis()
    # Note: action_spec est évalué au chargement, donc on ne peut pas utiliser _() ici
    # Le tooltip sera mis à jour dans genesis() si nécessaire
    action_spec = ('EPUB Workflow', None,
                   'Process selected EPUBs', None)
    
    def __init__(self, *args):
        """Initialisation du plugin"""
        InterfaceAction.__init__(self, *args)
        print("EPUB Workflow Plugin: Initialisation...")
        
    def genesis(self):
        """
        Créer l'interface utilisateur
        Appelé une fois au démarrage de Calibre
        """
        print("EPUB Workflow Plugin: genesis() appelé")
        
        # Charger les ressources d'icônes comme dans EpubMerge
        try:
            icon_resources = self.load_resources(['images/epub_workflow.png'])
            print(f"EPUB Workflow Plugin: Ressources chargées: {list(icon_resources.keys()) if icon_resources else 'Aucune'}")
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur load_resources: {e}")
            icon_resources = {}
        
        # Définir l'icône et le tooltip pour l'action (comme dans EpubMerge)
        try:
            icon = self.get_icon(icon_resources)
            if icon and not icon.isNull():
                self.qaction.setIcon(icon)
                print("EPUB Workflow Plugin: Icône définie avec succès")
            else:
                print("EPUB Workflow Plugin: Avertissement - Icône vide ou None")
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur lors de la création de l'icône: {e}")
            import traceback
            traceback.print_exc()
        
        # Mettre à jour le tooltip avec la traduction
        try:
            from .translations import _
            self.qaction.setToolTip(_('action_tooltip'))
        except:
            pass
        
        # Connecter le signal
        try:
            self.qaction.triggered.connect(self.show_config_dialog)
            print("EPUB Workflow Plugin: Signal connecté")
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur lors de la connexion du signal: {e}")
            import traceback
            traceback.print_exc()
        
        print("EPUB Workflow Plugin: Plugin initialisé avec succès")
    
    def get_icon(self, icon_resources=None):
        """Obtenir l'icône pour le plugin (méthode similaire à EpubMerge)"""
        # Méthode 1: Utiliser les ressources chargées (comme EpubMerge)
        # load_resources retourne des données brutes (bytes), pas un chemin
        if icon_resources and 'images/epub_workflow.png' in icon_resources:
            try:
                from PyQt5.QtGui import QPixmap
                pixmap = QPixmap()
                pixmap.loadFromData(icon_resources['images/epub_workflow.png'])
                if not pixmap.isNull():
                    icon = QIcon(pixmap)
                    if not icon.isNull():
                        print("EPUB Workflow Plugin: Icône chargée depuis icon_resources")
                        return icon
            except Exception as e:
                print(f"EPUB Workflow Plugin: Erreur avec icon_resources: {e}")
                import traceback
                traceback.print_exc()
        
        # Méthode 2: Utiliser get_icons de Calibre (comme EpubMerge)
        try:
            from calibre.gui2 import get_icons
            # Essayer avec le nom du plugin
            icon = get_icons('images/epub_workflow.png', self.name)
            if icon and not icon.isNull():
                print("EPUB Workflow Plugin: Icône chargée via get_icons")
                return icon
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur get_icons: {e}")
        
        # Méthode 3: Utiliser QIcon.ic() de Calibre (méthode moderne)
        try:
            icon = QIcon.ic('images/epub_workflow.png')
            if not icon.isNull():
                print("EPUB Workflow Plugin: Icône chargée via QIcon.ic()")
                return icon
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur QIcon.ic(): {e}")
        
        # Méthode 4: Charger depuis le système de fichiers
        try:
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(plugin_dir, 'images', 'epub_workflow.png')
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                if not icon.isNull():
                    print("EPUB Workflow Plugin: Icône chargée depuis le fichier")
                    return icon
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur chargement fichier: {e}")
        
        # Méthode 5: Créer une icône simple (fond noir avec point blanc)
        try:
            from PyQt5.QtGui import QPixmap, QPainter, QColor
            from PyQt5.QtCore import Qt
            
            # Créer une icône 64x64 pour une meilleure qualité
            pixmap = QPixmap(64, 64)
            pixmap.fill(QColor(0, 0, 0))  # Fond noir
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Point blanc au centre (plus grand pour 64x64)
            center = 32
            radius = 8
            painter.setBrush(QColor(255, 255, 255))  # Blanc
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)
            painter.end()
            
            print("EPUB Workflow Plugin: Icône créée dynamiquement (64x64)")
            return QIcon(pixmap)
        except Exception as e:
            print(f"EPUB Workflow Plugin: Erreur création icône: {e}")
            return QIcon()  # Icône vide
    
    def library_changed(self, db):
        """Appelé lorsque la bibliothèque change"""
        pass
    
    def show_config_dialog(self):
        """Afficher le dialog de configuration"""
        # Imports locaux pour éviter les problèmes au chargement
        from .config_dialog import WorkflowConfigDialog
        from .progress_dialog import ProgressDialog
        from .translations import _
        
        # Vérifier qu'il y a des livres sélectionnés
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            QMessageBox.information(
                self.gui,
                _('no_book_selected'),
                _('no_book_selected_msg')
            )
            return
        
        # Récupérer les livres sélectionnés
        db = self.gui.current_db
        book_ids = self.gui.library_view.get_selected_ids()
        
        # Filtrer les EPUBs seulement (ignorer autres formats)
        epub_paths = []
        epub_books = []
        
        for book_id in book_ids:
            try:
                book = db.get_metadata(book_id, index_is_id=True)
                # Vérifier si le livre a un format EPUB
                if 'EPUB' in book.formats:
                    # Ignorer les .kepub.epub
                    epub_format_path = db.format_abspath(book_id, 'EPUB', index_is_id=True)
                    if epub_format_path and not epub_format_path.lower().endswith('.kepub.epub'):
                        epub_paths.append(Path(epub_format_path))
                        epub_books.append((book_id, book))
            except Exception as e:
                print(f"Erreur lors de la récupération du livre {book_id}: {e}")
        
        # Si aucun EPUB trouvé, proposer de convertir
        if not epub_paths:
            # Trouver les livres sans EPUB
            books_to_convert = []
            for book_id in book_ids:
                try:
                    book = db.get_metadata(book_id, index_is_id=True)
                    if 'EPUB' not in book.formats and book.formats:
                        # Le livre a un format mais pas EPUB
                        books_to_convert.append((book_id, book))
                except Exception as e:
                    print(f"Erreur lors de la récupération du livre {book_id}: {e}")
            
            # Afficher un message informatif
            from .translations import _
            
            title = _('no_epub_found')
            msg = _('no_epub_found_msg')
            
            if books_to_convert:
                book_names = [book.title for _, book in books_to_convert[:3]]
                if len(books_to_convert) > 3:
                    more_text = _('and_more_books', count=len(books_to_convert) - 3)
                    book_names.append(more_text)
                books_list_text = _('books_not_epub_format', count=len(books_to_convert), names='\n'.join(book_names))
                convert_instruction = _('convert_instruction')
                msg += f'\n\n{books_list_text}\n\n{convert_instruction}'
            
            QMessageBox.information(
                self.gui,
                title,
                msg
            )
            return
        
        # Charger les préférences par défaut
        prefs = self.load_preferences()
        
        # Afficher le dialog de configuration
        dialog = WorkflowConfigDialog(self.gui, default_actions=prefs.get('actions', {}))
        
        if dialog.exec():
            # Récupérer les actions sélectionnées
            actions = dialog.get_selected_actions()
            
            if not actions:
                return
            
            # Sauvegarder les préférences
            prefs['actions'] = {action: action in actions for action in [
                'convert', 'repair', 'beautify', 'css', 'check', 'fonts', 'resize_images'
            ]}
            self.save_preferences(prefs)
            
            # Demander confirmation pour traitement batch
            if len(epub_paths) > 1:
                reply = QMessageBox.question(
                    self.gui,
                    _('confirmation'),
                    _('confirmation_msg', count=len(epub_paths), actions=', '.join(actions)),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                
                if reply != QMessageBox.StandardButton.Yes:
                    return
            
            # Afficher le dialog de progression
            progress_dialog = ProgressDialog(
                self.gui,
                epub_paths=epub_paths,
                actions=actions
            )
            
            # Exécuter le dialog (bloquant jusqu'à la fin)
            progress_dialog.exec()
            
            # Rafraîchir la bibliothèque si nécessaire
            # Les fichiers ont été modifiés, on peut forcer un refresh
            if hasattr(self.gui, 'library_view'):
                # Calibre détectera automatiquement les modifications
                pass
    
    def load_preferences(self):
        """Charger les préférences du plugin"""
        # Utiliser le mécanisme de configuration de Calibre
        try:
            from calibre.utils.config import JSONConfig
            prefs = JSONConfig('plugins/epub_workflow')
            # Définir les valeurs par défaut
            prefs.defaults['actions'] = {
                'convert': False,
                'repair': False,
                'beautify': False,
                'css': False,
                'check': False,
                'fonts': False,
                'resize_images': False
            }
            # Retourner les valeurs actuelles avec les défauts
            return {
                'actions': prefs['actions']
            }
        except Exception as e:
            print(f"Erreur lors du chargement des préférences: {e}")
            return {
                'actions': {
                    'convert': False,
                    'repair': False,
                    'beautify': False,
                    'css': False,
                    'check': False,
                    'fonts': False,
                    'resize_images': False
                }
            }
    
    def save_preferences(self, prefs):
        """Sauvegarder les préférences du plugin"""
        try:
            from calibre.utils.config import JSONConfig
            prefs_obj = JSONConfig('plugins/epub_workflow')
            prefs_obj['actions'] = prefs.get('actions', {})
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des préférences: {e}")
    
    def convert_books_to_epub(self, db, books_to_convert):
        """Convertir les livres vers EPUB"""
        try:
            from calibre.gui2 import error_dialog, info_dialog
            from calibre.ebooks.conversion.plumber import Plumber
            from calibre.ptempfile import TemporaryDirectory
            import os
            
            converted_count = 0
            failed_count = 0
            
            for book_id, book in books_to_convert:
                try:
                    # Trouver le premier format disponible
                    source_format = None
                    for fmt in book.formats:
                        if fmt.upper() != 'EPUB':
                            source_format = fmt.upper()
                            break
                    
                    if not source_format:
                        print(f"No source format found for book {book.title}")
                        failed_count += 1
                        continue
                    
                    # Obtenir le chemin du fichier source
                    source_path = db.format_abspath(book_id, source_format, index_is_id=True)
                    if not source_path or not os.path.exists(source_path):
                        print(f"Source file not found for book {book.title}")
                        failed_count += 1
                        continue
                    
                    # Convertir vers EPUB
                    print(f"Converting {book.title} from {source_format} to EPUB...")
                    
                    # Créer un fichier temporaire pour la sortie
                    with TemporaryDirectory('_epub_convert') as tdir:
                        output_path = os.path.join(tdir, f"{book_id}.epub")
                        
                        # Utiliser Plumber pour la conversion
                        try:
                            # Capturer les logs de conversion
                            from io import StringIO
                            log_buffer = StringIO()
                            
                            # Utiliser Plumber pour la conversion
                            plumber = Plumber(source_path, output_path, log=log_buffer)
                            plumber.run()
                            
                            # Récupérer les logs
                            log_output = log_buffer.getvalue()
                            if log_output:
                                print(f"Conversion log for {book.title}:")
                                print(log_output)
                            
                            # Vérifier que le fichier de sortie existe et n'est pas vide
                            if os.path.exists(output_path):
                                file_size = os.path.getsize(output_path)
                                if file_size > 0:
                                    # Ajouter le format EPUB à la base de données
                                    with open(output_path, 'rb') as f:
                                        db.add_format(book_id, 'EPUB', f, index_is_id=True)
                                    converted_count += 1
                                    print(f"✓ Converted {book.title} to EPUB ({file_size} bytes)")
                                else:
                                    error_msg = f"Conversion failed: output file is empty"
                                    if log_output:
                                        error_msg += f"\nLog: {log_output[:500]}"
                                    print(f"✗ {error_msg}")
                                    failed_count += 1
                            else:
                                error_msg = f"Conversion failed: output file not created"
                                if log_output:
                                    error_msg += f"\nLog: {log_output[:500]}"
                                print(f"✗ {error_msg}")
                                failed_count += 1
                                
                        except Exception as conv_error:
                            error_msg = f"Conversion error for {book.title}: {conv_error}"
                            print(f"✗ {error_msg}")
                            import traceback
                            traceback.print_exc()
                            failed_count += 1
                            
                except Exception as e:
                    print(f"Error converting {book.title}: {e}")
                    import traceback
                    traceback.print_exc()
                    failed_count += 1
            
            # Afficher un message de résultat
            from .translations import _
            
            msg = _('conversion_complete', converted=converted_count, failed=failed_count)
            
            if converted_count > 0:
                info_dialog(self.gui, _('conversion_complete_title'), msg, show=True)
            elif failed_count > 0:
                error_dialog(self.gui, _('conversion_failed_title'), msg, show=True)
                
        except Exception as e:
            print(f"Error in convert_books_to_epub: {e}")
            import traceback
            traceback.print_exc()
            try:
                from calibre.gui2 import error_dialog
                from .translations import _
                error_dialog(self.gui, _('conversion_error_title'), _('conversion_error_msg', error=str(e)), show=True)
            except:
                pass

