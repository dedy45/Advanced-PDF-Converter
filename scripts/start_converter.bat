@echo off
REM PDF Converter Launcher - Windows 11 Compatible
REM ==============================================

title PDF Converter Tool

echo.
echo ================================================
echo           PDF CONVERTER TOOL
echo ================================================
echo Checking system requirements...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if we're in the right directory
if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo Make sure you're running this from the pdf_converter folder
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo [INFO] Found main.py - OK
echo [INFO] Checking Python installation...

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH
    echo.
    echo Please install Python or add it to PATH
    echo You can download Python from: https://www.python.org/downloads/
    echo.
    echo Or if you have Anaconda, try opening Anaconda Prompt and run:
    echo   cd "%CD%"
    echo   python main.py
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python %PYTHON_VERSION% found - OK

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

echo [INFO] Installing/checking dependencies...
echo This may take a few minutes on first run...
echo.

REM Install dependencies with verbose output
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo.
    echo Trying alternative installation...
    pip install --user rich pypandoc PyPDF2 pdf2image Pillow python-magic-bin tqdm
    if %errorlevel% neq 0 (
        echo [ERROR] Could not install required packages
        echo.
        echo Please try manually:
        echo   pip install rich pypandoc PyPDF2 pdf2image Pillow python-magic-bin tqdm
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [INFO] Dependencies installed successfully!

REM Check pandoc installation
echo [INFO] Checking pandoc...
where pandoc >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Pandoc not found!
    echo.
    echo Pandoc is required for PDF conversion.
    echo.
    echo [INSTALL PANDOC]
    echo Choose one option:
    echo.
    echo 1. Download installer from:
    echo    https://github.com/jgm/pandoc/releases
    echo    (Download pandoc-3.x.x-windows-x86_64.msi)
    echo.
    echo 2. Use conda (if you have Anaconda):
    echo    conda install -c conda-forge pandoc
    echo.
    echo 3. Use chocolatey (if installed):
    echo    choco install pandoc
    echo.
    echo After installing pandoc, restart this script.
    echo.
    set /p CONTINUE="Continue without pandoc? (y/N): "
    if /i not "%CONTINUE%"=="y" (
        pause
        exit /b 1
    )
    echo.
    echo [WARNING] Continuing without pandoc - conversion will fail
) else (
    for /f "tokens=*" %%i in ('pandoc --version ^| findstr "pandoc"') do (
        echo [INFO] %%i found - OK
    )
)

echo [INFO] Starting PDF Converter...
echo.

REM Run the converter
python main.py
set CONVERTER_EXIT_CODE=%errorlevel%

echo.
if %CONVERTER_EXIT_CODE% equ 0 (
    echo [INFO] PDF Converter finished successfully!
) else (
    echo [ERROR] PDF Converter exited with error code: %CONVERTER_EXIT_CODE%
    echo.
    echo If you see import errors, try:
    echo   pip install --upgrade -r requirements.txt
)

echo.
echo Press any key to close...
pause >nul
