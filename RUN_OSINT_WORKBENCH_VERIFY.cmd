@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER OSINT Workbench Core MVP - verify and synthetic demo
echo ============================================================

python -m pip install -r requirements-dev.txt
if errorlevel 1 goto :fail
python -m pip install -r docs\osint-platform\validation\requirements.txt
if errorlevel 1 goto :fail

python -m pytest -q tests\test_osint_workbench_*.py
if errorlevel 1 goto :fail

python scripts\run_osint_workbench_demo.py --root data\osint-workbench-demo --force
if errorlevel 1 goto :fail

python scripts\validate_osint_workbench_demo.py --root data\osint-workbench-demo --case-id CASE-SYNTH-CORE-0001 --schemas docs\osint-platform\schemas
if errorlevel 1 goto :fail

python -m osint_workbench --root data\osint-workbench-demo verify-journal CASE-SYNTH-CORE-0001
if errorlevel 1 goto :fail

echo.
echo PASS - report:
echo data\osint-workbench-demo\cases\CASE-SYNTH-CORE-0001\reports\main_official_report_redacted.md
exit /b 0

:fail
echo.
echo FAIL - see output above.
exit /b 1
