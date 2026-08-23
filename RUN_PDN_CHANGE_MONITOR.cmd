@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER P0.7 change monitoring / bounded invalidation proof
echo real unchanged evidence reuse + synthetic new-version fixture
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\prove_pdn_change_reuse.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: unchanged evidence was reused and a changed-version fixture produced bounded downstream invalidation.
) else (
  echo FAIL: P0.7 reuse/invalidation proof did not satisfy the acceptance contract.
  echo See reports\pdn_live\P0_7_CHANGE_REUSE_PROOF.json
)

exit /b %RC%
