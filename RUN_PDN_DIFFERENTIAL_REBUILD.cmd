@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_logged_python_sequence.ps1 ^
  -RunId "PDN_DIFFERENTIAL_REBUILD" ^
  -Title "FATHER P0.7 differential D6-D13 oracle proof" ^
  -PythonExe "%PYTHON_EXE%" ^
  -Scripts "scripts\prove_pdn_differential_d6_d13.py" ^
  -SuccessMessage "differential oracle matched selective object reuse projection; canonical graph stayed immutable and D15 remains blocked." ^
  -FailureMessage "differential D6-D13 oracle proof did not complete. See reports\pdn_live\P0_7_DIFFERENTIAL_D6_D13.json"

exit /b %ERRORLEVEL%
