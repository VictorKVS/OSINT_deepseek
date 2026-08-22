@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN AUTO D0-D9
echo existing verified A0 captures -^> D4/D5 -^> quality -^> D6/D9 -^> quality
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

echo [1/5] Rebuild D4-D5 from the four verified official captures...
%PYTHON_EXE% scripts\run_pdn_operator_import.py ^
  --inbox "data\operator_import\pdn_official_source_pack" ^
  --root "data\knowledge_factory\pdn_official_batch" ^
  --export-review "reports\pdn_live" ^
  --document-id "DOC-RU-FZ-152-2006" ^
  --document-id "DOC-RU-PP-1119-2012" ^
  --document-id "DOC-RU-FSTEC-21-2013" ^
  --document-id "DOC-RU-FSB-378-2014"
if errorlevel 1 goto :fail

echo.
echo [2/5] Normalize 152-FZ article -^> point hierarchy...
%PYTHON_EXE% scripts\normalize_pdn_d4_d5_article_points.py
if errorlevel 1 goto :fail

echo.
echo [3/5] Enforce fail-closed D4-D5 quality gate...
%PYTHON_EXE% scripts\audit_pdn_d4_d5_structure.py
if errorlevel 1 goto :fail

echo.
echo [4/5] Extract D6-D9 review candidates with exact lineage...
%PYTHON_EXE% scripts\run_pdn_d6_d9.py
if errorlevel 1 goto :fail

echo.
echo [5/5] Enforce fail-closed D6-D9 candidate quality gate...
%PYTHON_EXE% scripts\audit_pdn_d6_d9.py
if errorlevel 1 goto :fail

echo.
echo ============================================================
echo PASS: PDN conveyor reached quality-checked D9 review candidates.
echo No autonomous KB promotion was performed.
echo ============================================================
exit /b 0

:fail
echo.
echo ============================================================
echo HOLD: automatic conveyor stopped at a fail-closed gate.
echo Inspect the error above; later stages were not promoted.
echo ============================================================
exit /b 2
