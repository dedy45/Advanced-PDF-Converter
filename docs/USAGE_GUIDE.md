# 📚 Usage Guide - Advanced PDF Converter

**Complete guide untuk menggunakan PDF Converter secara maksimal**

---

## 🚀 **Quick Start**

### 1️⃣ **Installation & Setup**
```bash
# Option 1: One-click installer
start_converter.bat

# Option 2: Manual setup
pip install -r requirements.txt
python main.py
```

### 2️⃣ **Basic Conversion**
```bash
# Place your PDF files in the main directory
# Run converter
python main.py

# Choose your PDF file
# Select conversion mode
# Done! ✨
```

---

## 🎯 **Conversion Modes Detailed**

### 🔄 **Hybrid Mode (`md-hybrid`)** - RECOMMENDED
**Best for: Trading books, technical documents, course materials**

**Features:**
- ✅ **Text extraction**: Searchable and editable content
- ✅ **Image preservation**: Charts, diagrams, screenshots kept as PNG
- ✅ **Smart processing**: Automatically detects content type
- ✅ **Optimized performance**: Smart sampling for large files

**Example input**: Trading PDF with candlestick charts
**Example output**:
```markdown
## Market Structure Analysis

BMS (Break in Market Structure) occurs when price breaks...

![Chart: Candlestick Pattern](images/page_5.png)

### Key Trading Rules:
1. Always wait for retracement after BMS
2. Use 50% or OTE Fibonacci levels
```

**File structure created**:
```
output/md/
├── TradingBook.md                    # Main markdown file
└── TradingBook_images/               # Image folder
    ├── page_1.png                   # Cover
    ├── page_5.png                   # Chart 1
    ├── page_12.png                  # Chart 2
    └── ...
```

### 🔍 **OCR Mode (`md-ocr`)**
**Best for: Scanned PDFs, image-based documents**

**Features:**
- ✅ **Full OCR processing**: Converts images to searchable text
- ✅ **Smart sampling**: For large files, samples key pages
- ✅ **Text-only output**: Fully searchable and editable
- ✅ **Language support**: Auto-detects text language

**Example**: Scanned trading book
**Output**: All content converted to searchable text

### 📝 **Standard Mode (`md`)**
**Best for: Text-heavy PDFs, quick conversion**

**Features:**
- ✅ **Fast processing**: Text extraction only
- ✅ **Universal compatibility**: Works with all PDF types
- ✅ **Lightweight output**: No image processing

---

## 🎛️ **Advanced Features**

### 📊 **Batch Processing**
Convert multiple PDFs at once:
```bash
# Place multiple PDFs in main directory
python main.py

# Select: all
# Choose format: md-hybrid
# All files converted automatically
```

### ⚙️ **Smart File Analysis**
The converter automatically:
- **Analyzes file size** → Chooses optimal processing method
- **Detects content type** → Text vs image-heavy documents
- **Applies timeout protection** → Prevents hanging on large files
- **Optimizes image quality** → Balance between quality and file size

### 🎯 **Performance Modes**

| File Size | Pages | Processing Mode | Time Estimate |
|-----------|-------|----------------|---------------|
| < 10MB | < 50 | Full extraction | 30-60 seconds |
| 10-50MB | 50-100 | Smart sampling | 2-5 minutes |
| 50-100MB | 100+ | Optimized batch | 5-10 minutes |
| > 100MB | Any | OCR sampling | 5-15 minutes |

---

## 🔧 **Troubleshooting**

### Common Issues & Solutions:

#### ❌ **"No images extracted in hybrid mode"**
**Cause**: PyMuPDF not installed or pdf2image issue
**Solution**:
```bash
# Install PyMuPDF
pip install PyMuPDF

# Check pdf2image
pip install --upgrade pdf2image

# Verify installation
python main.py --check
```

#### ❌ **"Conversion very slow"**
**Cause**: Large file without smart sampling
**Solution**:
- Use `md-ocr` mode for large scanned files
- File > 50MB automatically uses smart sampling
- Close other applications to free memory

#### ❌ **"Pandoc not found"**
**Cause**: Pandoc not installed or not in PATH
**Solution**:
```bash
# Download and install Pandoc
# https://pandoc.org/installing.html

# Add to PATH (Windows)
# System Properties → Environment Variables → PATH

# Verify installation
pandoc --version
```

---

## 🎯 **Best Practices**

### For Trading PDFs:
1. **Use hybrid mode** - Preserves charts and technical analysis
2. **Check image quality** - Ensure charts are readable
3. **Organize by topic** - Group related trading books
4. **Backup originals** - Keep original PDFs safe

### For Course Materials:
1. **Batch process** - Convert entire course at once
2. **Use consistent naming** - Course_Chapter_Topic format
3. **Check completeness** - Verify all pages converted
4. **Create index** - Link related documents

---

**Happy Converting! 📚➡️📝🚀**
