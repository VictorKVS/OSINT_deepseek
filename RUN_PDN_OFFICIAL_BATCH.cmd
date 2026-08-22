@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - OFFICIAL PDn DOCUMENT BATCH
echo Registry -^> official download -^> SHA256 -^> D4 -^> D5 -^> review
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% --version
if errorlevel 1 (
  echo ERROR: Python was not found.
  pause
  exit /b 1
)

%PYTHON_EXE% scripts\run_pdn_official_batch.py
set "RC=%ERRORLEVEL%"

echo.
echo Review package:
echo data\knowledge_factory\pdn_official_batch\review\REVIEW.md
echo data\knowledge_factory\pdn_official_batch\review\batch_review_manifest.json
echo.
if "%RC%"=="0" (
  echo PASS: all enabled official entries completed without hard failures.
) else (
  echo PARTIAL/FAIL: some enabled entries require attention. Pending disabled source locators are listed separately and do not count as downloaded.
)

pause
exit /b %RC%
