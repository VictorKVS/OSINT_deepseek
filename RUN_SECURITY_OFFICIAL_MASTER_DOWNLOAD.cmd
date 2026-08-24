@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Security - Official master document download
echo ============================================================
echo Mode: reuse-first, official-only, full deduplicated list
echo Workers: 5
echo Existing exact/A0 documents: reuse, no redownload
echo A2/reference copies: never treated as official truth
echo.

"%PY%" scripts\run_security_official_master_download.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\security_current_only\LATEST_MASTER_OFFICIAL_DOWNLOAD_RUN.json
echo Exit code: %RC%
exit /b %RC%
