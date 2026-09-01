@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER - PROGRAMMING_KB Source Factory (RU MIN)
echo ============================================================
echo 1. RU laws / GOST / regulator scope gate
 echo 2. Primary language authorities + scientific consensus + world practice
 echo 3. Telegram bibliography probe and rights plan
 echo 4. Open books/papers + explicitly owned/authorized Telegram books
 echo 5. Extract text, decompose knowledge, build graph
 echo 6. Audit L1-L5 readiness
 echo.
echo Commercial Telegram books are NOT auto-downloaded.
echo To assert owned/authorized copies for this run:
echo   set FATHER_OWNED_BOOK_IDS=BOOK-001,BOOK-011
 echo.
echo Technical PASS is not the same as PROGRAMMING_KB MIN ready.
echo No model training. No KB auto-promotion.
echo.

"%PY%" scripts\run_programming_kb_source_factory.py
set "RC=%ERRORLEVEL%"

echo.
echo Factory report: reports\programming_kb_factory\LATEST_PROGRAMMING_KB_SOURCE_FACTORY.json
echo Layer readiness: reports\programming_kb_factory\LATEST_PROGRAMMING_KB_LAYER_READINESS.json
echo Candidate graph: reports\programming_kb_factory\PROGRAMMING_KB_CANDIDATE_GRAPH.json
echo Exit code: %RC%
exit /b %RC%
