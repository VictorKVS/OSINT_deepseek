@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER resilient proof resolver - 152-FZ
echo verified local A0 evidence first; remote API is not serving-critical
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\resolve_152_proof_source.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: 152-FZ proof resolved from verified local A0 evidence without network dependency.
) else (
  echo FAIL: local proof evidence could not be verified.
  echo See reports\pdn_live\RESOLVE_152_PROOF_SOURCE.json
)

exit /b %RC%
