@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

echo ============================================================
echo FATHER Security KB - Legal / Regulatory Analytics - 5 streams
 echo ============================================================
echo Input: existing data\security_current_only metadata + normalized text
 echo Network acquisition: OFF
 echo Source mutation: OFF
 echo KB auto-promotion: OFF
 echo.
echo S1 Identity / currentness / legal gate
 echo S2 Terms / definitions / scope / applicability
 echo S3 Requirements / obligations / prohibitions / deadlines
 echo S4 Relations / references / contradiction review pairs
 echo S5 Applicability / control mapping / main analyst queue
 echo.

"%PY%" scripts\run_security_legal_analytics_5stream.py
set "RC=%ERRORLEVEL%"

echo.
echo Aggregate: reports\security_legal_analytics\LATEST_5STREAM_LEGAL_ANALYTICS.json
echo Main queue: reports\security_legal_analytics\LATEST_MAIN_ANALYST_QUEUE.json
echo Streams:    reports\security_legal_analytics\S*.json
echo Exit code: %RC%
exit /b %RC%
