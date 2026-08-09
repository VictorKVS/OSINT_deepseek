# Scripts

This directory contains a mix of legacy diagnostics/runners and current DEV launch scripts.

## Current DEV path

- `run_dev_osint.py` — direct simplified OSINT fixture run.
- `run_dev_pipeline.py` — bounded DEV research pipeline runner.

## Legacy/support scripts

`deepseek_safe.py`, `hello_agent.py`, `monitor.py`, `rtx3060_agent.py` and other pre-FATHER scripts remain **LEGACY / PRESERVE** until reviewed.

## Rule

A script is not an architecture boundary. It may orchestrate approved components for testing/operation, but new business logic should not be hidden in launch scripts.

```text
approved test/use case
    ↓
runner script
    ↓
existing component API
    ↓
recorded result
```
