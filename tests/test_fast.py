"""
Test Fast PDF Processor
=======================
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_fast_processor():
    """Test the fast PDF processor"""
    print("=" * 60)
    print("FAST PDF PROCESSOR - TEST")
    print("=" * 60)
    print()
    
    try:
        from fast_pdf_processor import FastPDFProcessor
        print("✅ Fast PDF Processor imported")
        
        # Initialize processor
        output_dir = current_dir / "output" / "md"
        temp_dir = current_dir / "temp"
        
        processor = FastPDFProcessor(output_dir, temp_dir)
        print("✅ Fast processor initialized")
        
        # Find a small PDF for testing
        pdf_files = list(current_dir.parent.glob("*.pdf"))
        if pdf_files:
            # Pick the smallest PDF
            test_pdf = min(pdf_files, key=lambda p: p.stat().st_size)
            print(f"✅ Test PDF: {test_pdf.name} ({test_pdf.stat().st_size / 1024 / 1024:.1f}MB)")
            
            # Quick analysis
            print(f"\n📊 QUICK ANALYSIS...")
            analysis = processor.analyze_pdf_simple(test_pdf)
            print(f"  📄 Pages: {analysis['total_pages']}")
            print(f"  💾 Size: {analysis['file_size_mb']:.1f}MB")
            print(f"  🎯 Recommended: {analysis['recommended_mode']}")
            
            # Test HYBRID mode (fast)
            print(f"\n🔄 TESTING FAST HYBRID...")
            success, message, output_path = processor.convert_pdf_fast(test_pdf, "hybrid")
            
            if success:
                print(f"✅ HYBRID SUCCESS: {message}")
                print(f"✅ Output: {output_path}")
                
                # Check if file was created
                if output_path.exists():
                    size_kb = output_path.stat().st_size / 1024
                    print(f"✅ File created: {size_kb:.1f}KB")
                    
                    # Check for images
                    images_dir = output_path.parent / f"{output_path.stem}_images"
                    if images_dir.exists():
                        image_files = list(images_dir.glob("*.png"))
                        print(f"✅ Images: {len(image_files)} files")
                else:
                    print("❌ Output file not created")
            else:
                print(f"❌ HYBRID FAILED: {message}")
            
            # Test OCR mode (if time allows)
            print(f"\n🔍 TESTING FAST OCR...")
            success2, message2, output_path2 = processor.convert_pdf_fast(test_pdf, "ocr")
            
            if success2:
                print(f"✅ OCR SUCCESS: {message2}")
                print(f"✅ Output: {output_path2}")
            else:
                print(f"⚠️  OCR: {message2}")
                print("   (This might be expected if OCR tools not installed)")
                
        else:
            print("❌ No PDF files found for testing")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_fast_processor()
