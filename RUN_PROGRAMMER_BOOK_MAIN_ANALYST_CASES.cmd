@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER - PROGRAMMER BOOK MAIN ANALYST CASE BUILDER
echo ============================================================
echo Input: PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json
echo Builds conservative comparison cases for the main analyst.
echo No semantic equivalence is asserted.
echo Potential conflicts are heuristic review signals only.
echo Underlying candidate provenance is preserved.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\build_programmer_book_main_analyst_cases.py
set "RC=%ERRORLEVEL%"

echo.
echo Summary: reports\programming_kb_factory\LATEST_PROGRAMMER_BOOK_MAIN_ANALYST_CASES.json
echo Queue:   reports\programming_kb_factory\PROGRAMMER_BOOK_MAIN_ANALYST_CASE_QUEUE.json
echo Hold:    reports\programming_kb_factory\PROGRAMMER_BOOK_MAIN_ANALYST_CASE_HOLD.json
echo Exit code: %RC%
exit /b %RC%
