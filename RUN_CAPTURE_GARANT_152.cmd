@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - CAPTURE GARANT 152-FZ
echo Browser clipboard -^> identity check -^> local UTF-8 capture
echo ============================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\capture_garant_clipboard.ps1" -DocumentId "DOC-RU-FZ-152-2006" -TimeoutSeconds 180
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo Capture complete.
  echo Next: RUN_PDN_GARANT_TIMELINE.cmd
) else (
  echo Capture failed or timed out. Review the message above.
)

pause
exit /b %RC%
