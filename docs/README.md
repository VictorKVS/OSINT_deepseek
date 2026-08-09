# Documentation Packs

This directory is the project control plane. Implementation must follow the document chain rather than invent requirements in code.

```text
PROJECT_GOVERNANCE
        ↓
OSINT_AGENT_TZ_V1
        ↓
REQUIREMENTS REVIEW
        ↓
03_architecture/
        ↓
ARCHITECTURE REVIEW GATE
        ↓
04_testing/  ← CURRENT STAGE
        ↓
TEST EXECUTION + TEST REPORT
        ↓
IMPLEMENTATION PLAN
        ↓
IMPLEMENTATION
        ↓
REGRESSION / ACCEPTANCE
        ↓
KEEP / CHANGE / DELETE / DEFER
```

## Current project stage

**Stage 04 — Test Design / ACTIVE.**

Stage 03 produced a conditional pass to test design. Functional code remains frozen while acceptance criteria are converted into explicit test oracles, current tests are reviewed, missing tests are specified, and the first execution plan is prepared.

Main pack: [04_testing/README.md](04_testing/README.md)

## Active documents

- `PROJECT_GOVERNANCE.md` — engineering lifecycle and gates.
- `OSINT_AGENT_TZ_V1.md` — current technical specification and acceptance criteria.
- `03_architecture/` — business analysis, architecture views, architecture review and decision register.
- `04_testing/01_ACCEPTANCE_TEST_SPEC.md` — observable AC-01…AC-10 contracts and architecture-contract tests.
- `04_testing/02_EXISTING_TEST_REVIEW.md` — KEEP / CHANGE / MIGRATE decisions for current tests.
- `04_testing/03_TEST_EXECUTION_PLAN.md` — exact first-run order and failure classification.
- `04_testing/04_TEST_REPORT_TEMPLATE.md` — required evidence format for actual runs.
- `TEST_PLAN_V1.md` — project-level verification strategy.
- `TRACEABILITY_MATRIX.md` — requirement → architecture → test → code → evidence map.
- `REPOSITORY_AUDIT_2026-08-09.md` — current file inventory/status.

## Research/history

- `DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md` — donor research, not an implementation approval.
- `FATHER_OSINT_AGENT_STANDARD_V0_1.md` — historical broad standard.
- `FATHER_OSINT_AGENT_STANDARD_V1.md` — simplified standard; subordinate to approved ТЗ.
- `OSINT_AGENT_MVP_V1.md` — earlier MVP notes; reconcile rather than silently overwrite.

A document can be useful without being an approved implementation contract. Status must remain visible.
