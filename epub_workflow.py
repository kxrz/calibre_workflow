#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB Batch Workflow - Interactive CLI Tool
Professional EPUB automation with interactive menu, batch processing, and recursive scanning
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

try:
    import questionary
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress
    from rich.table import Table
    from rich.box import ROUNDED
except ImportError:
    print("ERROR: Required packages not found!")
    print("Install with: pip install -r requirements.txt")
    print("Or: pip install rich questionary")
    sys.exit(1)

# Initialize Rich console for colored output
console = Console()


# ============================================================================
# ENVIRONMENT CHECKS
# ============================================================================

def check_environment() -> bool:
    """Check all required dependencies and environment setup"""
    console.print(Panel.fit(
        "[bold cyan]EPUB Batch Workflow[/bold cyan]\n"
        "[yellow]Interactive EPUB Processing Tool[/yellow]",
        box=ROUNDED
    ))

    console.print("\n[cyan][1/4] Checking environment...[/cyan]")

    # Check Python version
    if sys.version_info < (3, 6):
        console.print("[red]ERROR: Python 3.6+ required[/red]")
        return False
    console.print("  [green]✓[/green] Python version: OK")

    # Check calibre-debug
    if not shutil.which('calibre-debug'):
        console.print("  [red]✗[/red] calibre-debug not found in PATH")
        console.print("    [yellow]Fix: Add to ~/.zshrc or ~/.bash_profile:[/yellow]")
        console.print("    [yellow]export PATH=\"/Applications/calibre.app/Contents/MacOS:\$PATH\"[/yellow]")
        return False
    console.print("  [green]✓[/green] calibre-debug: Found")

    # Check ebook-convert
    if not shutil.which('ebook-convert'):
        console.print("  [red]✗[/red] ebook-convert not found in PATH")
        console.print("    [yellow]Same fix as calibre-debug above[/yellow]")
        return False
    console.print("  [green]✓[/green] ebook-convert: Found")

    # Check Calibre modules
    console.print("\n[cyan][2/4] Checking Calibre modules...[/cyan]")
    try:
        from calibre.ebooks.oeb.polish.container import get_container
        from calibre.ebooks.oeb.polish.pretty import fix_all_html, pretty_all
        from calibre.ebooks.oeb.polish.css import remove_unused_css
        from calibre.ebooks.oeb.polish.fonts import change_font, font_family_data
        from calibre.ebooks.oeb.polish.check.main import run_checks, fix_errors
        console.print("  [green]✓[/green] All Calibre modules imported")
    except ImportError as e:
        console.print(f"  [red]✗[/red] Import error: {e}")
        console.print("    [yellow]Run script with: calibre-debug -e epub_workflow.py -- <file>[/yellow]")
        return False

    console.print("\n[cyan][3/4] Checking Python packages...[/cyan]")
    try:
        import rich
        import questionary
        console.print("  [green]✓[/green] rich: OK")
        console.print("  [green]✓[/green] questionary: OK")
    except ImportError as e:
        console.print(f"  [red]✗[/red] Missing package: {e}")
        console.print("    [yellow]Run: pip install -r requirements.txt[/yellow]")
        return False

    console.print("\n[cyan][4/4] Verifying tools...[/cyan]")

    # Test calibre-debug version
    try:
        result = subprocess.run(['calibre-debug', '--version'], 
                              capture_output=True, text=True, timeout=5)
        version = result.stdout.strip()
        console.print(f"  [green]✓[/green] Calibre version: {version}")
    except Exception as e:
        console.print(f"  [yellow]⚠[/yellow] Could not verify Calibre version: {e}")

    console.print("\n[green]✓ All checks passed![/green]\n")
    return True


# ============================================================================
# FILE SELECTION
# ============================================================================

def find_epub_files(path: Path, recursive: bool = False) -> List[Path]:
    """Find all EPUB files in a directory"""
    epub_files = []

    if path.is_file() and path.suffix.lower() == '.epub':
        return [path]

    if path.is_dir():
        if recursive:
            # Recursive search
            for epub_path in path.rglob('*.epub'):
                if epub_path.is_file():
                    epub_files.append(epub_path)
        else:
            # Non-recursive search
            for epub_path in path.glob('*.epub'):
                if epub_path.is_file():
                    epub_files.append(epub_path)

    return sorted(epub_files)


