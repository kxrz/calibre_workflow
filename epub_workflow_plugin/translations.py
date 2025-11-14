# -*- coding: utf-8 -*-
"""
Système de traduction pour le plugin EPUB Workflow
Support français et anglais
"""

# Dictionnaire de traductions
TRANSLATIONS = {
    'fr': {
        # Plugin principal
        'plugin_name': 'EPUB Workflow',
        'plugin_description': 'Plugin d\'automatisation pour le traitement d\'EPUB avec menu interactif, traitement batch et balayage récursif',
        'action_tooltip': 'Traiter les EPUBs sélectionnés',
        
        # Messages du plugin
        'no_book_selected': 'Aucun livre sélectionné',
        'no_book_selected_msg': 'Veuillez sélectionner au moins un livre EPUB dans votre bibliothèque.',
        'no_epub_found': 'Aucun EPUB trouvé',
        'no_epub_found_msg': 'Aucun livre EPUB valide trouvé dans la sélection.\n\nNote: Les fichiers .kepub.epub sont automatiquement ignorés.',
        'and_more_books': '... et {count} autre(s)',
        'books_not_epub_format': '{count} livre(s) sélectionné(s) ne sont pas au format EPUB:\n{names}',
        'convert_instruction': 'Veuillez d\'abord les convertir en EPUB en utilisant la fonction de conversion de Calibre.',
        'confirmation': 'Confirmation',
        'confirmation_msg': 'Vous allez traiter {count} fichier(s) EPUB.\n\nActions sélectionnées: {actions}\n\nContinuer ?',
        
        # Dialog de configuration
        'config_title': 'EPUB Workflow - Configuration',
        'select_actions': 'Sélectionnez les actions à effectuer :',
        'available_actions': 'Actions disponibles',
        'action_convert': 'Convertir EPUB to EPUB (rafraîchir HTML)',
        'action_repair': 'Réparer le HTML',
        'action_beautify': 'Beautifier tous les fichiers',
        'action_css': 'Supprimer le CSS inutilisé',
        'action_check': 'Vérifier et corriger automatiquement les erreurs',
        'action_fonts': 'Supprimer les polices intégrées',
        'action_resize_images': 'Redimensionner les images à 480px (Xteink)',
        'resize_images_warning': '⚠ Une copie de sauvegarde du fichier original sera créée automatiquement (nom_du_fichier_backup.epub). Le fichier dans votre bibliothèque sera modifié avec toutes les actions sélectionnées, y compris le redimensionnement des images. Cette opération est irréversible sur le fichier original.',
        'select_all': 'Sélectionner tout (Workflow complet)',
        'ok': 'OK',
        'cancel': 'Annuler',
        'no_action_selected': 'Aucune action sélectionnée',
        'no_action_selected_msg': 'Veuillez sélectionner au moins une action à effectuer.',
        
        # Dialog de progression
        'progress_title': 'EPUB Workflow - Traitement en cours',
        'processing': 'Traitement: {filename}',
        'starting': 'Démarrage du traitement de {count} fichier(s)...',
        'selected_actions': 'Actions sélectionnées: {actions}',
        'processing_file': 'Traitement: {filename}',
        'success': '✓ {filename} - Traitement réussi',
        'error': '✗ {filename} - Échec du traitement',
        'errors_found': '  → {found} erreur(s) trouvée(s), {fixed} corrigée(s)',
        'fonts_removed': '  → {count} police(s) supprimée(s)',
        'summary': 'RÉSUMÉ',
        'total_files': 'Total de fichiers: {count}',
        'successful': 'Réussis: {count}',
        'failed': 'Échecs: {count}',
        'finished': 'Traitement terminé - {success}/{total} réussis',
        'cancel_processing': 'Annuler',
        'closing': 'Fermer',
        'cancelling': 'Annulation du traitement...',
        'cancelling_status': 'Annulation en cours...',
        'details_title': 'Détails du traitement',
        'initialization': 'Initialisation...',
        'processing_complete': 'Traitement terminé',
        
        # Messages du moteur
        'processing_file': 'Traitement: {filename}',
        'ignored_kepub': 'Fichier .kepub.epub ignoré',
        'converting': '→ Conversion EPUB to EPUB (refresh HTML)...',
        'conversion_success': '✓ Conversion réussie',
        'conversion_error': '✗ Erreur lors de la conversion',
        'repairing': '→ Réparation HTML...',
        'repair_success': '✓ HTML réparé',
        'repair_error': '✗ Erreur réparation HTML',
        'beautifying': '→ Beautification des fichiers...',
        'beautify_success': '✓ Beautification réussie',
        'beautify_error': '✗ Erreur beautification',
        'removing_css': '→ Suppression CSS inutilisé...',
        'css_success': '✓ CSS supprimé',
        'css_error': '✗ Erreur suppression CSS',
        'checking': '→ Vérification des erreurs...',
        'check_success': '✓ {found} erreur(s) trouvée(s), {fixed} corrigée(s)',
        'check_no_errors': '✓ Aucune erreur trouvée',
        'removing_fonts': '→ Suppression des polices intégrées...',
        'fonts_success': '✓ {count} police(s) supprimée(s)',
        'fonts_no_fonts': '✓ Aucune police intégrée trouvée',
        'saving': '→ Sauvegarde de l\'EPUB...',
        'saving_success': '✓ Sauvegarde réussie',
        'saving_error': '✗ Erreur lors de la sauvegarde: {error}',
        'cannot_open': '✗ Impossible d\'ouvrir l\'EPUB: {error}',
        'conversion_complete': 'Conversion terminée: {converted} converti(s), {failed} échec(s)',
        'conversion_complete_title': 'Conversion terminée',
        'conversion_failed_title': 'Échec de la conversion',
        'conversion_error_title': 'Erreur de conversion',
        'conversion_error_msg': 'Une erreur s\'est produite lors de la conversion: {error}',
        'backup_created': '→ Copie de sauvegarde créée: {path}',
        'backup_error': '⚠ Erreur lors de la création de la sauvegarde: {error}',
        'resizing_images': '→ Redimensionnement des images à 480px...',
        'resize_images_success': '✓ {count} image(s) redimensionnée(s)',
        'resize_images_no_images': '✓ Aucune image à redimensionner',
    },
    'en': {
        # Plugin principal
        'plugin_name': 'EPUB Workflow',
        'plugin_description': 'EPUB automation plugin with interactive menu, batch processing and recursive scanning',
        'action_tooltip': 'Process selected EPUBs',
        
        # Messages du plugin
        'no_book_selected': 'No book selected',
        'no_book_selected_msg': 'Please select at least one EPUB book in your library.',
        'no_epub_found': 'No EPUB found',
        'no_epub_found_msg': 'No valid EPUB book found in selection.\n\nNote: .kepub.epub files are automatically ignored.',
        'and_more_books': '... and {count} more',
        'books_not_epub_format': '{count} selected book(s) are not in EPUB format:\n{names}',
        'convert_instruction': 'Please convert them to EPUB first using Calibre\'s conversion feature.',
        'confirmation': 'Confirmation',
        'confirmation_msg': 'You will process {count} EPUB file(s).\n\nSelected actions: {actions}\n\nContinue?',
        
        # Dialog de configuration
        'config_title': 'EPUB Workflow - Configuration',
        'select_actions': 'Select actions to perform:',
        'available_actions': 'Available actions',
        'action_convert': 'Convert EPUB to EPUB (refresh HTML)',
        'action_repair': 'Repair HTML',
        'action_beautify': 'Beautify all files',
        'action_css': 'Remove unused CSS',
        'action_check': 'Check and auto-fix errors',
        'action_fonts': 'Remove embedded fonts',
        'action_resize_images': 'Resize images to 480px (Xteink)',
        'resize_images_warning': '⚠ A backup copy of the original file will be created automatically (filename_backup.epub). The file in your library will be modified with all selected actions, including image resizing. This operation is irreversible on the original file.',
        'select_all': 'Select all (Full workflow)',
        'ok': 'OK',
        'cancel': 'Cancel',
        'no_action_selected': 'No action selected',
        'no_action_selected_msg': 'Please select at least one action to perform.',
        
        # Dialog de progression
        'progress_title': 'EPUB Workflow - Processing',
        'processing': 'Processing: {filename}',
        'starting': 'Starting processing of {count} file(s)...',
        'selected_actions': 'Selected actions: {actions}',
        'processing_file': 'Processing: {filename}',
        'success': '✓ {filename} - Success',
        'error': '✗ {filename} - Failed',
        'errors_found': '  → {found} error(s) found, {fixed} fixed',
        'fonts_removed': '  → {count} font(s) removed',
        'summary': 'SUMMARY',
        'total_files': 'Total files: {count}',
        'successful': 'Successful: {count}',
        'failed': 'Failed: {count}',
        'finished': 'Processing complete - {success}/{total} successful',
        'cancel_processing': 'Cancel',
        'closing': 'Close',
        'cancelling': 'Cancelling processing...',
        'cancelling_status': 'Cancelling...',
        'details_title': 'Processing details',
        'initialization': 'Initializing...',
        'processing_complete': 'Processing complete',
        
        # Messages du moteur
        'processing_file': 'Processing: {filename}',
        'ignored_kepub': '.kepub.epub file ignored',
        'converting': '→ Converting EPUB to EPUB (refresh HTML)...',
        'conversion_success': '✓ Conversion successful',
        'conversion_error': '✗ Conversion error',
        'repairing': '→ Repairing HTML...',
        'repair_success': '✓ HTML repaired',
        'repair_error': '✗ HTML repair error',
        'beautifying': '→ Beautifying files...',
        'beautify_success': '✓ Beautification successful',
        'beautify_error': '✗ Beautification error',
        'removing_css': '→ Removing unused CSS...',
        'css_success': '✓ CSS removed',
        'css_error': '✗ CSS removal error',
        'checking': '→ Checking for errors...',
        'check_success': '✓ {found} error(s) found, {fixed} fixed',
        'check_no_errors': '✓ No errors found',
        'removing_fonts': '→ Removing embedded fonts...',
        'fonts_success': '✓ {count} font(s) removed',
        'fonts_no_fonts': '✓ No embedded fonts found',
        'saving': '→ Saving EPUB...',
        'saving_success': '✓ Save successful',
        'saving_error': '✗ Save error: {error}',
        'cannot_open': '✗ Cannot open EPUB: {error}',
        'conversion_complete': 'Conversion complete: {converted} converted, {failed} failed',
        'conversion_complete_title': 'Conversion Complete',
        'conversion_failed_title': 'Conversion Failed',
        'conversion_error_title': 'Conversion Error',
        'conversion_error_msg': 'An error occurred during conversion: {error}',
        'backup_created': '→ Backup copy created: {path}',
        'backup_error': '⚠ Error creating backup: {error}',
        'resizing_images': '→ Resizing images to 480px...',
        'resize_images_success': '✓ {count} image(s) resized',
        'resize_images_no_images': '✓ No images to resize',
    }
}


