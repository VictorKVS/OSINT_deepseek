# Lesson 03 — Delivery Strategy and Contract Model

Status: `DRAFT_FROM_CURRENT_EVIDENCE`

## Principle

The OSINT Agent must not jump from a technical demo directly to Production. Delivery is split into evidence-producing stages. Each stage has its own business purpose, uncertainty profile, acceptance evidence and appropriate commercial model.

## Recommended stage strategy

### Stage A — Technical PoC

Purpose:
- prove a narrow technical hypothesis;
- expose unknowns early;
- measure operational behavior on bounded lawful test sources;
- gather evidence for later ADRs.

Current OSINT example:
- TDLib PoC for Telegram transport behavior;
- optional GramJS comparison only if it still adds decision value.

Recommended commercial model for an external/customer PoC:
- `T&M` or `T&M with cap`.

Rationale:
- uncertainty is intentionally high;
- scope is experiment-oriented;
- the value is evidence, not a guaranteed production feature;
- forcing a fixed price before the unknowns are measured transfers estimation error into hidden risk or excessive contingency.

### Stage B — MVP

Purpose:
- prove that a bounded product path creates value for real users;
- expose product/operations issues that a technical PoC cannot reveal;
- validate a minimal set of production-like NFRs.

Candidate OSINT MVP must be selected from a product path already visible in the project registry, for example a bounded Telegram/Competitive Intelligence workflow. Selection remains an owner decision; this document does not promote an opportunity automatically.

Recommended commercial model:
- `T&M with cap`, milestone-based hybrid, or tightly scoped `FP` only after PoC evidence and a stable acceptance baseline exist.

### Stage C — Production

Purpose:
- operate the approved product capability with explicit SLO, security/privacy controls, support, monitoring, backup/recovery and change management.

Commercial model:
- may use `FP` for a stable implementation scope if requirements, responsibilities and acceptance are sufficiently baselined;
- operational support/continuous AI evolution usually needs a separate service/T&M/managed-service model because data, upstream APIs/models and security conditions change over time.

## Contract decision rule

Contract model follows uncertainty, not preference.

```text
High uncertainty / R&D
        ↓
T&M or capped T&M
        ↓
PoC evidence reduces uncertainty
        ↓
MVP with bounded scope
        ↓
Stable baseline + acceptance + change process
        ↓
FP may become reasonable for a defined delivery slice
```

## Fixed-price safeguards

If a later stage uses FP, the documentation package must explicitly contain:
- scope baseline and exclusions;
- acceptance criteria;
- customer dependencies/data-access obligations;
- external vendor/API assumptions;
- Change Request process;
- responsibility for delays caused by unavailable customer systems/data;
- treatment of new channels/source types/features;
- risk allocation and escalation path.

## Current project disposition

The current `OSINT_deepseek` work is best described as internal capability development with bounded PoC evidence on the active M5 path. No customer contract model is currently evidenced in the repository. Therefore any external commercial model remains `UNKNOWN / OWNER DECISION REQUIRED`.

## Traceability

- OTUS Lesson 03: staged value delivery, PoC/MVP/Prod and contract strategy.
- Existing project: `docs/PROJECT_ROADMAP_AND_CONTROL.md`.
- Existing project: `docs/PROJECT_EXECUTION_CONTROL.md`.
- Change recommendations: `docs/course_live_reproduction/IMPROVEMENT_BACKLOG.md`.
