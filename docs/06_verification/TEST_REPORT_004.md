# TEST REPORT 004 — Clean-checkout DEV baseline

**Date:** 2026-08-09  
**Stage:** 06 — Verification and Repository Rationalization  
**Environment:** GitHub-hosted clean checkout, Ubuntu 24.04, CPython 3.12.13  
**Verified commit:** `aecbdbcf2dcb5bb9ea47d0edc6c0c670dc032b2c`  
**Workflow:** `.github/workflows/dev-verification.yml`  
**Result:** **PASS for current DEV baseline**

## 1. Why this run was performed

Previous verification reconstructed the current DEV slice from GitHub files, but did not prove that the repository works after an actual clean checkout. Stage 06 therefore required a real filesystem checkout, pytest collection, full current test execution and both canonical DEV runners.

GitHub Actions was used as the clean Linux verification host. This is stronger evidence than the earlier reconstructed slice because `actions/checkout` fetched the repository into a fresh runner before execution.

## 2. Pre-run CI defect

Earlier workflow runs failed before any job was created. The workflow was reduced to a minimal valid Stage 06 form. After that change GitHub created and executed the `verify` job normally.

Classification: `ENV/CI`.

This was a verification-infrastructure defect, not evidence that `father_osint` failed.

## 3. First executable clean-checkout result

Once the workflow executed, these checks succeeded:

```text
checkout                     PASS
Python 3.12 setup            PASS
pytest install               PASS
import father_osint          PASS
pytest --collect-only        PASS
pytest                       15/15 PASS
```

The run then failed on:

```text
python scripts/run_dev_osint.py
```

with:

```text
ModuleNotFoundError: No module named 'father_osint'
```

### Classification

`IMPL — runner entrypoint/import-path defect`.

The package itself imported correctly from repository root. The failure appeared only when Python executed a file inside `scripts/`, because the script directory became the import base.

## 4. Test-first correction

Before changing the runner implementation, two executable acceptance checks were added in `tests/test_runner_entrypoints.py`:

- `run_dev_osint.py` must execute successfully from repository root;
- `run_dev_pipeline.py` must execute successfully from repository root.

This turned the discovered operational expectation into a permanent regression contract.

## 5. Minimal implementation corrections

### `scripts/run_dev_osint.py`

Added the repository root to `sys.path` before importing `father_osint`.

### `scripts/run_dev_pipeline.py`

Applied the same entrypoint correction.

Static review also found a stale output-field reference:

```text
cycle.review.reasons
```

but `SocratesReview` exposes:

```text
issues
questions
```

The runner was aligned with the current contract instead of adding an obsolete compatibility field to the domain model.

Classification: `IMPL — stale runner/API usage`.

## 6. Final clean-checkout evidence

GitHub Actions run for commit `aecbdbcf2dcb5bb9ea47d0edc6c0c670dc032b2c` completed successfully.

### Test collection

```text
17 tests collected
```

### Test execution

```text
17 passed
0 failed
0 errors
```

Covered suites include:

- architecture acceptance;
- storage/provenance and restart semantics;
- collector isolation;
- bounded review pipeline;
- OSINT MVP behavior;
- runner entrypoints;
- SimpleAnalyst;
- SimpleSocrates;
- Telegram collector boundary.

### DEV OSINT runner

```text
materials=2
duplicates_skipped=0
errors=0
stop_reason=collectors_exhausted
```

Result: **PASS**.

### Canonical DEV review pipeline runner

```text
pipeline_stop=review_passed
cycles=1
materials=2
package_stop=collectors_exhausted
socrates=PASS
```

Result: **PASS**.

## 7. Dependency evidence

The successful baseline required only:

```text
Python 3.12
pytest
```

The current acceptance path did **not** require:

- Ollama;
- `psutil` / GPU monitoring;
- Teleproto/Node Telegram bridge;
- Telegram credentials;
- Tor/proxy infrastructure;
- legacy PowerShell tooling;
- `services/llm-gateway`.

This confirms the intended separation between the current FATHER OSINT DEV core and legacy/experimental subsystems.

## 8. Non-blocking warning

GitHub reports that some third-party actions currently target deprecated Node 20 and are being forced to Node 24. This warning concerns action runtime compatibility, not the FATHER Python application. Track it as CI maintenance, not a product defect.

## 9. Gate decision

### Stage 06 current DEV baseline

**PASS on a clean Linux checkout.**

Proven chain:

```text
clean checkout
    ↓
father_osint import
    ↓
17 tests collect
    ↓
17/17 tests pass
    ↓
DEV OSINT runner passes
    ↓
DEV review pipeline runner passes
    ↓
legacy/experimental dependencies not required
```

### Still not claimed

This report does **not** claim:

- production readiness;
- live Telegram readiness;
- Windows-specific runtime validation;
- legacy cluster deletion completion;
- Knowledge Gate readiness;
- expert Analyst/Socrates quality.

## 10. Next authorized work

Proceed to **M2 — evidence-based repository cleanup/dependency rationalization**.

Before deleting any legacy asset:

```text
classify purpose
    ↓
search approved dependencies
    ↓
preserve useful requirement/experience
    ↓
archive or delete
    ↓
rerun clean-checkout CI
    ↓
record journal decision
```
