#!/usr/bin/env python
"""
PDF Converter Main Entry Point
==============================

Script utama untuk menjalankan PDF Converter
Dapat dijalankan dengan: python main.py
"""

import sys
import os
from pathlib import Path

# Tambahkan core ke Python path
current_dir = Path(__file__).parent
core_dir = current_dir / "core"
sys.path.insert(0, str(core_dir))

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import rich
    except ImportError:
        missing_deps.append("rich")
    
    try:
        import pypandoc
    except ImportError:
        missing_deps.append("pypandoc")
    
    try:
        import PyPDF2
    except ImportError:
        missing_deps.append("PyPDF2")
    
    try:
        from pdf2image import convert_from_path
    except ImportError:
        missing_deps.append("pdf2image")
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("Pillow")
    
    return missing_deps

def show_dependency_error(missing_deps):
    """Show user-friendly dependency error message"""
    print("=" * 60)
    print("❌ MISSING DEPENDENCIES")
    print("=" * 60)
    print()
    print("The following Python packages are required but not installed:")
    for dep in missing_deps:
        print(f"  • {dep}")
    print()
    print("📥 TO INSTALL:")
    print("Run one of these commands:")
    print()
    print("  pip install -r requirements.txt")
    print("  or")
    print("  pip install " + " ".join(missing_deps))
    print()
    print("🔧 ALTERNATIVE:")
    print("Use start_converter.bat which will install dependencies automatically")
    print()
    print("=" * 60)

def main():
    """
    Fungsi utama untuk menjalankan PDF Converter
    """
    try:
        print("PDF Converter - Starting...")
        print("Checking dependencies...")
        
        # Check dependencies first
        missing_deps = check_dependencies()
        if missing_deps:
            show_dependency_error(missing_deps)
            return False
        
        print("Dependencies OK ✓")
        print()
        
        # Import CLI class (after dependency check)
        # Fix import path
        sys.path.insert(0, str(core_dir))
        import cli
        
        # Jalankan converter
        print("Initializing PDF Converter...")
        cli_instance = cli.PDFConverterCLI(current_dir)
        return cli_instance.run_interactive_mode()
        
    except ImportError as e:
        print()
        print("=" * 60)
        print("❌ IMPORT ERROR")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("This usually means missing dependencies.")
        print("Please run: pip install -r requirements.txt")
        print("Or use: start_converter.bat")
        print()
        return False
        
    except FileNotFoundError as e:
        print()
        print("=" * 60)
        print("❌ FILE NOT FOUND")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Make sure you're running this from the pdf_converter directory")
        print("and all required files are present.")
        print()
        return False
        
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("👋 CANCELLED BY USER")
        print("=" * 60)
        print("PDF Converter was cancelled by user (Ctrl+C)")
        print()
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"Error: {e}")
        print(f"Type: {type(e).__name__}")
        print()
        print("Please report this error if it persists.")
        print()
        return False

if __name__ == "__main__":
    success = main()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
