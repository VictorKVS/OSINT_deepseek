# TEST_REPORT_001 — Stage 04 DEV Acceptance Run

**Date:** 2026-08-09  
**Stage:** 04 — Test Design / first execution evidence  
**Status:** PARTIAL EXECUTION / DEFECTS CONFIRMED

## 1. Purpose

Execute the newly aligned acceptance tests without changing production code and classify failures before any implementation fix.

## 2. Execution environment

A direct `git clone` from the runtime environment was attempted but outbound DNS/network access to `github.com` was unavailable. Therefore the run was performed against a local reconstruction of the current relevant repository files fetched through the connected GitHub tool.

This is valid as **behavioral evidence for the reviewed modules**, but it is not yet the final repository/CI acceptance run.

## 3. Scope executed

Executed focused Stage 04 tests covering:

- provenance-preserving duplicate payload behavior (AC-02);
- no-collector explicit failure behavior (AC-03);
- max-items bound (AC-04);
- collector failure isolation (AC-05);
- restart semantics with same payload from a new source (AT-04);
- full DEV review pipeline PASS path (AC-08/09);
- full DEV review pipeline hard cycle bound (AC-08).

## 4. Result

```text
7 tests executed
5 passed
2 failed
```

Failed tests:

1. `test_collects_distinct_source_observations_even_when_payload_matches`
2. `test_at04_restart_preserves_two_source_observations_for_same_payload`

## 5. Failure classification

### DEF-001 — provenance loss on identical payload

**Classification:** IMPLEMENTATION DEFECT / previously identified architecture mismatch  
**Affected component:** `father_osint/storage.py`  
**Requirement:** AC-02

Observed behavior:

```text
Source A -> payload X
Source B -> payload X

Current store result:
Source A retained
Source B discarded as duplicate
```

Expected behavior:

```text
Source A observation retained
Source B observation retained
raw payload X may be physically stored once
```

Root cause hypothesis supported by code inspection: `MaterialStore.save_material()` uses `content_hash` as a global material-level duplicate key and returns `False` when the payload hash is already known.

**Decision:** do not change code yet until implementation plan is approved.

### DEF-002 — restart repeats provenance loss

**Classification:** IMPLEMENTATION DEFECT / persistence semantics defect  
**Affected component:** `father_osint/storage.py`  
**Requirement:** AT-04 / AC-02

Observed behavior after process/store restart:

```text
Run 1: Source A -> payload X = retained
Restart
Run 2: Source B -> payload X = discarded
```

Expected behavior: second source observation must be retained while the raw blob is reused.

## 6. Passed behavior

The focused run supports the following behaviors:

- missing collectors produce explicit error state;
- `max_items` provides a hard collection bound;
- one collector exception does not erase material already collected by another collector;
- the full DEV ReviewPipeline can reach Socrates `PASS` on a complete fixture;
- unresolved research is bounded by `max_cycles`.

These remain **focused-run supported**, not final repository VERIFIED, until an exact checkout/CI run is recorded.

## 7. Gate decision

```text
Stage 04 test design: PASS for current scope
Implementation readiness: BLOCKED by DEF-001 / DEF-002
Production integration: NOT ALLOWED
```

## 8. Required next step

Prepare an implementation plan for storage semantics only. The plan must preserve the distinction between:

- source observation / Material record;
- raw content blob;
- exact duplicate observation (if later defined).

No database/framework change is justified by this defect. The smallest compliant fix should be designed first, then implemented, then regression-tested.
