@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if "%~1"=="" (
  echo Usage: RUN_TEAM_ROLE_COVERAGE.cmd PROGRAMMER
  exit /b 2
)

set "ROLE=%~1"
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

echo ============================================================
echo FATHER Team Role - Telegram topic coverage
echo ============================================================
echo Role: %ROLE%
echo Source: existing local acquisition report only
echo No Telegram connection or new download is performed.
echo.

%PY% scripts\analyze_team_role_telegram_coverage.py --role "%ROLE%"
set "RC=%ERRORLEVEL%"

echo.
echo Exit code: %RC%
exit /b %RC%
