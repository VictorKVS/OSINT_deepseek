@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security - FSTEC official direct-PDF recovery
echo ============================================================
echo Scope: 5 FSTEC documents only
 echo Routes: verified Russian Gazette direct PDF artifacts
 echo Purpose: test alternate technical host without re-running all 37
 echo Strict TLS remains enabled. No -k / insecure mode.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\run_security_official_recovery_fstec.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_FSTEC_OFFICIAL_RECOVERY_RUN.json
echo Exit code: %RC%
exit /b %RC%
