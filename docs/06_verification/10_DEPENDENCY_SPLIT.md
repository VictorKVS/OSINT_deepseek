# Stage 06 / M2 — Dependency Split

**Date:** 2026-08-09  
**Status:** PASS for dependency separation; legacy cleanup continues.

## Problem

The root `requirements.txt` still described the older Ollama/GPU runtime experiment:

```text
ollama
colorama
psutil
gputil
```

That made a new engineer believe those packages were required by the current FATHER OSINT DEV core.

## Evidence before change

`TEST_REPORT_004` proved a clean checkout could:

- import `father_osint`;
- collect and pass all 17 tests;
- run `run_dev_osint.py`;
- run `run_dev_pipeline.py`;

without installing any Ollama/GPU/monitoring package.

Therefore the historical root dependency list was not an approved dependency contract for the current product.

## Decision

Dependencies are now separated by purpose:

```text
requirements.txt
    current FATHER OSINT runtime
    currently stdlib-only

requirements-dev.txt
    verification/test tooling
    pytest

requirements-legacy.txt
    historical Ollama/GPU prototype
    ollama / colorama / psutil / gputil
```

## WHY

Dependency files are architecture-facing contracts. Mixing experimental and current dependencies:

- hides the real product boundary;
- increases installation/security surface;
- makes legacy code look mandatory;
- causes future developers to solve irrelevant environment problems.

The split preserves historical reproducibility without forcing legacy dependencies onto the current DEV core.

## CI proof

The Stage 06 workflow was changed to install:

```text
python -m pip install -r requirements-dev.txt
```

The clean-checkout GitHub Actions run completed successfully after the split.

This proves the current test and runner path does not transitively require `requirements-legacy.txt`.

## Current gate

```text
Dependency split     PASS
Legacy dependencies PRESERVED, isolated
Current CI           PASS
Legacy deletion      NOT YET AUTHORIZED as a bulk action
```

## Next action

Proceed to the next M2 cleanup group: `core/` legacy package. Before deletion/archive, verify no approved current path imports it, preserve useful observability requirements in documentation, then remove/archive and rerun clean CI.
