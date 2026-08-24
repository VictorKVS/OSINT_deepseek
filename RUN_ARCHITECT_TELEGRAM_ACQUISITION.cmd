@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY="
if exist ".venv\Scripts\python.exe" (
  .venv\Scripts\python.exe -c "import telethon" >nul 2>&1
  if not errorlevel 1 set "PY=.venv\Scripts\python.exe"
)

if not defined PY (
  python -c "import telethon" >nul 2>&1
  if not errorlevel 1 set "PY=python"
)

if not defined PY (
  echo ============================================================
  echo FATHER Architect Telegram acquisition - dependency missing
  echo ============================================================
  echo Telethon is not installed in .venv or system Python.
  echo Install into the project venv with:
  echo   .venv\Scripts\python.exe -m pip install telethon
  echo.
  echo No Telegram search or download was attempted.
  exit /b 2
)

set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Architect - Telegram remaining material acquisition
echo ============================================================
echo Python: %PY%
echo Course root: G:\1\OTUS ^(or ARCHITECT_COURSE_ROOT override^)
echo Search streams: 5
echo Download streams: 5
echo Policy: accessible Telegram scope only; no auto-join/no bypass
echo.

%PY% scripts\run_architect_telegram_acquisition.py %*
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\architect_telegram\LATEST_ARCHITECT_TELEGRAM_RUN.json
echo Exit code: %RC%
exit /b %RC%
