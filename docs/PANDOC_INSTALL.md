# 🔧 PANDOC INSTALLATION GUIDE - WINDOWS 11

## ⚡ Quick Install (Recommended)

### Method 1: Direct Download
1. Go to: **https://github.com/jgm/pandoc/releases**
2. Download: `pandoc-3.x.x-windows-x86_64.msi` (latest version)
3. Run the installer (double-click)
4. Follow installation wizard (just click Next → Next → Install)
5. **Restart Command Prompt**
6. Test: Open new command prompt and type `pandoc --version`

### Method 2: Using Chocolatey (if you have it)
```cmd
choco install pandoc
```

### Method 3: Using Conda (if you have Anaconda)
```cmd
conda install -c conda-forge pandoc
```

---

## ✅ How to Test Pandoc Installation

Open Command Prompt and type:
```cmd
pandoc --version
```

Should show something like:
```
pandoc 3.1.9
Features: +server +lua
Scripting engine: Lua 5.4
User data directory: C:\Users\[username]\AppData\Roaming\pandoc
```

---

## 🚀 After Installing Pandoc

1. **Restart Command Prompt** (important!)
2. Go to PDF converter directory:
   ```cmd
   cd e:\pdftradealgo\pdf_converter
   ```
3. Run one of these:
   - `start_converter.bat` (double-click)
   - `test_run.bat` (for testing)
   - `python main.py` (direct)

---

## 🐛 Troubleshooting

### "pandoc not found" after installation
- **Restart Command Prompt** completely
- Check if pandoc is in PATH:
  ```cmd
  where pandoc
  ```
- If still not found, try logging out and back in to Windows

### Download is slow
- Use Method 2 (Chocolatey) or 3 (Conda) if available
- Download during off-peak hours

### Antivirus blocking
- Temporarily disable antivirus during installation
- Add pandoc.exe to antivirus whitelist

---

## 📋 File Sizes (for reference)

- **pandoc-3.x.x-windows-x86_64.msi**: ~30-40 MB
- Installation takes: ~1-2 minutes
- Installed size: ~100-150 MB

---

## 🎯 After Success

Once pandoc is installed, PDF Converter will be able to:
- ✅ Convert PDF to Markdown
- ✅ Convert PDF to HTML  
- ✅ Convert PDF to Word (DOCX)
- ✅ Extract images from PDFs
- ✅ Batch process multiple files

**Ready to convert your 50+ PDF files! 🎉**
