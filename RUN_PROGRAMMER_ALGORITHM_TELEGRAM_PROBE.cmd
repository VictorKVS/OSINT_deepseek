@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Programmer - Algorithms bibliography Telegram probe
echo ============================================================
echo Scope: algorithms + data structures + analysis + Python/Java/C++/Go/Rust
 echo Mode: search/probe only, no book download
 echo Workers: up to 5
 echo.

"%PY%" scripts\probe_programmer_algorithm_bibliography_telegram.py --priority ALL
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\team_role_telegram\LATEST_PROGRAMMER_ALGORITHM_BIBLIOGRAPHY_PROBE.json
echo Exit code: %RC%
exit /b %RC%
