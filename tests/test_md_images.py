"""
Quick Test for MD with Images Converter
======================================
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_md_img_converter():
    """Test the markdown with images converter"""
    print("=" * 60)
    print("PDF TO MARKDOWN WITH IMAGES - TEST")
    print("=" * 60)
    print()
    
    try:
        # Test imports
        print("Testing imports...")
        from pdf_to_md_with_images import PDFToMarkdownWithImages
        print("✅ pdf_to_md_with_images imported")
        
        # Initialize converter
        output_dir = current_dir / "output" / "md"
        temp_dir = current_dir / "temp"
        
        converter = PDFToMarkdownWithImages(output_dir, temp_dir)
        print("✅ Converter initialized")
        
        # Check available methods
        methods = converter.available_methods
        print(f"✅ Available methods: {methods}")
        
        # Find a small PDF for testing
        pdf_files = list(current_dir.parent.glob("*.pdf"))
        if pdf_files:
            # Use the first PDF file
            test_pdf = pdf_files[0]
            print(f"✅ Test PDF: {test_pdf.name}")
            
            # Test conversion
            print(f"\nTesting conversion to markdown with images...")
            success, message, output_path = converter.convert_pdf_to_markdown_with_images(test_pdf)
            
            if success:
                print(f"✅ SUCCESS: {message}")
                print(f"✅ Output: {output_path}")
                
                # Check if images were created
                images_dir = output_path.parent / f"{output_path.stem}_images"
                if images_dir.exists():
                    image_files = list(images_dir.glob("*.png"))
                    print(f"✅ Images created: {len(image_files)} files")
                else:
                    print("ℹ️  No separate images directory (might be embedded)")
            else:
                print(f"❌ FAILED: {message}")
        else:
            print("❌ No PDF files found for testing")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_md_img_converter()
