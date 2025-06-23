"""
Fast PDF Processor - Optimized Version
=====================================

Versi optimized untuk processing cepat dan tidak stuck
"""

import os
import tempfile
import time
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
    console = Console()
except ImportError:
    class Console:
        def print(self, *args, **kwargs):
            print(*args)
    console = Console()

class FastPDFProcessor:
    """
    Fast and reliable PDF processor with timeout protection
    """
    
    def __init__(self, output_dir: Path, temp_dir: Path):
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)
        self.max_pages_for_image_conversion = 50  # Limit for performance
        self.max_processing_time = 300  # 5 minutes max
    
    def analyze_pdf_simple(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Quick PDF analysis without deep processing
        """
        analysis = {
            'total_pages': 0,
            'file_size_mb': 0.0,
            'recommended_mode': 'hybrid'
        }
        
        try:
            analysis['file_size_mb'] = pdf_path.stat().st_size / (1024 * 1024)
            
            if PYMUPDF_AVAILABLE:
                doc = fitz.open(str(pdf_path))
                analysis['total_pages'] = len(doc)
                doc.close()
            elif PYPDF2_AVAILABLE:
                reader = PdfReader(str(pdf_path))
                analysis['total_pages'] = len(reader.pages)
            
            # Simple recommendation based on file size
            if analysis['file_size_mb'] > 50:
                analysis['recommended_mode'] = 'ocr'  # Large files better with OCR
            elif analysis['total_pages'] > 100:
                analysis['recommended_mode'] = 'ocr'  # Many pages better with OCR
            else:
                analysis['recommended_mode'] = 'hybrid'
                
        except Exception as e:
            console.print(f"[yellow]Analysis warning: {e}[/yellow]")
        
        return analysis
    
    def convert_hybrid_fast(self, pdf_path: Path, output_md_path: Path) -> Tuple[bool, str]:
        """
        Fast hybrid conversion with guaranteed image extraction
        """
        start_time = time.time()
        
        try:
            console.print("[blue]🔄 FAST HYBRID MODE: Text + Images GUARANTEED[/blue]")
            
            # Quick analysis
            analysis = self.analyze_pdf_simple(pdf_path)
            console.print(f"[cyan]📊 {analysis['total_pages']} pages, {analysis['file_size_mb']:.1f}MB[/cyan]")
            
            # For large files, use smarter approach
            if analysis['file_size_mb'] > 20 or analysis['total_pages'] > 50:
                console.print("[yellow]⚡ Large file - using smart hybrid approach[/yellow]")
                return self._smart_hybrid_with_images(pdf_path, output_md_path, start_time)
            
            # For smaller files, use guaranteed image extraction
            else:
                console.print("[green]📄 Normal size - using guaranteed image extraction[/green]")
                return self._guaranteed_image_hybrid(pdf_path, output_md_path, start_time)
                
        except Exception as e:
            return False, f"Fast hybrid conversion failed: {str(e)}"
    
    def _guaranteed_image_hybrid(self, pdf_path: Path, output_md_path: Path, start_time: float) -> Tuple[bool, str]:
        """
        Guaranteed image extraction for normal-sized PDFs
        """
        try:
            if not PDF2IMAGE_AVAILABLE:
                return False, "pdf2image not available for image extraction"
            
            # Create images directory
            images_dir = output_md_path.parent / f"{output_md_path.stem}_images"
            images_dir.mkdir(exist_ok=True)
            
            # Step 1: Extract text using PyPDF2
            page_texts = {}
            total_text_chars = 0
            total_pages = 0
            
            if PYPDF2_AVAILABLE:
                try:
                    reader = PdfReader(str(pdf_path))
                    total_pages = len(reader.pages)
                    
                    for page_num, page in enumerate(reader.pages):
                        if time.time() - start_time > self.max_processing_time:
                            break
                        
                        try:
                            page_text = page.extract_text()
                            if page_text.strip():
                                page_texts[page_num] = self._clean_text_fast(page_text)
                                total_text_chars += len(page_texts[page_num])
                        except:
                            pass
                except:
                    pass
            
            # Step 2: Convert pages to images
            console.print("[cyan]🖼️  Converting pages to images...[/cyan]")
            
            total_images = 0
            
            try:
                # Convert all pages to images
                images = convert_from_path(str(pdf_path), dpi=150)
                total_pages = len(images)  # Update page count
                
                for page_num, image in enumerate(images):
                    if time.time() - start_time > self.max_processing_time:
                        console.print("[red]⏰ Timeout reached during image conversion[/red]")
                        break
                    
                    img_filename = f"page_{page_num + 1}.png"
                    img_path = images_dir / img_filename
                    image.save(str(img_path), "PNG", optimize=True)
                    total_images += 1
                    
                    if page_num % 10 == 0:
                        console.print(f"[green]Converted page {page_num + 1}/{total_pages}[/green]")
            
            except Exception as e:
                console.print(f"[red]Image conversion failed: {e}[/red]")
                return False, f"Image conversion failed: {e}"
            
            # Step 3: Generate markdown
            markdown_content = self._generate_header(pdf_path, "Fast Hybrid Mode - Guaranteed Images")
            
            for page_num in range(total_pages):
                markdown_content += f"\n## Page {page_num + 1}\n\n"
                
                # Add text if available and substantial
                if page_num in page_texts and len(page_texts[page_num]) > 50:
                    markdown_content += page_texts[page_num] + "\n\n"
                
                # ALWAYS add image (guaranteed to exist)
                img_filename = f"page_{page_num + 1}.png"
                relative_img_path = f"{images_dir.name}/{img_filename}"
                markdown_content += f"![Page {page_num + 1}]({relative_img_path})\n\n"
                
                markdown_content += "---\n\n"
            
            # Add summary
            markdown_content += self._generate_summary(total_text_chars, total_images, "guaranteed-hybrid")
            
            # Save result
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            elapsed = time.time() - start_time
            message = f"Guaranteed hybrid completed in {elapsed:.1f}s: {total_text_chars} chars, {total_images} images"
            return True, message
            
        except Exception as e:
            return False, f"Guaranteed hybrid failed: {str(e)}"
    
    def _smart_hybrid_with_images(self, pdf_path: Path, output_md_path: Path, start_time: float) -> Tuple[bool, str]:
        """
        Smart hybrid approach for large files
        """
        try:
            # Create images directory
            images_dir = output_md_path.parent / f"{output_md_path.stem}_images"
            images_dir.mkdir(exist_ok=True)
            
            # Step 1: Extract text using PyPDF2
            page_texts = {}
            total_text_chars = 0
            total_pages = 0
            
            if PYPDF2_AVAILABLE:
                try:
                    reader = PdfReader(str(pdf_path))
                    total_pages = len(reader.pages)
                    
                    console.print(f"[cyan]📄 Extracting text from {total_pages} pages...[/cyan]")
                    
                    for page_num, page in enumerate(reader.pages):
                        try:
                            page_text = page.extract_text()
                            if page_text.strip():
                                page_texts[page_num] = self._clean_text_fast(page_text)
                                total_text_chars += len(page_texts[page_num])
                        except:
                            pass
                except:
                    pass
            
            # Step 2: Smart image conversion (sample key pages)
            console.print("[cyan]🖼️  Smart image extraction (sampling key pages)...[/cyan]")
            
            # Sample pages intelligently
            sample_pages = []
            
            # First few pages
            sample_pages.extend(range(1, min(6, total_pages + 1)))
            
            # Pages with little text
            for page_num in range(total_pages):
                if page_num not in page_texts or len(page_texts[page_num]) < 100:
                    sample_pages.append(page_num + 1)
                    if len(sample_pages) >= 20:  # Limit to 20 image pages for performance
                        break
            
            # Last few pages
            if total_pages > 5:
                sample_pages.extend(range(max(1, total_pages - 2), total_pages + 1))
            
            # Remove duplicates and sort
            sample_pages = sorted(list(set(sample_pages)))
            
            console.print(f"[yellow]Converting {len(sample_pages)} key pages to images...[/yellow]")
            
            total_images = 0
            
            for page_num in sample_pages:
                if time.time() - start_time > self.max_processing_time:
                    break
                
                try:
                    page_images = convert_from_path(
                        str(pdf_path),
                        dpi=150,
                        first_page=page_num,
                        last_page=page_num
                    )
                    
                    if page_images:
                        img_filename = f"page_{page_num}.png"
                        img_path = images_dir / img_filename
                        page_images[0].save(str(img_path), "PNG", optimize=True)
                        total_images += 1
                        
                        if total_images % 5 == 0:
                            console.print(f"[green]Converted {total_images} images...[/green]")
                
                except Exception as e:
                    console.print(f"[yellow]Failed to convert page {page_num}: {e}[/yellow]")
            
            # Step 3: Generate markdown
            markdown_content = self._generate_header(pdf_path, "Fast Hybrid Mode - Smart Sampling")
            
            for page_num in range(total_pages):
                markdown_content += f"\n## Page {page_num + 1}\n\n"
                
                # Add text if available
                if page_num in page_texts:
                    markdown_content += page_texts[page_num] + "\n\n"
                
                # Add image if available
                img_filename = f"page_{page_num + 1}.png"
                img_path = images_dir / img_filename
                
                if img_path.exists():
                    relative_img_path = f"{images_dir.name}/{img_filename}"
                    markdown_content += f"![Page {page_num + 1}]({relative_img_path})\n\n"
                elif page_num not in page_texts:
                    markdown_content += "*[Page appears to be image-based - not sampled]*\n\n"
                
                markdown_content += "---\n\n"
            
            # Add note about sampling
            markdown_content += f"\n*Note: {total_images} key pages converted to images for performance.*\n\n"
            markdown_content += self._generate_summary(total_text_chars, total_images, "smart-hybrid")
            
            # Save result
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            elapsed = time.time() - start_time
            message = f"Smart hybrid completed in {elapsed:.1f}s: {total_text_chars} chars, {total_images} images"
            return True, message
            
        except Exception as e:
            return False, f"Smart hybrid failed: {str(e)}"
    
    def _hybrid_pymupdf_fast(self, pdf_path: Path, output_md_path: Path, start_time: float) -> Tuple[bool, str]:
        """
        Fast PyMuPDF-based hybrid conversion
        """
        try:
            doc = fitz.open(str(pdf_path))
            
            # Create images directory
            images_dir = output_md_path.parent / f"{output_md_path.stem}_images"
            images_dir.mkdir(exist_ok=True)
            
            markdown_content = self._generate_header(pdf_path, "Fast Hybrid Mode")
            
            total_images = 0
            total_text_chars = 0
            
            for page_num in range(len(doc)):
                # Timeout check
                if time.time() - start_time > self.max_processing_time:
                    console.print("[red]⏰ Timeout reached, stopping conversion[/red]")
                    break
                
                if page_num % 10 == 0:
                    console.print(f"[green]Processing page {page_num + 1}/{len(doc)}[/green]")
                
                page = doc.load_page(page_num)
                markdown_content += f"\n## Page {page_num + 1}\n\n"
                
                # Extract text (fast)
                page_text = page.get_text()
                if page_text.strip():
                    cleaned_text = self._clean_text_fast(page_text)
                    markdown_content += cleaned_text + "\n\n"
                    total_text_chars += len(cleaned_text)
                
                # Quick image extraction (skip if too many images already)
                if total_images < 50:  # Limit images for performance
                    try:
                        image_list = page.get_images(full=True)
                        for img_index, img in enumerate(image_list[:3]):  # Max 3 images per page
                            try:
                                xref = img[0]
                                pix = fitz.Pixmap(doc, xref)
                                
                                if pix.width > 50 and pix.height > 50:  # Skip tiny images
                                    img_filename = f"page_{page_num + 1}_img_{img_index + 1}.png"
                                    img_path = images_dir / img_filename
                                    pix.save(str(img_path))
                                    
                                    relative_img_path = f"{images_dir.name}/{img_filename}"
                                    markdown_content += f"![Image {total_images + 1}]({relative_img_path})\n\n"
                                    total_images += 1
                                
                                pix = None
                            except:
                                pass  # Skip problematic images
                    except:
                        pass  # Skip if image extraction fails
                
                markdown_content += "---\n\n"
            
            doc.close()
            
            # Save result
            markdown_content += self._generate_summary(total_text_chars, total_images, "fast-hybrid")
            
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            elapsed = time.time() - start_time
            message = f"Fast hybrid completed in {elapsed:.1f}s: {total_text_chars} chars, {total_images} images"
            return True, message
            
        except Exception as e:
            return False, f"PyMuPDF hybrid failed: {str(e)}"
    
    def _hybrid_pypdf2_fast(self, pdf_path: Path, output_md_path: Path, start_time: float) -> Tuple[bool, str]:
        """
        Fast PyPDF2-based hybrid conversion with image extraction
        """
        try:
            reader = PdfReader(str(pdf_path))
            
            # Create images directory
            images_dir = output_md_path.parent / f"{output_md_path.stem}_images"
            images_dir.mkdir(exist_ok=True)
            
            markdown_content = self._generate_header(pdf_path, "Fast Hybrid Mode - PyPDF2 + Images")
            total_text_chars = 0
            total_images = 0
            
            # Extract text using PyPDF2
            page_texts = {}
            
            try:
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text.strip():
                        page_texts[page_num] = self._clean_text_fast(page_text)
                        total_text_chars += len(page_texts[page_num])
            except Exception as e:
                console.print(f"[yellow]PyPDF2 text extraction failed: {e}[/yellow]")
            
            # Extract images using pdf2image for pages with little/no text
            if PDF2IMAGE_AVAILABLE:
                console.print("[blue]Converting pages with little text to images...[/blue]")
                
                # Identify pages that need image conversion
                pages_needing_images = []
                for page_num in range(len(reader.pages)):
                    if page_num not in page_texts or len(page_texts[page_num]) < 100:
                        pages_needing_images.append(page_num + 1)  # pdf2image uses 1-based
                
                if pages_needing_images:
                    # Convert only the pages that need images (more efficient)
                    try:
                        # For efficiency, limit to first 20 image pages
                        limited_pages = pages_needing_images[:20]
                        
                        for page_num in limited_pages:
                            # Timeout check
                            if time.time() - start_time > self.max_processing_time:
                                console.print("[red]⏰ Timeout reached during image conversion[/red]")
                                break
                            
                            try:
                                page_images = convert_from_path(
                                    str(pdf_path),
                                    dpi=150,  # Reasonable quality vs speed
                                    first_page=page_num,
                                    last_page=page_num
                                )
                                
                                if page_images:
                                    img_filename = f"page_{page_num}.png"
                                    img_path = images_dir / img_filename
                                    page_images[0].save(str(img_path), "PNG", optimize=True)
                                    total_images += 1
                                    
                                    console.print(f"[green]Created image for page {page_num}[/green]")
                                    
                            except Exception as e:
                                console.print(f"[yellow]Could not convert page {page_num} to image: {e}[/yellow]")
                    
                    except Exception as e:
                        console.print(f"[yellow]Image conversion failed: {e}[/yellow]")
            
            # Generate markdown content
            for page_num in range(len(reader.pages)):
                # Timeout check
                if time.time() - start_time > self.max_processing_time:
                    console.print("[red]⏰ Timeout reached, stopping conversion[/red]")
                    break
                
                if page_num % 20 == 0:
                    console.print(f"[green]Processing page {page_num + 1}/{len(reader.pages)}[/green]")
                
                markdown_content += f"\n## Page {page_num + 1}\n\n"
                
                # Add text if available
                if page_num in page_texts and len(page_texts[page_num]) > 50:
                    markdown_content += page_texts[page_num] + "\n\n"
                else:
                    # Check if we have an image for this page
                    img_filename = f"page_{page_num + 1}.png"
                    img_path = images_dir / img_filename
                    
                    if img_path.exists():
                        relative_img_path = f"{images_dir.name}/{img_filename}"
                        markdown_content += f"![Page {page_num + 1}]({relative_img_path})\n\n"
                    else:
                        markdown_content += "*[Page appears to be image-based - image conversion skipped]*\n\n"
                
                markdown_content += "---\n\n"
            
            # Save result
            markdown_content += self._generate_summary(total_text_chars, total_images, "fast-hybrid-with-images")
            
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            elapsed = time.time() - start_time
            message = f"Fast hybrid with images completed in {elapsed:.1f}s: {total_text_chars} chars, {total_images} images"
            return True, message
            
        except Exception as e:
            return False, f"PyPDF2 hybrid with images failed: {str(e)}"
    
    def convert_ocr_fast(self, pdf_path: Path, output_md_path: Path) -> Tuple[bool, str]:
        """
        Fast OCR conversion with smart sampling
        """
        start_time = time.time()
        
        try:
            console.print("[blue]🔍 FAST OCR MODE: Smart text extraction[/blue]")
            
            if not PDF2IMAGE_AVAILABLE:
                return False, "pdf2image not available for OCR mode"
            
            analysis = self.analyze_pdf_simple(pdf_path)
            
            # Smart page sampling for large PDFs
            if analysis['total_pages'] > 20:
                console.print(f"[yellow]⚡ Large PDF detected, using smart sampling[/yellow]")
                return self._ocr_smart_sampling(pdf_path, output_md_path, start_time)
            else:
                return self._ocr_all_pages(pdf_path, output_md_path, start_time)
                
        except Exception as e:
            return False, f"Fast OCR conversion failed: {str(e)}"
    
    def _ocr_smart_sampling(self, pdf_path: Path, output_md_path: Path, start_time: float) -> Tuple[bool, str]:
        """
        OCR with smart page sampling for large files
        """
        try:
            markdown_content = self._generate_header(pdf_path, "Fast OCR Mode - Smart Sampling")
            
            # Sample pages intelligently (first 5, middle 5, last 5)
            analysis = self.analyze_pdf_simple(pdf_path)
            total_pages = analysis['total_pages']
            
            sample_pages = []
            # First pages
            sample_pages.extend(range(1, min(6, total_pages + 1)))
            
            # Middle pages
            if total_pages > 10:
                middle_start = total_pages // 2 - 2
                middle_end = middle_start + 5
                sample_pages.extend(range(max(1, middle_start), min(total_pages + 1, middle_end)))
            
            # Last pages
            if total_pages > 5:
                sample_pages.extend(range(max(1, total_pages - 4), total_pages + 1))
            
            # Remove duplicates and sort
            sample_pages = sorted(list(set(sample_pages)))
            
            console.print(f"[cyan]📋 Sampling {len(sample_pages)} pages from {total_pages} total[/cyan]")
            
            total_text_chars = 0
            
            for page_num in sample_pages:
                # Timeout check
                if time.time() - start_time > self.max_processing_time:
                    break
                
                console.print(f"[green]OCR page {page_num}/{total_pages}[/green]")
                
                try:
                    # Convert single page
                    page_images = convert_from_path(
                        str(pdf_path),
                        dpi=150,  # Lower DPI for speed
                        first_page=page_num,
                        last_page=page_num
                    )
                    
                    if page_images and OCR_AVAILABLE:
                        # Try OCR
                        try:
                            page_text = pytesseract.image_to_string(
                                page_images[0],
                                config='--oem 3 --psm 6'
                            )
                            
                            if page_text.strip():
                                markdown_content += f"\n## Page {page_num}\n\n"
                                cleaned_text = self._clean_text_fast(page_text)
                                markdown_content += cleaned_text + "\n\n"
                                total_text_chars += len(cleaned_text)
                                markdown_content += "---\n\n"
                        except:
                            console.print(f"[yellow]OCR failed for page {page_num}[/yellow]")
                    
                except Exception as e:
                    console.print(f"[yellow]Error processing page {page_num}: {e}[/yellow]")
            
            # Add note about sampling
            markdown_content += f"\n*Note: This is a smart sample of {len(sample_pages)} pages from {total_pages} total pages.*\n\n"
            markdown_content += self._generate_summary(total_text_chars, 0, "fast-ocr-sampling")
            
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            elapsed = time.time() - start_time
            message = f"Fast OCR sampling completed in {elapsed:.1f}s: {total_text_chars} characters from {len(sample_pages)} pages"
            return True, message
            
        except Exception as e:
            return False, f"OCR sampling failed: {str(e)}"
    
    def _ocr_all_pages(self, pdf_path: Path, output_md_path: Path, start_time: float) -> Tuple[bool, str]:
        """
        OCR all pages for smaller files
        """
        try:
            markdown_content = self._generate_header(pdf_path, "Fast OCR Mode - All Pages")
            
            # Convert all pages at once (faster than one by one)
            console.print("[yellow]Converting PDF to images...[/yellow]")
            images = convert_from_path(str(pdf_path), dpi=200)
            
            total_text_chars = 0
            
            for page_num, image in enumerate(images):
                # Timeout check
                if time.time() - start_time > self.max_processing_time:
                    break
                
                console.print(f"[green]OCR page {page_num + 1}/{len(images)}[/green]")
                
                try:
                    if OCR_AVAILABLE:
                        page_text = pytesseract.image_to_string(
                            image,
                            config='--oem 3 --psm 6'
                        )
                        
                        markdown_content += f"\n## Page {page_num + 1}\n\n"
                        
                        if page_text.strip():
                            cleaned_text = self._clean_text_fast(page_text)
                            markdown_content += cleaned_text + "\n\n"
                            total_text_chars += len(cleaned_text)
                        else:
                            markdown_content += "*[No readable text found on this page]*\n\n"
                        
                        markdown_content += "---\n\n"
                    
                except Exception as e:
                    console.print(f"[yellow]OCR error on page {page_num + 1}: {e}[/yellow]")
                    markdown_content += f"*[OCR failed for page {page_num + 1}]*\n\n---\n\n"
            
            markdown_content += self._generate_summary(total_text_chars, 0, "fast-ocr-all")
            
            with open(output_md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            elapsed = time.time() - start_time
            message = f"Fast OCR completed in {elapsed:.1f}s: {total_text_chars} characters from {len(images)} pages"
            return True, message
            
        except Exception as e:
            return False, f"OCR all pages failed: {str(e)}"
    
    def _clean_text_fast(self, text: str) -> str:
        """Fast text cleaning"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _generate_header(self, pdf_path: Path, mode_description: str) -> str:
        """Generate markdown header"""
        return f"""# {pdf_path.stem}

*Generated by Fast PDF Converter - {mode_description}*

**Source:** `{pdf_path.name}`  
**Conversion Time:** {time.strftime("%Y-%m-%d %H:%M:%S")}  

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
**Tool:** Fast PDF Converter  

---
"""
    
    def convert_pdf_fast(self, pdf_path: Path, mode: str = "auto") -> Tuple[bool, str, Path]:
        """
        Main fast conversion method
        """
        # Determine output path
        if mode == "hybrid":
            output_md_path = self.output_dir / f"{pdf_path.stem}_hybrid.md"
        elif mode == "ocr":
            output_md_path = self.output_dir / f"{pdf_path.stem}_ocr.md"
        else:
            output_md_path = self.output_dir / f"{pdf_path.stem}.md"
        
        # Quick analysis for auto mode
        if mode == "auto":
            analysis = self.analyze_pdf_simple(pdf_path)
            mode = analysis['recommended_mode']
            console.print(f"[green]🎯 Auto-selected mode: {mode}[/green]")
        
        # Process based on mode
        if mode == "hybrid":
            success, message = self.convert_hybrid_fast(pdf_path, output_md_path)
        elif mode == "ocr":
            success, message = self.convert_ocr_fast(pdf_path, output_md_path)
        else:
            return False, f"Unknown mode: {mode}", output_md_path
        
        return success, message, output_md_path
