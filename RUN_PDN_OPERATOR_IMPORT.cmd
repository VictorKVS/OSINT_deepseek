@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDn OPERATOR-ASSISTED IMPORT
echo Browser-saved official HTML -^> identity -^> SHA256 -^> D4 -^> D5
echo ============================================================
echo.

set "INBOX=data\operator_import\pdn_inbox"
if not exist "%INBOX%" mkdir "%INBOX%"

echo Save official pages as HTML into:
echo   %CD%\%INBOX%
echo.
echo Expected file names for the active corpus:
echo   DOC-RU-FZ-152-2006.html
echo   DOC-RU-PP-1119-2012.html
echo   DOC-RU-FSTEC-21-2013.html
echo   DOC-RU-FSB-378-2014.html
echo.
echo IMPORTANT: save the official page HTML itself, not a screenshot.
echo PDF is intentionally not accepted by this runner yet.
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% --version
if errorlevel 1 (
  echo ERROR: Python was not found.
  pause
  exit /b 1
)

%PYTHON_EXE% scripts\run_pdn_operator_import.py
set "RC=%ERRORLEVEL%"

echo.
echo Review package:
echo   reports\pdn_live\REVIEW.md
echo   reports\pdn_live\batch_review_manifest.jsonl
echo.
if "%RC%"=="0" (
  echo PASS: all enabled operator-assisted imports completed without hard failures.
) else (
  echo PARTIAL/FAIL: check missing files, identity markers, or compilation reasons above.
)

pause
exit /b %RC%
