"""
Image Extraction Alternative
===========================

Alternative image extraction menggunakan pdf2image
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def extract_images_with_pdf2image():
    """Extract images using pdf2image"""
    print("=" * 60)
    print("ALTERNATIVE IMAGE EXTRACTION")
    print("=" * 60)
    print()
    
    try:
        from pdf2image import convert_from_path
        print("✅ pdf2image available")
        
        # Find market structure PDF
        pdf_files = list(current_dir.parent.glob("*.pdf"))
        target_pdf = None
        
        for pdf_file in pdf_files:
            if "Market structure" in pdf_file.name:
                target_pdf = pdf_file
                break
        
        # Try ctc folder
        if not target_pdf:
            ctc_folder = current_dir.parent / "ctc"
            if ctc_folder.exists():
                ctc_files = list(ctc_folder.glob("*Market*structure*.pdf"))
                if ctc_files:
                    target_pdf = ctc_files[0]
        
        if target_pdf:
            print(f"✅ Found PDF: {target_pdf.name}")
            
            # Create output directory
            output_dir = current_dir / "output" / "md"
            images_dir = output_dir / f"{target_pdf.stem}_images"
            images_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"📁 Images will be saved to: {images_dir}")
            
            # Convert first 5 pages as test
            print(f"🔄 Converting first 5 pages to images...")
            
            images = convert_from_path(
                str(target_pdf),
                dpi=200,
                first_page=1,
                last_page=5
            )
            
            total_images = 0
            
            for page_num, image in enumerate(images):
                img_filename = f"page_{page_num + 1}.png"
                img_path = images_dir / img_filename
                
                # Save image
                image.save(str(img_path), "PNG", optimize=True)
                total_images += 1
                
                print(f"✅ Saved: {img_filename} ({image.size[0]}x{image.size[1]})")
            
            print(f"\n✅ SUCCESS: Created {total_images} images")
            print(f"📁 Check folder: {images_dir}")
            
            # Create sample markdown
            md_path = output_dir / f"{target_pdf.stem}_with_images.md"
            markdown_content = f"""# {target_pdf.stem}

*Generated with Image Extraction*

---

"""
            
            for i in range(total_images):
                page_num = i + 1
                img_filename = f"page_{page_num}.png"
                relative_path = f"{images_dir.name}/{img_filename}"
                
                markdown_content += f"""## Page {page_num}

![Page {page_num}]({relative_path})

---

"""
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ Sample markdown created: {md_path}")
            
        else:
            print("❌ Market structure PDF not found")
    
    except ImportError:
        print("❌ pdf2image not available")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    extract_images_with_pdf2image()
