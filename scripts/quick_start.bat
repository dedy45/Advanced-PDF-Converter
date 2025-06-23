@echo off
REM Quick Start PDF Converter
REM =========================

title PDF Converter - Quick Start

echo.
echo ================================================
echo        PDF CONVERTER - QUICK START
echo ================================================
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo Error: main.py not found!
    echo Please run this from the pdf_converter directory
    pause
    exit /b 1
)

echo Starting PDF Converter...
echo.

REM Try to run with existing conda environment
conda run --live-stream --name converterpdf python main.py 2>nul

if %errorlevel% neq 0 (
    echo.
    echo Environment not found or error occurred.
    echo Running setup...
    call run_converter.bat
)

echo.
pause
