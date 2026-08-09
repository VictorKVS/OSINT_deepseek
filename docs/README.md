# Documentation Packs

This directory is the project control plane. Implementation must follow the document chain rather than invent requirements in code.

```text
PROJECT_GOVERNANCE
        ↓
OSINT_AGENT_TZ_V1
        ↓
ARCHITECTURE_DEV_V1
        ↓
TEST_PLAN_V1 + TRACEABILITY_MATRIX
        ↓
IMPLEMENTATION
        ↓
TEST EVIDENCE
        ↓
KEEP / CHANGE / DELETE / DEFER
```

## Active documents

- `PROJECT_GOVERNANCE.md` — engineering lifecycle and gates.
- `OSINT_AGENT_TZ_V1.md` — current technical specification.
- `ARCHITECTURE_DEV_V1.md` — minimal DEV architecture.
- `TEST_PLAN_V1.md` — required order of verification.
- `TRACEABILITY_MATRIX.md` — requirements to code/tests mapping.
- `REPOSITORY_AUDIT_2026-08-09.md` — current file inventory/status.

## Research/history

- `DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md` — donor research, not an implementation approval.
- `FATHER_OSINT_AGENT_STANDARD_V0_1.md` — historical broad standard.
- `FATHER_OSINT_AGENT_STANDARD_V1.md` — simplified standard; subordinate to approved ТЗ.
- `OSINT_AGENT_MVP_V1.md` — earlier MVP notes; reconcile rather than silently overwrite.

A document can be useful without being an approved implementation contract. Status must remain visible.
