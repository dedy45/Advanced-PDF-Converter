"""
Test Specific PDF - Market Structure
===================================
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_market_structure_pdf():
    """Test the specific PDF mentioned by user"""
    print("=" * 60)
    print("MARKET STRUCTURE PDF - TEST")
    print("=" * 60)
    print()
    
    try:
        from fast_pdf_processor import FastPDFProcessor
        
        # Initialize processor
        output_dir = current_dir / "output" / "md"
        temp_dir = current_dir / "temp"
        
        processor = FastPDFProcessor(output_dir, temp_dir)
        print("✅ Fast processor initialized")
        
        # Find the specific PDF file
        pdf_files = list(current_dir.parent.glob("*.pdf"))
        target_pdf = None
        
        for pdf_file in pdf_files:
            if "Market structure" in pdf_file.name or "powerfull setup" in pdf_file.name:
                target_pdf = pdf_file
                break
        
        # Try finding in ctc folder
        if not target_pdf:
            ctc_folder = current_dir.parent / "ctc"
            if ctc_folder.exists():
                ctc_files = list(ctc_folder.glob("*Market*structure*.pdf"))
                if ctc_files:
                    target_pdf = ctc_files[0]
        
        if target_pdf:
            print(f"✅ Found PDF: {target_pdf.name}")
            print(f"✅ Size: {target_pdf.stat().st_size / 1024 / 1024:.1f}MB")
            
            # Test HYBRID mode with focus on images
            print(f"\n🔄 TESTING HYBRID MODE (with image extraction)...")
            success, message, output_path = processor.convert_pdf_fast(target_pdf, "hybrid")
            
            if success:
                print(f"✅ SUCCESS: {message}")
                print(f"✅ Output: {output_path}")
                
                # Check images directory
                images_dir = output_path.parent / f"{output_path.stem}_images"
                if images_dir.exists():
                    image_files = list(images_dir.glob("*.png"))
                    print(f"✅ IMAGES FOUND: {len(image_files)} files")
                    
                    for img_file in image_files[:5]:  # Show first 5
                        print(f"   - {img_file.name}")
                    
                    if len(image_files) > 5:
                        print(f"   ... and {len(image_files) - 5} more")
                else:
                    print("❌ NO IMAGES DIRECTORY FOUND")
                
                # Check output file content
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Count image references
                    image_refs = content.count("![")
                    print(f"✅ Image references in markdown: {image_refs}")
                    
                    # Show which method was used
                    if "PyMuPDF" in content:
                        print("✅ Used: PyMuPDF method (best for images)")
                    elif "PyPDF2" in content:
                        print("⚠️  Used: PyPDF2 method (limited image support)")
                    
            else:
                print(f"❌ FAILED: {message}")
                
        else:
            print("❌ Market structure PDF not found!")
            print("Available PDFs:")
            for pdf_file in pdf_files[:10]:
                print(f"   - {pdf_file.name}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_market_structure_pdf()
