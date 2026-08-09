# Stage 06 — Dependency Audit Before Cleanup

**Status:** REVIEWED / MIGRATION ALLOWED / DELETION NOT YET ALLOWED

## Purpose

Prove which files are actually depended on before any cleanup. The rule is:

```text
observe dependency
      ↓
classify owner/purpose
      ↓
migrate caller
      ↓
rerun tests
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

`father_osint/review_pipeline.py` is the current canonical bounded DEV orchestration because it includes both Analyst and Socrates and preserves the maximum-cycle stop condition.

## Duplicate pipeline finding

### `father_osint/pipeline.py`

Role: older partial orchestration.

Path:

```text
OSINT → Analyst → optional follow-up
```

It does not include Socrates. Its useful semantics are:

- stop when Analyst has no follow-up;
- hard maximum cycle limit;
- expose final analysis.

Those semantics are already covered by `DevReviewPipeline` plus acceptance tests.

**Decision:** `DELETE CANDIDATE`, but retain until callers are migrated and regression is rerun.

### `father_osint/review_pipeline.py`

Role: current complete DEV orchestration.

Path:

```text
OSINT → Analyst → Socrates → optional follow-up → bounded stop
```

**Decision:** `KEEP / CANONICAL DEV PIPELINE`.

## Known caller requiring migration

`scripts/run_dev_pipeline.py` imports `DevResearchPipeline` from `father_osint.pipeline`.

Current dependency:

```text
run_dev_pipeline.py
       ↓
father_osint.pipeline.DevResearchPipeline
```

Required dependency:

```text
run_dev_pipeline.py
       ↓
father_osint.review_pipeline.DevReviewPipeline
```

The script should also print Socrates review state so the executable DEV scenario matches the approved architecture.

**Decision:** `CHANGE / MIGRATE`.

## Test dependency requiring migration

`tests/test_dev_pipeline.py` currently tests `DevResearchPipeline` directly. Its two useful invariants are already required at the canonical layer:

1. complete evidence can stop in one cycle;
2. unresolved research is hard bounded.

Equivalent acceptance coverage exists in `tests/test_architecture_acceptance.py` for `DevReviewPipeline`.

**Decision:** `MIGRATE OR RETIRE AFTER REGRESSION`.

Do not delete this test in the same step as migration. First run the canonical tests and compare behavior.

## Legacy groups

### `core/`

Contains legacy `agent_tracker.py` and `logger.py`. The current `father_osint` DEV package does not declare them as part of its contract.

**Decision:** `LEGACY / ISOLATE`. No deletion before a full repository import/runtime scan.

### `services/llm-gateway/`

Independent experimental subsystem with its own API/core/simulation/enigma/sphinx structure.

**Decision:** `DEFER / OUTSIDE CURRENT OSINT DEV ACCEPTANCE BOUNDARY`.

### root scripts and PowerShell

Historical runtime/stress tooling remains outside the approved DEV path.

**Decision:** `LEGACY / DEFER` until local checkout confirms whether they are still intentionally used.

## Dependency gate result

### Allowed now

- migrate `scripts/run_dev_pipeline.py` to `DevReviewPipeline`;
- add/adjust tests for the canonical pipeline;
- rerun focused verification.

### Not allowed yet

- delete `father_osint/pipeline.py`;
- delete legacy `core/`;
- delete root PowerShell/runtime scripts;
- merge `services/llm-gateway` into current architecture.

## Exit condition

Deletion of `father_osint/pipeline.py` becomes allowed only when all are true:

- no current DEV script imports it;
- canonical `DevReviewPipeline` tests pass;
- focused DEV scenario passes;
- local/full-repository verification finds no remaining required caller.
