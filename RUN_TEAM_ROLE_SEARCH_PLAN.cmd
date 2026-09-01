@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if "%~1"=="" (
  echo Usage: RUN_TEAM_ROLE_SEARCH_PLAN.cmd PROGRAMMER
  exit /b 2
)

set "ROLE=%~1"
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

echo ============================================================
echo FATHER Team Role - doctrine search plan
echo ============================================================
echo Role: %ROLE%
echo This command plans search only. It performs no Telegram/web collection.
echo.

%PY% scripts\plan_team_role_search.py --role "%ROLE%"
set "RC=%ERRORLEVEL%"

echo.
echo Exit code: %RC%
exit /b %RC%
