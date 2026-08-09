# Tests

Tests are executable evidence for the approved DEV contract.

## Required chain

```text
ТЗ acceptance criterion
        ↓
architecture responsibility
        ↓
test specification
        ↓
execution on clean checkout
        ↓
PASS/FAIL evidence
        ↓
KEEP / CHANGE / DELETE decision
```

## Current suites

- `test_father_osint_mvp.py` — OSINT orchestration and provenance/storage behavior.
- `test_architecture_acceptance.py` — collector isolation, restart provenance, bounded full DEV path.
- `test_semantic_remediation.py` — cumulative follow-up evidence, payload reuse semantics, file-only SHA-256.
- `test_telegram_collector.py` — transport-neutral Telegram collector mapping.
- `test_simple_analyst.py` — deterministic DEV Analyst handoff/gap behavior.
- `test_simple_socrates.py` — deterministic DEV Socrates PASS/RESEARCH_MORE behavior.
- `test_dev_pipeline.py` — canonical bounded review pipeline.
- `test_runner_entrypoints.py` — both documented DEV entrypoints execute from repository root.

## Current evidence status

The suite is part of the active Stage 06 verification baseline and is executed by `.github/workflows/dev-verification.yml` on a clean GitHub-hosted Linux checkout.

Current semantic-remediation baseline: **21 tests collected / 21 passed**, followed by both canonical runner executions.

Passing DEV tests prove the current contract only. They do not prove live Telegram operation, expert-quality analysis, production security, Dark Web access, Knowledge Gate behavior, or autonomous KB publication.
