@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN OFFICIAL SOURCE PACK
echo Trusted A0/A1 acquisition first; GARANT is HOLD.
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\start_pdn_official_source_pack_session.py
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo.
  echo FAIL: could not start source-pack acquisition session.
  pause
  exit /b %RC%
)

echo.
echo Save each opened official publication page with Ctrl+S as HTML into Downloads.
echo Then run RUN_PDN_OFFICIAL_SOURCE_PACK_INVENTORY.cmd
echo.
pause
