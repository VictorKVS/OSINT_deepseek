@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER Architect - Telegram remaining material acquisition
echo ============================================================
echo Course root: G:\1\OTUS ^(or ARCHITECT_COURSE_ROOT override^)
echo Search streams: 5
echo Download streams: 5
echo Policy: accessible Telegram scope only; no auto-join/no bypass
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\run_architect_telegram_acquisition.ps1" %*
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\architect_telegram\LATEST_ARCHITECT_TELEGRAM_RUN.json
echo Exit code: %RC%
exit /b %RC%
