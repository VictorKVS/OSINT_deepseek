@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER - PROGRAMMING_KB Source Factory (RU MIN)
echo ============================================================
echo 1. Probe Telegram bibliography
 echo 2. Build rights/acquisition plan
 echo 3. Download official/open sources (max 5 workers)
 echo 4. Download only explicitly owned/authorized Telegram books
 echo 5. Extract text and build knowledge candidates + graph
 echo.
echo Commercial Telegram books are NOT auto-downloaded.
echo To assert owned/authorized copies for this run:
echo   set FATHER_OWNED_BOOK_IDS=BOOK-001,BOOK-011
 echo.
echo No model training. No KB auto-promotion.
echo.

"%PY%" scripts\run_programming_kb_source_factory.py
set "RC=%ERRORLEVEL%"

echo.
echo Factory report: reports\programming_kb_factory\LATEST_PROGRAMMING_KB_SOURCE_FACTORY.json
echo Candidate graph: reports\programming_kb_factory\PROGRAMMING_KB_CANDIDATE_GRAPH.json
echo Exit code: %RC%
exit /b %RC%
