# OSINT Agent — Improvement Backlog / Что стоит поменять или доработать

Status: `ACTIVE / SEPARATE FROM AS-IS DOCUMENTATION`

Purpose: keep improvement recommendations separate from the factual description of the current project. This file records what should be changed, strengthened, clarified or added as the OTUS lessons are applied to the existing `OSINT_deepseek` project.

## Core rule

`AS-IS` documents describe what the project currently is and what is supported by evidence.

`IMPROVEMENT_BACKLOG` describes what we recommend changing later.

A recommendation does **not** become project truth, requirement or implementation work until its accountable owner accepts it and the appropriate change/architecture gate is passed.

## Status vocabulary

- `PROPOSED` — recommendation identified, not yet accepted.
- `OWNER_REVIEW` — awaiting accountable-owner decision.
- `ACCEPTED` — approved for a future lesson/work package.
- `IN_PROGRESS` — documentation or implementation change is underway.
- `DONE` — change completed and verified.
- `REJECTED` — deliberately not adopted; rationale retained.
- `DEFERRED` — useful but postponed to a later lesson/stage.
- `SUPERSEDED` — replaced by a newer recommendation.

## Priority vocabulary

- `P0` — blocks a material gate, creates false confidence, or threatens legal/security correctness.
- `P1` — materially improves architecture, requirements, delivery predictability or verification.
- `P2` — improves maintainability, usability, documentation quality or future evolution.
- `P3` — optional enhancement / polish.

## Improvement register

