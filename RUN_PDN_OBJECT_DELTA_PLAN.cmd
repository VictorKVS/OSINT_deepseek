@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_logged_python_sequence.ps1 ^
  -RunId "PDN_OBJECT_DELTA_PLAN" ^
  -Title "FATHER P0.7 object-level delta invalidation plan" ^
  -PythonExe "%PYTHON_EXE%" ^
  -Scripts "scripts\prove_pdn_object_delta_plan.py" ^
  -SuccessMessage "object-level invalidation plan completed." ^
  -FailureMessage "object-level delta plan failed."

exit /b %ERRORLEVEL%
