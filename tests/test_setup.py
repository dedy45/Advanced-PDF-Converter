"""
Test Script untuk PDF Converter
===============================

Script sederhana untuk testing basic functionality
"""

import sys
import os
from pathlib import Path

# Tambahkan src ke path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_imports():
    """Test basic imports"""
    print("Testing imports...")
    
    try:
        # Test rich import
        from rich.console import Console
        console = Console()
        console.print("[green]✓ Rich library OK[/green]")
    except ImportError:
        print("✗ Rich library not available (will use fallback)")
    
    try:
        # Test pandoc check
        from utils import check_pandoc_installation
        if check_pandoc_installation():
            print("✓ Pandoc installation OK")
        else:
            print("✗ Pandoc not found")
    except Exception as e:
        print(f"✗ Error checking pandoc: {e}")
    
    try:
        # Test converter class
        from converter import PDFConverter
        converter = PDFConverter(current_dir / "temp", current_dir / "output")
        formats = converter.get_supported_formats()
        print(f"✓ Converter class OK - {len(formats)} formats supported")
    except Exception as e:
        print(f"✗ Error loading converter: {e}")

def test_directory_structure():
    """Test directory structure"""
    print("\nTesting directory structure...")
    
    dirs_to_check = ['src', 'output', 'temp']
    for dir_name in dirs_to_check:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory missing")
            dir_path.mkdir(exist_ok=True)
            print(f"  → Created {dir_name}/ directory")

def test_find_pdf_files():
    """Test finding PDF files"""
    print("\nTesting PDF file detection...")
    
    try:
        from utils import get_available_pdf_files
        
        # Check parent directory for PDFs
        pdf_files = get_available_pdf_files(current_dir.parent)
        print(f"✓ Found {len(pdf_files)} PDF files in workspace")
        
        # Show first few files
        for i, pdf_file in enumerate(pdf_files[:5]):
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"  - {pdf_file.name} ({size_mb:.1f} MB)")
        
        if len(pdf_files) > 5:
            print(f"  ... and {len(pdf_files) - 5} more files")
            
    except Exception as e:
        print(f"✗ Error finding PDF files: {e}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("PDF CONVERTER - SYSTEM TEST")
    print("=" * 50)
    
    test_directory_structure()
    test_imports()
    test_find_pdf_files()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)
    
    # Check if ready to run
    print("\nReady to run PDF Converter!")
    print("Use: python main.py")
    print("Or:  quick_start.bat")

if __name__ == "__main__":
    main()
