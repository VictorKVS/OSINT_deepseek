# OSINT Agent — Live Reproduction / OTUS Lessons 01–20

Status: `ACTIVE / LESSONS 01–09 DOCUMENTED`

This directory is the canonical cross-lesson engineering package for one real project: **FATHER OSINT Agent**.

The course is treated as one continuous development lifecycle. Each lesson extends, validates or revises the same project rather than producing an isolated homework artifact. The implementation is not changed by this documentation pass.

## Project mission

OSINT Agent receives a bounded research task, lawfully collects material from permitted sources, preserves provenance, returns structured evidence and does not silently decide truth or publish knowledge on its own.

Existing root/project documents remain canonical for implemented behavior. This course package adds missing upstream/downstream engineering evidence and cross-links them.

## Current review point

**[Lessons 01–09 Master Review](LESSONS_01_09_MASTER_REVIEW.md)** — one-page view of the entire course/project chain, document tree, gates, UNKNOWNs, Lesson 09 ADR/CTO decision and improvement priorities.

## Core lifecycle

```text
SOURCE / NEED
  ↓
PRODUCT / PRESALE                     Lesson 01
  ↓
REQUIREMENTS / NFR / ESTIMATE         Lesson 02
  ↓
POC → MVP → PRODUCTION STRATEGY        Lesson 03
  ↓
HLD / C4                              Lesson 04
  ↓
LLD / COMPONENTS / API                Lesson 05
  ↓
RAG OPTIONS / EVALUATION              Lesson 06
  ↓
AGENT / MULTI-AGENT HANDOFFS          Lesson 07
  ↓
ADR / ARCHITECTURE-AS-CODE            Lesson 08
  ↓
CTO CHALLENGE / HOSTING DECISION      Lesson 09
  ↓
GOVERNANCE / INTEGRATION / DATA / QUALITY / SECURITY / OPS   Lessons 10–20
```

## Course checkpoints

| Lesson | Layer | Project package | State |
|---|---|---|---|
| 01 | Presale / Product | `01_product/` | `CONDITIONAL_PASS` |
| 02 | Estimation / Risks / Cost | `02_delivery_feasibility/` | `CONDITIONAL_PASS` |
| 03 | PoC → MVP → Production | `03_poc_to_production/` | `CONDITIONAL_PASS` |
| 04 | HLD / C4 | `04_hld_c4/` | `CONDITIONAL_PASS` |
| 05 | LLD / Components / API | `05_lld/` | `CONDITIONAL_PASS` |
| 06 | RAG patterns | `06_rag/` | `CANDIDATE / EVAL REQUIRED` |
| 07 | AI Agents / Multi-Agent | `07_agents/` | `CANDIDATE / VALUE+SECURITY PROOF REQUIRED` |
| 08 | ADR | `08_adr/` | `PASS FOR DOCUMENTATION DISCIPLINE` |
| 09 | Architecture Verification / CTO Challenge | `09_cto_challenge/` | `READY FOR HOMEWORK REVIEW` |
| 10 | Architecture governance / Tech debt | future | QUEUED |
| 11 | Integrations | existing inputs + future normalization | QUEUED |
| 12 | Data architecture for AI | future | QUEUED |
| 13 | GenAI quality | future | QUEUED |
| 14 | Security by Design | existing security baseline + future normalization | QUEUED |
| 15 | Observability | future | QUEUED |
| 16 | Sizing | future | QUEUED |
| 17 | LLM inference sizing | future | QUEUED |
| 18 | IaC + CI/CD | existing inputs + future normalization | QUEUED |
| 19 | MLOps | future | QUEUED |
| 20 | Production deployment | future | QUEUED |

## Current project classification

```text
DEV BASELINE      = EXISTING_VERIFIED
TECHNICAL POC     = ACTIVE / EVIDENCE-PRODUCING PATH
MVP PRODUCT       = UNKNOWN / OWNER DECISION REQUIRED
RAG               = CANDIDATE / NOT CLAIMED IMPLEMENTED
PRODUCTION AGENTS = CANDIDATE / NOT CLAIMED IMPLEMENTED
PRODUCTION READY  = NOT CLAIMED
```

## Existing canonical project evidence reused

- `docs/OSINT_AGENT_TZ_V1.md` — requirements and acceptance criteria;
- `docs/03_architecture/` — existing architecture/business-analysis pack;
- `docs/04_testing/` — acceptance test design;
- `docs/06_verification/` — verification/frozen baseline evidence;
- `docs/TRACEABILITY_MATRIX.md` — requirement → architecture → test → code → evidence;
- `docs/SECURITY_THREAT_REGISTER.md` — security/agent/supply-chain threats;
- `docs/OPERATIONS_GOVERNANCE_MODEL.md` — operations roles/controls;
- `docs/PROJECT_ROADMAP_AND_CONTROL.md` — capability roadmap / risks / gates;
- `docs/PROJECT_EXECUTION_CONTROL.md` — DoR/DoD, WIP, PoC/ADR/change controls;
- `config/model_stage_registry.yaml` — semantic capability/model-stage policy.

## Separate improvement control

[`IMPROVEMENT_BACKLOG.md`](IMPROVEMENT_BACKLOG.md) holds TO-BE recommendations separately from AS-IS facts.

```text
AS-IS / EVIDENCE
      ≠
RECOMMENDATION / TO-BE
```

Each lesson records what to improve, how, priority, owner, evidence, affected artifacts and target lesson/gate.

## Status vocabulary

- `EXISTING_VERIFIED` — supported by current repository evidence;
- `EXISTING_NEEDS_NORMALIZATION` — useful artifact exists but needs mapping into this course structure;
- `DRAFT_FROM_CURRENT_EVIDENCE` — reconstructed from repo facts, owner review remains;
- `CANDIDATE` — architecture/design option, not implementation truth;
- `GAP` — missing artifact/input;
- `UNKNOWN` — explicitly unknown fact; never guessed;
- `FUTURE_LESSON` — intentionally deferred.

## Deliverable strategy

By Lesson 09 the repository now tells a coherent project story from business need through architecture verification/ADR. Lessons 10–20 will extend the **same package** into architecture governance, integrations, data, quality, Security by Design, observability, sizing, IaC/CI-CD, MLOps and Production deployment.
