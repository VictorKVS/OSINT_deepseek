@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER resilient proof resolver - PDn official source pack
echo four verified local A0 captures; no serving-time network dependency
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\resolve_pdn_proof_sources.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: all bounded PDn proof artifacts resolved from verified local official-publication captures.
) else (
  echo FAIL: one or more PDn proof artifacts could not be verified.
  echo See reports\pdn_live\RESOLVE_PDN_PROOF_SOURCES.json
)

exit /b %RC%
