@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Semantic Audit - prebuilt Russian Law MCP DB / 152-FZ
echo version scope + per-article quality + true SQLite hot path
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\audit_152_prebuilt_db_semantics.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: semantic/version/hot-path audit completed.
  echo See reports\pdn_live\AUDIT_152_PREBUILT_DB_SEMANTICS.json
) else (
  echo FAIL: semantic audit did not complete.
)

exit /b %RC%
