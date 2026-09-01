@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

if "%~1"=="" (
  echo Usage: IMPORT_FSTEC_RECOVERY_BUNDLE.cmd ^<path-to-fstec-official-recovery.zip^>
  exit /b 2
)

echo ============================================================
echo FATHER Security - Import FSTEC recovery bundle
 echo ============================================================
echo Verifies bundle report, execution environment, SHA-256 and PDF magic.
echo Legal truth/currentness is NOT auto-promoted.
echo.

"%PY%" scripts\import_fstec_recovery_bundle.py "%~1"
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_FSTEC_RECOVERY_IMPORT.json
echo Exit code: %RC%
exit /b %RC%
