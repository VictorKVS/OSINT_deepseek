@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER - PROGRAMMER BOOK MAIN ANALYST PILOT
echo ============================================================
echo Single book: Software Architecture: The Hard Parts
echo Pilot: 3 batches, 1-stream baseline, resume-safe.
echo KB auto-promotion is disabled.
echo.

python -m py_compile scripts\run_programmer_book_main_analyst.py
if errorlevel 1 goto :fail

python scripts\run_programmer_book_main_analyst.py --limit-batches 3
if errorlevel 1 goto :fail

echo.
echo PILOT COMPLETE. Review:
echo   reports\programming_kb_factory\LATEST_PROGRAMMER_BOOK_MAIN_ANALYST.json
echo.
exit /b 0

:fail
echo.
echo ERROR/BLOCKED: Main Analyst PILOT stopped with exit code %errorlevel%.
exit /b %errorlevel%
