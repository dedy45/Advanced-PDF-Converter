"""
Direct Converter Test
====================
Test converter directly without CLI
"""

import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_converter_direct():
    """Test converter directly"""
    print("=" * 60)
    print("DIRECT CONVERTER TEST")
    print("=" * 60)
    print()
    
    try:
        from converter import PDFConverter
        from utils import create_output_directory
        
        print("✅ Converter imported")
        
        # Initialize converter
        output_dir = current_dir / "output"
        temp_dir = current_dir / "temp"
        
        converter = PDFConverter(temp_dir, output_dir)
        print("✅ Converter initialized")
        
        # Find test PDF
        pdf_files = list(current_dir.parent.glob("*.pdf"))
        if pdf_files:
            test_pdf = pdf_files[0]
            print(f"✅ Test PDF: {test_pdf.name}")
            
            # Test md-hybrid directly
            print(f"\n🔄 TESTING MD-HYBRID DIRECT...")
            result = converter.convert_pdf(test_pdf, 'md-hybrid')
            
            if result:
                print(f"✅ SUCCESS: {result}")
                print(f"✅ File size: {result.stat().st_size / 1024:.1f}KB")
                
                # Check content
                with open(result, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"✅ Content length: {len(content)} characters")
                    
                    # Show first few lines
                    lines = content.split('\n')[:10]
                    print("✅ First few lines:")
                    for line in lines:
                        if line.strip():
                            print(f"   {line[:80]}...")
                            break
            else:
                print("❌ Conversion failed")
                
        else:
            print("❌ No PDF files found")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_converter_direct()
