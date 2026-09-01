@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security - departmental shadow D4-D9 candidate build
echo ============================================================
echo Python: %PY%
echo Repo root on PYTHONPATH: %CD%
echo.

%PY% scripts\run_security_departmental_candidate_d4_d9.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_DEPARTMENTAL_D4_D9_CANDIDATE.json
echo Exit code: %RC%
exit /b %RC%
