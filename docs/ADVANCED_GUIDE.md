# 🔧 Advanced Features Guide

**Technical documentation untuk advanced users dan developers**

---

## 🏗️ **Architecture Overview**

### Core Components:
```
pdf_converter/
├── 🧠 core/                          # Core processing engine
│   ├── fast_pdf_processor.py         # Advanced hybrid processor
│   ├── converter.py                  # Main converter class
│   ├── pdf_extractor.py              # Text extraction engine
│   ├── cli.py                        # Command line interface
│   └── utils.py                      # Utility functions
├── 📁 scripts/                       # Automation scripts
├── 📁 docs/                          # Documentation
├── 📁 tests/                         # Test suite
└── 📁 output/                        # Conversion results
```

### Processing Pipeline:
```
PDF Input → Analysis → Mode Selection → Processing → Output
     ↓         ↓           ↓             ↓          ↓
   File     Content    Hybrid/OCR     Text+Img   Markdown
  Validation  Type    /Standard      Extraction   + Images
```

---

## ⚙️ **Processing Modes Deep Dive**

### 🔄 **Hybrid Mode Technical Details**

#### Smart Processing Algorithm:
```python
if file_size < 10MB and pages < 50:
    mode = "guaranteed_image_extraction"  # All pages → images
elif file_size < 50MB and pages < 100:
    mode = "smart_sampling"              # Key pages → images  
else:
    mode = "ocr_fallback"                # Text-focused
```

#### Image Extraction Strategy:
1. **PyMuPDF Method** (Primary):
   - Extract embedded images directly
   - Preserve original quality
   - Fastest processing

2. **pdf2image Method** (Fallback):
   - Convert pages to images
   - Guaranteed image output
   - More memory intensive

3. **Smart Sampling** (Large files):
   - First 5 pages (intro)
   - Pages with minimal text (likely charts)
   - Last 5 pages (conclusion)
   - Maximum 20 images for performance

#### Performance Optimizations:
```python
# Timeout protection
MAX_PROCESSING_TIME = 300  # 5 minutes

# Image quality settings
DPI_SETTINGS = {
    'fast': 150,    # Quick conversion
    'quality': 200, # Better quality
    'max': 300      # Best quality
}

# Memory management
BATCH_SIZE = 10     # Pages per batch
MAX_IMAGES = 50     # Image limit per document
```

### 🔍 **OCR Mode Technical Details**

#### OCR Processing Pipeline:
```
PDF → pdf2image → PIL Image → Tesseract → Text → Markdown
 ↓        ↓           ↓          ↓         ↓        ↓
File   Image      Optimized   OCR       Clean   Formatted
      Array      Resolution  Engine     Text    Output
```

#### Smart Sampling for Large PDFs:
```python
def smart_sampling(total_pages):
    sample_pages = []
    
    # Strategy 1: Key sections
    sample_pages.extend([1, 2, 3, 4, 5])  # Introduction
    
    # Strategy 2: Middle content  
    middle = total_pages // 2
    sample_pages.extend(range(middle-2, middle+3))
    
    # Strategy 3: Conclusion
    sample_pages.extend(range(total_pages-4, total_pages+1))
    
    return sorted(set(sample_pages))
```

#### OCR Optimization Settings:
```python
TESSERACT_CONFIG = {
    'oem': 3,        # OCR Engine Mode (LSTM)
    'psm': 6,        # Page Segmentation Mode (uniform block)
    'dpi': 200,      # Resolution for OCR
    'lang': 'eng'    # Language (auto-detect available)
}
```

---

## 🎛️ **Configuration & Customization**

### Performance Tuning:
```python
# In core/fast_pdf_processor.py
class FastPDFProcessor:
    def __init__(self):
        self.max_processing_time = 300      # Timeout (seconds)
        self.max_pages_for_image = 50       # Image conversion limit
        self.max_images_per_doc = 50        # Total image limit
        self.dpi_setting = 150              # Image quality
        self.batch_size = 10                # Processing batch size
```

### Custom Output Formats:
```python
# In core/converter.py
SUPPORTED_FORMATS = {
    'md-hybrid': 'Markdown with preserved images',
    'md-ocr': 'Markdown with OCR text',
    'md': 'Basic markdown',
    'html': 'Web format',
    'docx': 'Microsoft Word',
    'latex': 'Academic format',
    'epub': 'eBook format'
}
```

### Advanced Processing Options:
```python
# Custom conversion with options
converter = PDFConverter(temp_dir, output_dir)
result = converter.convert_pdf(
    input_file=pdf_path,
    output_format='md-hybrid',
    custom_options=[
        '--dpi=200',           # Higher image quality
        '--max-images=100',    # More images allowed
        '--timeout=600'        # Longer timeout
    ]
)
```

---

## 🔬 **Testing & Quality Assurance**

### Test Suite Structure:
```
tests/
├── test_fast.py              # Fast processor tests
├── test_direct.py            # Direct conversion tests  
├── test_market_specific.py   # Trading PDF tests
├── test_image_extraction.py  # Image processing tests
└── test_setup.py             # Environment tests
```

