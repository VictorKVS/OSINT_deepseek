@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN OFFICIAL SOURCE PACK D0-D3
echo clean A0 session HTML -^> identity -^> exact bytes -^> SHA256
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
  echo PASS: all four official publication captures closed D0-D3.
) else (
  echo PARTIAL: some official publication HTML captures are still missing or failed identity checks.
)

pause
exit /b %RC%
