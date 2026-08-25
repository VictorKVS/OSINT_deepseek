@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Programmer - Expand MIN Golden curriculum
echo ============================================================
echo Parents: 8 local GOLDEN_APPROVED cases
echo Output: 40 derived TRAIN candidates
echo Modes: implement / repair / tests / review / edge cases
echo HOLDOUT: never used as parent and never exported
echo Derived tasks are NOT training-ready yet.
echo.

"%PY%" scripts\build_programmer_min_expansion.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\programmer_training_gym\LATEST_PROGRAMMER_MIN_EXPANSION.json
echo Tasks: reports\programmer_training_gym\MIN_DERIVED_TASKS.json
echo Prompts: reports\programmer_training_gym\MIN_DERIVED_PROMPTS.jsonl
echo Exit code: %RC%
exit /b %RC%
