@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER P0.7 object-level delta invalidation plan
echo current real D13 graph + synthetic changed-document fixture
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\prove_pdn_object_delta_plan.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: object-level invalidation plan preserves unaffected graph objects.
) else (
  echo FAIL: object-level delta plan did not complete.
  echo See reports\pdn_live\P0_7_OBJECT_DELTA_PLAN.json
)

exit /b %RC%
