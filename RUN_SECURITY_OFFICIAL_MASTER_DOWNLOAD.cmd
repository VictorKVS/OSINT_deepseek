@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security - Official master document download
echo ============================================================
echo Mode: reuse-first, official-only, full deduplicated list
echo Workers: 5
echo Existing exact/A0 documents: reuse, no redownload
echo A2/reference copies: never treated as official truth
echo Transport gate: READ ONLY diagnostic must PASS first
echo.

"%PY%" scripts\diagnose_security_official_transport.py
set "PRE_RC=%ERRORLEVEL%"
if not "%PRE_RC%"=="0" (
  echo.
  echo [STOP] Official transport diagnostic failed.
  echo Full 37-document acquisition was NOT started.
  echo Review: reports\security_current_only\LATEST_OFFICIAL_TRANSPORT_DIAGNOSTIC.json
  exit /b %PRE_RC%
)

echo.
echo [PASS] Transport diagnostic passed. Starting full master acquisition.
echo.

"%PY%" scripts\run_security_official_master_download.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json
echo Exit code: %RC%
exit /b %RC%
