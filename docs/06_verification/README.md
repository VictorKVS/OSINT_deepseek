# Stage 06 — Verification and Repository Rationalization

**Status:** ACTIVE / STATIC AUDIT BEFORE FULL LOCAL RUN

This stage verifies that the repository structure matches the approved contracts before a full local checkout/runtime campaign.

No new product functionality is introduced here.

## Purpose

Before spending time on runtime debugging, decide which existing files are part of the approved FATHER OSINT DEV path and which are legacy, overlapping, experimental or deferred.

## Chain

```text
Approved ТЗ
  ↓
Architecture Review
  ↓
Acceptance Test Design
  ↓
Focused defect/fix evidence
  ↓
STATIC REPOSITORY AUDIT   ← CURRENT
  ↓
KEEP / CHANGE / DELETE / DEFER plan
  ↓
Full local checkout
  ↓
pytest + script/runtime runs
  ↓
TEST_REPORT_003
  ↓
cleanup / regression
```

## Rule

A file is not kept because it already exists. It is kept only when it has:

1. an approved requirement or explicit DEV-harness purpose;
2. a clear owner/responsibility;
3. a defined input/output boundary;
4. a verification obligation.

Deletion is also not performed during static review if runtime dependency is still uncertain. Such files are marked `DELETE CANDIDATE` until full-checkout verification.

## Documents

- [01_STATIC_REPOSITORY_AUDIT.md](01_STATIC_REPOSITORY_AUDIT.md) — file/group disposition and WHY.
- Future: `02_FULL_RUN_PLAN.md` — exact local checkout/run procedure after static audit closes.
- Future: `TEST_REPORT_003.md` — full-repository execution evidence.
