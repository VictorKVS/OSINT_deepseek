@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - DIFF GARANT 152-FZ EDITIONS
echo archived ODT -^> semantic dedupe -^> structural article diff
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\diff_garant_152_editions.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: semantic GARANT edition diffs generated.
) else (
  echo PARTIAL/FAIL: at least two semantic editions are required for structural diff.
)

pause
exit /b %RC%
