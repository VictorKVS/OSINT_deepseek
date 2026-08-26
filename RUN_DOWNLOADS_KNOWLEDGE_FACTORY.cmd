@echo off
setlocal
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
set "PYTHONPATH=%CD%;%PYTHONPATH%"

set "DOWNLOADS=%USERPROFILE%\Downloads"
set "MAX_ITEMS=2"
if not "%~1"=="" set "DOWNLOADS=%~1"
if not "%~2"=="" set "MAX_ITEMS=%~2"

echo ============================================================
echo FATHER - Downloads Knowledge Factory
 echo ============================================================
echo Source folder: %DOWNLOADS%
echo Source files are NEVER modified or deleted.
echo Unknown files go to local quarantine and are not sent to models.
echo Local corpus is Git-ignored.
echo First model pass: M5 terminology + M6 knowledge extraction.
echo Main analyst review is mandatory. KB auto-promotion is disabled.
echo.

"%PY%" scripts\intake_downloads_knowledge_factory.py --downloads "%DOWNLOADS%"
set "RC1=%ERRORLEVEL%"
if not "%RC1%"=="0" (
  echo [STOP] Downloads intake failed. RC=%RC1%
  exit /b %RC1%
)

echo.
echo [PASS] Intake ready. Discovering local models and planning work...
"%PY%" scripts\plan_local_model_semifabricates.py
set "RC2=%ERRORLEVEL%"
if not "%RC2%"=="0" (
  echo.
  echo [HOLD] No usable local model files were auto-discovered.
  echo Set FATHER_MODEL_ROOTS to your model directories and rerun.
  echo Plan: reports\knowledge_intake\LATEST_LOCAL_MODEL_ASSIGNMENTS.json
  exit /b %RC2%
)

echo.
echo [PASS] Model plan ready. Running a small semifinal batch: %MAX_ITEMS% work items.
"%PY%" scripts\run_local_semifabricate_batch.py --max-items %MAX_ITEMS% --models-per-stage 2
set "RC3=%ERRORLEVEL%"

echo.
echo Intake report: reports\knowledge_intake\LATEST_DOWNLOADS_INTAKE.json
echo Model plan:    reports\knowledge_intake\LATEST_LOCAL_MODEL_ASSIGNMENTS.json
echo Semifabricates: _LOCAL_DOWNLOADS_KB_INTAKE\semifabricates
echo Analyst queue: reports\knowledge_intake\LATEST_MAIN_ANALYST_SEMIFABRICATE_QUEUE.json
echo Exit code: %RC3%
exit /b %RC3%
