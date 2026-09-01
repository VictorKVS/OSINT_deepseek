@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER - PROGRAMMER BOOK KB DEEP ANALYSIS
 echo ============================================================
echo Read-only source processing of already acquired programming materials.
echo Extracts architecture/programming candidates for analyst review:
echo   principle / pattern / tradeoff / decision criterion
echo   failure mode / definition / term / example / claim
echo.
echo Source bytes are not modified.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\process_programmer_books_deep.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\programming_kb_factory\LATEST_PROGRAMMER_BOOK_DEEP_ANALYSIS.json
echo Candidates: reports\programming_kb_factory\PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES.json
echo Exit code: %RC%
exit /b %RC%
