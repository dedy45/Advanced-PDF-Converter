"""
PDF Converter Core Class
========================
"""

import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import tempfile
import os

try:
    import pypandoc
except ImportError:
    pypandoc = None

try:
    from rich.console import Console
    from rich.progress import Progress, track
    console = Console()
except ImportError:
    # Fallback jika rich tidak tersedia
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    console = Console()
    def track(iterable, description="Processing..."):
        return iterable

try:
    from .utils import (
        validate_pdf_file, create_output_directory, clean_temp_directory,
        show_success_message, show_error_message, check_pandoc_installation
    )
    from .pdf_extractor import PDFTextExtractor
except ImportError:
    # Fallback untuk import absolut
    import sys
    import os
    current_file_dir = os.path.dirname(__file__)
    sys.path.insert(0, current_file_dir)
    
    from utils import (
        validate_pdf_file, create_output_directory, clean_temp_directory,
        show_success_message, show_error_message, check_pandoc_installation
    )
    from pdf_extractor import PDFTextExtractor
    from pdf_to_md_with_images import PDFToMarkdownWithImages
    from advanced_pdf_processor import AdvancedPDFProcessor
    from fast_pdf_processor import FastPDFProcessor

class PDFConverter:
    """
    Kelas utama untuk konversi PDF ke berbagai format
    """
    
    def __init__(self, temp_dir: Path, output_dir: Path):
        self.temp_dir = Path(temp_dir)
        self.output_dir = Path(output_dir)
        self.pdf_extractor = PDFTextExtractor()
        self.pdf_to_md_with_images = PDFToMarkdownWithImages(output_dir, temp_dir)
        self.advanced_processor = AdvancedPDFProcessor(output_dir, temp_dir)
        self.fast_processor = FastPDFProcessor(output_dir, temp_dir)  # Fast replacement
        self.supported_formats = {
            'md': 'Markdown (text only)',
            'md-hybrid': 'Markdown Hybrid (text + images preserved)',
            'md-ocr': 'Markdown OCR (everything as text)',
            'html': 'HTML',
            'docx': 'Microsoft Word Document',
            'txt': 'Plain Text',
            'rtf': 'Rich Text Format',
            'odt': 'OpenDocument Text',
            'epub': 'EPUB eBook',
            'latex': 'LaTeX',
            'json': 'JSON'
        }
        
        # Pandoc options untuk setiap format
        self.pandoc_options = {
            'md': [
                '--extract-media=temp/images',
                '--wrap=none',
                '--standalone'
            ],
            'md-hybrid': [],  # Special handling
            'md-ocr': [],     # Special handling
            'html': [
                '--extract-media=temp/images',
                '--standalone',
                '--self-contained'
            ],
            'docx': [
                '--extract-media=temp/images'
            ],
            'txt': [
                '--wrap=none'
            ],
            'rtf': [],
            'odt': [
                '--extract-media=temp/images'
            ],
            'epub': [
                '--extract-media=temp/images'
            ],
            'latex': [
                '--extract-media=temp/images',
                '--standalone'
            ],
            'json': []
        }
    
    def check_dependencies(self) -> bool:
        """
        Memeriksa dependensi yang diperlukan
        """
        if not check_pandoc_installation():
            console.print("[red]Error: Pandoc tidak ditemukan![/red]")
            return False
        
        return True
    
    def convert_pdf(self, input_file: Path, output_format: str, 
                   custom_options: Optional[List[str]] = None) -> Optional[Path]:
        """
        Konversi PDF ke format yang ditentukan
        
        Args:
            input_file: Path ke file PDF input
            output_format: Format output (md, html, docx, dll)
            custom_options: Opsi pandoc tambahan
            
        Returns:
            Path ke file output yang berhasil dibuat, atau None jika gagal
        """
        
        # Validasi input
        is_valid, message = validate_pdf_file(input_file)
        if not is_valid:
            show_error_message(message)
            return None
        
        if output_format not in self.supported_formats:
            show_error_message(f"Format '{output_format}' tidak didukung")
            return None
        
        # Buat direktori output
        format_dir = create_output_directory(self.output_dir, output_format)
        
        # Bersihkan dan buat direktori temp
        clean_temp_directory(self.temp_dir)
        
        # Tentukan nama file output
        output_filename = input_file.stem + f".{output_format}"
        output_file = format_dir / output_filename
        
        try:
            console.print(f"[yellow]Mengkonversi {input_file.name} ke {output_format.upper()}...[/yellow]")
            
            # Special handling for advanced markdown formats
            if output_format in ['md-hybrid', 'md-ocr']:
                format_dir = create_output_directory(self.output_dir, 'md')
                
                console.print(f"[cyan]🚀 Using FAST processor for {output_format}[/cyan]")
                
                if output_format == 'md-hybrid':
                    success, msg, result_path = self.fast_processor.convert_pdf_fast(input_file, "hybrid")
                else:  # md-ocr
                    success, msg, result_path = self.fast_processor.convert_pdf_fast(input_file, "ocr")
                
                if success:
                    # Move result to correct location if needed
                    final_output = format_dir / f"{input_file.stem}.md"
                    if result_path != final_output:
                        if final_output.exists():
                            final_output.unlink()
                        
                        # Move the file
                        result_path.rename(final_output)
                        
                        # Also move images directory if it exists
                        src_images_dir = result_path.parent / f"{result_path.stem}_images"
                        dest_images_dir = final_output.parent / f"{final_output.stem}_images"
                        if src_images_dir.exists() and src_images_dir != dest_images_dir:
                            if dest_images_dir.exists():
                                shutil.rmtree(dest_images_dir)
                            src_images_dir.rename(dest_images_dir)
                    
                    show_success_message(input_file, final_output, f"FAST {output_format.upper()}")
                    return final_output
                else:
                    show_error_message(f"Fast {output_format} conversion failed: {msg}")
                    return None
            
            # Special handling for legacy md-img format
            elif output_format == 'md-img':
                format_dir = create_output_directory(self.output_dir, 'md')
                output_file = format_dir / f"{input_file.stem}.md"
                
                console.print("[blue]Using legacy PDF to Markdown with Images converter...[/blue]")
                success, msg, result_path = self.pdf_to_md_with_images.convert_pdf_to_markdown_with_images(
                    input_file
                )
                
                if success:
                    # Move result to correct location
                    if result_path != output_file:
                        shutil.move(str(result_path), str(output_file))
                        # Also move images directory if it exists
                        src_images_dir = result_path.parent / f"{result_path.stem}_images"
                        dest_images_dir = output_file.parent / f"{output_file.stem}_images"
                        if src_images_dir.exists() and src_images_dir != dest_images_dir:
                            if dest_images_dir.exists():
                                shutil.rmtree(dest_images_dir)
                            shutil.move(str(src_images_dir), str(dest_images_dir))
                    
                    show_success_message(input_file, output_file, "Markdown with Images")
                    return output_file
                else:
                    show_error_message(f"Markdown with images conversion failed: {msg}")
                    return None
            
            # Regular conversion process for other formats
            # Step 1: Extract text from PDF
            console.print("[blue]Step 1: Extracting text from PDF...[/blue]")
            success, text_content, extract_msg = self.pdf_extractor.extract_text(input_file)
            
            if not success:
                show_error_message(f"Failed to extract text from PDF: {extract_msg}")
                return None
            
            console.print(f"[green]✓ {extract_msg}[/green]")
            
            # Step 2: Save as temporary markdown
            temp_md_file = self.temp_dir / f"{input_file.stem}_temp.md"
            if not self.pdf_extractor.save_text_as_markdown(text_content, temp_md_file):
                show_error_message("Failed to save temporary markdown file")
                return None
            
            # Step 3: Use pandoc to convert from markdown to target format
            if output_format == 'md':
                # For markdown, just copy the temp file
                shutil.copy2(temp_md_file, output_file)
            else:
                # Use pandoc to convert from markdown to other formats
                pandoc_args = ['pandoc']
                
                # Add options for format
                if output_format in self.pandoc_options:
                    pandoc_args.extend(self.pandoc_options[output_format])
                
                # Add custom options if provided
                if custom_options:
                    pandoc_args.extend(custom_options)
                
                # Add input and output
                pandoc_args.extend([
                    str(temp_md_file),
                    '-o', str(output_file)
                ])
                
                console.print(f"[blue]Step 2: Converting to {output_format.upper()} using pandoc...[/blue]")
                
                # Run pandoc
                result = subprocess.run(
                    pandoc_args,
                    cwd=self.temp_dir.parent,
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            # Periksa apakah file output berhasil dibuat
            if output_file.exists() and output_file.stat().st_size > 0:
                # Pindahkan gambar jika ada
                self._move_extracted_images(format_dir, output_filename)
                
                show_success_message(input_file, output_file, 
                                   self.supported_formats[output_format])
                return output_file
            else:
                show_error_message("File output tidak berhasil dibuat")
                return None
                
        except subprocess.CalledProcessError as e:
            error_msg = f"Pandoc error: {e.stderr if e.stderr else str(e)}"
            show_error_message(error_msg)
            return None
        except Exception as e:
            show_error_message(f"Konversi gagal: {str(e)}")
            return None
    
    def _move_extracted_images(self, format_dir: Path, output_filename: str):
        """
        Memindahkan gambar yang diekstrak ke direktori output
        """
        temp_images_dir = self.temp_dir / "images"
        if temp_images_dir.exists():
            # Buat direktori gambar di output
            output_images_dir = format_dir / f"{Path(output_filename).stem}_images"
            output_images_dir.mkdir(exist_ok=True)
            
            # Pindahkan semua gambar
            for image_file in temp_images_dir.glob("*"):
                if image_file.is_file():
                    shutil.copy2(image_file, output_images_dir)
    
    def batch_convert(self, input_files: List[Path], output_format: str,
                     custom_options: Optional[List[str]] = None) -> List[Path]:
        """
        Konversi batch multiple PDF files
        
        Args:
            input_files: List file PDF untuk dikonversi
            output_format: Format output
            custom_options: Opsi pandoc tambahan
            
        Returns:
            List path file output yang berhasil dibuat
        """
        successful_conversions = []
        
        for input_file in track(input_files, description=f"Converting to {output_format.upper()}"):
            result = self.convert_pdf(input_file, output_format, custom_options)
            if result:
                successful_conversions.append(result)
        
        return successful_conversions
    
    def get_supported_formats(self) -> Dict[str, str]:
        """
        Mendapatkan daftar format yang didukung
        """
        return self.supported_formats.copy()
    
    def preview_conversion(self, input_file: Path, output_format: str) -> Dict[str, Any]:
        """
        Preview informasi konversi tanpa melakukan konversi
        """
        is_valid, message = validate_pdf_file(input_file)
        
        format_dir = create_output_directory(self.output_dir, output_format)
        output_filename = input_file.stem + f".{output_format}"
        output_file = format_dir / output_filename
        
        return {
            'input_file': input_file,
            'output_file': output_file,
            'format': self.supported_formats.get(output_format, output_format),
            'is_valid': is_valid,
            'validation_message': message,
            'estimated_size': input_file.stat().st_size if input_file.exists() else 0
        }