def select_files(input_path: str) -> Tuple[List[Path], str]:
    """Interactive file selection menu"""
    input_path = Path(input_path).expanduser().resolve()

    console.print("\n[cyan]FILE SELECTION[/cyan]\n")

    if input_path.is_file():
        console.print(f"  File: [yellow]{input_path.name}[/yellow]")
        return [input_path], "single"

    if not input_path.is_dir():
        console.print(f"[red]ERROR: Path not found: {input_path}[/red]")
        sys.exit(1)

    epub_count_flat = len(list(input_path.glob('*.epub')))
    epub_count_recursive = len(list(input_path.rglob('*.epub')))

    console.print(f"  Directory: [yellow]{input_path}[/yellow]")
    console.print(f"  EPUBs in directory: {epub_count_flat}")
    console.print(f"  EPUBs (recursive): {epub_count_recursive}\n")

    mode = questionary.select(
        "How would you like to process files?",
        choices=[
            "All EPUBs in this directory (non-recursive)",
            "All EPUBs recursively (including subfolders)",
            "Cancel"
        ]
    ).ask()

    if mode is None or "Cancel" in mode:
        console.print("[yellow]Cancelled[/yellow]")
        sys.exit(0)

    recursive = "recursive" in mode.lower()
    epub_files = find_epub_files(input_path, recursive=recursive)

    if not epub_files:
        console.print("[red]ERROR: No EPUB files found[/red]")
        sys.exit(1)

    mode_str = "recursive" if recursive else "non-recursive"
    console.print(f"\n[green]✓[/green] Found {len(epub_files)} EPUB file(s) ({mode_str})\n")

    return epub_files, mode_str


# ============================================================================
# ACTION SELECTION
# ============================================================================

def select_actions() -> List[str]:
    """Interactive action selection menu"""
    console.print("[cyan]ACTION SELECTION[/cyan]\n")

    actions_display = [
        "1. Convert EPUB to EPUB (refresh HTML)",
        "2. Repair HTML",
        "3. Beautify all files",
        "4. Remove unused CSS",
        "5. Check and auto-fix errors",
        "6. Remove embedded fonts",
        "7. Run full workflow (all steps)",
        "Cancel"
    ]

    choice = questionary.select(
        "Select action(s) to perform:",
        choices=actions_display
    ).ask()

    if choice is None or "Cancel" in choice:
        console.print("[yellow]Cancelled[/yellow]")
        sys.exit(0)

    if "full workflow" in choice.lower():
        return ["convert", "repair", "beautify", "css", "check", "fonts"]

    actions_map = {
        "1. Convert": "convert",
        "2. Repair": "repair",
        "3. Beautify": "beautify",
        "4. Remove unused": "css",
        "5. Check": "check",
        "6. Remove embedded": "fonts"
    }

    selected = []
    for action_name, action_key in actions_map.items():
        if action_name in choice:
            selected.append(action_key)

    console.print(f"\n[green]✓[/green] Selected actions: {', '.join(selected)}\n")

    return selected if selected else ["convert"]


# ============================================================================
# WORKFLOW PROCESSING
# ============================================================================

