@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo FATHER Reuse-First Benchmark - 152-FZ
echo RusLawOD single-law lookup -^> resilient provider fallback -^> FATHER compare
echo ============================================================
echo.
echo NOTE: the benchmark does NOT download the full RusLawOD corpus.
echo If Hugging Face Dataset Server returns 5xx, an isolated DuckDB fallback
echo queries remote Parquet files with filter pushdown and reports setup time separately.
echo.

set "PYTHON_EXE="
if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
if not defined PYTHON_EXE if exist "venv\Scripts\python.exe" set "PYTHON_EXE=venv\Scripts\python.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

%PYTHON_EXE% scripts\benchmark_152_reuse.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo PASS: 152-FZ external bootstrap text retrieved and compared.
) else (
  echo FAIL: all retrieval providers failed or document identity did not match.
  echo See reports\pdn_live\BENCHMARK_152_REUSE.json for provider evidence.
)

exit /b %RC%
