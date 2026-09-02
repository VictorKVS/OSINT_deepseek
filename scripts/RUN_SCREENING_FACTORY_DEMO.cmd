@echo off
setlocal
cd /d "%~dp0\.."

echo ============================================================
echo FATHER OSINT - Screening Factory M3 offline demo
echo ============================================================

python -m pytest -q tests\test_screening_factory_m3.py
if errorlevel 1 exit /b 1

python scripts\run_screening_factory_demo.py
if errorlevel 1 exit /b 1

echo.
echo Output: runtime\screening-factory-demo
endlocal
