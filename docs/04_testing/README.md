# Stage 04 — Test Design

**Status:** ACTIVE / DESIGN BEFORE EXECUTION

Stage 04 starts only after Stage 03 architecture review has produced explicit component decisions and test obligations. This stage does not change production or DEV behavior. Its purpose is to convert approved requirements into executable evidence.

## Chain

```text
Approved ТЗ
    ↓
Architecture Review
    ↓
Acceptance Criteria
    ↓
Test Specification
    ↓
Existing Test Review
    ↓
Missing Test Design
    ↓
Test Execution
    ↓
Test Report
    ↓
Defect Classification
    ↓
KEEP / CHANGE / DELETE / DEFER
```

## Documents

- `01_ACCEPTANCE_TEST_SPEC.md` — AC-01…AC-10 expressed as test contracts.
- `02_EXISTING_TEST_REVIEW.md` — file-by-file review of current tests.
- `03_TEST_EXECUTION_PLAN.md` — exact run order and evidence to capture.
- `04_TEST_REPORT_TEMPLATE.md` — report structure for the first real run.

## Rule

A test is not accepted because it passes existing code. It is accepted only when it proves an approved requirement without embedding an obsolete architectural assumption.

No functional code changes are allowed during test design. If test design discovers a requirements or architecture defect, the issue returns to Stage 02/03 first.
