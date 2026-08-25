@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Programmer - Review 40 MIN derived candidates
echo ============================================================
echo Inputs: local MIN_DERIVED_TASKS.json + GOLDEN_CASES_MIN.json
echo Gates: parent SHA + sources + HOLDOUT isolation + mutation quality + prompt contracts
echo Result: automated-pass candidates only; critic review still required
echo No derived task becomes training-ready here.
echo.

"%PY%" scripts\review_programmer_min_derived_candidates.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\programmer_training_gym\LATEST_PROGRAMMER_MIN_DERIVED_REVIEW.json
echo Reviewed: reports\programmer_training_gym\MIN_DERIVED_AUTOMATED_REVIEW.json
echo Exit code: %RC%
exit /b %RC%
