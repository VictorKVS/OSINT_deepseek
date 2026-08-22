@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN OFFICIAL SOURCE PACK INVENTORY
echo Downloads -^> candidate exact bytes -^> MIME guess -^> SHA256
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\inventory_pdn_official_downloads.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: official-download candidates found. Candidate status is not yet D3 verified.
) else (
  echo PARTIAL: no matching official-download candidates found yet.
)

pause
exit /b %RC%
