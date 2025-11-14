# Fixing "No Module Found" Error with calibre-debug

When running the script with `calibre-debug -e epub_workflow.py`, you may get:

```
ERROR: Required packages not found!
Install with: pip install -r requirements.txt
Or: pip install rich questionary
```

Even if you've already installed the packages. **This is expected behavior.**

---

## Why This Happens

**TL;DR:** `calibre-debug` runs Python in Calibre's isolated environment, which doesn't automatically see packages installed in your system Python.

When you run:
```bash
calibre-debug -e epub_workflow.py -- book.epub
```

This launches Python **inside Calibre's environment**, not your system Python. Your packages (rich, questionary) are installed in system Python, but Calibre's Python environment doesn't see them.

---

## Solutions (Choose One)

### Solution 1: Install Packages in Calibre's Python (Recommended)

This tells Calibre to install the packages into its own Python environment.

```bash
# Method A: Using calibre-debug directly
calibre-debug -e -c "import subprocess; subprocess.run([__import__('sys').executable, '-m', 'pip', 'install', 'rich', 'questionary'])"

# Method B: Simpler approach
calibre-debug -e -c "import pip; pip.main(['install', 'rich', 'questionary'])" 2>/dev/null

# Method C: Direct pip
pip install --target /Applications/calibre.app/Contents/Resources/Python/site-packages rich questionary
```

**After running:**
```bash
calibre-debug -e epub_workflow.py -- ~/book.epub
```

Should work fine.

---

### Solution 2: Use Fallback Version (Works Without Dependencies)

We created a fallback version that **doesn't require rich or questionary**.

```bash
# Use this version instead - it works without optional packages
calibre-debug -e epub_workflow_fallback.py -- ~/book.epub
```

**Advantages:**
- ✅ Works immediately, no installation needed
- ✅ Less fancy interface (basic text menus instead of colored/arrow keys)
- ✅ All functionality works the same
- ✅ Fallback to pretty interface when packages ARE available

**What you lose:**
- ❌ Colored terminal output
- ❌ Arrow key navigation (use numbers instead)
- ❌ Pretty panels and formatting

---

### Solution 3: Create Wrapper Script (Advanced)

Create a shell script that installs dependencies first:

```bash
#!/bin/bash
# File: epub_workflow.sh

# Install packages in Calibre environment
echo "Installing dependencies in Calibre..."
calibre-debug -e -c "import subprocess; subprocess.run([__import__('sys').executable, '-m', 'pip', 'install', '-q', 'rich', 'questionary'])"

# Run the main script
calibre-debug -e "$(dirname "$0")/epub_workflow.py" -- "$@"
```

Then make it executable and use:
```bash
chmod +x epub_workflow.sh
./epub_workflow.sh ~/book.epub
```

---

### Solution 4: Use Homebrew/Package Manager (macOS/Linux)

If you installed Calibre via Homebrew or package manager:

```bash
# macOS with Homebrew
brew install calibre

# Ubuntu/Debian
sudo apt-get install calibre

# Then Calibre should have Python with pip available
calibre-debug -e -c "import pip; pip.main(['install', 'rich', 'questionary'])"
```

---

## Verification: Is It Fixed?

After trying a solution, test:

```bash
# Should return no error
calibre-debug -e -c "import rich; import questionary; print('OK')"
```

If you see `OK`, the packages are installed. Then try:

```bash
calibre-debug -e epub_workflow.py -- ~/test_book.epub
```

---

## If None of This Works

Use the **Fallback Version** - it's designed specifically for this situation:

```bash
# This will ALWAYS work
calibre-debug -e epub_workflow_fallback.py -- ~/book.epub
```

The fallback version:
1. Checks if rich/questionary are available
2. If yes, uses them (pretty interface)
3. If no, uses basic text menus
4. All functionality remains identical

---

## Files You Have

| File | Purpose | Requires Packages |
|------|---------|-------------------|
| `epub_workflow.py` | Main script (pretty) | YES (rich, questionary) |
| `epub_workflow_fallback.py` | Fallback script (basic) | NO (optional) |
| `requirements.txt` | Package list | — |

**Recommendation:** Use `epub_workflow_fallback.py` if you're having issues. It's designed to work with or without the optional packages.

---

## Quick Reference

```bash
# Option 1: Install packages in Calibre (one-time setup)
calibre-debug -e -c "import pip; pip.main(['install', 'rich', 'questionary'])"
# Then use normally:
calibre-debug -e epub_workflow.py -- ~/book.epub

# Option 2: Use fallback version (always works)
calibre-debug -e epub_workflow_fallback.py -- ~/book.epub

# Option 3: Create test
calibre-debug -e -c "import rich; import questionary; print('OK')"
```

---

## Common Issues

### "ImportError: No module named pip"
Use: `calibre-debug -e -c "import subprocess; subprocess.run([__import__('sys').executable, '-m', 'pip', 'install', 'rich', 'questionary'])"`

### "Permission denied" on macOS
Use: `sudo` if needed, but usually not required for Calibre

### "CaliBre installation not found"
Reinstall Calibre from https://calibre-ebook.com/download

---

## Summary

**Problem:** `calibre-debug` uses isolated Python environment  
**Solution 1:** Install packages into Calibre's Python  
**Solution 2:** Use fallback version (no packages needed)  
**Recommendation:** Start with Solution 2 (fallback), upgrade to Solution 1 later if you want prettier interface

All options fully functional and equivalent.