def get_language():
    """Déterminer la langue actuelle
    - Anglais par défaut
    - Français seulement si Calibre est en français
    - Anglais pour toutes les autres langues (espagnol, etc.)
    """
    try:
        # Essayer d'obtenir la langue depuis Calibre directement
        try:
            from calibre.utils.localization import get_lang
            calibre_lang = get_lang()
            if calibre_lang:
                # Extraire le code de langue (ex: 'fr_FR' -> 'fr', 'en_US' -> 'en')
                lang_prefix = calibre_lang.split('_')[0].lower() if '_' in calibre_lang else calibre_lang.lower()
                
                # Retourner 'fr' seulement si Calibre est en français
                if lang_prefix == 'fr':
                    return 'fr'
                # Pour toutes les autres langues (en, es, de, etc.), retourner 'en'
                else:
                    return 'en'
        except:
            pass
        
        # Fallback: essayer depuis les variables d'environnement
        try:
            import os
            lang = os.environ.get('CALIBRE_OVERRIDE_LANG', None)
            if lang and isinstance(lang, str):
                lang_prefix = lang.split('_')[0].lower() if '_' in lang else lang.lower()
                # Retourner 'fr' seulement si c'est français
                if lang_prefix == 'fr':
                    return 'fr'
                # Sinon, retourner 'en' par défaut
                else:
                    return 'en'
        except:
            pass
        
        # Fallback: utiliser locale système
        try:
            import locale
            system_lang = locale.getdefaultlocale()[0]
            if system_lang and isinstance(system_lang, str):
                lang_prefix = system_lang.split('_')[0].lower() if '_' in system_lang else system_lang.lower()
                # Retourner 'fr' seulement si c'est français
                if lang_prefix == 'fr':
                    return 'fr'
                # Sinon, retourner 'en' par défaut
                else:
                    return 'en'
        except:
            pass
        
        # Par défaut, retourner anglais
        return 'en'
    except:
        # En cas d'erreur, retourner anglais par défaut
        return 'en'


def _(key, **kwargs):
    """Fonction de traduction"""
    # S'assurer que key est une chaîne valide
    if not key or not isinstance(key, str):
        return str(key) if key else ''
    
    try:
        lang = get_language()
        # S'assurer que lang est valide
        if not lang or not isinstance(lang, str):
            lang = 'en'
        
        # Obtenir la traduction
        translation = TRANSLATIONS.get(lang, TRANSLATIONS.get('en', {})).get(key, key)
        
        # S'assurer que translation est une chaîne
        if not translation or not isinstance(translation, str):
            translation = str(key)
        
        # Remplacer les placeholders si présents
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except:
                pass
        
        return translation
    except Exception:
        # En cas d'erreur, retourner la clé
        return str(key) if key else ''

