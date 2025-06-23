"""
PDF Text Extractor
==================

Module untuk ekstraksi teks dari PDF menggunakan berbagai metode
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple, List
import subprocess

# Import libraries dengan fallback
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from rich.console import Console
    console = Console()
except ImportError:
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    console = Console()

class PDFTextExtractor:
    """
    Kelas untuk ekstraksi teks dari PDF menggunakan berbagai metode
    """
    
    def __init__(self):
        self.available_methods = self._check_available_methods()
    
    def _check_available_methods(self) -> List[str]:
        """Check which extraction methods are available"""
        methods = []
        
        if PYMUPDF_AVAILABLE:
            methods.append("pymupdf")
        if PYPDF2_AVAILABLE:
            methods.append("pypdf2")
        if OCR_AVAILABLE:
            methods.append("ocr")
        
        return methods
    
    def extract_text_pymupdf(self, pdf_path: Path) -> Tuple[bool, str, str]:
        """
        Extract text using PyMuPDF (fitz) - Best for text-based PDFs
        """
        try:
            doc = fitz.open(str(pdf_path))
            text_content = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += f"\n\n# Page {page_num + 1}\n\n"
                text_content += page.get_text()
            
            doc.close()
            
            if text_content.strip():
                return True, text_content, "Text extracted successfully using PyMuPDF"
            else:
                return False, "", "No text found in PDF (might be image-based)"
                
        except Exception as e:
            return False, "", f"PyMuPDF extraction failed: {str(e)}"
    
    def extract_text_pypdf2(self, pdf_path: Path) -> Tuple[bool, str, str]:
        """
        Extract text using PyPDF2 - Fallback method
        """
        try:
            reader = PdfReader(str(pdf_path))
            text_content = ""
            
            for page_num, page in enumerate(reader.pages):
                text_content += f"\n\n# Page {page_num + 1}\n\n"
                text_content += page.extract_text()
            
            if text_content.strip():
                return True, text_content, "Text extracted successfully using PyPDF2"
            else:
                return False, "", "No text found in PDF (might be image-based)"
                
        except Exception as e:
            return False, "", f"PyPDF2 extraction failed: {str(e)}"
    
    def extract_text_ocr(self, pdf_path: Path) -> Tuple[bool, str, str]:
        """
        Extract text using OCR - For image-based PDFs
        """
        if not OCR_AVAILABLE:
            return False, "", "OCR not available (install pytesseract and pdf2image)"
        
        try:
            # Check if tesseract is installed
            subprocess.run(['tesseract', '--version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False, "", "Tesseract OCR not installed. Download from: https://github.com/UB-Mannheim/tesseract/wiki"
        
        try:
            console.print("[yellow]Converting PDF to images for OCR...[/yellow]")
            
            # Convert PDF to images
            images = convert_from_path(str(pdf_path), dpi=300)
            text_content = ""
            
            console.print(f"[yellow]Processing {len(images)} pages with OCR...[/yellow]")
            
            for page_num, image in enumerate(images):
                text_content += f"\n\n# Page {page_num + 1}\n\n"
                
                # Perform OCR
                page_text = pytesseract.image_to_string(image, lang='eng')
                text_content += page_text
                
                console.print(f"[green]Processed page {page_num + 1}/{len(images)}[/green]")
            
            if text_content.strip():
                return True, text_content, f"Text extracted successfully using OCR ({len(images)} pages)"
            else:
                return False, "", "No text found even with OCR"
                
        except Exception as e:
            return False, "", f"OCR extraction failed: {str(e)}"
    
    def extract_text(self, pdf_path: Path, method: str = "auto") -> Tuple[bool, str, str]:
        """
        Extract text from PDF using specified or automatic method selection
        
        Args:
            pdf_path: Path to PDF file
            method: "auto", "pymupdf", "pypdf2", or "ocr"
            
        Returns:
            (success, text_content, message)
        """
        
        if method == "auto":
            # Try methods in order of preference
            for auto_method in ["pymupdf", "pypdf2", "ocr"]:
                if auto_method in self.available_methods:
                    console.print(f"[blue]Trying {auto_method} extraction...[/blue]")
                    
                    if auto_method == "pymupdf":
                        success, text, msg = self.extract_text_pymupdf(pdf_path)
                    elif auto_method == "pypdf2":
                        success, text, msg = self.extract_text_pypdf2(pdf_path)
                    elif auto_method == "ocr":
                        success, text, msg = self.extract_text_ocr(pdf_path)
                    
                    if success:
                        console.print(f"[green]✓ {msg}[/green]")
                        return True, text, msg
                    else:
                        console.print(f"[yellow]⚠ {msg}[/yellow]")
            
            return False, "", "All extraction methods failed"
        
        else:
            # Use specific method
            if method not in self.available_methods:
                return False, "", f"Method '{method}' not available"
            
            if method == "pymupdf":
                return self.extract_text_pymupdf(pdf_path)
            elif method == "pypdf2":
                return self.extract_text_pypdf2(pdf_path)
            elif method == "ocr":
                return self.extract_text_ocr(pdf_path)
            else:
                return False, "", f"Unknown method: {method}"
    
    def save_text_as_markdown(self, text_content: str, output_path: Path) -> bool:
        """
        Save extracted text as markdown file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # Add basic markdown formatting
                f.write(f"# Extracted from PDF\n\n")
                f.write(f"*Generated by PDF Converter Tool*\n\n")
                f.write("---\n\n")
                f.write(text_content)
            
            return True
        except Exception as e:
            console.print(f"[red]Error saving markdown: {e}[/red]")
            return False
    
    def get_status_info(self) -> dict:
        """Get status information about available methods"""
        return {
            'available_methods': self.available_methods,
            'pymupdf_available': PYMUPDF_AVAILABLE,
            'pypdf2_available': PYPDF2_AVAILABLE,
            'ocr_available': OCR_AVAILABLE,
            'recommended_method': self.available_methods[0] if self.available_methods else None
        }
