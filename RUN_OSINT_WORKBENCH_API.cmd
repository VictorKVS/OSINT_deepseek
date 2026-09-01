@echo off
setlocal
cd /d "%~dp0"

if not exist "data\osint-workbench-demo\cases\CASE-SYNTH-CORE-0001\case.json" (
  python scripts\run_osint_workbench_demo.py --root data\osint-workbench-demo --force
  if errorlevel 1 exit /b 1
)

echo Open: http://127.0.0.1:8765/api/v1/cases
python -m osint_workbench --root data\osint-workbench-demo serve --host 127.0.0.1 --port 8765
