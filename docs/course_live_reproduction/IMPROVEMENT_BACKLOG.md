# OSINT Agent — Improvement Backlog / Что стоит поменять или доработать

Status: `ACTIVE / SEPARATE FROM AS-IS DOCUMENTATION`

Purpose: keep improvement recommendations separate from the factual description of the current project. A recommendation does **not** become project truth, requirement or implementation work until its accountable owner accepts it and the appropriate change/architecture gate is passed.

## Core rule

```text
AS-IS / FACT / EVIDENCE
        ≠
TO-BE / RECOMMENDATION
```

## Status vocabulary

`PROPOSED` · `OWNER_REVIEW` · `ACCEPTED` · `IN_PROGRESS` · `DONE` · `REJECTED` · `DEFERRED` · `SUPERSEDED`

## Priority vocabulary

- `P0` — blocks a material gate, legal/security correctness or creates false confidence.
- `P1` — materially improves architecture, requirements, delivery predictability or verification.
- `P2` — improves maintainability, usability, documentation or future evolution.
- `P3` — optional enhancement/polish.

## Improvement register

| ID | Priority | What to change / improve | Why / evidence | Owner | Target | Status |
|---|---|---|---|---|---|---|
| IMP-001 | P1 | Add explicit product/business KPI baseline | technical acceptance exists, product value baseline is incomplete | Product / Business Owner | 1–3 | OWNER_REVIEW |
| IMP-002 | P0 | Formalize Production legal/compliance applicability and named authority | live OSINT/data processing cannot rely on assumed applicability | Legal + Security | 3–14 | PROPOSED |
| IMP-003 | P0 | Create Production data inventory/classification/retention/external-processing rules | provenance exists, production data lifecycle is incomplete | Data Owner + Security | 12–14 | PROPOSED |
| IMP-004 | P1 | Normalize architecture into C4/HLD/LLD without overlapping truths | Lesson 4/5 created course views but existing views still coexist | Architect / System Engineer | 4–10 | IN_PROGRESS |
| IMP-005 | P1 | Keep architecture drivers separate from technology candidates | prevents technology-first design | Architect + Requirements | 4–9 | IN_PROGRESS |
| IMP-006 | P1 | Add measurable Production NFR baselines and verification | current DEV qualities are stronger than Production SLO baseline | Requirements + QA + Ops | 2–16 | IN_PROGRESS |
| IMP-007 | P1 | Build evidence-backed Estimate v0 for active roadmap | WBS exists; numeric estimates still need owner inputs | PM + Leads | 2–3 / planning | IN_PROGRESS |
| IMP-008 | P1 | Cross-link project/security/delivery risks without collapsing meanings | several risk registers must not diverge | PM + Security + KGA | 2–10 | IN_PROGRESS |
| IMP-009 | P1 | Instantiate formal Change Request on next material baseline change | change model now documented but not yet exercised in course package | PM / Change Manager | next change | ACCEPTED |
| IMP-010 | P1 | Maintain TCO scenarios for API/cloud-GPU/on-prem/hybrid | Lesson 9 model exists; measured workload/current quotes still missing | Finance + Architect + Ops | 2–9 / Production ADR | IN_PROGRESS |
| IMP-011 | P1 | Establish versioned Golden/Evaluation set ownership | RAG/LLM choices need common quality evidence | QA + Product + SME | 6–13 | PROPOSED |
| IMP-012 | P2 | Convert only material historic decisions into immutable ADR timeline | ADR-0001..0003 created; migration should remain selective | Architect + Reviewer | 8–10 | IN_PROGRESS |
| IMP-013 | P1 | Add independent challenge/sign-off for major ADRs | Lesson 9 challenge pack exists; human independent approval remains | Skeptical Reviewer / CTO | 9–10 | OWNER_REVIEW |
| IMP-014 | P2 | Map every course document to canonical evidence | prevents course mirror becoming second truth source | KGA / Maintainer | 1–20 | IN_PROGRESS |
| IMP-015 | P2 | Keep lesson-by-lesson change-understanding journal | preserves evolution/WHY | PM / KGA | 1–20 | IN_PROGRESS |
| IMP-016 | P2 | Keep explicit UNKNOWN panel at material gates | prevents reconstructed docs from appearing falsely complete | all artifact owners | 1–20 | ACCEPTED |
| IMP-017 | P1 | Select one bounded MVP product outcome | current roadmap has options, not one approved MVP | Product / Business Owner | before MVP claim | OWNER_REVIEW |
| IMP-018 | P1 | Standardize PoC report as hypothesis → setup → raw evidence → limitations → decision impact | improves comparability and ADR reuse | Architect + QA + PoC owner | 3–9+ | PROPOSED |
| IMP-019 | P1 | Define Production workload/freshness/SLO assumptions before sizing/final TCO | avoids false precision | Product + Ops + Requirements | 15–17 | PROPOSED |
| IMP-020 | P2 | Show capability lifecycle badge DEV / POC / MVP / PRODUCTION / RETIRED | prevents prototype/readiness confusion | PM + KGA | 3–10/site | ACCEPTED |
| IMP-021 | P1 | Create one canonical C4/architecture-as-code source and render C1/C2/C3 from it | current diagrams are consistent but maintained in several documents | Architect | 4/8/10 | PROPOSED |
| IMP-022 | P1 | Version domain schemas independently of Python classes | future API/services/RAG/agents need stable contracts | System/Integration Engineer | 5/11/12 | PROPOSED |
| IMP-023 | P0 | Replace local filesystem paths with safe artifact references in any future remote API | prevents path disclosure/arbitrary-file risks | Security + API owner | before API implementation | ACCEPTED |
| IMP-024 | P1 | Create versioned retrieval/eval query set with expected evidence refs | RAG currently has design, not measured quality | QA + Product + SME | 6/13 | PROPOSED |
| IMP-025 | P0 | Enforce retrieved/source content as untrusted data, never policy/tool instruction | retrieval/prompt poisoning is Critical/High risk | Security + Agent/RAG owners | before agentic RAG | ACCEPTED |
| IMP-026 | P0 | Define formal tool permission/delegation policy before executable agents | prevents excessive agency/confused deputy/privilege escalation | Security + System Owner | before agent tools | PROPOSED |
| IMP-027 | P1 | Define provider-neutral Model Gateway contract + policy/compliance tests | ADR-0004 depends on replaceability and data gating | Architect + Security + Integration | before external LLM runtime dependency | PROPOSED |
| IMP-028 | P1 | Benchmark hosted and local model candidates on one eval set and collect workload/TCO telemetry | Lesson 9 cannot name Production cost/quality winner yet | QA + Ops + Finance + AI Lead | 9/13/17 | PROPOSED |
| IMP-029 | P1 | Require independent reviewer record for material accepted ADRs | producer must not self-certify architecture | Skeptical Reviewer / CTO | 9/10 | PROPOSED |
| IMP-030 | P2 | Visualize driver → requirement → option → trade-off → ADR → test → operation trace | makes evidence-backed architecture inspectable | FATHER site / KGA | site pass | PROPOSED |

## Mandatory per-lesson review template

```text
Lesson N — Improvement Review

What should be improved:
- ...

How / what exactly to change:
- ...

Why / evidence:
- ...

Priority:
- P0 / P1 / P2 / P3

Owner:
- ...

Affected artifacts:
- ...

When to close:
- lesson / gate

Status:
- PROPOSED / OWNER_REVIEW / ACCEPTED / IN_PROGRESS / DONE / ...
```

## Review rule

Review recommendations together with:
- `00_MASTER_ARTIFACT_REGISTER.yaml`;
- lesson gate decision;
- requirements/architecture traceability;
- project/security risk registers;
- implementation/verification evidence when a recommendation reaches implementation scope.

No recommendation is silently implemented just because it appears here.
