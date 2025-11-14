# EPUB Workflow Plugin for Calibre

Automation plugin for EPUB processing with interactive menu, batch processing and recursive scanning.

**Author:** Florent Bertiaux (u/iamkxrz on Reddit)

## 📋 Description

EPUB Workflow is a Calibre plugin that automates EPUB file processing with an intuitive graphical interface. It offers several processing actions that you can combine according to your needs:

- **Convert EPUB to EPUB** : Refresh HTML
- **Repair HTML** : Fix HTML errors
- **Beautify** : Format and indent code
- **Remove unused CSS** : Remove unused CSS
- **Check and auto-fix errors** : Check and automatically fix errors
- **Remove embedded fonts** : Remove embedded fonts
- **Resize images to 480px** : Resize images for Xteink e-readers (irreversible)

## ✨ Features

- 🎯 **Intuitive graphical interface** : Easily select actions to perform
- 📦 **Batch processing** : Process multiple EPUBs at once
- 🔄 **Automatic backup** : A backup copy is automatically created before any modification
- 🌍 **Multilingual** : French and English support (follows Calibre's language)
- ⚡ **Fast processing** : Uses Calibre's polish tools for efficient processing

## 📦 Installation

1. Download the `epub_workflow_plugin.zip` file
2. Open Calibre
3. Go to **Preferences** → **Plugins** → **Load plugin from file**
4. Select the `epub_workflow_plugin.zip` file
5. Restart Calibre

## 🚀 Usage

1. Select one or more EPUB books in your Calibre library
2. Click on the **EPUB Workflow** icon in the toolbar (or add it via **Preferences** → **Interface** → **Toolbars**)
3. In the configuration dialog, select the actions to perform
4. Click **OK** to start processing

### ⚠️ Important

- **Automatic backup** : A backup copy (`filename_backup.epub`) is automatically created in the same folder as the original EPUB before any modification
- **Modified file** : The file in your library will be modified with all selected actions
- **Image resizing** : The image resizing operation is irreversible. A backup copy is always created before processing.

## 🔧 Available Actions

| Action | Description |
|--------|-------------|
| **Convert EPUB to EPUB** | Refreshes HTML by reconverting the EPUB |
| **Repair HTML** | Fixes HTML errors in the file |
| **Beautify** | Formats and indents HTML/CSS code |
| **Remove unused CSS** | Removes unused CSS to reduce file size |
| **Check and auto-fix errors** | Checks and automatically fixes detected errors |
| **Remove embedded fonts** | Removes embedded fonts |
| **Resize images to 480px** | Resizes images to 480px width (for Xteink e-readers) |

## 📁 File Structure

```
epub_workflow_plugin/
├── __init__.py              # Plugin entry point
├── plugin.py                # Main plugin class
├── config_dialog.py         # Configuration interface
├── progress_dialog.py       # Progress dialog
├── workflow_engine.py       # Processing engine
├── translations.py          # Translation system
├── images/
│   └── epub_workflow.png    # Plugin icon
└── README.md                # This file
```

## 🌍 Supported Languages

- **French** : If Calibre is in French
- **English** : Default or if Calibre is in another language

## 📝 Notes

- `.kepub.epub` files are automatically ignored
- The plugin requires Calibre 6.0 or higher
- The backup copy is overwritten if it already exists during a new processing

## 🔗 Python CLI Version

A standalone Python script version is available in the **`Python-CLI`** folder for command-line use without Calibre.

## 🐛 Known Issues

- The plugin can only process EPUB files. If you select books in other formats, a message will invite you to convert them to EPUB first.

## 📄 License

GPL v3

## 👤 Author

**Florent Bertiaux** (u/iamkxrz on Reddit)

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or a pull request.

---

**Note** : This plugin uses Calibre's polish tools for EPUB processing. Make sure you have a recent version of Calibre installed.
