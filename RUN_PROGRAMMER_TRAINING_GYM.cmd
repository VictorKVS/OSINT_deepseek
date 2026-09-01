@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"

echo ============================================================
echo FATHER Programmer Training Gym - MIN Foundation
echo ============================================================
echo Task library: 12 MIN tasks (8 TRAIN / 4 HOLDOUT)
echo Mode: validate + build prompts + Golden Case queue
echo No model training is performed yet.
echo.

"%PY%" scripts\build_programmer_training_gym.py
set "RC=%ERRORLEVEL%"

echo.
echo Report: reports\programmer_training_gym\LATEST_PROGRAMMER_TRAINING_GYM_BUILD.json
echo Training prompts: reports\programmer_training_gym\TRAIN_PROMPTS.jsonl
echo Golden queue: reports\programmer_training_gym\GOLDEN_CASE_QUEUE.json
echo Exit code: %RC%
exit /b %RC%
