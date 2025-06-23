@echo off
REM PDF Converter Troubleshooting
REM =============================

title PDF Converter - Troubleshooting

echo.
echo ================================================
echo    PDF CONVERTER - TROUBLESHOOTING MODE
echo ================================================
echo.

REM Go to correct directory
cd /d "%~dp0"

echo [STEP 1] Checking directory structure...
echo Current directory: %CD%
echo.

REM Check required files
set MISSING_FILES=

if not exist "main.py" (
    echo ❌ main.py - MISSING
    set MISSING_FILES=1
) else (
    echo ✅ main.py - OK
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt - MISSING
    set MISSING_FILES=1
) else (
    echo ✅ requirements.txt - OK
)

if not exist "src\" (
    echo ❌ src folder - MISSING
    set MISSING_FILES=1
) else (
    echo ✅ src folder - OK
)

if defined MISSING_FILES (
    echo.
    echo [ERROR] Missing required files!
    echo Make sure you're in the correct pdf_converter directory
    pause
    exit /b 1
)

echo.
echo [STEP 2] Checking Python installation...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
    echo.
    echo [SOLUTION] Install Python:
    echo   1. Download from: https://www.python.org/downloads/
    echo   2. Make sure to check "Add Python to PATH" during installation
    echo   3. Restart command prompt after installation
    echo.
    
    REM Check if python exists in common locations
    if exist "C:\Python*\python.exe" (
        echo Python might be installed but not in PATH
    )
    
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version') do echo ✅ Python %%i - OK
)

echo.
echo [STEP 3] Checking pip...

pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    echo This usually means Python installation is incomplete
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('pip --version') do echo ✅ pip %%i - OK
)

echo.
echo [STEP 4] Checking dependencies...

python -c "import sys; print('Python executable:', sys.executable)" 2>&1
echo.

echo Checking required packages...

python -c "import rich; print('✅ rich - OK')" 2>nul || echo ❌ rich - MISSING
python -c "import pypandoc; print('✅ pypandoc - OK')" 2>nul || echo ❌ pypandoc - MISSING  
python -c "import PyPDF2; print('✅ PyPDF2 - OK')" 2>nul || echo ❌ PyPDF2 - MISSING
python -c "import PIL; print('✅ Pillow - OK')" 2>nul || echo ❌ Pillow - MISSING
python -c "import pdf2image; print('✅ pdf2image - OK')" 2>nul || echo ❌ pdf2image - MISSING

echo.
echo [STEP 5] Installing missing dependencies...
echo This may take a few minutes...
echo.

pip install rich pypandoc PyPDF2 pdf2image Pillow python-magic-bin tqdm
set INSTALL_RESULT=%errorlevel%

echo.
if %INSTALL_RESULT% equ 0 (
    echo ✅ Dependencies installation completed
) else (
    echo ❌ Dependencies installation failed
    echo.
    echo [SOLUTION] Try these alternatives:
    echo   1. pip install --user rich pypandoc PyPDF2 pdf2image Pillow python-magic-bin tqdm
    echo   2. Use Anaconda Prompt instead of regular Command Prompt
    echo   3. Run as Administrator
    echo.
    pause
    exit /b 1
)

echo.
echo [STEP 6] Testing PDF Converter...
echo.

python main.py
set CONVERTER_RESULT=%errorlevel%

echo.
echo ================================================
echo               DIAGNOSIS COMPLETE
echo ================================================

if %CONVERTER_RESULT% equ 0 (
    echo ✅ PDF Converter ran successfully!
    echo You can now use: start_converter.bat
) else (
    echo ❌ PDF Converter failed to run
    echo Error code: %CONVERTER_RESULT%
    echo.
    echo [NEXT STEPS]
    echo 1. Check error messages above
    echo 2. Try running: python main.py
    echo 3. Make sure pandoc is installed: https://pandoc.org/installing.html
)

echo.
echo Press any key to exit...
pause >nul
