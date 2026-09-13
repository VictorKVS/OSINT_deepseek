# OSINT Agent — Live Reproduction / OTUS Lessons 01–20

Status: `ACTIVE / CUMULATIVE PROJECT`

This directory is the canonical cross-lesson engineering package for one real project: **FATHER OSINT Agent**.

The course is treated as one continuous development lifecycle. Each lesson extends, validates or revises the same project rather than producing an isolated homework artifact.

## Project mission

OSINT Agent receives a bounded research task, lawfully collects material from permitted sources, preserves provenance, returns structured evidence and does not silently decide truth or publish knowledge on its own.

Canonical implementation and existing technical baseline remain in the repository root and existing `docs/` packages. This course package does **not** duplicate them; it adds missing upstream/downstream engineering evidence and cross-links all layers.

## Core rule

```text
SOURCE / NEED
  ↓
PRODUCT
  ↓
BUSINESS ANALYSIS
  ↓
SECURITY + LEGAL + DATA
  ↓
SYSTEM MODEL
  ↓
REQUIREMENTS + NFR
  ↓
DELIVERY FEASIBILITY
  ↓
ARCHITECTURE OPTIONS
  ↓
ADR + CTO CHALLENGE
  ↓
LLD / IMPLEMENTATION
  ↓
TEST / SECURITY / DEVSECOPS
  ↓
PRODUCTION / OBSERVABILITY / SIZING
  ↓
OPERATIONS / FEEDBACK / EVOLUTION
```

## Course checkpoints

| Lesson | Layer | Course artifact | Project state |
|---|---|---|---|
| 01 | Presale / Requirements foundation | Product + RFP + business requirement intake | ACTIVE DRAFT |
| 02 | Estimation / Risks / Cost | NFR + WBS + Estimate v0 + Risk + TCO v0 + Change model | ACTIVE DRAFT |
| 03 | PoC → Production value delivery | PoC gate / MVP / production transition | QUEUED |
| 04 | HLD / C4 | Context + Container + HLD views | PARTLY EXISTS / TO NORMALIZE |
| 05 | LLD | Components + interactions + API/data contracts | PARTLY EXISTS / TO NORMALIZE |
| 06 | RAG patterns | Retrieval architecture decision pack | FUTURE / CONDITIONAL |
| 07 | Agents / Multi-Agent | Agent orchestration + handoff contracts | FUTURE / CONDITIONAL |
| 08 | ADR | Architecture decision lifecycle | PARTLY EXISTS |
| 09 | CTO Challenge / Verification | SaaS LLM vs Self-hosted ADR + tradeoff verification | TARGET HOMEWORK |
| 10 | Architecture governance / Tech debt | Conformance + debt register + review loop | QUEUED |
| 11 | Integrations | Integration landscape + interface contracts | PARTLY EXISTS |
| 12 | Data architecture for AI | Data ownership, lineage, storage, index lifecycle | QUEUED |
| 13 | GenAI quality | Eval strategy + golden set + quality gates | QUEUED |
| 14 | Security by Design | Threat model refinement + controls | PARTLY EXISTS |
| 15 | Observability | Logs/metrics/traces + LLM observability | QUEUED |
| 16 | Sizing | workload model + compute/storage sizing | QUEUED |
| 17 | LLM inference sizing | model runtime / VRAM / latency / throughput | QUEUED |
| 18 | IaC + CI/CD | reproducible environments and pipelines | PARTLY EXISTS |
| 19 | MLOps | model/data/eval/deploy lifecycle | QUEUED |
| 20 | Production deployment | rollout / rollback / acceptance / operations handoff | QUEUED |

## Existing canonical project evidence reused

- `docs/OSINT_AGENT_TZ_V1.md` — reviewed requirements and acceptance criteria.
- `docs/03_architecture/` — architecture/business-analysis pack.
- `docs/04_testing/` — acceptance test design.
- `docs/06_verification/` — verification and frozen baseline evidence.
- `docs/TRACEABILITY_MATRIX.md` — requirement → architecture → test → code → evidence.
- `docs/SECURITY_THREAT_REGISTER.md` — security/supply-chain threats.
- `docs/OPERATIONS_GOVERNANCE_MODEL.md` — production operations roles and controls.
- `docs/PROJECT_ROADMAP_AND_CONTROL.md` — capability roadmap / risks / gates.

## Separate improvement control

Recommendations are deliberately kept outside the AS-IS project description.

Canonical improvement document:

- [`IMPROVEMENT_BACKLOG.md`](IMPROVEMENT_BACKLOG.md) — what should be changed or strengthened, why, evidence/source, priority, accountable owner, affected artifacts, target lesson and status.

Rule:

```text
AS-IS / EVIDENCE
      ≠
RECOMMENDATION / TO-BE
```

A recommendation does not silently become a requirement or implementation task. It must be accepted by the accountable owner and pass the relevant change/architecture gate.

At the end of every lesson we update this backlog with three mandatory fields:

- `что стоит улучшить`;
- `как улучшить / что именно поменять`;
- `приоритет`;

plus owner, evidence, affected artifacts, target lesson and status.

## Status vocabulary

`EXISTING_VERIFIED` — already supported by current repository evidence.

`EXISTING_NEEDS_NORMALIZATION` — useful artifact exists but must be mapped into the course/FATHER structure.

`DRAFT_FROM_CURRENT_EVIDENCE` — created from repository facts but still requires accountable-owner review.

`GAP` — missing artifact/input.

`UNKNOWN` — explicitly unknown fact; must not be guessed.

`FUTURE_LESSON` — intentionally postponed until the corresponding course lesson.

## Deliverable strategy

By lesson 9 the repository must already tell a coherent project story from business need to architecture verification. By lesson 20 the same folder should represent a broad end-to-end software/AI-system engineering evidence package.
