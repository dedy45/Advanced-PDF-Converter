"""
Test Advanced PDF Processor
===========================
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_advanced_processor():
    """Test the advanced PDF processor"""
    print("=" * 60)
    print("ADVANCED PDF PROCESSOR - TEST")
    print("=" * 60)
    print()
    
    try:
        from advanced_pdf_processor import AdvancedPDFProcessor
        print("✅ Advanced PDF Processor imported")
        
        # Initialize processor
        output_dir = current_dir / "output" / "md"
        temp_dir = current_dir / "temp"
        
        processor = AdvancedPDFProcessor(output_dir, temp_dir)
        print("✅ Processor initialized")
        
        # Check available methods
        methods = processor.available_methods
        print(f"✅ Available methods: {methods}")
        
        # Find test PDF
        pdf_files = list(current_dir.parent.glob("*.pdf"))
        if pdf_files:
            test_pdf = pdf_files[0]
            print(f"✅ Test PDF: {test_pdf.name}")
            
            # Analyze PDF
            print(f"\n🔍 ANALYZING PDF...")
            analysis = processor.analyze_pdf_content(test_pdf)
            
            print(f"  📊 Total pages: {analysis['total_pages']}")
            print(f"  📝 Text pages: {analysis['text_pages']}")
            print(f"  🖼️  Image pages: {analysis['image_pages']}")
            print(f"  🔄 Mixed pages: {analysis['mixed_pages']}")
            print(f"  📈 Text ratio: {analysis['text_ratio']:.1%}")
            print(f"  🎯 Recommended mode: {analysis['recommended_mode']}")
            
            # Test modes
            print(f"\n🔥 TESTING HYBRID MODE...")
            success, message, output_path = processor.convert_pdf(test_pdf, "hybrid")
            
            if success:
                print(f"✅ HYBRID SUCCESS: {message}")
                print(f"✅ Output: {output_path}")
                
                # Check images
                images_dir = output_path.parent / f"{output_path.stem}_images"
                if images_dir.exists():
                    image_files = list(images_dir.glob("*.png"))
                    print(f"✅ Images: {len(image_files)} files")
                
                print(f"\n🔍 TESTING OCR MODE...")
                success2, message2, output_path2 = processor.convert_pdf(test_pdf, "ocr")
                
                if success2:
                    print(f"✅ OCR SUCCESS: {message2}")
                    print(f"✅ Output: {output_path2}")
                else:
                    print(f"⚠️  OCR failed: {message2}")
                    print("   (This is expected if Tesseract is not installed)")
            else:
                print(f"❌ HYBRID FAILED: {message}")
        else:
            print("❌ No PDF files found for testing")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_advanced_processor()
