@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Reuse-First Benchmark - 152-FZ
echo cold external acquisition once -^> warm local reuse thereafter
echo ============================================================
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

if exist ".runtime\benchmarks\152_fz\ruslawod_candidate.json" goto :warm

echo [COLD] No cached 152-FZ candidate found.
echo Running one resilient external retrieval and comparison...
%PYTHON_EXE% scripts\benchmark_152_reuse.py
if errorlevel 1 goto :fail

echo.
echo [WARM] External candidate is now cached locally.
echo Measuring normal repeated-use path without network...
%PYTHON_EXE% scripts\benchmark_152_warm_cache.py
if errorlevel 1 goto :fail
goto :pass

:warm
echo [WARM] Cached external 152-FZ candidate found.
echo Skipping network/provider retries and measuring local verification + compare only.
%PYTHON_EXE% scripts\benchmark_152_warm_cache.py
if errorlevel 1 goto :fail
goto :pass

:pass
echo.
echo PASS: 152-FZ reuse benchmark completed.
echo Cold acquisition is paid once; normal repeated use is local and network-independent.
exit /b 0

:fail
echo.
echo FAIL: benchmark did not complete or cached identity is invalid.
exit /b 2
