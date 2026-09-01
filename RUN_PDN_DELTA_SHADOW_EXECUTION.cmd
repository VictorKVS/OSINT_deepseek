@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_logged_python_sequence.ps1 ^
  -RunId "PDN_DELTA_SHADOW_EXECUTION" ^
  -Title "FATHER P0.7 shadow delta execution proof" ^
  -PythonExe "%PYTHON_EXE%" ^
  -Scripts "scripts\prove_pdn_object_delta_plan.py;scripts\prove_pdn_delta_shadow_execution.py" ^
  -SuccessMessage "delta invalidation executed in shadow mode; canonical graph stayed immutable and D15 remains blocked." ^
  -FailureMessage "shadow delta execution proof did not complete. See reports\pdn_live\P0_7_DELTA_SHADOW_EXECUTION.json"

exit /b %ERRORLEVEL%
