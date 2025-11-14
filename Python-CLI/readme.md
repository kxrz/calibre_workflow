# EPUB Batch Workflow - Interactive CLI Tool

A professional Python script for automating EPUB file processing and cleanup at scale. Process single files, entire directories, or recursively scan for EPUB files with an interactive menu-driven interface.

## Features

- **Interactive CLI Menu** with arrow keys and multi-step workflow
- **Single File or Batch Processing** - process one EPUB or hundreds in a directory
- **Recursive Scanning** - find and process EPUBs in nested folders
- **Full Workflow Automation**:
  - Convert EPUB to EPUB (refresh HTML with `ebook-convert`)
  - Repair malformed HTML
  - Beautify all files (proper indentation and formatting)
  - Remove unused CSS rules
  - Check and auto-fix errors
  - Remove all embedded fonts
  - Run full workflow in one command
- **Verbose Logging** - clear step-by-step progress with detailed output
- **Colored Output** - beautiful terminal interface with status indicators
- **Environment Check** - automatically detects missing dependencies and suggests fixes
- **Batch Progress Tracking** - see which files succeeded/failed when processing folders

## Prerequisites

### 1. Install Calibre
Download and install from https://calibre-ebook.com/download

Verify installation:
```bash
which calibre-debug
which ebook-convert
```

### 2. (macOS only) Add Calibre to PATH
If `calibre-debug` or `ebook-convert` commands not found, add to your shell profile:

```bash
# For zsh (macOS default)
echo 'export PATH="/Applications/calibre.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'export PATH="/Applications/calibre.app/Contents/MacOS:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Verify:
```bash
calibre-debug --version
ebook-convert --version
```

### 3. Install Python Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt

# Or manually:
pip install rich questionary
```

Verify Python version:
```bash
python3 --version  # Must be >= 3.6
```

## Quick Start

### 1. Basic Usage - Single File

```bash
calibre-debug -e epub_workflow.py -- ~/Desktop/mybook.epub
```

### 2. Process All EPUBs in a Folder

```bash
calibre-debug -e epub_workflow.py -- ~/Calibre\ Library/Fiction
```

The script will prompt you to:
- Choose file selection mode (single file, all in folder, or recursive)
- Select which actions to perform (or run full workflow)
- Review results with detailed logging

### 3. Save Processed Files to New Location

```bash
calibre-debug -e epub_workflow.py -- input_folder output_folder
```

## Usage Guide

### Starting the Script

```bash
calibre-debug -e epub_workflow.py -- <input> [output]
```

**Arguments:**
- `<input>`: Path to EPUB file or directory containing EPUBs
- `[output]`: (Optional) Directory to save processed files. If omitted, files are processed in-place.

### Interactive Menu

Once launched, you'll see:

1. **Environment Check** - Verification of all required tools
2. **File Selection Menu**:
   - Select single file
   - Process all EPUBs in directory (non-recursive)
   - Process all EPUBs recursively (all subfolders)

3. **Action Selection Menu**:
   Use arrow keys to navigate:
   - Convert EPUB to EPUB (refresh HTML)
   - Repair HTML
   - Beautify all files
   - Remove unused CSS
   - Check and auto-fix errors
   - Remove embedded fonts
   - Run full workflow (all steps)
   - Exit

4. **Processing** - Watch real-time progress with verbose logging
5. **Results Summary** - Success count, failures, and detailed logs

## Available Actions

### 1. Convert EPUB to EPUB
Converts EPUB to EPUB format using `ebook-convert`, refreshing the internal HTML code. Useful for old/corrupted EPUB files.

### 2. Repair HTML
Uses Calibre's HTML5 parser to fix malformed HTML tags, unclosed elements, and invalid attributes.

### 3. Beautify All Files
Reformats HTML and CSS with proper indentation and spacing for readability.

### 4. Remove Unused CSS
Removes unused CSS rules, classes, and unreferenced stylesheets to reduce file size and complexity.

### 5. Check and Auto-Fix Errors
Runs Calibre's book checker to detect OPF errors, broken links, invalid covers, etc. Automatically fixes solvable issues.

### 6. Remove Embedded Fonts
Removes all embedded font files from the EPUB. Readers will use their default fonts instead.

### 7. Run Full Workflow
Executes all steps 1-6 in sequence automatically.

## Examples

### Example 1: Clean Single Book
```bash
calibre-debug -e epub_workflow.py -- ~/Downloads/book.epub
# Select: Single file
# Select: Run full workflow
# Result: Cleaned book.epub in place
```

