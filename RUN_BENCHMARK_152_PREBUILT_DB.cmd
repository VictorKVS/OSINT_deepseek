@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Reuse-First Benchmark - prebuilt Russian Law MCP DB
echo one-time npm package acquisition -^> local SQLite -^> 152-FZ compare
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\benchmark_152_prebuilt_mcp_db.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: prebuilt local legal DB acquired/reused and 152-FZ compared.
  echo Subsequent runs reuse the local SQLite file and require no network.
) else (
  echo FAIL: prebuilt DB benchmark did not complete.
  echo See reports\pdn_live\BENCHMARK_152_PREBUILT_MCP_DB.json
)

exit /b %RC%
