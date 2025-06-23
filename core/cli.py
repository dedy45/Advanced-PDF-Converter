"""
PDF Converter Command Line Interface
====================================
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

# Import dengan fallback untuk dependencies yang mungkin belum terinstall
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback console
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    
    class Prompt:
        @staticmethod
        def ask(prompt, choices=None, default=None):
            if choices:
                print(f"{prompt} {choices}")
            user_input = input(f"{prompt}: ")
            return user_input if user_input else default

# Import local modules
try:
    # Try relative imports first
    from .converter import PDFConverter
    from .utils import (
        get_available_pdf_files, check_pandoc_installation, 
        install_pandoc_guide, show_error_message
    )
except ImportError:
    # Fallback untuk import absolut
    import sys
    import os
    current_file_dir = os.path.dirname(__file__)
    sys.path.insert(0, current_file_dir)
    
    from converter import PDFConverter
    from utils import (
        get_available_pdf_files, check_pandoc_installation,
        install_pandoc_guide, show_error_message
    )

console = Console()

class PDFConverterCLI:
    """
    Command Line Interface untuk PDF Converter
    """
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.temp_dir = self.base_dir / "temp"
        self.output_dir = self.base_dir / "output"
        self.converter = PDFConverter(self.temp_dir, self.output_dir)
        
        # Buat direktori jika belum ada
        self.temp_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def show_banner(self):
        """
        Menampilkan banner aplikasi
        """
        banner_text = """
    ╔══════════════════════════════════════════════════════════╗
    ║                   PDF CONVERTER TOOL                     ║
    ║                                                          ║
    ║   Mengkonversi PDF ke berbagai format dengan pandoc     ║
    ║   Mendukung: Markdown, HTML, Word, Text, dan lainnya    ║
    ╚══════════════════════════════════════════════════════════╝
        """
        
        if RICH_AVAILABLE:
            console.print(Panel(banner_text, border_style="blue"))
        else:
            print(banner_text)
    
    def check_system_requirements(self) -> bool:
        """
        Memeriksa requirements sistem
        """
        if not check_pandoc_installation():
            install_pandoc_guide()
            return False
        
        return True
    
    def get_pdf_files_menu(self) -> List[Path]:
        """
        Menampilkan menu pemilihan file PDF
        """
        # Cari file PDF di direktori utama
        pdf_files = get_available_pdf_files(self.base_dir.parent)
        
        if not pdf_files:
            console.print("[red]Tidak ada file PDF ditemukan![/red]")
            return []
        
        if RICH_AVAILABLE:
            # Tampilkan tabel file PDF
            table = Table(title="File PDF Tersedia")
            table.add_column("No", style="cyan", width=4)
            table.add_column("Nama File", style="magenta")
            table.add_column("Ukuran", style="green")
            table.add_column("Lokasi", style="yellow")
            
            for i, pdf_file in enumerate(pdf_files, 1):
                file_size = pdf_file.stat().st_size / (1024 * 1024)  # MB
                table.add_row(
                    str(i),
                    pdf_file.name,
                    f"{file_size:.1f} MB",
                    str(pdf_file.parent.name)
                )
            
            console.print(table)
        else:
            print("\nFile PDF Tersedia:")
            print("-" * 60)
            for i, pdf_file in enumerate(pdf_files, 1):
                file_size = pdf_file.stat().st_size / (1024 * 1024)
                print(f"{i:2d}. {pdf_file.name} ({file_size:.1f} MB) - {pdf_file.parent.name}")
        
        return pdf_files
    
    def select_files(self, pdf_files: List[Path]) -> List[Path]:
        """
        Memilih file untuk dikonversi
        """
        print("\nPilihan:")
        print("- Ketik nomor file (misal: 1,3,5)")
        print("- Ketik 'all' untuk semua file")
        print("- Ketik 'q' untuk keluar")
        
        choice = input("\nMasukkan pilihan: ").strip().lower()
        
        if choice == 'q':
            return []
        elif choice == 'all':
            return pdf_files
        else:
            try:
                selected_indices = []
                for num_str in choice.split(','):
                    num = int(num_str.strip())
                    if 1 <= num <= len(pdf_files):
                        selected_indices.append(num - 1)
                
                return [pdf_files[i] for i in selected_indices]
            except ValueError:
                console.print("[red]Input tidak valid![/red]")
                return []
    
    def select_output_format(self) -> Optional[str]:
        """
        Memilih format output
        """
        formats = self.converter.get_supported_formats()
        
        if RICH_AVAILABLE:
            table = Table(title="Format Output Tersedia")
            table.add_column("Kode", style="cyan")
            table.add_column("Nama Format", style="magenta")
            table.add_column("Deskripsi", style="green")
            
            descriptions = {
                'md': 'Text only markdown (basic)',
                'md-hybrid': '🔥 HYBRID: Text+images preserved (RECOMMENDED)',
                'md-ocr': '🔍 OCR: Everything as text (for scanned PDFs)',
                'html': 'HTML untuk web dan presentasi',
                'docx': 'Microsoft Word format',
                'txt': 'Plain text sederhana',
                'rtf': 'Rich Text Format',
                'odt': 'OpenDocument Text',
                'epub': 'Format eBook',
                'latex': 'Untuk publikasi akademik',
                'json': 'Format data terstruktur'
            }
            
            for code, name in formats.items():
                table.add_row(code, name, descriptions.get(code, ''))
            
            console.print(table)
        else:
            print("\nFormat Output Tersedia:")
            print("-" * 40)
            for code, name in formats.items():
                print(f"{code:6s} - {name}")
        
        # Input format yang dipilih
        format_choice = input(f"\nPilih format output [md-hybrid]: ").strip().lower()
        
        if not format_choice:
            format_choice = 'md-hybrid'
        
        if format_choice in formats:
            return format_choice
        else:
            console.print(f"[red]Format '{format_choice}' tidak valid![/red]")
            return None
    
    def run_interactive_mode(self):
        """
        Menjalankan mode interaktif
        """
        self.show_banner()
        
        # Periksa requirements
        if not self.check_system_requirements():
            return False
        
        while True:
            try:
                # Dapatkan daftar file PDF
                pdf_files = self.get_pdf_files_menu()
                if not pdf_files:
                    break
                
                # Pilih file
                selected_files = self.select_files(pdf_files)
                if not selected_files:
                    print("Tidak ada file dipilih.")
                    continue
                
                # Pilih format output
                output_format = self.select_output_format()
                if not output_format:
                    continue
                
                # Konfirmasi konversi
                print(f"\nAkan mengkonversi {len(selected_files)} file ke format {output_format.upper()}")
                confirm = input("Lanjutkan? (y/n) [y]: ").strip().lower()
                
                if confirm in ('', 'y', 'yes'):
                    # Jalankan konversi
                    successful = self.converter.batch_convert(selected_files, output_format)
                    
                    print(f"\nKonversi selesai!")
                    print(f"Berhasil: {len(successful)} file")
                    print(f"Gagal: {len(selected_files) - len(successful)} file")
                    print(f"Output tersimpan di: {self.output_dir / output_format}")
                
                # Tanya apakah ingin konversi lagi
                again = input("\nKonversi file lain? (y/n) [n]: ").strip().lower()
                if again not in ('y', 'yes'):
                    break
                    
            except KeyboardInterrupt:
                print("\n\nKeluar...")
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
                continue
        
        console.print("[green]Terima kasih telah menggunakan PDF Converter![/green]")
        return True

def main():
    """
    Fungsi utama
    """
    parser = argparse.ArgumentParser(description='PDF Converter Tool')
    parser.add_argument('--base-dir', type=str, default=None,
                       help='Base directory untuk converter')
    
    args = parser.parse_args()
    
    # Tentukan base directory
    if args.base_dir:
        base_dir = Path(args.base_dir)
    else:
        # Gunakan direktori saat ini
        base_dir = Path(__file__).parent.parent
    
    # Jalankan CLI
    cli = PDFConverterCLI(base_dir)
    cli.run_interactive_mode()

if __name__ == "__main__":
    main()
