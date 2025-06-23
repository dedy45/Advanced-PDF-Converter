@echo off
REM PDF Converter Launcher
REM =====================

title PDF Converter Tool

echo.
echo ================================================
echo           PDF CONVERTER TOOL
echo ================================================
echo.
echo Checking Python environment...

REM Check if conda environment exists
conda info --envs | findstr "converterpdf" >nul
if %errorlevel% neq 0 (
    echo Creating conda environment...
    conda create -n converterpdf python=3.11 -y
    if %errorlevel% neq 0 (
        echo Error: Failed to create conda environment
        pause
        exit /b 1
    )
)

echo Activating environment and installing dependencies...
conda run --live-stream --name converterpdf pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Starting PDF Converter...
echo.

REM Run the PDF converter
conda run --live-stream --name converterpdf python src/cli.py

echo.
echo PDF Converter finished.
pause
