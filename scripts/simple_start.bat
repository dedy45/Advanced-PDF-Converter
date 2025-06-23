@echo off
REM Simple PDF Converter - No Dependencies Check
REM ============================================

title PDF Converter - Simple

echo.
echo ========================================
echo      PDF CONVERTER - SIMPLE MODE
echo ========================================
echo.

REM Go to script directory
cd /d "%~dp0"

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo Make sure you're in the pdf_converter directory
    pause
    exit /b 1
)

echo Starting converter directly...
echo.

REM Try to run directly
python main.py

echo.
echo Converter finished.
echo.
echo If you saw errors above, run: start_converter.bat
echo That version will install missing dependencies automatically.
echo.
pause
