@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security - Official transport diagnostic READ ONLY
echo ============================================================
echo Probes: publication.pravo.gov.ru / government.ru / protect.gost.ru
echo Transports: urllib / curl / robust fallback
echo No source bytes are persisted. No KB state is changed.
echo.

"%PY%" scripts\diagnose_security_official_transport.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_OFFICIAL_TRANSPORT_DIAGNOSTIC.json
echo Exit code: %RC%
exit /b %RC%