### Performance Benchmarks:
```python
# Run performance tests
python tests/test_fast.py

# Expected results:
# Small PDF (< 10MB): 30-60 seconds
# Medium PDF (10-50MB): 2-5 minutes  
# Large PDF (50-100MB): 5-10 minutes
```

### Quality Metrics:
- **Text Extraction Rate**: > 95% accuracy
- **Image Preservation**: > 90% of charts captured
- **Processing Success**: > 98% completion rate
- **Memory Efficiency**: < 2GB RAM usage

---

## 🛠️ **Development & Extension**

### Adding New Processors:
```python
# 1. Create new processor class
class CustomPDFProcessor:
    def convert_pdf(self, pdf_path, mode):
        # Your custom logic here
        return success, message, output_path

# 2. Register in converter.py
self.custom_processor = CustomPDFProcessor()

# 3. Add to supported formats
'custom-mode': 'Your custom description'
```

### Custom Output Formats:
```python
# Add new format to pandoc_options
'your-format': [
    '--your-option',
    '--another-option'
]
```

### Performance Monitoring:
```python
# Add timing and memory monitoring
import time
import psutil

start_time = time.time()
start_memory = psutil.Process().memory_info().rss

# ... processing ...

elapsed = time.time() - start_time
memory_used = psutil.Process().memory_info().rss - start_memory
print(f"Processed in {elapsed:.1f}s using {memory_used/1024/1024:.1f}MB")
```

---

## 🔧 **Troubleshooting Advanced Issues**

### Memory Issues:
```python
# Increase virtual memory (Windows)
# Control Panel → System → Advanced → Performance → Virtual Memory

# Code optimization for large files
def process_large_pdf(pdf_path):
    # Process in smaller chunks
    batch_size = 5  # Reduce batch size
    
    # Clear memory between batches
    import gc
    gc.collect()
    
    # Use generators instead of lists
    for page_batch in page_generator(pdf_path, batch_size):
        process_batch(page_batch)
        gc.collect()  # Force garbage collection
```

### Dependency Conflicts:
```bash
# Create isolated environment
python -m venv pdf_converter_env
pdf_converter_env\Scripts\activate

# Install specific versions
pip install PyPDF2==3.0.1
pip install pdf2image==1.16.3
pip install PyMuPDF==1.20.0
```

### Custom OCR Languages:
```python
# Install additional languages
# Download from: https://github.com/tesseract-ocr/tessdata

# Configure in fast_pdf_processor.py
OCR_CONFIG = {
    'lang': 'eng+fra+deu',  # English + French + German
    'oem': 3,
    'psm': 6
}
```

---

## 📊 **Monitoring & Analytics**

### Performance Logging:
```python
# Enable detailed logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)
```

### Conversion Statistics:
```python
class ConversionStats:
    def __init__(self):
        self.total_files = 0
        self.successful_conversions = 0
        self.total_pages = 0
        self.total_images = 0
        self.total_time = 0
        
    def log_conversion(self, pages, images, time_taken):
        self.total_files += 1
        self.successful_conversions += 1
        self.total_pages += pages
        self.total_images += images
        self.total_time += time_taken
```

---

## 🚀 **Production Deployment**

### Optimization for Production:
```python
# Production settings
PRODUCTION_CONFIG = {
    'max_workers': 4,           # Parallel processing
    'cache_enabled': True,      # Cache processed files
    'compression': True,        # Compress output images
    'backup_originals': True,   # Keep original PDFs
    'detailed_logging': True    # Full audit trail
}
```

### Batch Processing Script:
```python
# scripts/batch_convert.py
def batch_convert_directory(input_dir, output_dir, format='md-hybrid'):
    converter = PDFConverter(temp_dir, output_dir)
    
    for pdf_file in Path(input_dir).glob('*.pdf'):
        try:
            result = converter.convert_pdf(pdf_file, format)
            if result:
                print(f"✅ {pdf_file.name} → {result}")
            else:
                print(f"❌ Failed: {pdf_file.name}")
        except Exception as e:
            print(f"💥 Error: {pdf_file.name} - {e}")
```

---

## 🎯 **Best Practices for Developers**

### Code Organization:
- **Separation of concerns**: Each class has single responsibility
- **Error handling**: Comprehensive try-catch blocks
- **Logging**: Detailed logging for debugging
- **Testing**: Unit tests for all major functions

### Performance Guidelines:
- **Memory management**: Clean up large objects
- **Timeout protection**: Prevent infinite loops
- **Resource limits**: Set maximum processing limits
- **Progress feedback**: Keep users informed

### Security Considerations:
- **Input validation**: Verify PDF file integrity
- **Path traversal**: Prevent directory escape
- **Resource limits**: Prevent DoS via large files
- **Temporary cleanup**: Remove temp files securely

---

**Advanced usage unlocked! 🔓⚡**
