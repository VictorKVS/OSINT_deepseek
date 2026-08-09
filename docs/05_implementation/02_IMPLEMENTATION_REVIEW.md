# Stage 05 — Implementation Review Gate

**Status:** READY FOR REVIEW

## Scope under review

Only the minimal provenance-preserving storage fix described in `01_STORAGE_SEMANTICS_PLAN.md`.

## Gate checklist

- [x] Requirement defect is not being hidden by changing the test.
- [x] AC-02 explicitly distinguishes observation from payload.
- [x] Failure reproduced by focused test execution.
- [x] Root cause points to `MaterialStore.save_material()`.
- [x] Proposed change does not require a new database/framework.
- [x] Collector, Analyst and Socrates contracts remain unchanged.
- [x] PROD Telegram/Tor/transport work remains frozen.
- [x] Regression obligations are identified.

## Architecture consistency

```text
Collector
   ↓ Material observation
OSINTAgent
   ↓
MaterialStore
   ├── append observation metadata
   └── store/reuse raw payload blob by hash
   ↓
MaterialPackage
```

This preserves the Stage 03 responsibility split: storage optimizes bytes, but does not decide whether two source observations are epistemically equivalent.

## Decision

**APPROVE MINIMAL IMPLEMENTATION** provided the code change is limited to the planned storage semantics and is followed immediately by regression execution.

Any newly discovered requirement affecting models, collectors, databases or orchestration must stop implementation and return to the relevant earlier stage.
