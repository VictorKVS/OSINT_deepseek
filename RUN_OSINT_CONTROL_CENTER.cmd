@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ============================================================
echo FATHER OSINT Control Center
echo ============================================================
echo Local UI: http://127.0.0.1:8765/
echo Browser will open automatically.
echo Close this window or press Ctrl+C to stop the server.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\run_osint_control_center.ps1"
exit /b %ERRORLEVEL%
