@echo off
setlocal
cd /d "%~dp0"
set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
echo ============================================================
echo FATHER - Global Shared Document Registry
echo ============================================================
echo Canonical documents once; role/domain applicability as bindings.
"%PY%" scripts\build_global_document_registry.py %*
set "RC=%ERRORLEVEL%"
echo.
echo Exit code: %RC%
exit /b %RC%
