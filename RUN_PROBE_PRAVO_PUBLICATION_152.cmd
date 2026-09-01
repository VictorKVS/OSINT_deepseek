@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER official publication API probe - 152-FZ
echo metadata discovery only; no D2/D3 promotion
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\probe_pravo_publication_152.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: official publication API probe completed.
  echo Metadata discovery never promotes D2/D3 by itself.
) else (
  echo FAIL: official publication API probe could not complete.
  echo See reports\pdn_live\PROBE_PRAVO_PUBLICATION_152.json
)

exit /b %RC%
