# Stage 04 — Test Execution Plan

**Status:** READY AFTER TEST FILE RECONCILIATION

## Execution principle

Run the smallest deterministic DEV suite first. Do not mix code fixes into the same step as evidence collection.

## Environment to record

- OS and version;
- Python version;
- dependency versions from the actual environment;
- repository commit SHA;
- command executed;
- date/time;
- whether any production credentials were present or required.

## Run order

```text
0. Static review of revised tests
   ↓
1. Contract/unit suite
   pytest -q
   ↓
2. Record PASS/FAIL exactly
   ↓
3. Classify each failure
   REQUIREMENT / ARCHITECTURE / TEST / IMPLEMENTATION / ENVIRONMENT
   ↓
4. Run simplified DEV scenario
   python scripts/run_dev_pipeline.py
   ↓
5. If review-pipeline runner is approved/available, run it separately
   ↓
6. Produce TEST_REPORT_001
   ↓
7. Only then authorize implementation corrections
```

## Expected first-run signals

- AC-02/provenance preservation should fail until storage semantics are corrected.
- Existing tests that still assert old duplicate semantics must be revised before they can count as acceptance evidence.
- No live Telegram transport is needed.
- No Knowledge Gate is needed.

## Failure classification

| Class | Meaning | Action |
|---|---|---|
| REQUIREMENT DEFECT | expected behavior is unclear/wrong | return to Stage 01/02 |
| ARCHITECTURE DEFECT | responsibility/flow cannot satisfy requirement cleanly | return to Stage 03 |
| TEST DEFECT | test does not represent approved contract | correct Stage 04 test |
| IMPLEMENTATION DEFECT | code violates approved test | Stage 05 change plan, then code fix |
| ENVIRONMENT DEFECT | failure is setup/dependency/runtime related | repair environment, rerun unchanged test |

## Exit from Stage 04 design

Test design is complete when every AC has a reviewed proof method, missing tests are specified, obsolete tests are marked for change, and execution can begin without guessing expected behavior.
