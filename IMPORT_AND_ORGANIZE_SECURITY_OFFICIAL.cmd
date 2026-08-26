@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security - Import and organize manual official files
echo ============================================================
echo 1. Read files from _MANUAL_OFFICIAL_INBOX
echo 2. Calculate SHA-256 and normalize where possible
echo 3. Preserve legal review gates
echo 4. Move successfully imported originals into authority/domain folders
echo 5. Rebuild archive index
echo.

if not exist "_MANUAL_OFFICIAL_INBOX" mkdir "_MANUAL_OFFICIAL_INBOX"

"%PY%" scripts\import_security_official_manual_inbox.py
set "IMPORT_RC=%ERRORLEVEL%"
if not "%IMPORT_RC%"=="0" (
  echo.
  echo [STOP] Import step returned %IMPORT_RC%. Originals were NOT reorganized.
  exit /b %IMPORT_RC%
)

echo.
echo [PASS] Import completed. Organizing originals...
echo.

"%PY%" scripts\organize_security_manual_archive.py
set "ORG_RC=%ERRORLEVEL%"

echo.
echo Inbox:   _MANUAL_OFFICIAL_INBOX
echo Archive: _MANUAL_OFFICIAL_ARCHIVE
echo Index:   _MANUAL_OFFICIAL_ARCHIVE\INDEX.md
echo Import report:   reports\security_current_only\LATEST_MANUAL_OFFICIAL_IMPORT.json
echo Organize report: reports\security_current_only\LATEST_MANUAL_OFFICIAL_ORGANIZE.json
echo Exit code: %ORG_RC%
exit /b %ORG_RC%
