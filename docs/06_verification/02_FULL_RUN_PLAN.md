# Stage 06 — Full Local Verification Run Plan

**Status:** READY FOR LOCAL CHECKOUT AFTER STATIC AUDIT  
**Purpose:** obtain repository-level execution evidence without mixing legacy and current DEV dependencies.

## 1. Why a local checkout is required

GitHub static inspection can prove structure, imports visible in source, contracts and documentation consistency. It cannot fully prove:

- package import behavior in a real filesystem;
- pytest collection across the whole repository;
- path handling and generated data directories;
- script execution from repository root;
- dependency/environment conflicts;
- PowerShell/Node runtime behavior.

Therefore this plan is the first point where a real checkout is required.

## 2. Environment capture

Before installing anything, record:

```text
OS
Python version
pip version
Git commit SHA
working tree status
Node version (only for deferred transport diagnostics; not required for DEV acceptance)
PowerShell version (legacy diagnostics only)
```

No Telegram credentials, Tor configuration or production secrets are required.

## 3. Dependency split

Current root `requirements.txt` contains:

```text
ollama
colorama
psutil
gputil
```

These belong primarily to earlier prototype/runtime experiments and are not required by the current pure-Python `father_osint` DEV core.

For current acceptance verification, start with the smallest environment:

```text
Python 3.12+
pytest
```

Do **not** install Ollama/GPU/monitoring dependencies merely to make legacy scripts happy during the first FATHER OSINT acceptance run.

If pytest collection proves that a current approved test unexpectedly imports a legacy dependency, classify it as an architecture/dependency defect before installing more packages.

## 4. Run sequence

### V-01 — repository snapshot

```bash
git status
git rev-parse HEAD
python --version
python -m pip --version
```

### V-02 — import smoke test

```bash
python -c "import father_osint; print('father_osint import OK')"
```

Expected: no optional/legacy/Node dependency is required.

### V-03 — pytest collection only

```bash
python -m pytest --collect-only -q
```

Purpose: detect import/collection failures before executing tests.

### V-04 — full current test suite

```bash
python -m pytest -q
```

Record every pass/fail/error exactly. Do not patch immediately.

### V-05 — focused current DEV runner

```bash
python scripts/run_dev_osint.py
```

Expected: fixture-only OSINT collection works without external credentials.

### V-06 — old pipeline runner diagnostic

```bash
python scripts/run_dev_pipeline.py
```

This is a **migration diagnostic**, not canonical acceptance. It currently imports `father_osint.pipeline.DevResearchPipeline` and is used to decide whether the older pipeline path can be removed after a canonical review-pipeline runner exists.

### V-07 — deferred/legacy isolation check

Do not execute live Telegram, Node bridge, Ollama, GPU or PowerShell stress paths as part of FATHER OSINT DEV acceptance. Instead verify they are not transitively required by V-02…V-06.

## 5. Failure classification

Every failure receives exactly one primary class before code changes:

- `REQ` — requirement defect;
- `ARCH` — architecture/contract defect;
- `TEST` — test defect;
- `IMPL` — implementation defect;
- `ENV` — environment/dependency defect;
- `LEGACY` — obsolete/old path interfering with current verification.

## 6. Evidence artifact

Create `docs/06_verification/TEST_REPORT_003.md` containing:

- commit SHA;
- environment;
- commands executed;
- pytest collection count;
- pass/fail/error count;
- runner results;
- failure classifications;
- file disposition changes justified by evidence;
- final gate decision.

## 7. Decisions after TEST_REPORT_003

Only after the report may we authorize, as separate reviewed changes:

1. migrate `run_dev_pipeline.py` to the canonical review pipeline;
2. delete `father_osint/pipeline.py` if no approved dependency remains;
3. separate current DEV requirements from legacy requirements;
4. archive or relocate legacy root/core/scripts/services assets;
5. update root navigation to present a single canonical DEV execution path.

## 8. Exit criterion

Stage 06 passes when a fresh local checkout can demonstrate:

```text
current contracts import
        ↓
all approved tests collect
        ↓
current DEV tests execute
        ↓
fixture OSINT runner executes
        ↓
legacy/experimental systems are not required
        ↓
repository cleanup decisions are evidence-backed
```
