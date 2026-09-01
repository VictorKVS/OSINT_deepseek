@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER Programmer - bibliography next-action plan
echo ============================================================
echo Reads existing probe report. No Telegram search. No downloads.
echo Routes each target to official-open, rights/edition verification,
echo or official purchase/user-owned-copy path.
echo.

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

"%PY%" "scripts\build_programmer_bibliography_acquisition_plan.py"
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\team_role_telegram\LATEST_PROGRAMMER_BIBLIOGRAPHY_ACQUISITION_PLAN.json
echo Exit code: %RC%
exit /b %RC%
