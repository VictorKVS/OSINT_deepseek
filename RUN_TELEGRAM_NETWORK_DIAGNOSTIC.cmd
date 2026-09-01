@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER Telegram - Windows network path diagnostic
echo ============================================================
echo No Telegram credentials are read by this command.
echo No routes, VPNs, proxies or firewall settings are changed.
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\test_telegram_network_path.ps1" %*
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\architect_telegram\LATEST_TELEGRAM_NETWORK_DIAGNOSTIC.json
echo Exit code: %RC%
exit /b %RC%
