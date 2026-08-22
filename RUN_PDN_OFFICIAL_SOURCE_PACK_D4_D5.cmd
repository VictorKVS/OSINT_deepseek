@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN OFFICIAL SOURCE PACK D4-D5
echo verified A0 captures -^> normal acquisition -^> structure -^> chunks
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\run_pdn_operator_import.py ^
  --inbox "data\operator_import\pdn_official_source_pack" ^
  --root "data\knowledge_factory\pdn_official_batch" ^
  --export-review "reports\pdn_live" ^
  --document-id "DOC-RU-FZ-152-2006" ^
  --document-id "DOC-RU-PP-1119-2012" ^
  --document-id "DOC-RU-FSTEC-21-2013" ^
  --document-id "DOC-RU-FSB-378-2014"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: verified official source pack reached D4-D5 through the normal conveyor.
) else (
  echo PARTIAL/FAIL: inspect acquisition or compiler status before D6.
)

pause
exit /b %RC%
