# Documentation Packs

This directory is the project control plane. Implementation must follow the document chain rather than invent requirements in code.

```text
PROJECT_GOVERNANCE
        ↓
OSINT_AGENT_TZ_V1
        ↓
REQUIREMENTS REVIEW
        ↓
03_architecture/  ← CURRENT STAGE
        ↓
ARCHITECTURE REVIEW GATE
        ↓
TEST_PLAN_V1 + TRACEABILITY_MATRIX
        ↓
IMPLEMENTATION PLAN
        ↓
IMPLEMENTATION
        ↓
TEST EVIDENCE
        ↓
KEEP / CHANGE / DELETE / DEFER
```

## Current project stage

**Stage 03 — Architecture + Business Analysis / OPEN.**

The current work is to prove what enters each stage, what leaves it, who owns the transition, why the component exists, which failure modes must be visible and which technical decisions are intentionally deferred.

Main pack: [03_architecture/README.md](03_architecture/README.md)

## Active documents

- `PROJECT_GOVERNANCE.md` — engineering lifecycle and gates.
- `OSINT_AGENT_TZ_V1.md` — current technical specification.
- `ARCHITECTURE_DEV_V1.md` — earlier minimal DEV architecture; now input to formal Stage 3 review.
- `03_architecture/01_BUSINESS_ANALYSIS.md` — actors, SIPOC, value stream, business boundaries and functional decomposition.
- `03_architecture/02_ARCHITECTURE_VIEWS.md` — system context, process, data, failure and DEV/PROD views.
- `03_architecture/03_ARCHITECTURE_REVIEW.md` — formal architecture gate, risks and unresolved decisions.
- `03_architecture/04_DECISION_REGISTER.md` — WHY and architecture decision register.
- `TEST_PLAN_V1.md` — required order of verification; execution follows Stage 3 PASS.
- `TRACEABILITY_MATRIX.md` — requirements to code/tests mapping; must be updated as part of Stage 3 exit.
- `REPOSITORY_AUDIT_2026-08-09.md` — current file inventory/status.

## Research/history

- `DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md` — donor research, not an implementation approval.
- `FATHER_OSINT_AGENT_STANDARD_V0_1.md` — historical broad standard.
- `FATHER_OSINT_AGENT_STANDARD_V1.md` — simplified standard; subordinate to approved ТЗ.
- `OSINT_AGENT_MVP_V1.md` — earlier MVP notes; reconcile rather than silently overwrite.

A document can be useful without being an approved implementation contract. Status must remain visible.
