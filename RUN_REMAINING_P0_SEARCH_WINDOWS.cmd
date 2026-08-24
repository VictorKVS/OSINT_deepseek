@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ============================================================
echo FATHER - Remaining P0 role searches
echo ============================================================
echo Opening separate PowerShell windows with isolated local sessions:
echo   SYSTEM_ANALYST
echo   LEGAL_COMPLIANCE
echo   ML_LLM_ENGINEER
echo.

set "SRC_SESSION=%CD%\legacy\telegram\reader_session.session"
if not exist "%SRC_SESSION%" (
  echo Shared authorized session is missing: %SRC_SESSION%
  exit /b 5
)

if not exist ".runtime\telegram\sessions" mkdir ".runtime\telegram\sessions"
copy /Y "%SRC_SESSION%" ".runtime\telegram\sessions\system_analyst.session" >nul
copy /Y "%SRC_SESSION%" ".runtime\telegram\sessions\legal_compliance.session" >nul
copy /Y "%SRC_SESSION%" ".runtime\telegram\sessions\ml_llm_engineer.session" >nul

start "FATHER SYSTEM_ANALYST" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$env:TELEGRAM_SESSION_PATH='%CD%\.runtime\telegram\sessions\system_analyst'; Set-Location '%CD%'; .\RUN_TEAM_ROLE_ACQUISITION.cmd SYSTEM_ANALYST"
start "FATHER LEGAL_COMPLIANCE" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$env:TELEGRAM_SESSION_PATH='%CD%\.runtime\telegram\sessions\legal_compliance'; Set-Location '%CD%'; .\RUN_TEAM_ROLE_ACQUISITION.cmd LEGAL_COMPLIANCE"
start "FATHER ML_LLM_ENGINEER" powershell.exe -NoExit -ExecutionPolicy Bypass -Command "$env:TELEGRAM_SESSION_PATH='%CD%\.runtime\telegram\sessions\ml_llm_engineer'; Set-Location '%CD%'; .\RUN_TEAM_ROLE_ACQUISITION.cmd ML_LLM_ENGINEER"

echo Three operator windows started with independent Telethon session databases.
exit /b 0
