"""
Quick Test Script for PDF Converter
===================================

Script cepat untuk test basic functionality tanpa dependencies berat
"""

import sys
import os
from pathlib import Path

def test_basic_setup():
    """Test basic setup tanpa dependencies eksternal"""
    print("=" * 50)
    print("PDF CONVERTER - QUICK TEST")  
    print("=" * 50)
    print()
    
    # Test 1: Directory structure
    print("🔍 Testing directory structure...")
    current_dir = Path(__file__).parent
    
    required_files = ['main.py', 'requirements.txt']
    required_dirs = ['src', 'output', 'temp']
    
    all_good = True
    
    for file in required_files:
        if (current_dir / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            all_good = False
    
    for dir_name in required_dirs:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ - MISSING")
            # Auto-create missing directories
            dir_path.mkdir(exist_ok=True)
            print(f"     → Created {dir_name}/")
    
    print()
    
    # Test 2: Python version
    print("🐍 Testing Python...")
    python_version = sys.version.split()[0]
    print(f"  ✅ Python {python_version}")
    
    # Check if Python version is adequate
    major, minor = map(int, python_version.split('.')[:2])
    if major >= 3 and minor >= 8:
        print(f"  ✅ Version OK (>= 3.8)")
    else:
        print(f"  ⚠️  Version might be too old (need >= 3.8)")
    
    print()
    
    # Test 3: Find PDF files
    print("📚 Looking for PDF files...")
    pdf_count = 0
    
    # Search in parent directory
    for pdf_file in current_dir.parent.rglob("*.pdf"):
        pdf_count += 1
        if pdf_count <= 3:  # Show first 3
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"  📄 {pdf_file.name} ({size_mb:.1f} MB)")
    
    if pdf_count > 3:
        print(f"  ... and {pdf_count - 3} more files")
    
    print(f"  ✅ Total: {pdf_count} PDF files found")
    print()
    
    # Test 4: Check if we can import basic modules
    print("📦 Testing basic imports...")
    
    try:
        import pathlib
        print("  ✅ pathlib")
    except ImportError:
        print("  ❌ pathlib")
        all_good = False
    
    try:
        import subprocess
        print("  ✅ subprocess")
    except ImportError:
        print("  ❌ subprocess")
        all_good = False
    
    print()
    
    # Test 5: Check external dependencies
    print("🔧 Testing external dependencies...")
    
    deps_status = {}
    
    # Check rich
    try:
        import rich
        deps_status['rich'] = True
        print("  ✅ rich")
    except ImportError:
        deps_status['rich'] = False
        print("  ❌ rich - will use fallback")
    
    # Check pandoc
    try:
        import subprocess
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            deps_status['pandoc'] = True
            print("  ✅ pandoc")
        else:
            deps_status['pandoc'] = False
            print("  ❌ pandoc")
    except:
        deps_status['pandoc'] = False
        print("  ❌ pandoc")
    
    print()
    
    # Summary
    print("=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if all_good and pdf_count > 0:
        print("✅ Basic setup looks good!")
        print(f"✅ Found {pdf_count} PDF files to convert")
        
        if all(deps_status.values()):
            print("✅ All dependencies available")
            print()
            print("🚀 READY TO RUN!")
            print("Use: start_converter.bat")
        else:
            print("⚠️  Some dependencies missing")
            print()
            print("🔧 NEXT STEPS:")
            if not deps_status.get('rich', True):
                print("   pip install rich")
            if not deps_status.get('pandoc', True):
                print("   Install pandoc from: https://pandoc.org/installing.html")
            print()
            print("Or run: install.bat")
    else:
        print("❌ Setup incomplete")
        print()
        print("🔧 ISSUES FOUND:")
        if not all_good:
            print("   - Missing required files/directories")
        if pdf_count == 0:
            print("   - No PDF files found to convert")
    
    print("=" * 50)
    return all_good and pdf_count > 0

if __name__ == "__main__":
    test_basic_setup()
