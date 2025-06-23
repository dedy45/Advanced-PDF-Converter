"""
Test Market Structure PDF Specifically
=====================================
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_market_structure_specific():
    """Test market structure PDF specifically"""
    print("=" * 60)
    print("MARKET STRUCTURE PDF - SPECIFIC TEST")
    print("=" * 60)
    
    try:
        from converter import PDFConverter
        
        # Initialize
        output_dir = current_dir / "output"
        temp_dir = current_dir / "temp"
        converter = PDFConverter(temp_dir, output_dir)
        
        # Find market structure PDF
        ctc_folder = current_dir.parent / "ctc"
        target_pdf = None
        
        if ctc_folder.exists():
            for pdf_file in ctc_folder.glob("*.pdf"):
                if "Market structure" in pdf_file.name or "powerfull setup" in pdf_file.name:
                    target_pdf = pdf_file
                    break
        
        if not target_pdf:
            # Try parent directory
            for pdf_file in current_dir.parent.glob("*.pdf"):
                if "Market structure" in pdf_file.name:
                    target_pdf = pdf_file
                    break
        
        if target_pdf:
            print(f"✅ Found: {target_pdf.name}")
            print(f"✅ Size: {target_pdf.stat().st_size / 1024 / 1024:.1f}MB")
            print(f"✅ Location: {target_pdf.parent.name}")
            
            print(f"\n🔄 Converting to md-hybrid...")
            result = converter.convert_pdf(target_pdf, 'md-hybrid')
            
            if result:
                print(f"✅ SUCCESS!")
                print(f"✅ Output: {result}")
                
                # Check images
                images_dir = result.parent / f"{result.stem}_images"
                if images_dir.exists():
                    image_files = list(images_dir.glob("*.png"))
                    print(f"🖼️  IMAGES: {len(image_files)} files created!")
                    
                    # Show first few
                    for img in image_files[:5]:
                        size_kb = img.stat().st_size / 1024
                        print(f"   - {img.name} ({size_kb:.1f}KB)")
                    
                    if len(image_files) > 5:
                        print(f"   ... and {len(image_files) - 5} more images")
                    
                    print(f"✅ IMAGES TOTAL: {len(image_files)} files")
                else:
                    print("❌ No images directory found")
                
                # Check markdown content
                with open(result, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                image_refs = content.count("![")
                print(f"📄 Image references in markdown: {image_refs}")
                
                if image_refs > 0:
                    print("✅ IMAGES SUCCESSFULLY INTEGRATED!")
                else:
                    print("⚠️  No image references found in markdown")
            
            else:
                print("❌ Conversion failed")
        
        else:
            print("❌ Market structure PDF not found")
            print("Available files in ctc:")
            if ctc_folder.exists():
                for f in ctc_folder.glob("*.pdf")[:10]:
                    print(f"   - {f.name}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

if __name__ == "__main__":
    test_market_structure_specific()
