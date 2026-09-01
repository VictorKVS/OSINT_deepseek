@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_logged_python_sequence.ps1 ^
  -RunId "PDN_DUAL_PATH_D13_REBUILD" ^
  -Title "FATHER P0.7 dual-path FULL vs SELECTIVE D13 proof" ^
  -PythonExe "%PYTHON_EXE%" ^
  -Scripts "scripts\prove_pdn_dual_path_d13.py" ^
  -SuccessMessage "FULL and SELECTIVE D13 paths converged; bounded graph fragments were replaced and D15 remains blocked." ^
  -FailureMessage "selective D13 dual-path proof did not complete. See reports\pdn_live\P0_7_DUAL_PATH_D13.json"

exit /b %ERRORLEVEL%
