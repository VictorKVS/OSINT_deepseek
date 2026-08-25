@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

if not exist "_MANUAL_OFFICIAL_INBOX" mkdir "_MANUAL_OFFICIAL_INBOX"
"%PY%" scripts\import_security_official_manual_inbox.py > nul 2>&1

echo Checklist: %CD%\_MANUAL_OFFICIAL_INBOX\MANUAL_DOWNLOAD_CHECKLIST.tsv
echo Save downloaded files as DOC-RU-....pdf/html/docx into this folder.
start "" "%CD%\_MANUAL_OFFICIAL_INBOX"
exit /b 0
