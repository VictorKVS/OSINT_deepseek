# Scripts

This directory now contains only the canonical executable DEV adapters for the current FATHER OSINT product.

## Current DEV path

```text
ResearchTask
    ↓
run_dev_osint.py / run_dev_pipeline.py
    ↓
father_osint components
    ↓
recorded DEV result
```

- `run_dev_osint.py` — **KEEP**; direct simplified OSINT fixture run.
- `run_dev_pipeline.py` — **KEEP / CANONICAL DEV RUNNER**; bounded `OSINT → Analyst → Socrates` scenario.

The earlier Ollama/GPU/workstation scripts were removed during Stage 06 M2 after their useful engineering lessons had been captured in `docs/06_verification/06_LEGACY_RUNTIME_AUDIT.md` and clean-checkout CI proved they were not required by the current product.

## Rule

A script is an executable adapter, not a business-logic boundary.

```text
approved requirement/use case
        ↓
approved component contract
        ↓
runner script
        ↓
execution result
```

New domain decisions, evidence rules, analysis logic or persistence semantics must not be hidden inside launch scripts.
