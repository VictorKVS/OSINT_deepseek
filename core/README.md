# Legacy Core

`core/` belongs to the original OSINT_deepseek prototype and predates the current FATHER requirements-first package.

Current files:
- `agent_tracker.py` — legacy agent tracking/monitoring logic.
- `logger.py` — legacy logging/resource telemetry support.

## Current decision

Status: **LEGACY / ARCHIVE / DELETE CANDIDATE AFTER CLEANUP GATE**.

The detailed review is recorded in:

- [`../docs/06_verification/05_LEGACY_CORE_AUDIT.md`](../docs/06_verification/05_LEGACY_CORE_AUDIT.md)

The important distinction is:

```text
old code                       future useful capability
----------------------------   --------------------------------
agent_tracker.py            →  execution traceability / audit
logger.py                   →  structured logs / host metrics
```

The code itself is not approved for migration into `father_osint`.

`agent_tracker.py` also contains persistence of intermediate agent "thoughts". That mechanism must **not** become the FATHER observability contract. Future tracing should store explicit actions, tool events, outputs, errors, timings and declared business rationale where required — not private model reasoning.

Do not import these modules into the new `father_osint` path merely to reuse code. First identify an approved requirement, design the contract, design tests, and only then implement an observability adapter.

Deletion of this directory is deferred until root/legacy callers are audited and a regression run proves current DEV behavior is unaffected.
