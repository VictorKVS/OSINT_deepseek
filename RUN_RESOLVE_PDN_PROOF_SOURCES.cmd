@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_logged_python_sequence.ps1 ^
  -RunId "RESOLVE_PDN_PROOF_SOURCES" ^
  -Title "FATHER resilient proof resolver - PDn official source pack" ^
  -PythonExe "%PYTHON_EXE%" ^
  -Scripts "scripts\resolve_pdn_proof_sources.py" ^
  -SuccessMessage "all bounded PDn proof artifacts resolved from verified local official-publication captures." ^
  -FailureMessage "one or more PDn proof artifacts could not be verified."

exit /b %ERRORLEVEL%
