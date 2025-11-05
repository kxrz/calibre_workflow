#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB Batch Workflow - Interactive CLI Tool
Professional EPUB automation with interactive menu, batch processing, and recursive scanning
Fallback version: Works even without rich/questionary installed
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

# Try importing optional packages, fallback to basic CLI if missing
try:
    import questionary
    from rich.console import Console
    from rich.panel import Panel
    from rich.box import ROUNDED
    HAS_RICH = True
    HAS_QUESTIONARY = True
except ImportError:
    HAS_RICH = False
    HAS_QUESTIONARY = False
    Console = None
    Panel = None

# Fallback functions if rich not available
if not HAS_RICH:
    class SimpleConsole:
        def print(self, msg, **kwargs):
            print(str(msg).replace("[", "").replace("]", "").replace("/", "").replace("cyan", "").replace("green", "").replace("red", "").replace("yellow", "").replace("bold", "").replace("dim", ""))
    console = SimpleConsole()
else:
    console = Console()

def print_info(msg):
    if HAS_RICH:
        console.print(f"[cyan][INFO] {msg}[/cyan]")
    else:
        print(f"[INFO] {msg}")

def print_success(msg):
    if HAS_RICH:
        console.print(f"[green][OK] {msg}[/green]")
    else:
        print(f"[OK] {msg}")

def print_warning(msg):
    if HAS_RICH:
        console.print(f"[yellow][WARN] {msg}[/yellow]")
    else:
        print(f"[WARN] {msg}")

def print_error(msg):
    if HAS_RICH:
        console.print(f"[red][ERR] {msg}[/red]")
    else:
        print(f"[ERR] {msg}")

# ============================================================================
# ENVIRONMENT CHECKS
# ============================================================================

def check_environment() -> bool:
    """Check all required dependencies and environment setup"""

    if HAS_RICH:
        console.print(f"\n[cyan]{'='*60}[/cyan]")
        console.print("[bold cyan]EPUB Batch Workflow[/bold cyan]")
        console.print("[yellow]Interactive EPUB Processing Tool[/yellow]")
        console.print(f"[cyan]{'='*60}[/cyan]")
    else:
        print("\n" + "="*60)
        print("EPUB Batch Workflow")
        print("Interactive EPUB Processing Tool")
        print("="*60)

    print_info("Checking environment...")

    # Check Python version
    if sys.version_info < (3, 6):
        print_error("Python 3.6+ required")
        return False
    print_success("Python version: OK")

    # Check calibre-debug
    if not shutil.which('calibre-debug'):
        print_error("calibre-debug not found in PATH")
        print_warning("Fix: Add to ~/.zshrc or ~/.bash_profile:")
        print('  export PATH="/Applications/calibre.app/Contents/MacOS:$PATH"')
        return False
    print_success("calibre-debug: Found")

    # Check ebook-convert
    if not shutil.which('ebook-convert'):
        print_error("ebook-convert not found in PATH")
        print_warning("Same fix as calibre-debug above")
        return False
    print_success("ebook-convert: Found")

    # Check Calibre modules
    print_info("Checking Calibre modules...")
    try:
        from calibre.ebooks.oeb.polish.container import get_container
        from calibre.ebooks.oeb.polish.pretty import fix_all_html, pretty_all
        from calibre.ebooks.oeb.polish.css import remove_unused_css
        from calibre.ebooks.oeb.polish.fonts import change_font, font_family_data
        from calibre.ebooks.oeb.polish.check.main import run_checks, fix_errors
        print_success("All Calibre modules imported")
    except ImportError as e:
        print_error(f"Import error: {e}")
        print_warning("Run script with: calibre-debug -e epub_workflow.py -- <file>")
        return False

    # Check optional packages
    print_info("Checking optional packages...")
    if HAS_RICH and HAS_QUESTIONARY:
        print_success("rich: OK")
        print_success("questionary: OK")
    else:
        print_warning("Optional packages (rich, questionary) not found")
        print_warning("Script will use basic text interface")
        print_warning("Install with: pip install rich questionary")

    # Test calibre-debug version
    try:
        result = subprocess.run(['calibre-debug', '--version'], 
                              capture_output=True, text=True, timeout=5)
        version = result.stdout.strip()
        print_success(f"Calibre version: {version}")
    except Exception as e:
        print_warning(f"Could not verify Calibre version: {e}")

    print_success("All checks passed!\n")
    return True


