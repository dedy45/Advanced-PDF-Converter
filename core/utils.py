"""
Utility Functions for PDF Converter
===================================
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Try to import magic, but provide fallback
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

console = Console()

def check_pandoc_installation() -> bool:
    """
    Memeriksa apakah pandoc sudah terinstall
    """
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_pandoc_guide():
    """
    Menampilkan panduan instalasi pandoc
    """
    guide_text = """
    [bold red]Pandoc belum terinstall![/bold red]
    
    Silakan install pandoc dari: https://pandoc.org/installing.html
    
    [bold]Untuk Windows:[/bold]
    1. Download installer dari https://github.com/jgm/pandoc/releases
    2. Jalankan file .msi dan ikuti petunjuk instalasi
    3. Restart command prompt/terminal
    
    [bold]Alternatif menggunakan conda:[/bold]
    conda install -c conda-forge pandoc
    
    [bold]Menggunakan chocolatey:[/bold]
    choco install pandoc
    """
    
    console.print(Panel(guide_text, title="Panduan Instalasi Pandoc", 
                       border_style="red"))

def get_file_type(file_path: Path) -> str:
    """
    Mendapatkan tipe file menggunakan python-magic atau fallback
    """
    if MAGIC_AVAILABLE:
        try:
            mime = magic.Magic(mime=True)
            return mime.from_file(str(file_path))
        except Exception:
            pass
    
    # Fallback to extension-based detection
    return f"application/{file_path.suffix.lower().lstrip('.')}"

def validate_pdf_file(file_path: Path) -> Tuple[bool, str]:
    """
    Memvalidasi apakah file adalah PDF yang valid
    """
    if not file_path.exists():
        return False, f"File tidak ditemukan: {file_path}"
    
    if file_path.suffix.lower() != '.pdf':
        return False, f"File bukan PDF: {file_path}"
    
    # Check file size
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    if file_size_mb > 100:  # 100MB limit
        return False, f"File terlalu besar: {file_size_mb:.1f}MB (maksimum: 100MB)"
    
    # Check if it's actually a PDF file
    if MAGIC_AVAILABLE:
        file_type = get_file_type(file_path)
        if 'pdf' not in file_type.lower():
            return False, f"File bukan PDF yang valid: {file_type}"
    else:
        # Simple check - just verify extension
        pass  # Extension already checked above
    
    return True, "File PDF valid"

def create_output_directory(output_dir: Path, format_name: str) -> Path:
    """
    Membuat direktori output untuk format tertentu
    """
    format_dir = output_dir / format_name
    format_dir.mkdir(parents=True, exist_ok=True)
    return format_dir

def clean_temp_directory(temp_dir: Path):
    """
    Membersihkan direktori temporary
    """
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

def get_available_pdf_files(directory: Path) -> List[Path]:
    """
    Mendapatkan semua file PDF di direktori
    """
    pdf_files = []
    
    # Search in root directory
    for file in directory.glob("*.pdf"):
        if file.is_file():
            pdf_files.append(file)
    
    # Search in subdirectories
    for subdir in directory.iterdir():
        if subdir.is_dir():
            for file in subdir.glob("*.pdf"):
                if file.is_file():
                    pdf_files.append(file)
    
    return sorted(pdf_files)

def format_file_size(size_bytes: int) -> str:
    """
    Format ukuran file yang mudah dibaca
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def show_success_message(input_file: Path, output_file: Path, format_name: str):
    """
    Menampilkan pesan sukses konversi
    """
    success_text = f"""
    [bold green]✓ Konversi Berhasil![/bold green]
    
    [bold]Input:[/bold] {input_file.name}
    [bold]Output:[/bold] {output_file.name}
    [bold]Format:[/bold] {format_name}
    [bold]Lokasi:[/bold] {output_file.parent}
    [bold]Ukuran:[/bold] {format_file_size(output_file.stat().st_size)}
    """
    
    console.print(Panel(success_text, title="Konversi Selesai", 
                       border_style="green"))

def show_error_message(error: str):
    """
    Menampilkan pesan error
    """
    console.print(Panel(f"[bold red]Error:[/bold red] {error}", 
                       title="Terjadi Kesalahan", border_style="red"))
