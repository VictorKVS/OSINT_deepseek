@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER - PROGRAMMER BOOK KB REVIEW QUEUE REDUCTION
echo ============================================================
echo Input: reports\programming_kb_factory\PROGRAMMER_BOOK_ARCHITECTURE_CANDIDATES.json
echo Exact normalized duplicates are collapsed with source support preserved.
echo Low-priority candidates are held, not deleted.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\reduce_programmer_book_candidates.py
set "RC=%ERRORLEVEL%"

echo.
echo Summary: reports\programming_kb_factory\LATEST_PROGRAMMER_BOOK_REDUCTION.json
echo Queue: reports\programming_kb_factory\PROGRAMMER_BOOK_MAIN_ANALYST_REVIEW_QUEUE.json
echo Hold: reports\programming_kb_factory\PROGRAMMER_BOOK_CANDIDATES_HOLD.json
echo Exit code: %RC%
exit /b %RC%
