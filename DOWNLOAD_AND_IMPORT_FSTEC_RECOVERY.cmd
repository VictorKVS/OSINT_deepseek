@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Security - Download and import FSTEC recovery bundle
echo ============================================================
echo Downloads the latest non-expired GitHub Actions recovery artifact.
echo Then verifies execution environment, SHA-256 and PDF magic before import.
echo Legal truth/currentness is NOT auto-promoted.
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\download_and_import_fstec_recovery.ps1"
set "RC=%ERRORLEVEL%"

echo.
echo Import report: reports\security_current_only\LATEST_FSTEC_RECOVERY_IMPORT.json
echo Exit code: %RC%
exit /b %RC%
