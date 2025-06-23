# PDF Converter Tool

Alat konversi PDF yang powerful untuk mengubah file PDF ke berbagai format seperti Markdown, HTML, Word, dan lainnya menggunakan pandoc.

## ✨ Fitur Utama

- **Multi-format Output**: Mendukung konversi ke Markdown, HTML, DOCX, TXT, RTF, ODT, EPUB, LaTeX, dan JSON
- **Ekstraksi Gambar**: Otomatis mengekstrak dan menyimpan gambar dari PDF
- **Batch Processing**: Konversi multiple file sekaligus
- **Interface yang User-friendly**: Menu interaktif dengan tampilan yang menarik
- **Validasi File**: Memvalidasi file PDF sebelum konversi
- **Output Terorganisir**: File hasil disimpan dalam folder terpisah berdasarkan format

## 🚀 Cara Instalasi

### Prasyarat

1. **Python 3.8+** dengan Anaconda
2. **Pandoc** - Download dari [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

#### Instalasi Pandoc di Windows:
```bash
# Menggunakan conda (recommended)
conda install -c conda-forge pandoc

# Atau download installer dari:
# https://github.com/jgm/pandoc/releases

# Atau menggunakan chocolatey:
choco install pandoc
```

### Instalasi Dependencies

1. **Cara Otomatis (Recommended)**:
   - Double-click file `run_converter.bat`
   - Script akan otomatis membuat environment dan install dependencies

2. **Cara Manual**:
   ```bash
   # Buat conda environment
   conda create -n converterpdf python=3.11 -y
   conda activate converterpdf
   
   # Install dependencies
   pip install -r requirements.txt
   ```

## 📁 Struktur Project

```
pdf_converter/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Command line interface
│   ├── converter.py         # Core conversion logic
│   └── utils.py             # Utility functions
├── output/                  # Hasil konversi (dibuat otomatis)
│   ├── md/                  # File Markdown
│   ├── html/                # File HTML
│   ├── docx/                # File Word
│   └── ...                  # Format lainnya
├── temp/                    # File temporary (dibuat otomatis)
├── config.py                # Konfigurasi
├── requirements.txt         # Dependencies
├── main.py                  # Entry point utama
├── run_converter.bat        # Launcher Windows
└── README.md               # Dokumentasi ini
```

## 🎯 Cara Penggunaan

### 1. Menggunakan Batch File (Recommended)
```bash
# Double-click atau jalankan dari command prompt
start_converter.bat
```

### 2. Menggunakan Python Langsung
```bash
# Dengan conda environment (jika tersedia)
conda run --live-stream --name converterpdf python main.py

# Atau langsung dengan Python
python main.py
```

### 3. Testing & Troubleshooting
```bash
# Test sistem sebelum konversi
python quick_test.py

# Troubleshooting jika ada masalah  
troubleshoot.bat

# Install dependencies manual
install.bat
```

### 3. Workflow Penggunaan

1. **Jalankan Program**: Gunakan salah satu metode di atas
2. **Pilih File PDF**: Program akan menampilkan daftar semua file PDF di direktori
3. **Pilih File Target**: 
   - Ketik nomor file (contoh: `1,3,5`)
   - Ketik `all` untuk semua file
   - Ketik `q` untuk keluar
4. **Pilih Format Output**: 
   - **`md-img`** (RECOMMENDED): Markdown dengan gambar lengkap
   - **`md`**: Markdown text-only
   - **`html`**: HTML dengan gambar
   - **`docx`**: Microsoft Word
   - Dan format lainnya
5. **Konfirmasi**: Tekan `y` untuk memulai konversi
6. **Selesai**: File hasil akan tersimpan di folder `output/[format]/`

### 🎯 Rekomendasi Format

| Untuk Apa | Format Terbaik | Alasan |
|------------|----------------|---------|
| **PDF Trading Books** | `md-img` | Perfect untuk chart + text |
| **Technical Analysis** | `md-img` | Grafik tetap terlihat jelas |
| **Documentation** | `md-img` atau `md` | Mudah diedit dan dibaca |
| **Sharing Online** | `html` | Self-contained dengan gambar |
| **Collaboration** | `docx` | Editable di Microsoft Word |

## 📋 Format Yang Didukung

| Kode | Format | Deskripsi |
|------|--------|-----------|
| `md-img` | **Markdown with Images** | **🔥 RECOMMENDED - Markdown dengan gambar lengkap** |
| `md` | Markdown | Text-only markdown untuk editing |
| `html` | HTML | Untuk web dan presentasi |
| `docx` | Microsoft Word | Format dokumen Word |
| `txt` | Plain Text | Text sederhana tanpa format |
| `rtf` | Rich Text Format | Format text dengan basic formatting |
| `odt` | OpenDocument Text | Format OpenOffice/LibreOffice |
| `epub` | EPUB eBook | Format buku elektronik |
| `latex` | LaTeX | Untuk publikasi akademik |
| `json` | JSON | Format data terstruktur |

## 🔧 Konfigurasi Lanjutan

### Custom Pandoc Options

Anda dapat mengmodifikasi opsi pandoc di file `config.py`:

```python
PANDOC_OPTIONS = {
    'md': [
        '--extract-media=temp/images',
        '--wrap=none',
        '--standalone'
    ],
    'html': [
        '--extract-media=temp/images',
        '--standalone',
        '--self-contained'
    ],
    # ... dst
}
```

### Pengaturan Output

- **Lokasi Output**: File hasil disimpan di `output/[format]/`
- **Gambar**: Gambar yang diekstrak disimpan di `output/[format]/[filename]_images/`
- **File Temporary**: Disimpan di `temp/` dan dibersihkan setelah konversi

## 🐛 Troubleshooting

## 🔧 Troubleshooting

### ✅ **MD-HYBRID SUDAH DIPERBAIKI!**
**Issue fixed:** md-hybrid tidak lagi stuck/hanging
**Solusi:** Menggunakan Fast PDF Processor dengan timeout protection

### Error: "Pandoc tidak ditemukan"
- Pastikan pandoc sudah terinstall dan ada di PATH
- Coba restart command prompt setelah instalasi pandoc

### Error: "Unknown input format pdf" 
**SUDAH DIPERBAIKI:** Sekarang menggunakan Fast PDF Processor
- **md-hybrid**: Fast text + image extraction dengan timeout
- **md-ocr**: Smart OCR dengan page sampling untuk file besar

### Conversion lambat atau hanging?
**SUDAH DIPERBAIKI:** 
- ✅ Timeout protection (max 5 menit)
- ✅ Smart sampling untuk PDF besar (>20 pages)
- ✅ Progress indicators yang real-time
- ✅ Memory-efficient processing

### Error: "Import module could not be resolved"
- Jalankan `pip install -r requirements.txt`
- Atau gunakan `start_converter.bat`

### Error: "File PDF tidak valid"
- Pastikan file benar-benar dalam format PDF
- Periksa apakah file tidak corrupt
- Cek ukuran file (maksimum 100MB untuk optimal performance)

## 📝 Contoh Output

### 🔥 Markdown with Images (md-img) - RECOMMENDED
- **File utama**: `document.md`
- **Gambar**: `document_images/` folder dengan PNG files
- **Fitur**: 
  - Text yang bisa diekstrak ditampilkan sebagai text
  - Halaman dengan sedikit text dikonversi jadi gambar
  - Gambar embedded dalam PDF diekstrak terpisah
  - Perfect untuk PDF yang kombinasi text + gambar

### Markdown (md) - Text Only
- File utama: `document.md`
- Format yang clean dan mudah diedit
- Hanya text, tidak ada gambar

### HTML (html)
- File standalone dengan gambar embedded
- Bisa dibuka langsung di browser
- Cocok untuk sharing dan presentasi

### Word (docx)
- Format yang bisa diedit di Microsoft Word
- Mempertahankan formatting dan gambar
- Cocok untuk kolaborasi

## 🔄 Update dan Maintenance

Untuk update dependencies:
```bash
conda activate converterpdf
pip install --upgrade -r requirements.txt
```

## 📞 Support

Jika mengalami masalah:
1. Periksa error message yang muncul
2. Pastikan semua dependencies terinstall
3. Coba dengan file PDF yang berbeda
4. Restart command prompt dan coba lagi

## 📜 License

Tool ini dibuat untuk keperluan pribadi dan pembelajaran. Silakan digunakan dan dimodifikasi sesuai kebutuhan.

---

**Happy Converting! 🎉**