| ID | Priority | What to change / improve | Why | Evidence / source | Owner | Affected artifacts | Target lesson | Status |
|---|---|---|---|---|---|---|---:|---|
| IMP-001 | P1 | Add explicit product/business KPI baseline instead of relying only on technical acceptance criteria | Current repository proves technical behavior well, but product success is not yet quantified | `README.md`, `docs/OSINT_AGENT_TZ_V1.md`, Product Pack reconstruction | Product Owner / Business Owner | `01_product/SUCCESS_METRICS`, future validation pack | 1–3 | OWNER_REVIEW |
| IMP-002 | P0 | Formalize production legal/compliance applicability and named authority before live collection expands | DEV scope is bounded, but production OSINT/Telegram/data processing requires explicit applicability and authority | `docs/OSINT_AGENT_TZ_V1.md`, Security/Operations docs | Legal/Compliance + Security | Regulatory applicability, data handling, production gate | 3–14 | PROPOSED |
| IMP-003 | P0 | Create production data inventory/classification/retention rules before storing real evidence at scale | Provenance is strong, but production data lifecycle constraints are not yet complete | Existing material/provenance contracts | Data Owner + Security | Data inventory, classification, retention, deletion, archive | 12–14 | PROPOSED |
| IMP-004 | P1 | Normalize current architecture documentation into explicit C4/HLD and later LLD views instead of leaving several overlapping diagrams/descriptions | Existing architecture pack is strong but predates the new cumulative course structure | `docs/03_architecture/` | Solution Architect / System Engineer | HLD, C4, LLD, view catalog | 4–5 | DEFERRED |
| IMP-005 | P1 | Separate logical architecture drivers from technology candidates such as concrete DB/LLM/transport choices | Avoid technology-first decisions and prepare for lesson 9 trade-off review | `docs/03_architecture/README.md`, FATHER Architecture Workbench model | Architect + Requirements | architecture characteristics, option set, ADR inputs | 4–9 | PROPOSED |
| IMP-006 | P1 | Add measurable production NFRs with baseline/target/verification method for latency, throughput, reliability, evidence freshness and quality | Current DEV NFRs are mostly qualitative; lesson 2 requires measurable and testable NFRs | OTUS Lesson 2 NFR method; current TZ | Requirements + QA + Ops | NFR catalog, verification matrix | 2–4 | PROPOSED |
| IMP-007 | P1 | Build Estimate v0 / WBS / uncertainty register for the current roadmap instead of using calendar promises | The project is capability-driven, but future production work still needs evidence-backed delivery feasibility | OTUS Lesson 2; `docs/PROJECT_ROADMAP_AND_CONTROL.md` | PM + Architect + Leads | WBS v0, estimate register, assumption log | 2–3 | PROPOSED |
| IMP-008 | P1 | Unify project risk, security risk and delivery risk through references without collapsing them into one register | Several risk views exist; cross-links will prevent duplication and inconsistent treatment | security register, roadmap/control, lesson 2 risk model | PM + Security + KGA | risk registers + traceability | 2–9 | PROPOSED |
| IMP-009 | P1 | Add formal Change Request workflow for material scope/requirement/architecture changes | Current governance has change-impact rules, but a course-visible CR artifact will make decisions auditable | OTUS Lessons 1–2; `docs/PROJECT_EXECUTION_CONTROL.md` | PM / Change Manager | CR template, impact analysis, baseline updates | 2–10 | PROPOSED |
| IMP-010 | P1 | Create TCO scenario model for LLM/API/self-hosted/on-prem options before lesson 9 ADR | Lesson 9 requires evidence-based hosting choice; current project should reuse the same model rather than invent numbers in ADR | OTUS Lessons 2 and 9 | Finance/Procurement + Architect + Ops | TCO v0/v1, ADR evidence | 2–9 | PROPOSED |
| IMP-011 | P1 | Establish Golden Dataset / evaluation set ownership and versioning for future RAG/LLM quality decisions | Model/RAG decisions cannot be validated by subjective demos alone | OTUS Lesson 2 and future Lessons 6/13 | QA + Product + Domain SME | Golden set plan, eval policy, acceptance evidence | 2–13 | PROPOSED |
| IMP-012 | P2 | Convert existing architecture decisions into an immutable ADR timeline with supersession links | Decisions exist in several documents; lesson 8/9 expects a clean decision history | existing decision register + future lesson 8 | Architect + Reviewer | ADR directory, decision register | 8–9 | DEFERRED |
| IMP-013 | P1 | Add independent architecture challenge pack before accepting major hosting/LLM/integration decisions | Current review is good, but lesson 9 explicitly requires challenge/defense and honest trade-offs | OTUS Lesson 9 | Skeptical Reviewer / CTO Challenge role | review findings, trade-off matrix, risk storm | 9 | DEFERRED |
| IMP-014 | P2 | Map each course document to existing canonical project evidence to prevent duplicated truth | The repository already contains rich docs; course package should remain an index/projection, not a second source of truth | `docs/course_live_reproduction/README.md` | KGA / Maintainer | artifact register, traceability | 1–20 | IN_PROGRESS |
| IMP-015 | P2 | Add lesson-by-lesson “what changed in project understanding” journal | Helps prove evolution and avoids silently rewriting history | course live reproduction model | PM / KGA | course journal / change log | 1–20 | IN_PROGRESS |
| IMP-016 | P2 | Add explicit `what we still do not know` panel to every major lesson/gate | Prevents reconstructed documentation from looking more certain than the evidence supports | FATHER UNKNOWN/evidence rule | Every accountable owner | gate decisions, lesson summaries | 1–20 | ACCEPTED |
| IMP-017 | P1 | Select one bounded MVP product outcome before labeling any Telegram capability as MVP | PoC feasibility and product value are different claims; current roadmap contains several opportunities but no single approved MVP | OTUS Lesson 03 + project product opportunity roadmap | Product Owner / Business Owner | MVP scope, success metrics, roadmap | 3–4 | OWNER_REVIEW |
| IMP-018 | P1 | Standardize every technical PoC report as hypothesis → setup → raw evidence → limitations → decision impact | Current governance correctly requires evidence, but a uniform report will improve comparability and ADR reuse | OTUS Lesson 03 + `PROJECT_EXECUTION_CONTROL.md` | Architect + QA + PoC owner | PoC reports, ADR evidence | 3–9 | PROPOSED |
| IMP-019 | P1 | Define production workload, freshness and SLO assumptions before sizing/TCO/hosting ADR | Without workload and service targets, architecture/cost comparisons can create false precision | Lesson 03 discovery questions; future Lessons 15–17 | Product + Ops + Requirements | NFR, sizing, TCO, ADR | 3–17 | PROPOSED |
| IMP-020 | P2 | Add visible lifecycle state for each capability: DEV / POC / MVP / PRODUCTION / RETIRED | Prevents technical prototypes from being mistaken for product or production readiness | OTUS Lesson 03 staged delivery model | PM + KGA | roadmap, course index, future site/dashboard | 3–10 | ACCEPTED |

## Per-lesson review template

At the end of every lesson, add a section using this structure:

```text
Lesson N — Improvement Review

What should be improved:
- ...

Why:
- ...

Evidence / source:
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
- PROPOSED / OWNER_REVIEW / ACCEPTED / ...
```

## Review rule

Recommendations are reviewed together with:

- `00_MASTER_ARTIFACT_REGISTER.yaml`;
- lesson gate decision;
- requirement/architecture traceability;
- project risk register;
- current implementation evidence when a recommendation reaches implementation scope.

No recommendation is silently implemented just because it appears in this file.
