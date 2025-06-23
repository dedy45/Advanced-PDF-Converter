@echo off
REM Ultra Simple PDF Converter Test
REM ===============================

title PDF Converter Test

REM Just run the quick test first
echo Running quick system test...
echo.

python quick_test.py

echo.
echo =================================
echo.
echo If test passed, try running the converter:
echo.

set /p RUN_CONVERTER="Run PDF Converter now? (y/N): "

if /i "%RUN_CONVERTER%"=="y" (
    echo.
    echo Starting converter...
    python main.py
)

echo.
echo Done.
pause
