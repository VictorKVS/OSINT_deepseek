@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - IMPORT GARANT 152-FZ ODT
echo GARANT download -^> identity -^> exact bytes -^> SHA256 -^> timeline
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\import_latest_garant_152_odt.py
if errorlevel 1 (
  echo.
  echo FAIL: no identity-valid 152-FZ ODT was imported from Downloads.
  pause
  exit /b 2
)

echo.
echo Running GARANT timeline extraction from the imported ODT...
%PYTHON_EXE% scripts\run_pdn_garant_timeline.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: GARANT 152-FZ ODT imported and timeline metadata processed.
) else (
  echo PARTIAL/FAIL: ODT identity passed, but timeline extraction needs inspection.
)

pause
exit /b %RC%
