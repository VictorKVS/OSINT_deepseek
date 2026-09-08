@echo off
setlocal
cd /d "%~dp0.."
python -m osint_factory demo --profile RU_ORG --root runtime\osint-factory-demo --workers 5
if errorlevel 1 exit /b %errorlevel%
echo.
echo Output: runtime\osint-factory-demo\cases\CASE-DEMO-RU_ORG
endlocal
