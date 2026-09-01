@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER donor audit - 100 laws / official source identity
echo local prebuilt SQLite -^> 5 workers -^> pravo.gov.ru verification
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\audit_prebuilt_db_100_source_identity.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo AUDIT COMPLETE: donor prebuilt content remains quarantined pending independent verification.
  echo See reports\pdn_live\AUDIT_PREBUILT_DB_100_SOURCE_IDENTITY.json
) else (
  echo FAIL: 100-law donor source identity audit did not complete.
)

exit /b %RC%
