# Scripts

This directory contains both the approved DEV runners and historical pre-FATHER experiments. They must not be treated as one architecture.

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

## Legacy / archive candidates

The following scripts predate the current requirements-first FATHER package:

- `deepseek_safe.py` — local Ollama/resource experiment;
- `hello_agent.py` — early agent prototype;
- `monitor.py` — workstation hardware monitoring;
- `rtx3060_agent.py` — RTX 3060/model experiment;
- `smart_agent.py` — local Ollama chat agent with resource-based model switching.

Status: **ARCHIVE / DELETE CANDIDATES — NOT PART OF CURRENT DEV CONTRACT**.

Their useful ideas are documented in `docs/06_verification/06_LEGACY_RUNTIME_AUDIT.md`; code must not be copied into `father_osint` without a new approved requirement, architecture decision and acceptance test.

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
