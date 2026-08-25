@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER - PROGRAMMER BOOK CROSS-SOURCE LINK BUILDER
echo ============================================================
echo Builds conservative cross-source review hypotheses from the
 echo reduced programmer-book candidate queue.
echo Similarity is lexical/deterministic only.
echo No semantic equivalence or contradiction is asserted.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\build_programmer_book_cross_source_links.py
set "RC=%ERRORLEVEL%"

echo.
echo Summary: reports\programming_kb_factory\LATEST_PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.json
echo Links:   reports\programming_kb_factory\PROGRAMMER_BOOK_CROSS_SOURCE_LINKS.json
echo Queue:   reports\programming_kb_factory\PROGRAMMER_BOOK_CROSS_SOURCE_ANALYST_QUEUE.json
echo Exit code: %RC%
exit /b %RC%
