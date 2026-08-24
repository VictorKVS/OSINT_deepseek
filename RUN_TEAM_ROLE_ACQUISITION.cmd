@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if "%~1"=="" (
  echo ============================================================
  echo FATHER Team Role - Telegram acquisition
  echo ============================================================
  echo Usage:
  echo   RUN_TEAM_ROLE_ACQUISITION.cmd PROGRAMMER
  echo   RUN_TEAM_ROLE_ACQUISITION.cmd SYSTEM_ANALYST
  echo   RUN_TEAM_ROLE_ACQUISITION.cmd LEGAL_COMPLIANCE
  echo   RUN_TEAM_ROLE_ACQUISITION.cmd ML_LLM_ENGINEER
  echo.
  echo Other role IDs are read from config\team_role_material_registry.json
  exit /b 2
)

set "ROLE=%~1"
shift

echo ============================================================
echo FATHER Team Role - Telegram acquisition
echo ============================================================
echo Role: %ROLE%
echo Shared gates: DPAPI -^> network -^> Telethon session -^> acquisition
echo Max search streams: 5
echo Max download streams: 5
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\run_team_role_acquisition.ps1" -Role "%ROLE%" %*
set "RC=%ERRORLEVEL%"

echo.
echo Exit code: %RC%
exit /b %RC%
