@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDn MVP / 152-FZ
echo Official source -^> exact original -^> SHA256 -^> D4 -^> D5
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% --version
if errorlevel 1 (
  echo.
  echo ERROR: Python was not found.
  pause
  exit /b 1
)

echo.
echo Running live acquisition from the configured official source...
%PYTHON_EXE% scripts\run_pdn_152fz_mvp.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: D0-D5 preliminary PDn package created.
  echo Output: data\knowledge_factory\pdn_mvp
) else (
  echo FAIL: runner returned exit code %RC%.
  echo Check the printed acquisition reason and network access to pravo.gov.ru.
)

pause
exit /b %RC%
