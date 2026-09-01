@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - GARANT VERSION TIMELINE METADATA
echo GARANT timeline -^> amendment events -^> A0/A1 evidence requests
echo No GARANT full legal text is mirrored into Git.
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

if not exist "data\operator_import\garant_timeline" mkdir "data\operator_import\garant_timeline"

%PYTHON_EXE% scripts\run_pdn_garant_timeline.py
set "RC=%ERRORLEVEL%"

echo.
echo Operator input folder:
echo data\operator_import\garant_timeline\
echo.
echo Sanitized timeline outputs:
echo reports\pdn_timelines\PLAN.md
echo reports\pdn_timelines\timeline_metadata.jsonl
echo.
if "%RC%"=="0" (
  echo PASS: timeline metadata extraction completed without parser failures.
) else (
  echo PARTIAL/FAIL: inspect pending inputs or parser failures.
)

pause
exit /b %RC%
