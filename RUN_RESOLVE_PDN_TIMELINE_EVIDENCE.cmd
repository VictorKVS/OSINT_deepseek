@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - RESOLVE PDN TIMELINE EVIDENCE
echo OER -^> verified A0/A1 proof -^> confirmed/pending linkage
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\resolve_pdn_timeline_evidence.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: all timeline evidence requests are backed by verified A0/A1 proof records.
) else (
  echo PENDING: missing or incomplete official evidence remains; no legal date was invented.
)

exit /b %RC%
