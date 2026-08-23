@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER P0.7 shadow delta execution proof
echo object delta plan -> non-destructive shadow invalidation -> delta D14 packet
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\prove_pdn_object_delta_plan.py
if errorlevel 1 goto :fail

%PYTHON_EXE% scripts\prove_pdn_delta_shadow_execution.py
if errorlevel 1 goto :fail

echo.
echo PASS: delta invalidation executed in shadow mode; canonical graph stayed immutable and D15 remains blocked.
exit /b 0

:fail
echo.
echo FAIL: shadow delta execution proof did not complete.
echo See reports\pdn_live\P0_7_DELTA_SHADOW_EXECUTION.json
exit /b 2
