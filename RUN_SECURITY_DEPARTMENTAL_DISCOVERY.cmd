@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

echo ============================================================
echo FATHER Security CURRENT_ONLY - departmental orders discovery
echo ============================================================
echo Python: %PY%
echo.

%PY% scripts\discover_security_departmental_orders.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_DEPARTMENTAL_DISCOVERY.json
echo Exit code: %RC%
exit /b %RC%