### Example 2: Batch Clean Library
```bash
calibre-debug -e epub_workflow.py -- ~/Calibre\ Library
# Select: All EPUBs in directory (non-recursive)
# Select: Run full workflow
# Result: All books in library cleaned
```

### Example 3: Recursive Scan with Backup
```bash
mkdir ~/epub_cleaned
calibre-debug -e epub_workflow.py -- ~/old_books ~/epub_cleaned
# Select: All EPUBs recursively (all subfolders)
# Select: Remove unused CSS only
# Result: Cleaned files saved to ~/epub_cleaned, originals preserved
```

### Example 4: Check Errors Only
```bash
calibre-debug -e epub_workflow.py -- book.epub
# Select: Single file
# Select: Check and auto-fix errors
# Result: Report of errors found and fixed
```

## Troubleshooting

### Error: "calibre-debug: command not found"

**Solution 1 (macOS):** Add to PATH
```bash
echo 'export PATH="/Applications/calibre.app/Contents/MacOS:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Solution 2:** Use full path
```bash
/Applications/calibre.app/Contents/MacOS/calibre-debug -e epub_workflow.py -- book.epub
```

**Solution 3 (Linux):** Install Calibre package
```bash
sudo apt-get install calibre  # Debian/Ubuntu
sudo yum install calibre      # RHEL/CentOS
```

### Error: "ebook-convert: command not found"

Same solution as above - add Calibre to PATH.

### Error: "No module named 'rich'" or "questionary"

Install Python dependencies:
```bash
pip install -r requirements.txt
# or
pip install rich questionary
```

### Error: "ImportError: calibre modules not found"

Ensure you're running the script with `calibre-debug`:
```bash
# Correct
calibre-debug -e epub_workflow.py -- book.epub

# Wrong
python3 epub_workflow.py -- book.epub
```

### Error: "No EPUB files found in directory"

- Check folder path is correct
- Verify files have `.epub` extension (case-sensitive on Linux/macOS)
- Check file permissions (must be readable)

### Script Hangs or Stops Mid-Process

- Large EPUBs may take longer - be patient
- Check disk space (processing may temporarily use 2-3x file size)
- Kill with Ctrl+C and try a smaller test file first

## Performance Tips

### Processing Speed
- **Single file:** 30-60 seconds
- **10 files:** 5-10 minutes
- **100 files:** 30-60 minutes
- **1000+ files:** 5+ hours (consider running overnight)

### Optimize for Large Batches
```bash
# Process files in parallel (macOS/Linux)
# Note: Requires manual setup with GNU parallel
parallel calibre-debug -e epub_workflow.py -- {} ::: *.epub
```

## Environment Variables

You can optionally set:

```bash
# Use alternate Python interpreter
PYTHON=/usr/bin/python3 calibre-debug -e epub_workflow.py -- book.epub

# Verbose debug output (shows all API calls)
DEBUG=1 calibre-debug -e epub_workflow.py -- book.epub
```

## Supported Platforms

- **macOS** 10.12+ (tested on Big Sur, Monterey, Ventura, Sonoma)
- **Linux** (Ubuntu 18.04+, Debian 9+, etc.)
- **Windows** (via WSL2 or native Python with Calibre)

## Limitations

- **DRMS/DRM books:** Cannot process DRM-protected EPUBs (Calibre limitation)
- **Very large EPUBs:** May be slow (>100MB files) or cause memory issues
- **Corrupted files:** Some severely corrupted EPUBs cannot be recovered
- **Smarten punctuation:** Applied during conversion step only (Calibre limitation)

## Advanced: Batch Script Wrapper

Create `batch_epub.sh` for unattended processing:

```bash
#!/bin/bash
INPUT_DIR="$1"
OUTPUT_DIR="${2:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$OUTPUT_DIR"

calibre-debug -e "$SCRIPT_DIR/epub_workflow.py" -- "$INPUT_DIR" "$OUTPUT_DIR" << EOF
3
7
EOF
```

Then run:
```bash
chmod +x batch_epub.sh
./batch_epub.sh ~/Calibre\ Library ~/cleaned_books
```

## Support & Contributions

- **Issues?** Check troubleshooting section above
- **Calibre docs:** https://manual.calibre-ebook.com/
- **Report bugs:** Include Python version, Calibre version, and exact error message

## License

This script uses Calibre's official Python API. Calibre is licensed under GPLv3.

## Changelog

### v1.0.0 (Initial Release)
- Interactive CLI menu with arrow keys
- Single file and batch processing
- Recursive directory scanning
- Full workflow automation
- Verbose logging
- Environment detection and troubleshooting
- Support for macOS/Linux/Windows (WSL2)
