@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

echo ============================================================
echo FATHER Security CURRENT_ONLY - 5 stream acquisition
echo ============================================================
echo Python: %PY%
echo.

%PY% scripts\run_security_current_only_5stream.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_5STREAM_RUN.json
echo Exit code: %RC%
exit /b %RC%