# ============================================================================
# FILE SELECTION
# ============================================================================

def find_epub_files(path: Path, recursive: bool = False) -> List[Path]:
    """Find all EPUB files in a directory (excluding .kepub.epub files)"""
    epub_files = []

    if path.is_file() and path.suffix.lower() == '.epub':
        # Ignore .kepub.epub files
        if not path.name.lower().endswith('.kepub.epub'):
            return [path]
        else:
            return []

    if path.is_dir():
        if recursive:
            for epub_path in path.rglob('*.epub'):
                if epub_path.is_file() and not epub_path.name.lower().endswith('.kepub.epub'):
                    epub_files.append(epub_path)
        else:
            for epub_path in path.glob('*.epub'):
                if epub_path.is_file() and not epub_path.name.lower().endswith('.kepub.epub'):
                    epub_files.append(epub_path)

    return sorted(epub_files)


def select_files(input_path: str) -> Tuple[List[Path], str]:
    """Interactive file selection menu"""
    input_path = Path(input_path).expanduser().resolve()

    print_info("FILE SELECTION\n")

    if input_path.is_file():
        print(f"  File: {input_path.name}")
        return [input_path], "single"

    if not input_path.is_dir():
        print_error(f"Path not found: {input_path}")
        sys.exit(1)

    epub_count_flat = len(list(input_path.glob('*.epub')))
    epub_count_recursive = len(list(input_path.rglob('*.epub')))

    print(f"  Directory: {input_path}")
    print(f"  EPUBs in directory: {epub_count_flat}")
    print(f"  EPUBs (recursive): {epub_count_recursive}\n")

    if HAS_QUESTIONARY:
        mode = questionary.select(
            "How would you like to process files?",
            choices=[
                "All EPUBs in this directory (non-recursive)",
                "All EPUBs recursively (including subfolders)",
                "Cancel"
            ]
        ).ask()
    else:
        print("Choose mode:")
        print("1) All EPUBs in this directory (non-recursive)")
        print("2) All EPUBs recursively (including subfolders)")
        print("3) Cancel")
        choice = input("Enter choice (1-3): ").strip()
        mode_map = {"1": "non-recursive", "2": "recursive", "3": "Cancel"}
        mode = mode_map.get(choice, "Cancel")

    if mode is None or "Cancel" in mode:
        print_warning("Cancelled")
        sys.exit(0)

    recursive = "recursive" in mode.lower()
    epub_files = find_epub_files(input_path, recursive=recursive)

    if not epub_files:
        print_error("No EPUB files found")
        sys.exit(1)

    mode_str = "recursive" if recursive else "non-recursive"
    print_success(f"Found {len(epub_files)} EPUB file(s) ({mode_str})\n")

    return epub_files, mode_str


# ============================================================================
# ACTION SELECTION
# ============================================================================

