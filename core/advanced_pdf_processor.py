"""
Advanced PDF Processing Engine
==============================

Engine canggih untuk processing PDF dengan berbagai mode konversi
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
import subprocess

# Import libraries dengan fallback
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    from PIL import Image
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import pytesseract
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
    from rich.progress import Progress, SpinnerColumn, TextColumn
    console = Console()
except ImportError:
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    console = Console()

class AdvancedPDFProcessor:
    """
    Processor canggih untuk PDF dengan berbagai mode konversi
    """
    
    def __init__(self, output_dir: Path, temp_dir: Path):
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)
        self.available_methods = self._check_available_methods()
    
    def _check_available_methods(self) -> Dict[str, bool]:
        """Check which processing methods are available"""
        return {
            'pymupdf': PYMUPDF_AVAILABLE,
            'pdf2image': PDF2IMAGE_AVAILABLE,
            'ocr': OCR_AVAILABLE,
            'pypdf2': PYPDF2_AVAILABLE
        }
    
    def analyze_pdf_content(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Analyze PDF untuk menentukan strategy konversi terbaik
        """
        analysis = {
            'total_pages': 0,
            'text_pages': 0,
            'image_pages': 0,
            'mixed_pages': 0,
            'embedded_images': 0,
            'text_ratio': 0.0,
            'recommended_mode': 'hybrid'
        }
        
        if not PYMUPDF_AVAILABLE:
            console.print("[yellow]Warning: PyMuPDF not available, limited analysis[/yellow]")
            return analysis
        
        try:
            doc = fitz.open(str(pdf_path))
            analysis['total_pages'] = len(doc)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Check text content
                page_text = page.get_text().strip()
                text_length = len(page_text)
                
                # Check embedded images
                image_list = page.get_images(full=True)
                image_count = len(image_list)
                
                analysis['embedded_images'] += image_count
                
                # Categorize page type
                if text_length > 100 and image_count > 0:
                    analysis['mixed_pages'] += 1
                elif text_length > 100:
                    analysis['text_pages'] += 1
                else:
                    analysis['image_pages'] += 1
            
            doc.close()
            
            # Calculate text ratio
            if analysis['total_pages'] > 0:
                analysis['text_ratio'] = (analysis['text_pages'] + analysis['mixed_pages']) / analysis['total_pages']
            
            # Recommend mode based on analysis
            if analysis['text_ratio'] > 0.7:
                analysis['recommended_mode'] = 'hybrid'
            elif analysis['text_ratio'] < 0.3:
                analysis['recommended_mode'] = 'ocr'
            else:
                analysis['recommended_mode'] = 'hybrid'
                
        except Exception as e:
            console.print(f"[red]Error analyzing PDF: {e}[/red]")
        
        return analysis
    
    def process_hybrid_mode(self, pdf_path: Path, output_md_path: Path) -> Tuple[bool, str]:
        """
        Mode 1: Hybrid - Text tetap text, gambar tetap gambar (preserve original format)
        """
        try:
            console.print("[blue]🔄 HYBRID MODE: Preserving original format (text + images)[/blue]")
            
            # Fallback to pdf2image + OCR if PyMuPDF not available
            if not PYMUPDF_AVAILABLE:
                console.print("[yellow]PyMuPDF not available, using pdf2image + OCR fallback[/yellow]")
                return self._hybrid_fallback_mode(pdf_path, output_md_path)
            
            doc = fitz.open(str(pdf_path))
            
            # Create images directory
            images_dir = output_md_path.parent / f"{output_md_path.stem}_images"
            images_dir.mkdir(exist_ok=True)
            
            markdown_content = self._generate_header(pdf_path, "Hybrid Mode - Original Format Preserved")
            
            total_images = 0
            total_text_chars = 0
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Processing pages...", total=len(doc))
                
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    progress.update(task, description=f"Processing page {page_num + 1}/{len(doc)}")
                    
                    markdown_content += f"\n## Page {page_num + 1}\n\n"
                    
                    # Extract text first
                    page_text = page.get_text()
                    
                    if page_text.strip():
                        # Clean and format text
                        cleaned_text = self._clean_extracted_text(page_text)
                        markdown_content += cleaned_text + "\n\n"
                        total_text_chars += len(cleaned_text)
                    
                    # Extract embedded images
                    image_list = page.get_images(full=True)
                    
                    for img_index, img in enumerate(image_list):
                        try:
                            xref = img[0]
                            pix = fitz.Pixmap(doc, xref)
                            
                            if pix.n - pix.alpha < 4:  # Valid image
                                img_filename = f"page_{page_num + 1}_img_{img_index + 1}.png"
                                img_path = images_dir / img_filename
                                
                                pix.save(str(img_path))
                                
                                # Add image reference to markdown
                                relative_img_path = f"{images_dir.name}/{img_filename}"
                                markdown_content += f"![Image {total_images + 1}]({relative_img_path})\n\n"
                                
                                total_images += 1
                            
                            pix = None
                            
                        except Exception as e:
                            console.print(f"[yellow]Warning: Could not extract image {img_index + 1} from page {page_num + 1}: {e}[/yellow]")
                    
                    # If page has little text and no images, convert page to image
                    if len(page_text.strip()) < 50 and not image_list:
                        console.print(f"[yellow]Converting page {page_num + 1} to image (low text content)[/yellow]")
                        
                        if PDF2IMAGE_AVAILABLE:
                            try:
                                page_images = convert_from_path(
                                    str(pdf_path),
                                    dpi=200,
                                    first_page=page_num + 1,
                                    last_page=page_num + 1
                                )
                                
                                if page_images:
                                    img_filename = f"page_{page_num + 1}_full.png"
                                    img_path = images_dir / img_filename
                                    page_images[0].save(str(img_path), "PNG", optimize=True)
                                    
                                    relative_img_path = f"{images_dir.name}/{img_filename}"
                                    markdown_content += f"![Page {page_num + 1}]({relative_img_path})\n\n"
                                    total_images += 1
                                    
                            except Exception as e:
                                console.print(f"[yellow]Could not convert page {page_num + 1} to image: {e}[/yellow]")
                    
                    markdown_content += "---\n\n"
                    progress.advance(task)
            
            doc.close()
            
            # Add summary at the end
            markdown_content += self._generate_summary(total_text_chars, total_images, "hybrid")
            
            # Save markdown file
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            message = f"Hybrid conversion completed: {total_text_chars} chars text, {total_images} images"
            return True, message
            
        except Exception as e:
            return False, f"Hybrid mode failed: {str(e)}"
    
    def _hybrid_fallback_mode(self, pdf_path: Path, output_md_path: Path) -> Tuple[bool, str]:
        """
        Fallback hybrid mode using pdf2image + simple text extraction
        """
        try:
            if not PDF2IMAGE_AVAILABLE:
                return False, "pdf2image not available for fallback mode"
            
            # Create images directory
            images_dir = output_md_path.parent / f"{output_md_path.stem}_images"
            images_dir.mkdir(exist_ok=True)
            
            markdown_content = self._generate_header(pdf_path, "Hybrid Mode - Fallback Method")
            
            # Try to extract text using PyPDF2 first
            total_text_chars = 0
            page_texts = {}
            
            if PYPDF2_AVAILABLE:
                try:
                    reader = PdfReader(str(pdf_path))
                    for page_num, page in enumerate(reader.pages):
                        page_text = page.extract_text()
                        if page_text.strip():
                            page_texts[page_num] = self._clean_extracted_text(page_text)
                            total_text_chars += len(page_texts[page_num])
                except Exception as e:
                    console.print(f"[yellow]PyPDF2 text extraction failed: {e}[/yellow]")
            
            # Convert pages to images
            console.print("[blue]Converting PDF to images...[/blue]")
            images = convert_from_path(str(pdf_path), dpi=200)
            
            total_images = 0
            
            for page_num, image in enumerate(images):
                markdown_content += f"\n## Page {page_num + 1}\n\n"
                
                # Add text if available
                if page_num in page_texts:
                    markdown_content += page_texts[page_num] + "\n\n"
                else:
                    # Convert page to image since no text
                    img_filename = f"page_{page_num + 1}.png"
                    img_path = images_dir / img_filename
                    image.save(str(img_path), "PNG", optimize=True)
                    
                    relative_img_path = f"{images_dir.name}/{img_filename}"
                    markdown_content += f"![Page {page_num + 1}]({relative_img_path})\n\n"
                    total_images += 1
                
                markdown_content += "---\n\n"
            
            # Add summary
            markdown_content += self._generate_summary(total_text_chars, total_images, "hybrid-fallback")
            
            # Save markdown file
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            message = f"Hybrid fallback completed: {total_text_chars} chars text, {total_images} images"
            return True, message
            
        except Exception as e:
            return False, f"Hybrid fallback failed: {str(e)}"
    
    def process_ocr_mode(self, pdf_path: Path, output_md_path: Path) -> Tuple[bool, str]:
        """
        Mode 2: OCR - Convert everything to text using OCR
        """
        try:
            console.print("[blue]🔍 OCR MODE: Converting all content to text[/blue]")
            
            if not OCR_AVAILABLE or not PDF2IMAGE_AVAILABLE:
                return False, "OCR dependencies not available (need pytesseract and pdf2image)"
            
            # Check tesseract installation
            try:
                subprocess.run(['tesseract', '--version'], 
                             capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False, "Tesseract OCR not installed. Download from: https://github.com/UB-Mannheim/tesseract/wiki"
            
            markdown_content = self._generate_header(pdf_path, "OCR Mode - All Content as Text")
            
            # Convert PDF to images
            console.print("[yellow]Converting PDF to images for OCR...[/yellow]")
            images = convert_from_path(str(pdf_path), dpi=300)  # Higher DPI for better OCR
            
            total_text_chars = 0
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Performing OCR...", total=len(images))
                
                for page_num, image in enumerate(images):
                    progress.update(task, description=f"OCR on page {page_num + 1}/{len(images)}")
                    
                    markdown_content += f"\n## Page {page_num + 1}\n\n"
                    
                    try:
                        # First try to extract text using PyMuPDF if available
                        extracted_text = ""
                        
                        if PYMUPDF_AVAILABLE:
                            try:
                                doc = fitz.open(str(pdf_path))
                                page = doc.load_page(page_num)
                                pymupdf_text = page.get_text().strip()
                                doc.close()
                                
                                if len(pymupdf_text) > 100:  # If sufficient text found
                                    extracted_text = self._clean_extracted_text(pymupdf_text)
                                    console.print(f"[green]Page {page_num + 1}: Using extracted text[/green]")
                            except:
                                pass
                        
                        # If no sufficient text extracted, use OCR
                        if not extracted_text:
                            console.print(f"[yellow]Page {page_num + 1}: Performing OCR...[/yellow]")
                            
                            # Perform OCR with multiple languages and optimized settings
                            ocr_text = pytesseract.image_to_string(
                                image, 
                                lang='eng',
                                config='--oem 3 --psm 6'  # Optimized OCR settings
                            )
                            
                            extracted_text = self._clean_extracted_text(ocr_text)
                        
                        if extracted_text.strip():
                            markdown_content += extracted_text + "\n\n"
                            total_text_chars += len(extracted_text)
                        else:
                            markdown_content += "*[No readable text found on this page]*\n\n"
                        
                    except Exception as e:
                        console.print(f"[red]Error processing page {page_num + 1}: {e}[/red]")
                        markdown_content += f"*[Error processing page {page_num + 1}: {e}]*\n\n"
                    
                    markdown_content += "---\n\n"
                    progress.advance(task)
            
            # Add summary
            markdown_content += self._generate_summary(total_text_chars, 0, "ocr")
            
            # Save markdown file
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            message = f"OCR conversion completed: {total_text_chars} characters extracted"
            return True, message
            
        except Exception as e:
            return False, f"OCR mode failed: {str(e)}"
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean and format extracted text"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                cleaned_lines.append(line)
        
        # Join lines with proper spacing
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove excessive whitespace
        import re
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)
        
        return cleaned_text
    
    def _generate_header(self, pdf_path: Path, mode_description: str) -> str:
        """Generate markdown header"""
        return f"""# {pdf_path.stem}

*Generated by Advanced PDF Converter - {mode_description}*

**Source:** `{pdf_path.name}`  
**Conversion Date:** {self._get_current_date()}  
**Mode:** {mode_description}

---

"""
    
    def _generate_summary(self, text_chars: int, images: int, mode: str) -> str:
        """Generate conversion summary"""
        return f"""
---

## Conversion Summary

**Mode:** {mode.upper()}  
**Text Characters:** {text_chars:,}  
**Images Extracted:** {images}  
**Generated by:** Advanced PDF Converter Tool  

---
"""
    
    def _get_current_date(self) -> str:
        """Get current date string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def convert_pdf(self, pdf_path: Path, mode: str = "auto") -> Tuple[bool, str, Path]:
        """
        Main conversion method
        
        Args:
            pdf_path: Path to PDF file
            mode: "auto", "hybrid", "ocr"
            
        Returns:
            (success, message, output_path)
        """
        
        # Analyze PDF first
        analysis = self.analyze_pdf_content(pdf_path)
        
        # Determine output path
        if mode == "hybrid":
            output_md_path = self.output_dir / f"{pdf_path.stem}_hybrid.md"
        elif mode == "ocr":
            output_md_path = self.output_dir / f"{pdf_path.stem}_ocr.md"
        else:
            output_md_path = self.output_dir / f"{pdf_path.stem}.md"
        
        console.print(f"[blue]📊 PDF Analysis Results:[/blue]")
        console.print(f"  Total pages: {analysis['total_pages']}")
        console.print(f"  Text pages: {analysis['text_pages']}")
        console.print(f"  Image pages: {analysis['image_pages']}")
        console.print(f"  Mixed pages: {analysis['mixed_pages']}")
        console.print(f"  Text ratio: {analysis['text_ratio']:.1%}")
        console.print(f"  Recommended mode: {analysis['recommended_mode']}")
        console.print()
        
        # Auto-select mode if needed
        if mode == "auto":
            mode = analysis['recommended_mode']
            console.print(f"[green]Auto-selected mode: {mode}[/green]")
        
        # Process based on mode
        if mode == "hybrid":
            success, message = self.process_hybrid_mode(pdf_path, output_md_path)
        elif mode == "ocr":
            success, message = self.process_ocr_mode(pdf_path, output_md_path)
        else:
            return False, f"Unknown mode: {mode}", output_md_path
        
        return success, message, output_md_path
