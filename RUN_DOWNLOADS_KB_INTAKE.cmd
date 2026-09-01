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
echo Catalogs are converted into a live coverage/missing list.
echo KB auto-promotion is disabled.
echo.

"%PY%" scripts\intake_windows_downloads.py
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" goto :done

echo.
echo [PASS] Intake complete. Building live coverage gaps...
echo.
"%PY%" scripts\build_downloads_coverage_gaps.py
set "RC=%ERRORLEVEL%"

:done
echo.
echo Summary:       reports\downloads_intake\LATEST_DOWNLOADS_KB_INTAKE.json
echo Coverage:      reports\downloads_intake\LATEST_DOWNLOADS_COVERAGE_GAPS.json
echo Local inventory: _LOCAL_DOWNLOADS_KB_INTAKE\INVENTORY.json
echo Model queue:     _LOCAL_DOWNLOADS_KB_INTAKE\model_queue\TASKS.jsonl
echo Catalog refs:    _LOCAL_DOWNLOADS_KB_INTAKE\CATALOG_REFERENCES.json
echo Missing list:    _LOCAL_DOWNLOADS_KB_INTAKE\COVERAGE_GAPS.tsv
echo Exit code: %RC%
exit /b %RC%
