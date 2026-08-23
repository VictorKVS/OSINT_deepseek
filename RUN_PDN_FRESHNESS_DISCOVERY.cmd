@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_logged_python_sequence.ps1 ^
  -RunId "PDN_FRESHNESS_DISCOVERY" ^
  -Title "FATHER P0.7 fail-safe PDn freshness discovery" ^
  -PythonExe "%PYTHON_EXE%" ^
  -Scripts "scripts\run_pdn_freshness_discovery.py" ^
  -SuccessMessage "freshness discovery behaved fail-safe; verified local serving remains independent from remote discovery and no false currentness was promoted." ^
  -FailureMessage "freshness discovery operational contract failed. See reports\pdn_live\P0_7_FRESHNESS_DISCOVERY.json"

exit /b %ERRORLEVEL%
