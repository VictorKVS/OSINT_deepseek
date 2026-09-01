@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security - Manual official document inbox
 echo ============================================================
echo Put manually downloaded official files into:
echo   _MANUAL_OFFICIAL_INBOX
echo.
echo File name must start with document id, for example:
echo   DOC-RU-FZ-187-2017.pdf
echo Optional provenance sidecar:
echo   DOC-RU-FZ-187-2017.source.txt
echo containing the exact browser source URL.
echo.
echo This importer calculates SHA-256, preserves exact bytes,
echo normalizes text where possible, and keeps legal promotion blocked.
echo.

if not exist "_MANUAL_OFFICIAL_INBOX" mkdir "_MANUAL_OFFICIAL_INBOX"

"%PY%" scripts\import_security_official_manual_inbox.py
set "RC=%ERRORLEVEL%"

echo.
echo Inbox:     _MANUAL_OFFICIAL_INBOX
echo Checklist: _MANUAL_OFFICIAL_INBOX\MANUAL_DOWNLOAD_CHECKLIST.tsv
echo Report:    reports\security_current_only\LATEST_MANUAL_OFFICIAL_IMPORT.json
echo Exit code: %RC%
exit /b %RC%
