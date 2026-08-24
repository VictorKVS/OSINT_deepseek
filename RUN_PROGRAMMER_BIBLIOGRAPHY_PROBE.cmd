@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER Programmer - Telegram bibliography probe
echo ============================================================
echo Mode: PROBE ONLY - no downloads
echo Targets: config\programmer_bibliography_targets.json
echo Shared gates: DPAPI -^> network -^> Telethon session -^> probe
echo Max parallel streams: 5
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\run_team_role_acquisition.ps1" -Role PROGRAMMER -BibliographyProbe
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\team_role_telegram\LATEST_PROGRAMMER_BIBLIOGRAPHY_PROBE.json
echo Exit code: %RC%
exit /b %RC%
