@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - APPLY PDN D14 REVIEW DECISIONS
echo human decisions -^> D14 VERIFIED -^> D15 promotion request only
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\apply_pdn_d14_decisions.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: D14 expert review is VERIFIED.
  echo D15 remains NOT_DONE and requires explicit approval.
) else (
  echo HOLD: D14 is incomplete, escalated, or invalid. D15 remains blocked.
)

pause
exit /b %RC%
