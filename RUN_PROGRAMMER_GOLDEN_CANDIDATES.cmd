@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Programmer - Golden Case candidate review
echo ============================================================
echo Scope: 8 MIN TRAIN reference solutions
echo Gates: source refs + HOLDOUT isolation + targeted regression tests
echo Result: candidate only; critic approval still required
echo.

"%PY%" scripts\review_programmer_golden_candidates.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\programmer_training_gym\LATEST_PROGRAMMER_GOLDEN_CANDIDATE_REVIEW.json
echo Candidates: reports\programmer_training_gym\GOLDEN_CASE_CANDIDATES.json
echo Exit code: %RC%
exit /b %RC%
