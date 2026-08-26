@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER Architect - Current Library Gap OSINT Discovery
 echo ============================================================
echo Step 1: scan Downloads/OTUS/local corpus for the current 15-gap list
echo Step 2: search Telegram only for books still missing locally
echo Commercial titles: discovery metadata only, no auto-download
echo Open/official titles: candidate review only
echo Search streams: 5
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\run_architect_book_osint_discovery.ps1" %*
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\architect_books\LATEST_ARCHITECT_BOOK_OSINT_DISCOVERY.json
echo Exit code: %RC%
exit /b %RC%
