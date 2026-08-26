@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER - Windows Downloads Knowledge Intake
echo ============================================================
echo Scans %%USERPROFILE%%\Downloads recursively.
echo Originals are NEVER moved or deleted.
echo Copies are stored under _LOCAL_DOWNLOADS_KB_INTAKE.
echo SHA-256, text extraction, classification and deterministic
echo semifabricates are generated before local-model review.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\intake_windows_downloads.py
set "RC=%ERRORLEVEL%"

echo.
echo Summary: reports\downloads_intake\LATEST_DOWNLOADS_KB_INTAKE.json
echo Local inventory: _LOCAL_DOWNLOADS_KB_INTAKE\INVENTORY.json
echo Model queue:     _LOCAL_DOWNLOADS_KB_INTAKE\model_queue\TASKS.jsonl
echo Catalog refs:    _LOCAL_DOWNLOADS_KB_INTAKE\CATALOG_REFERENCES.json
echo Exit code: %RC%
exit /b %RC%
