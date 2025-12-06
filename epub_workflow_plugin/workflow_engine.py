# -*- coding: utf-8 -*-
"""
Moteur de traitement EPUB
Adapté depuis epub_workflow_fallback.py pour fonctionner avec les objets Calibre
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Callable
from calibre.ebooks.oeb.polish.container import get_container

from .translations import _


def process_repair_html(container) -> bool:
    """Repair HTML"""
    try:
        from calibre.ebooks.oeb.polish.pretty import fix_all_html
        fix_all_html(container)
        return True
    except Exception as e:
        print(f"Erreur lors de la réparation HTML: {e}")
        return False


def process_beautify(container) -> bool:
    """Beautify all files"""
    try:
        from calibre.ebooks.oeb.polish.pretty import pretty_all
        pretty_all(container)
        return True
    except Exception as e:
        print(f"Erreur lors du beautify: {e}")
        return False


def process_remove_css(container) -> bool:
    """Remove unused CSS"""
    try:
        from calibre.ebooks.oeb.polish.css import remove_unused_css
        remove_unused_css(
            container,
            remove_unused_classes=True,
            merge_rules=True,
            remove_unreferenced_sheets=True
        )
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression CSS: {e}")
        return False


def process_check_errors(container) -> Tuple[bool, int, int]:
    """Check and auto-fix errors"""
    try:
        from calibre.ebooks.oeb.polish.check.main import run_checks, fix_errors

        errors = run_checks(container)

        if errors:
            error_count = len(errors)
            fixed = fix_errors(container, errors)
            if fixed:
                return True, error_count, error_count
            else:
                return True, error_count, 0
        else:
            return True, 0, 0
    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")
        return False, 0, 0


def process_remove_fonts(container) -> Tuple[bool, int]:
    """Remove embedded fonts"""
    try:
        from calibre.ebooks.oeb.polish.fonts import change_font, font_family_data

        fonts_data = font_family_data(container)
        embedded_fonts = [f for f, is_embedded in fonts_data.items() if is_embedded]

        if embedded_fonts:
            for font_name in embedded_fonts:
                change_font(container, font_name, new_name=None)
            return True, len(embedded_fonts)
        else:
            return True, 0
    except Exception as e:
        print(f"Erreur lors de la suppression des polices: {e}")
        return False, 0

def process_resize_images(container, max_width: int = 480) -> Tuple[bool, int]:
    """Resize images to max_width (for Xteink e-readers)"""
    try:
        from PIL import Image
        from io import BytesIO

        resized_count = 0

        # Parcourir toutes les ressources du container via mime_map
        for href, media_type in container.mime_map.items():
            if media_type and media_type.startswith('image/'):
                try:
                    # Lire l'image
                    image_data = container.raw_data(href)
                    image = Image.open(BytesIO(image_data))

                    # Vérifier si l'image est plus large que max_width
                    if image.width > max_width:
                        # Calculer la nouvelle hauteur en conservant le ratio
                        ratio = max_width / image.width
                        new_height = int(image.height * ratio)

                        # Redimensionner l'image
                        resized_image = image.resize(
                            (max_width, new_height),
                            Image.Resampling.LANCZOS
                        )

                        # Sauvegarder l'image redimensionnée
                        output = BytesIO()
                        format_ext = image.format or 'JPEG'
                        if format_ext.upper() == 'JPEG':
                            resized_image.save(output, format='JPEG',
                                               quality=85, optimize=True)
                        elif format_ext.upper() == 'PNG':
                            resized_image.save(output, format='PNG',
                                               optimize=True)
                        else:
                            # Par défaut, convertir en JPEG
                            resized_image = resized_image.convert('RGB')
                            resized_image.save(output, format='JPEG',
                                               quality=85, optimize=True)

                        # Mettre à jour le container avec la nouvelle image
                        container.raw_set(href, output.getvalue())
                        resized_count += 1

                except Exception as e:
                    print(f"Erreur lors du redimensionnement de l'image {href}: {e}")
                    continue

        return True, resized_count
    except Exception as e:
        print(f"Erreur lors du redimensionnement des images: {e}")
        import traceback
        traceback.print_exc()
        return False, 0


def process_convert_epub(input_path: Path, output_path: Optional[Path] = None) -> bool:
    """Convert EPUB to EPUB using ebook-convert (refresh HTML)"""
    try:
        out_path = output_path or input_path

        result = subprocess.run(
            ['ebook-convert', str(input_path), str(out_path), '--pretty-print'],
            capture_output=True,
            text=True,
            timeout=120
        )

        return result.returncode == 0
    except Exception as e:
        print(f"Erreur lors de la conversion: {e}")
        return False


def process_epub_file(epub_path: Path, actions: List[str], progress_callback: Optional[Callable[[str], None]] = None) -> Tuple[bool, dict]:
    """
    Traiter un fichier EPUB avec toutes les actions sélectionnées

    Args:
        epub_path: Chemin vers le fichier EPUB
        actions: Liste des actions à effectuer
        progress_callback: Fonction optionnelle pour les messages de progression

    Returns:
        Tuple (success, stats)
    """
    stats = {
        "convert": False,
        "repair": False,
        "beautify": False,
        "css": False,
        "check": {"success": False, "found": 0, "fixed": 0},
        "fonts": {"success": False, "removed": 0},
        "resize_images": {"success": False, "resized": 0}
    }

    def log(msg):
        if progress_callback:
            progress_callback(msg)
        else:
            print(msg)

    log(_('processing_file', filename=epub_path.name))

    # Ignorer les fichiers .kepub.epub
    if epub_path.name.lower().endswith('.kepub.epub'):
        log(_('ignored_kepub'))
        return False, stats

    # Créer une copie de sauvegarde AVANT toutes les modifications
    # Cette copie contient le fichier original intact
    backup_path = None
    try:
        backup_path = epub_path.with_name(epub_path.stem + "_backup.epub")
        # Écraser la sauvegarde si elle existe déjà
        if backup_path.exists():
            backup_path.unlink()
        shutil.copy2(epub_path, backup_path)
        log(_('backup_created', path=str(backup_path.name)))
    except Exception as e:
        log(_('backup_error', error=str(e)))
        # Continuer quand même, mais avertir l'utilisateur

    # Convert EPUB→EPUB
    if "convert" in actions:
        log(_('converting'))
        temp_path = epub_path.with_name(epub_path.stem + "_tmp.epub")
        if process_convert_epub(epub_path, temp_path):
            shutil.move(temp_path, epub_path)
            stats["convert"] = True
            log(_('conversion_success'))
        else:
            log(_('conversion_error'))

    # Load container for other operations
    try:
        container = get_container(str(epub_path), tweak_mode=True)
    except Exception as e:
        log(_('cannot_open', error=str(e)))
        return False, stats

    # Repair HTML
    if "repair" in actions:
        log(_('repairing'))
        stats["repair"] = process_repair_html(container)
        log(_('repair_success') if stats["repair"] else _('repair_error'))

    # Beautify
    if "beautify" in actions:
        log(_('beautifying'))
        stats["beautify"] = process_beautify(container)
        log(_('beautify_success') if stats["beautify"] else _('beautify_error'))

    # Remove CSS
    if "css" in actions:
        log(_('removing_css'))
        stats["css"] = process_remove_css(container)
        log(_('css_success') if stats["css"] else _('css_error'))

    # Check errors
    if "check" in actions:
        log(_('checking'))
        success, found, fixed = process_check_errors(container)
        stats["check"]["success"] = success
        stats["check"]["found"] = found
        stats["check"]["fixed"] = fixed
        if found > 0:
            log(_('check_success', found=found, fixed=fixed))
        else:
            log(_('check_no_errors'))

    # Remove fonts
    if "fonts" in actions:
        log(_('removing_fonts'))
        success, removed = process_remove_fonts(container)
        stats["fonts"]["success"] = success
        stats["fonts"]["removed"] = removed
        if removed > 0:
            log(_('fonts_success', count=removed))
        else:
            log(_('fonts_no_fonts'))

    # Resize images
    if "resize_images" in actions:
        log(_('resizing_images'))
        success, resized = process_resize_images(container, max_width=480)
        stats["resize_images"]["success"] = success
        stats["resize_images"]["resized"] = resized
        if resized > 0:
            log(_('resize_images_success', count=resized))
        else:
            log(_('resize_images_no_images'))

    # Save
    try:
        log(_('saving'))
        container.commit(outpath=str(epub_path))
        log(_('saving_success'))
        return True, stats
    except Exception as e:
        log(_('saving_error', error=str(e)))
        return False, stats

