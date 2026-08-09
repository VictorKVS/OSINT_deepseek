# Stage 06 — Dependency Audit Before Cleanup

**Status:** DUPLICATE PIPELINE CLEANUP COMPLETED / LEGACY CLEANUP STILL FROZEN

## Purpose

Prove which files are actually depended on before cleanup. The rule is:

```text
observe dependency
      ↓
classify owner/purpose
      ↓
migrate caller
      ↓
rerun tests
      ↓
scan repository
      ↓
only then delete obsolete implementation
```

No file is deleted because it merely looks old.

## Canonical DEV path

```text
ResearchTask
    ↓
OSINTAgent
    ↓
MaterialPackage
    ↓
SimpleAnalyst
    ↓
SimpleSocrates
    ↓
DevReviewPipeline
    ↓
PASS / follow-up / max_cycles
```

`father_osint/review_pipeline.py` is the canonical bounded DEV orchestration because it includes Analyst and Socrates and preserves the maximum-cycle stop condition.

## Duplicate pipeline resolution

### Removed: `father_osint/pipeline.py`

The old implementation provided only:

```text
OSINT → Analyst → optional follow-up
```

Useful semantics from it were retained in the canonical path:

- bounded cycle count;
- stop when no follow-up is required;
- access to the final cycle state.

Before deletion:

1. `scripts/run_dev_pipeline.py` was migrated to `DevReviewPipeline`;
2. `tests/test_dev_pipeline.py` was migrated to the canonical review pipeline;
3. architecture acceptance tests already covered bounded review behavior;
4. focused DEV verification passed on the reconstructed current DEV slice;
5. repository code search after migration returned no remaining `DevResearchPipeline` references;
6. the recursive repository tree was inspected before deletion.

**Decision:** `DELETE COMPLETED`.

This is the first cleanup executed through the full FATHER chain rather than by visual judgement.

## Canonical files after cleanup

### `father_osint/review_pipeline.py`

**Decision:** `KEEP / CANONICAL DEV PIPELINE`.

### `scripts/run_dev_pipeline.py`

**Decision:** `KEEP / CANONICAL DEV EXECUTABLE SCENARIO`.

It now executes:

```text
OSINT → Analyst → Socrates
```

and reports the review state.

### `tests/test_dev_pipeline.py`

**Decision:** `KEEP` for now.

It retains two explicit regression invariants:

1. complete evidence can stop in one cycle;
2. unresolved research is hard bounded.

Overlap with architecture acceptance tests may be reconsidered later, but duplication of test intent is not currently harmful enough to justify immediate deletion.

## Legacy groups — still frozen

### `core/`

Contains legacy `agent_tracker.py` and `logger.py`. The current `father_osint` DEV package does not declare them as part of its contract.

**Decision:** `LEGACY / ISOLATE`.

No deletion until their callers and historical purpose are mapped.

### `services/llm-gateway/`

Independent experimental subsystem with its own API/core/simulation/enigma/sphinx structure.

**Decision:** `DEFER / OUTSIDE CURRENT OSINT DEV ACCEPTANCE BOUNDARY`.

It must not be merged into the current OSINT architecture merely because it already exists in the repository.

### root scripts and PowerShell

Historical runtime/stress tooling remains outside the approved DEV path.

**Decision:** `LEGACY / DEFER` until its dependencies and intended ownership are audited.

### Telegram live transport / bridge

Experimental transport remains outside the simplified DEV execution boundary.

**Decision:** `DEFER`.

## Cleanup evidence chain

```text
Architecture decision
        ↓
Tests designed
        ↓
15/15 focused DEV tests passed
        ↓
Caller migration
        ↓
Repository reference scan
        ↓
Old pipeline deleted
        ↓
Next: legacy dependency mapping
```

## Next gate

The next cleanup target is **not automatically another deletion**.

Stage 06 now moves to legacy ownership/dependency classification:

```text
core/
root runtime scripts
PowerShell diagnostics
services/llm-gateway/
Telegram experimental transport
```

For every group we must answer:

- What business/engineering purpose did it serve?
- Is that purpose still required by the approved OSINT scope?
- Who calls it?
- Does it contain reusable knowledge even if the implementation is obsolete?
- Should it be KEEP, ARCHIVE, DEFER, MIGRATE, or DELETE?

Only after those answers may another destructive change be authorized.
