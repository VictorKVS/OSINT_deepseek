@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Reuse-First Benchmark - 152-FZ
echo RusLawOD single-row retrieval -^> FATHER local comparison
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\benchmark_152_reuse.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: 152-FZ external bootstrap row downloaded and compared.
) else (
  echo FAIL: benchmark did not complete or identity did not match.
)

exit /b %RC%
