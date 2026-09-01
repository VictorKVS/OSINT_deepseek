@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - INVENTORY GARANT 152-FZ EDITIONS
echo Downloads ODT -^> identity -^> SHA256 dedupe -^> local archive -^> metadata
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\import_garant_152_editions.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: GARANT 152-FZ edition inventory updated.
  echo Next: download another historical edition from the GARANT Redaktsii tab and run this command again.
) else (
  echo PARTIAL/FAIL: no identity-valid 152-FZ ODT captures were inventoried.
)

pause
exit /b %RC%
