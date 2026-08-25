@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER - PROGRAMMER BOOK MAIN ANALYST FULL RUN
echo ============================================================
echo Single book: Software Architecture: The Hard Parts
echo Resume-safe. 1-stream baseline. KB auto-promotion disabled.
echo.

python -m py_compile scripts\run_programmer_book_main_analyst.py
if errorlevel 1 goto :fail

python scripts\run_programmer_book_main_analyst.py
if errorlevel 1 goto :fail

echo.
echo MAIN ANALYST RUN COMPLETE/UPDATED. Review:
echo   reports\programming_kb_factory\LATEST_PROGRAMMER_BOOK_MAIN_ANALYST.json
echo   reports\programming_kb_factory\PROGRAMMER_BOOK_PROFESSOR_REVIEW_QUEUE.json
echo.
exit /b 0

:fail
echo.
echo ERROR/BLOCKED: Main Analyst run stopped with exit code %errorlevel%.
exit /b %errorlevel%
