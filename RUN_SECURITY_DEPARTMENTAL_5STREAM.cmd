@echo off
setlocal
cd /d "%~dp0"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

echo ============================================================
echo FATHER Security CURRENT_ONLY - departmental 5 stream acquisition
echo ============================================================
echo Python: %PY%
echo Repo root on PYTHONPATH: %CD%
echo.

%PY% scripts\run_security_departmental_5stream.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_DEPARTMENTAL_5STREAM_RUN.json
echo Exit code: %RC%
exit /b %RC%
