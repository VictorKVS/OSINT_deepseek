@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Knowledge Factory - PDN AUTO D0-D14 PREP
echo A0 captures -^> D4/D5 -^> D6/D9 -^> D10/D12 -^> D13 -^> D14 packet
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

echo [1/10] Rebuild D4-D5 from the four verified official captures...
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
echo [2/10] Normalize 152-FZ article -^> point hierarchy...
%PYTHON_EXE% scripts\normalize_pdn_d4_d5_article_points.py
if errorlevel 1 goto :fail

echo.
echo [3/10] Enforce fail-closed D4-D5 quality gate...
%PYTHON_EXE% scripts\audit_pdn_d4_d5_structure.py
if errorlevel 1 goto :fail

echo.
echo [4/10] Extract D6-D9 review candidates with exact lineage...
%PYTHON_EXE% scripts\run_pdn_d6_d9.py
if errorlevel 1 goto :fail

echo.
echo [5/10] Enforce fail-closed D6-D9 candidate quality gate...
%PYTHON_EXE% scripts\audit_pdn_d6_d9.py
if errorlevel 1 goto :fail

echo.
echo [6/10] Build D10-D12 relations and conflict/overlap candidates...
%PYTHON_EXE% scripts\run_pdn_d10_d12.py
if errorlevel 1 goto :fail

echo.
echo [7/10] Enforce fail-closed D10-D12 relation quality gate...
%PYTHON_EXE% scripts\audit_pdn_d10_d12.py
if errorlevel 1 goto :fail

echo.
echo [8/10] Build D13 graph and D14 controlled review queue...
%PYTHON_EXE% scripts\run_pdn_d13_review_queue.py
if errorlevel 1 goto :fail

echo.
echo [9/10] Validate D13 graph and D14/D15 stop states...
%PYTHON_EXE% scripts\audit_pdn_d13.py
if errorlevel 1 goto :fail

echo.
echo [10/10] Prepare compact D14 rule-level expert review packet...
%PYTHON_EXE% scripts\prepare_pdn_d14_review.py
if errorlevel 1 goto :fail

echo.
echo ============================================================
echo PASS: PDN conveyor reached D14 expert-review preparation.
echo Open reports\pdn_live\D14_REVIEW_PACKET.md
echo D14 remains NEEDS_REVIEW; D15 autonomous promotion is blocked.
echo ============================================================
exit /b 0

:fail
echo.
echo ============================================================
echo HOLD: automatic conveyor stopped at a fail-closed gate.
echo Inspect the error above; later stages were not promoted.
echo ============================================================
exit /b 2
