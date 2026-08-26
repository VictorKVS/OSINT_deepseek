@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Architect - Official/Open Source Acquisition
 echo ============================================================
echo Target: G:\1\OTUS\Библиотека\5. Открытые официальные источники
echo Sources: Google SRE, SRE Workbook, Building Secure and Reliable Systems,
echo          Cosmic Python, Obey the Testing Goat
echo Policy: official/author-published open sources only
echo Commercial full-text auto-download: DISABLED
echo.

"%PY%" scripts\run_architect_open_source_acquisition.py %*
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\architect_open_sources\LATEST_ARCHITECT_OPEN_SOURCE_ACQUISITION.json
echo Exit code: %RC%
exit /b %RC%
