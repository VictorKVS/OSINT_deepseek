@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN D4-D5 STRUCTURE QUALITY
echo structure lineage -> parent integrity -> fail-closed D6 gate
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\audit_pdn_d4_d5_structure.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: D4-D5 structural quality gate is green; D6 may be considered next.
) else (
  echo HOLD: D4-D5 structure needs remediation before D6.
)

pause
exit /b %RC%
