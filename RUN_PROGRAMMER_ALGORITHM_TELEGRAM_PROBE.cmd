@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Programmer - Algorithms bibliography Telegram probe
echo ============================================================
echo Scope: algorithms + data structures + analysis + Python/Java/C++/Go/Rust
echo Mode: search/probe only, no book download
echo Workers: up to 5
echo Credentials: Windows env / DPAPI bootstrap + Telethon session check
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\run_team_role_acquisition.ps1" -Role PROGRAMMER -AlgorithmBibliographyProbe --priority ALL
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\team_role_telegram\LATEST_PROGRAMMER_ALGORITHM_BIBLIOGRAPHY_PROBE.json
echo Exit code: %RC%
exit /b %RC%
