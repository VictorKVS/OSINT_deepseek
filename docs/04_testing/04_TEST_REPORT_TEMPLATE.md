# TEST REPORT TEMPLATE

**Report ID:** TEST_REPORT_XXX  
**Stage:** 04 / Execution Evidence  
**Repository commit:** `<sha>`  
**Date/time:** `<timestamp>`  
**Environment:** `<OS / Python / dependencies>`

## 1. Scope

What requirements and tests were executed in this run.

## 2. Commands

```text
<exact commands>
```

## 3. Summary

| Metric | Value |
|---|---|
| Tests collected | |
| Passed | |
| Failed | |
| Skipped | |
| Errors | |

## 4. Acceptance evidence

| AC | Test/evidence | Result | Notes |
|---|---|---|---|
| AC-01 | | | |
| AC-02 | | | |
| AC-03 | | | |
| AC-04 | | | |
| AC-05 | | | |
| AC-06 | | | |
| AC-07 | | | |
| AC-08 | | | |
| AC-09 | | | |
| AC-10 | | | |

## 5. Failures

For every failure record:

```text
Failure ID
Requirement / AC
Observed behavior
Expected behavior
Reproduction
Evidence/log
Classification:
  REQUIREMENT DEFECT
  ARCHITECTURE DEFECT
  TEST DEFECT
  IMPLEMENTATION DEFECT
  ENVIRONMENT DEFECT
Severity
Recommended next gate
```

## 6. Architecture consequences

List any component whose Stage 03 status changes because of test evidence.

## 7. Decision

```text
TEST GATE:
PASS / CONDITIONAL PASS / FAIL

Development authorization:
YES / NO / LIMITED TO LISTED DEFECTS
```

No failure is silently fixed before it is recorded in this report.
