@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "LIBRARY=G:\1\OTUS\Библиотека"
if not "%~1"=="" set "LIBRARY=%~1"

echo ============================================================
echo FATHER Architect - Local Library Gap Audit
echo ============================================================
echo Library: %LIBRARY%
echo Source files are read-only; nothing is moved or deleted.
echo Output: inventory, SHA duplicates, competency coverage, P0/P1 gaps.
echo.

"%PY%" scripts\audit_architect_library.py --library "%LIBRARY%"
set "RC=%ERRORLEVEL%"

echo.
echo Markdown: reports\architect_library\ARCHITECT_LIBRARY_GAPS.md
echo JSON:     reports\architect_library\LATEST_ARCHITECT_LIBRARY_AUDIT.json
echo TSV:      reports\architect_library\ARCHITECT_LIBRARY_FILES.tsv
echo Exit code: %RC%
exit /b %RC%
