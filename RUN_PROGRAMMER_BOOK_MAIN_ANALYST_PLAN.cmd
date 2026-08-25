@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER - PROGRAMMER BOOK MAIN ANALYST PLAN
echo ============================================================
echo Single book: Software Architecture: The Hard Parts
echo No LLM calls. No KB promotion.
echo.

python -m py_compile scripts\run_programmer_book_main_analyst.py
if errorlevel 1 goto :fail

python scripts\run_programmer_book_main_analyst.py --plan-only
if errorlevel 1 goto :fail

exit /b 0

:fail
echo.
echo ERROR: Main Analyst PLAN stopped with exit code %errorlevel%.
exit /b %errorlevel%
