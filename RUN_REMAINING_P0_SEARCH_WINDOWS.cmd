@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER - Remaining P0 role searches
echo ============================================================
echo Opening separate PowerShell windows for:
echo   SYSTEM_ANALYST
echo   LEGAL_COMPLIANCE
echo   ML_LLM_ENGINEER
echo.

start "FATHER SYSTEM_ANALYST" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%CD%'; .\RUN_TEAM_ROLE_ACQUISITION.cmd SYSTEM_ANALYST"
start "FATHER LEGAL_COMPLIANCE" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%CD%'; .\RUN_TEAM_ROLE_ACQUISITION.cmd LEGAL_COMPLIANCE"
start "FATHER ML_LLM_ENGINEER" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "Set-Location '%CD%'; .\RUN_TEAM_ROLE_ACQUISITION.cmd ML_LLM_ENGINEER"

echo Three operator windows started.
exit /b 0
