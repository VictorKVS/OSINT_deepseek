# Lesson 03 — Discovery Questions for OSINT Agent

Status: `DRAFT_FROM_CURRENT_EVIDENCE`

Purpose: remove uncertainty before promoting the current OSINT Agent from bounded DEV/PoC work toward MVP or Production.

## Source basis

This document applies the OTUS Lesson 03 requirement to formulate clarifying questions before committing to delivery stages. It uses the existing OSINT project evidence rather than inventing a new project.

## Questions requiring explicit answers

| ID | Question | Why it matters | Owner to answer | Current state |
|---|---|---|---|---|
| DQ-03-001 | Which concrete user/business outcome defines success for the first externally useful OSINT product path? | Current core is reusable research infrastructure; MVP cannot be defined only as “more collection”. | Product Owner / Business Owner | UNKNOWN |
| DQ-03-002 | Which source classes are mandatory for the first MVP: Telegram only, Telegram + web, or another bounded set? | Source scope changes legal, operational, cost and architecture requirements. | Product + Analyst + Legal/Security | PARTIAL |
| DQ-03-003 | What evidence freshness is required for the target use case: near-real-time, hourly, daily, on-demand? | Determines polling/update strategy, operational cost, rate-limit risk and SLO. | Product + Analyst | UNKNOWN |
| DQ-03-004 | What is the acceptable failure mode when one collector/source is unavailable? | DEV already isolates collector failures, but MVP/Prod need explicit user-visible service behavior. | Product + Operations + Analyst | PARTIAL |
| DQ-03-005 | Which data categories may be collected, stored and sent to external AI/model providers in Production? | Blocks legal/privacy/security design and hosting choice. | Legal/Compliance + Data Owner + Security | UNKNOWN |
| DQ-03-006 | What production workload must the system support: watched sources, events/day, retention volume, concurrent research tasks? | Needed for sizing, TCO, platform and performance NFRs. | Product + Operations | UNKNOWN |
| DQ-03-007 | What quality evidence is required before an analytical result may be used by a human analyst or later KB gate? | Needed to distinguish material collection success from evidence sufficiency/analysis quality. | Analyst + QA + Knowledge Gate owner | PARTIAL |
| DQ-03-008 | Is the first target deployment local/on-prem, private cloud, public cloud or hybrid? | Affects privacy, secrets, networking, model hosting, operations and cost. | Business Owner + Security + Operations | UNKNOWN |
| DQ-03-009 | Which commercial model is intended for an external customer pilot: T&M, fixed-price, capped T&M or internal investment? | Contract model changes scope/change/risk allocation. | Business Owner + PM + Finance | UNKNOWN |
| DQ-03-010 | What is the Production acceptance authority and who can accept residual operational/security risk? | Current engineering roles exist, but production authority must be explicit. | Business Owner / Risk Owner | UNKNOWN |

## Rule

An unanswered question remains `UNKNOWN`; it must not be silently converted into a technical assumption. If work must continue, create an explicit assumption with owner, validation trigger and downstream impact.

## Existing evidence already answering part of discovery

- OSINT Agent is a research-material supplier, not a truth engine.
- Research tasks and loops are bounded.
- Provenance must survive payload reuse.
- Collector failures must remain visible.
- Current DEV baseline is not Production readiness.
- Current active product capability is Telegram Radar, with TDLib PoC on the critical path.

Canonical evidence: repository `README.md`, `docs/OSINT_AGENT_TZ_V1.md`, `docs/PROJECT_ROADMAP_AND_CONTROL.md`, `docs/PROJECT_EXECUTION_CONTROL.md`.