def process_convert_epub(input_path: Path, output_path: Path = None) -> bool:
    """Convert EPUB to EPUB using ebook-convert (refresh HTML)"""
    try:
        out_path = output_path or input_path

        console.print("  [cyan]→[/cyan] Converting EPUB to EPUB (refresh HTML)...", end=" ")

        result = subprocess.run(
            ['ebook-convert', str(input_path), str(out_path), '--pretty-print'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            console.print("[green]✓[/green]")
            return True
        else:
            console.print(f"[red]✗[/red]")
            console.print(f"    [red]Error: {result.stderr}[/red]")
            return False
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
        return False


def process_repair_html(container) -> bool:
    """Repair HTML"""
    try:
        from calibre.ebooks.oeb.polish.pretty import fix_all_html

        console.print("  [cyan]→[/cyan] Repairing HTML...", end=" ")
        fix_all_html(container)
        console.print("[green]✓[/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
        return False


def process_beautify(container) -> bool:
    """Beautify all files"""
    try:
        from calibre.ebooks.oeb.polish.pretty import pretty_all

        console.print("  [cyan]→[/cyan] Beautifying files...", end=" ")
        pretty_all(container)
        console.print("[green]✓[/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
        return False


def process_remove_css(container) -> bool:
    """Remove unused CSS"""
    try:
        from calibre.ebooks.oeb.polish.css import remove_unused_css

        console.print("  [cyan]→[/cyan] Removing unused CSS...", end=" ")
        remove_unused_css(
            container,
            remove_unused_classes=True,
            merge_rules=True,
            remove_unreferenced_sheets=True
        )
        console.print("[green]✓[/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
        return False


def process_check_errors(container) -> Tuple[bool, int, int]:
    """Check and auto-fix errors"""
    try:
        from calibre.ebooks.oeb.polish.check.main import run_checks, fix_errors

        console.print("  [cyan]→[/cyan] Checking for errors...", end=" ")
        errors = run_checks(container)

        if errors:
            error_count = len(errors)
            console.print(f"[yellow]Found {error_count}[/yellow]", end=" ")

            console.print("[cyan]Fixing...[/cyan]", end=" ")
            fixed = fix_errors(container, errors)

            if fixed:
                console.print("[green]✓[/green]")
                return True, error_count, error_count
            else:
                console.print("[yellow]Partial[/yellow]")
                return True, error_count, 0
        else:
            console.print("[green]No errors[/green]")
            return True, 0, 0
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
        return False, 0, 0


def process_remove_fonts(container) -> Tuple[bool, int]:
    """Remove embedded fonts"""
    try:
        from calibre.ebooks.oeb.polish.fonts import change_font, font_family_data

        console.print("  [cyan]→[/cyan] Removing fonts...", end=" ")

        fonts_data = font_family_data(container)
        embedded_fonts = [f for f, is_embedded in fonts_data.items() if is_embedded]

        if embedded_fonts:
            for font_name in embedded_fonts:
                change_font(container, font_name, new_name=None)
            console.print(f"[green]✓ ({len(embedded_fonts)} fonts)[/green]")
            return True, len(embedded_fonts)
        else:
            console.print("[green]✓ (none found)[/green]")
            return True, 0
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
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

    console.print(f"\n[cyan]Processing: {epub_path.name}[/cyan]")

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
        epub_path.stat()  # Refresh file

    # Load container for other operations
    try:
        from calibre.ebooks.oeb.polish.container import get_container
        container = get_container(str(epub_path), tweak_mode=True)
    except Exception as e:
        console.print(f"[red]ERROR: Cannot open EPUB: {e}[/red]")
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
        console.print("  [cyan]→[/cyan] Saving EPUB...", end=" ")
        container.commit(outpath=str(output_path))
        console.print("[green]✓[/green]")
        return True, stats
    except Exception as e:
        console.print(f"[red]✗[/red]")
        console.print(f"    [red]Exception: {e}[/red]")
        return False, stats


# ============================================================================
# BATCH PROCESSING
# ============================================================================

def process_batch(epub_files: List[Path], actions: List[str], output_dir: Path = None):
    """Process multiple EPUB files with progress tracking"""

    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[cyan]Output directory created: {output_dir}[/cyan]\n")

    results = []
    success_count = 0
    fail_count = 0

    total = len(epub_files)
    console.print(f"[cyan]Processing {total} file(s)...[/cyan]\n")

    for i, epub_path in enumerate(epub_files, 1):
        console.print(f"[dim][{i}/{total}][/dim]", end=" ")

        success, stats = process_epub_file(epub_path, actions, output_dir)

        if success:
            success_count += 1
            console.print(f"[green]DONE[/green]\n")
        else:
            fail_count += 1
            console.print(f"[red]FAILED[/red]\n")

        results.append({
            "file": epub_path.name,
            "success": success,
            "stats": stats
        })

    # Summary
    console.print("\n" + "="*60)
    console.print("[cyan]SUMMARY[/cyan]")
    console.print("="*60)
    console.print(f"  Total files: {total}")
    console.print(f"  [green]Successful: {success_count}[/green]")
    console.print(f"  [red]Failed: {fail_count}[/red]")

    if output_dir:
        console.print(f"  Output directory: [yellow]{output_dir}[/yellow]")

    console.print("="*60 + "\n")

    return results


# ============================================================================
# OUTPUT PATH
# ============================================================================

def select_output_path(input_path: str) -> Path:
    """Select or confirm output directory"""
    use_custom = questionary.confirm(
        "Save to a different directory?",
        default=False
    ).ask()

    if use_custom:
        output_path = questionary.path(
            "Select output directory:",
            default=str(Path.home())
        ).ask()
        return Path(output_path).expanduser().resolve() if output_path else None

    return None


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""

    # Check environment
    if not check_environment():
        console.print("[red]ERROR: Environment check failed[/red]")
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) < 2:
        console.print("[red]ERROR: Missing input path[/red]")
        console.print("[yellow]Usage: calibre-debug -e epub_workflow.py -- <input> [output][/yellow]")
        sys.exit(1)

    input_path = sys.argv[1]
    preset_output = sys.argv[2] if len(sys.argv) > 2 else None

    # Select files
    epub_files, mode = select_files(input_path)

    # Select actions
    actions = select_actions()

    # Select output path
    if preset_output:
        output_dir = Path(preset_output).expanduser().resolve()
        console.print(f"[cyan]Output directory: {output_dir}[/cyan]\n")
    else:
        output_dir = select_output_path(input_path)
        if output_dir:
            console.print(f"[cyan]Output directory: {output_dir}[/cyan]\n")

    # Confirm
    console.print("[yellow]Ready to process. Press ENTER to start or Ctrl+C to cancel[/yellow]")
    try:
        input()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
        sys.exit(0)

    # Process
    if len(epub_files) == 1:
        process_epub_file(epub_files[0], actions, output_dir)
    else:
        process_batch(epub_files, actions, output_dir)

    console.print("[green]✓ All done![/green]\n")


if __name__ == "__main__":
    main()
