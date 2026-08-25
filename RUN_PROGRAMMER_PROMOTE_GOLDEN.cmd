@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Programmer - Promote reviewed MIN Golden Cases
echo ============================================================
echo Requires: local GOLDEN_CASE_CANDIDATES.json with PASS regression
 echo Critic: explicit professor APPROVE decisions for 8 TRAIN tasks
 echo Output: 8 GOLDEN_APPROVED records + 8 SFT records if every gate passes
 echo HOLDOUT: never exported
 echo No model training is performed yet.
echo.

"%PY%" scripts\promote_programmer_min_golden_cases.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\programmer_training_gym\LATEST_PROGRAMMER_MIN_GOLDEN_PROMOTION.json
echo Golden: reports\programmer_training_gym\GOLDEN_CASES_MIN.json
echo SFT: reports\programmer_training_gym\SFT_MIN_GOLDEN.jsonl
echo Exit code: %RC%
exit /b %RC%