def select_actions() -> List[str]:
    """Interactive action selection menu"""
    print_info("ACTION SELECTION\n")

    actions_display = [
        "1. Convert EPUB to EPUB (refresh HTML)",
        "2. Repair HTML",
        "3. Beautify all files",
        "4. Remove unused CSS",
        "5. Check and auto-fix errors",
        "6. Remove embedded fonts",
        "7. Run full workflow (all steps)",
        "8. Cancel"
    ]

    if HAS_QUESTIONARY:
        choice = questionary.select(
            "Select action(s) to perform:",
            choices=actions_display
        ).ask()
    else:
        print("Select action(s):")
        for action in actions_display:
            print(f"  {action}")
        choice = input("\nEnter choice (1-8): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(actions_display):
            choice = actions_display[int(choice)-1]
        else:
            choice = None

    if choice is None or "Cancel" in choice or "8." in str(choice):
        print_warning("Cancelled")
        sys.exit(0)

    if "full workflow" in str(choice).lower():
        return ["convert", "repair", "beautify", "css", "check", "fonts"]

    actions_map = {
        "1": "convert",
        "2": "repair",
        "3": "beautify",
        "4": "css",
        "5": "check",
        "6": "fonts"
    }

    for num, action_key in actions_map.items():
        if num in str(choice):
            print_success(f"Selected action: {choice}\n")
            return [action_key]

    return ["convert"]


# ============================================================================
# WORKFLOW PROCESSING
# ============================================================================

def process_convert_epub(input_path: Path, output_path: Path = None) -> bool:
    """Convert EPUB to EPUB using ebook-convert (refresh HTML)"""
    try:
        out_path = output_path or input_path

        print("  → Converting EPUB to EPUB (refresh HTML)... ", end="", flush=True)

        result = subprocess.run(
            ['ebook-convert', str(input_path), str(out_path), '--pretty-print'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print_success("")
            return True
        else:
            print_error("")
            print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False


def process_repair_html(container) -> bool:
    """Repair HTML"""
    try:
        from calibre.ebooks.oeb.polish.pretty import fix_all_html

        print("  → Repairing HTML... ", end="", flush=True)
        fix_all_html(container)
        print_success("")
        return True
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False


def process_beautify(container) -> bool:
    """Beautify all files"""
    try:
        from calibre.ebooks.oeb.polish.pretty import pretty_all

        print("  → Beautifying files... ", end="", flush=True)
        pretty_all(container)
        print_success("")
        return True
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False


def process_remove_css(container) -> bool:
    """Remove unused CSS"""
    try:
        from calibre.ebooks.oeb.polish.css import remove_unused_css

        print("  → Removing unused CSS... ", end="", flush=True)
        remove_unused_css(
            container,
            remove_unused_classes=True,
            merge_rules=True,
            remove_unreferenced_sheets=True
        )
        print_success("")
        return True
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False


def process_check_errors(container) -> Tuple[bool, int, int]:
    """Check and auto-fix errors"""
    try:
        from calibre.ebooks.oeb.polish.check.main import run_checks, fix_errors

        print("  → Checking for errors... ", end="", flush=True)
        errors = run_checks(container)

        if errors:
            error_count = len(errors)
            print(f"Found {error_count}, ", end="", flush=True)

            fixed = fix_errors(container, errors)

            if fixed:
                print_success("")
                return True, error_count, error_count
            else:
                print_warning("")
                return True, error_count, 0
        else:
            print_success("")
            return True, 0, 0
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False, 0, 0


def process_remove_fonts(container) -> Tuple[bool, int]:
    """Remove embedded fonts"""
    try:
        from calibre.ebooks.oeb.polish.fonts import change_font, font_family_data

        print("  → Removing fonts... ", end="", flush=True)

        fonts_data = font_family_data(container)
        embedded_fonts = [f for f, is_embedded in fonts_data.items() if is_embedded]

        if embedded_fonts:
            for font_name in embedded_fonts:
                change_font(container, font_name, new_name=None)
            print_success(f"({len(embedded_fonts)} fonts removed)")
            return True, len(embedded_fonts)
        else:
            print_success("(no embedded fonts found)")
            return True, 0
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False, 0


def process_epub_file(epub_path: Path, actions: List[str], output_dir: Path = None) -> Tuple[bool, dict]:
    """Process a single EPUB file with all selected actions"""
    stats = {
        "convert": False,
        "repair": False,
        "beautify": False,
        "css": False,
        "check": {"success": False, "found": 0, "fixed": 0},
        "fonts": {"success": False, "removed": 0}
    }

    print(f"\nProcessing: {epub_path.name}")

    # Determine output path
    if output_dir:
        output_path = output_dir / epub_path.name
    else:
        output_path = epub_path

    # Convert EPUB→EPUB
    if "convert" in actions:
        temp_path = epub_path.with_name(epub_path.stem + "_tmp.epub")
        if process_convert_epub(epub_path, temp_path):
            shutil.move(temp_path, epub_path)
            stats["convert"] = True

    # Load container for other operations
    try:
        from calibre.ebooks.oeb.polish.container import get_container
        container = get_container(str(epub_path), tweak_mode=True)
    except Exception as e:
        print_error(f"Cannot open EPUB: {e}")
        return False, stats

    # Repair HTML
    if "repair" in actions:
        stats["repair"] = process_repair_html(container)

    # Beautify
    if "beautify" in actions:
        stats["beautify"] = process_beautify(container)

    # Remove CSS
    if "css" in actions:
        stats["css"] = process_remove_css(container)

    # Check errors
    if "check" in actions:
        success, found, fixed = process_check_errors(container)
        stats["check"]["success"] = success
        stats["check"]["found"] = found
        stats["check"]["fixed"] = fixed

    # Remove fonts
    if "fonts" in actions:
        success, removed = process_remove_fonts(container)
        stats["fonts"]["success"] = success
        stats["fonts"]["removed"] = removed

    # Save
    try:
        print("  → Saving EPUB... ", end="", flush=True)
        container.commit(outpath=str(output_path))
        print_success("")
        return True, stats
    except Exception as e:
        print_error("")
        print(f"    Exception: {e}")
        return False, stats


# ============================================================================
# BATCH PROCESSING
# ============================================================================

def process_batch(epub_files: List[Path], actions: List[str], output_dir: Path = None):
    """Process multiple EPUB files with progress tracking"""

    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print_info(f"Output directory created: {output_dir}\n")

    results = []
    success_count = 0
    fail_count = 0

    total = len(epub_files)
    print_info(f"Processing {total} file(s)...\n")

    for i, epub_path in enumerate(epub_files, 1):
        print(f"[{i}/{total}] ", end="")

        success, stats = process_epub_file(epub_path, actions, output_dir)

        if success:
            success_count += 1
            print_success("DONE")
        else:
            fail_count += 1
            print_error("FAILED")

        results.append({
            "file": epub_path.name,
            "success": success,
            "stats": stats
        })

    # Summary
    print("\n" + "="*60)
    print_info("SUMMARY")
    print("="*60)
    print(f"  Total files: {total}")
    print_success(f"Successful: {success_count}")
    print_error(f"Failed: {fail_count}")

    if output_dir:
        print(f"  Output directory: {output_dir}")

    print("="*60 + "\n")

    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""

    # Check environment
    if not check_environment():
        print_error("Environment check failed")
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) < 2:
        print_error("Missing input path")
        print_warning("Usage: calibre-debug -e epub_workflow.py -- <input> [output]")
        sys.exit(1)

    input_path = sys.argv[1]
    preset_output = sys.argv[2] if len(sys.argv) > 2 else None

    # Select files
    epub_files, mode = select_files(input_path)

    # Select actions
    actions = select_actions()

    # Set output directory
    if preset_output:
        output_dir = Path(preset_output).expanduser().resolve()
        print_info(f"Output directory: {output_dir}\n")
    else:
        if HAS_QUESTIONARY:
            use_custom = questionary.confirm(
                "Save to a different directory?",
                default=False
            ).ask()
        else:
            print("Save to different directory? (y/n) [n]:")
            use_custom = input().strip().lower() == 'y'

        if use_custom:
            if HAS_QUESTIONARY:
                output_path = questionary.path(
                    "Select output directory:",
                    default=str(Path.home())
                ).ask()
            else:
                output_path = input("Enter output directory: ").strip()
            output_dir = Path(output_path).expanduser().resolve() if output_path else None
            if output_dir:
                print_info(f"Output directory: {output_dir}\n")
        else:
            output_dir = None

    # Confirm
    print_warning("Ready to process. Press ENTER to start or Ctrl+C to cancel")
    try:
        input()
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print_warning("Cancelled")
        print("="*60 + "\n")
        sys.exit(0)

    # Process
    if len(epub_files) == 1:
        process_epub_file(epub_files[0], actions, output_dir)
    else:
        process_batch(epub_files, actions, output_dir)

    print_success("All done!\n")


if __name__ == "__main__":
    main()
