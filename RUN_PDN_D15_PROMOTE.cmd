@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - EXPLICIT PDN D15 PROMOTION
echo D14 VERIFIED -^> explicit operator approval -^> local KB_READY package
echo ============================================================
echo.
set /p "REVIEWER=Reviewer/System Owner name: "
if "%REVIEWER%"=="" (
  echo HOLD: reviewer identity is required.
  exit /b 2
)
set /p "CONFIRM=Type APPROVE_D15 to promote the reviewed corpus: "
if /I not "%CONFIRM%"=="APPROVE_D15" (
  echo HOLD: explicit D15 approval was not given.
  exit /b 2
)

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\promote_pdn_d15.py --approve --reviewer "%REVIEWER%"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: reviewed PDN corpus is D15 KB_READY locally.
) else (
  echo HOLD: D15 promotion gate rejected the request.
)
pause
exit /b %RC%
