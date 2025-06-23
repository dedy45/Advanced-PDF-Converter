"""
Advanced PDF Converter - Main Entry Point
==========================================

Professional PDF to Markdown converter dengan smart image extraction.
Perfect untuk trading books, technical analysis, dan course materials.

Usage:
    python main.py              # Interactive mode
    python main.py --help       # Show help
    python main.py --check      # Check dependencies

Author: Advanced PDF Converter Team
Version: 2.0
"""

import sys
import argparse
from pathlib import Path

# Add core directory to Python path
current_dir = Path(__file__).parent
core_dir = current_dir / "core"
sys.path.insert(0, str(core_dir))

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...\n")
    
    try:
        # Check core imports
        from cli import PDFConverterCLI
        from converter import PDFConverter
        from utils import check_pandoc_installation
        
        print("✅ Core modules: OK")
        
        # Check pandoc
        if check_pandoc_installation():
            print("✅ Pandoc: OK")
        else:
            print("❌ Pandoc: Not found")
            print("   Please install from: https://pandoc.org/installing.html")
            return False
        
        # Check Python libraries
        try:
            import PyPDF2
            print("✅ PyPDF2: OK")
        except ImportError:
            print("❌ PyPDF2: Not found")
            
        try:
            from pdf2image import convert_from_path
            print("✅ pdf2image: OK")
        except ImportError:
            print("❌ pdf2image: Not found")
            
        try:
            from rich.console import Console
            print("✅ rich: OK")
        except ImportError:
            print("❌ rich: Not found")
            
        try:
            import pypandoc
            print("✅ pypandoc: OK")
        except ImportError:
            print("❌ pypandoc: Not found")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def show_help():
    """Show help information"""
    help_text = """
🚀 Advanced PDF Converter v2.0

USAGE:
    python main.py              Interactive mode (recommended)
    python main.py --help       Show this help
    python main.py --check      Check dependencies

CONVERSION MODES:
    md-hybrid     Text + images preserved (RECOMMENDED for trading PDFs)
    md-ocr        Everything as text via OCR (for scanned documents)  
    md            Text only (basic mode)
    html          Web format
    docx          Microsoft Word
    txt           Plain text
    latex         Academic format

EXAMPLES:
    1. Convert trading PDF with charts:
       → Run: python main.py
       → Choose: md-hybrid
       → Result: Text + preserved charts
       
    2. Convert scanned document:
       → Run: python main.py  
       → Choose: md-ocr
       → Result: Searchable text
       
    3. Batch convert multiple files:
       → Place PDFs in main directory
       → Run: python main.py
       → Select: all

SUPPORT:
    📖 Documentation: docs/USAGE_GUIDE.md
    🔧 Advanced Guide: docs/ADVANCED_GUIDE.md
    🐛 Issues: Create GitHub issue

Happy Converting! 📚➡️📝
"""
    print(help_text)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Advanced PDF Converter - Professional PDF to Markdown conversion",
        add_help=False
    )
    parser.add_argument('--help', action='store_true', help='Show help information')
    parser.add_argument('--check', action='store_true', help='Check dependencies')
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        return
    
    if args.check:
        if check_dependencies():
            print("\n✅ All dependencies OK!")
        else:
            print("\n❌ Some dependencies missing. Please install them.")
        return
    
    # Run interactive mode
    try:
        from cli import PDFConverterCLI
        
        print("PDF Converter - Starting...")
        
        # Check dependencies first
        print("Checking dependencies...")
        
        # Quick dependency check for interactive mode
        try:
            from utils import check_pandoc_installation
            if not check_pandoc_installation():
                print("❌ Pandoc not found! Please install Pandoc first.")
                print("Download from: https://pandoc.org/installing.html")
                input("Press Enter to exit...")
                return
        except:
            print("⚠️  Could not verify Pandoc installation")
        
        print("Dependencies OK ✓")
        
        # Initialize and run CLI
        print("Initializing PDF Converter...")
        cli = PDFConverterCLI()
        cli.run_interactive_mode()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n👋 Conversion cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the error and try again.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
