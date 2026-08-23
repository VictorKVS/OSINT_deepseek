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
if not "%RC%"=="0" goto :fail

echo.
echo [GATE] Checking donor source identity against the FATHER golden 152-FZ identity...
%PYTHON_EXE% scripts\gate_152_prebuilt_db_source_identity.py
set "RC=%ERRORLEVEL%"
if "%RC%"=="3" goto :blocked
if not "%RC%"=="0" goto :fail

echo.
echo PASS: prebuilt local legal DB acquired/reused, 152-FZ compared, and source identity gate passed.
echo Subsequent runs reuse the local SQLite file and require no network.
exit /b 0

:blocked
echo.
echo BLOCKED: donor metadata/content source identity collision detected.
echo Prebuilt donor CONTENT is quarantined; only implementation/schema/search patterns may be reused.
echo See reports\pdn_live\GATE_152_PREBUILT_DB_SOURCE_IDENTITY.json
exit /b 3

:fail
echo.
echo FAIL: prebuilt DB benchmark or source identity gate did not complete.
echo See reports\pdn_live\BENCHMARK_152_PREBUILT_MCP_DB.json
exit /b 2
