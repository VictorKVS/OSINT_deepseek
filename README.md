# OSINT_deepseek / FATHER Knowledge Factory

> **Status:** PROJECT / DEV / **DEV v1 BASELINE FROZEN**
>
> **Stage 06:** ✅ COMPLETE — Verification and Repository Rationalization
>
> **Current development:** **Stage 07 / M5 — Telegram Radar**
>
> **Engineering rule:** **NO CODE BEFORE CONTRACT.** Requirements are reviewed first, including commercial/reuse potential and security/supply-chain impact, then architecture, acceptance tests, implementation plan, code, verification and experience capture.

This repository is evolving from the original `OSINT_deepseek` prototype into the first practical worker of the FATHER ecosystem: an OSINT supplier for the Knowledge Factory.

## Mission

The OSINT worker does **not** decide what is true and does **not** publish knowledge by itself. It receives a research task, finds and preserves materials, records provenance and returns evidence to Analyst.

```mermaid
flowchart LR
    A[Research Task / Analyst] --> B[OSINT]
    B --> C[Material Package]
    C --> D[Analyst]
    D --> E[Socrates]
    E -->|PASS| F[DEV phase output / Knowledge Gate planned]
    E -->|RESEARCH MORE| A
```

## Engineering lifecycle

```mermaid
flowchart TD
    R[1. Requirements / ТЗ] --> CR[2. Commercial + Reuse Review]
    CR --> SR[3. Security + Supply-Chain Review]
    SR --> RV[4. Requirements Review]
    RV --> A[5. Architecture + Business Analysis]
    A --> CR2[Commercial + Reuse Recheck]
    CR2 --> TM[Threat Model / Top-100 Coverage]
    TM --> AV[Architecture Review Gate]
    AV -->|PASS| T[6. Acceptance + Security Test Design]
    AV -->|REWORK| R
    T --> P[7. Implementation Plan]
    P --> C[8. Code]
    C --> TR[9. Test + SAST/SCA/Secrets]
    TR --> V[10. Verification / Acceptance]
    V --> PR[11. Product + Security Registry Recheck]
    PR --> E[12. Experience -> KB / baseline]
```

## Project control

The project is managed by **capability and evidence gates**, not invented calendar deadlines or cosmetic completion percentages.

**[Capability Roadmap & Project Control](docs/PROJECT_ROADMAP_AND_CONTROL.md)** — integrated MUST/SHOULD/OPTION roadmap, dependency/critical-path diagrams, gate-based progress dashboard, project threat/risk matrix, opportunity paths and immediate controlled backlog.

Planning rule:

```text
MUST    = required core capability / next gate
SHOULD  = materially reduces risk or strengthens several paths
OPTION  = commercial/product opportunity; promoted only by evidence
```

Roadmap, risk register, product registry, security register, journal and traceability are reviewed together whenever a material gate or decision changes.

## Security / DevSecOps direction

Security is a permanent cross-cutting workstream. Approved libraries, GitHub Actions, binaries, models, containers, services and donor-derived components remain under lifecycle monitoring after adoption.

Key security governance:

- **[DevSecOps & Software Supply-Chain Governance](docs/SECURITY_SUPPLY_CHAIN_CONTROL.md)**
- **[Security & Supply-Chain Threat Register](docs/SECURITY_THREAT_REGISTER.md)**
- **[FATHER Security Top-100 Control Catalog](docs/SECURITY_TOP100_CONTROL_CATALOG.md)**
- **[Operations Governance Model](docs/OPERATIONS_GOVERNANCE_MODEL.md)**

The Top-100 is an internal coverage catalog built from authoritative security families and project-specific risks; it is a coverage aid, not a replacement for threat modelling. Operational roles are planned separately for production: Director/Product Owner, Security Administrator/Security Officer, System Administrator/DevOps, Analyst/Operator, End User and Developer/Maintainer.

## Commercial product direction

Commercialization is a **separate product-development track**, not a substitute for the core engineering roadmap. Every reusable block should be reviewed before development, during architecture review and after verification for additional lawful uses and product opportunities.

The living registry is here:

**[Commercial Product Opportunity Registry](docs/PRODUCT_OPPORTUNITY_REGISTRY.md)**

It tracks potential products built from shared FATHER blocks, including competitive/channel intelligence, content-origin and propagation analysis, brand/reputation monitoring, technology/market radar, research tooling, security/risk use cases and future marketing/advertising/analytics scenarios where appropriate and lawful.

Principle:

```text
ONE VERIFIED CORE
      ↓
Telegram Radar / Artifact / Provenance / Analyst / Socrates / KB
      ↓
MANY PRODUCT ASSEMBLIES
```

Commercial ideas may influence reusable interfaces and metadata, but they must not contaminate the core with one customer's domain logic or bypass requirements, legal constraints, tests, donor review, benchmarks or architecture gates.

## Frozen DEV v1 baseline

Current clean-checkout CI proves:

```text
checkout
  ↓
Python 3.12
  ↓
DEV dependency install
  ↓
import father_osint
  ↓
21 tests PASS
  ↓
run_dev_osint.py PASS
  ↓
run_dev_pipeline.py PASS
```

The frozen semantic baseline proves:
- equal payload does not collapse independent source observations;
- raw text payloads may be reused by SHA-256 without dropping provenance;
- file-only Material is hashed from original file bytes;
- missing local files fail explicitly;
- follow-up research accumulates evidence across cycles;
- research loops remain hard bounded;
- collector failures remain isolated and visible;
- Telegram collection stays independent of a concrete transport library.

Historical Ollama/GPU/workstation code, old `core/`, `vip/`, the unapproved Teleproto/Node bridge and the unrelated experimental policy/"llm-gateway" prototype were removed only after their useful engineering lessons were documented and clean CI proved the current product did not depend on them.

## Development control

Living history, WHY decisions, completed work, risks and roadmap:

**[Development Journal](docs/DEVELOPMENT_JOURNAL.md)**

Formal freeze record:

**[DEV v1 Baseline Freeze](docs/06_verification/16_DEV_V1_BASELINE_FREEZE.md)**

## Key documentation

| Pack | Purpose |
|---|---|
| [Capability Roadmap & Project Control](docs/PROJECT_ROADMAP_AND_CONTROL.md) | Goals, dependencies, progress gates, project risks, opportunity paths and controlled backlog |
| [Development Journal](docs/DEVELOPMENT_JOURNAL.md) | Living history, status, WHY decisions and roadmap |
| [Commercial Product Registry](docs/PRODUCT_OPPORTUNITY_REGISTRY.md) | Separate living product track: reusable blocks → commercial opportunities, priorities and review gates |
| [DevSecOps & Supply Chain](docs/SECURITY_SUPPLY_CHAIN_CONTROL.md) | Secure development, dependency/upstream lifecycle and supply-chain gates |
| [Security Threat Register](docs/SECURITY_THREAT_REGISTER.md) | Living technical/security/supply-chain threat register |
| [Security Top-100](docs/SECURITY_TOP100_CONTROL_CATALOG.md) | Broad weakness/attack-surface coverage catalog for every engineering gate |
| [Operations Governance](docs/OPERATIONS_GOVERNANCE_MODEL.md) | Planned production roles, separation of duties, monitoring and operational control domains |
| [Project Governance](docs/PROJECT_GOVERNANCE.md) | Mandatory engineering chain and gates |
| [OSINT Agent ТЗ v1](docs/OSINT_AGENT_TZ_V1.md) | Current requirements and acceptance criteria |
| [Stage 03 — Architecture Review](docs/03_architecture/README.md) | Business analysis, diagrams and architecture decisions |
| [Stage 04 — Testing](docs/04_testing/README.md) | Acceptance test design and execution rules |
| [Stage 06 — Verification](docs/06_verification/README.md) | Completed verification/rationalization evidence |
| [Stage 07 — Next Requirement](docs/07_next_requirement/) | M5 Telegram Radar requirements, donor research and PoC planning |
| [Full Project Audit](docs/06_verification/14_FULL_PROJECT_AUDIT_2026-08-09.md) | Full-project findings and remediation priorities |
| [Semantic Remediation Plan](docs/06_verification/15_SEMANTIC_REMEDIATION_PLAN.md) | Contract for cumulative evidence, reuse metric and file hashing |
| [DEV v1 Freeze](docs/06_verification/16_DEV_V1_BASELINE_FREEZE.md) | Formal frozen baseline and change-control gate |
| [Traceability Matrix](docs/TRACEABILITY_MATRIX.md) | requirement → architecture → test → code → evidence |
| [Donor KB: Telegram](docs/DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md) | Research notes for future transport selection; not approval |

## Directory map

| Directory | Role |
|---|---|
| `father_osint/` | Frozen FATHER OSINT DEV v1 implementation |
| `scripts/` | Canonical DEV execution adapters |
| `tests/` | Verified executable contract evidence |
| `data/` | DEV fixtures/runtime data references |
| `config/` | Draft mission/profile/policy inputs |
| `docs/` | Requirements, architecture, tests, decisions, verification, product registry, security governance, roadmap/control and journal |

## Current disposition

```text
father_osint/                 DEV v1 BASELINE
scripts/run_dev_osint.py      KEEP
scripts/run_dev_pipeline.py   KEEP / CANONICAL DEV RUNNER
tests/                        VERIFIED CONTRACT EVIDENCE
config/                       DRAFT PROFILE/POLICY INPUTS
data/dev/                     TEST FIXTURES ONLY
father_osint/transports/      M5 EXTENSION BOUNDARY / NO APPROVED IMPLEMENTATION
```

## Dependencies

- `requirements.txt` — current runtime dependency declaration; the DEV core is stdlib-only.
- `requirements-dev.txt` — verification/test dependencies (`pytest`).

Historical prototype dependencies are retained in Git history and audit documents, not in the active dependency surface.

## DEV vs PROD

The frozen baseline is **DEV / SIMPLIFIED**, not production readiness. Real MTProto sessions, Tor gateways, proxy rotation, schedulers, secrets infrastructure, production LLM routing, battle monitoring, generic Artifact ingestion, local transcription, Knowledge Gate and autonomous KB publication remain separate future requirements.

Production operation additionally requires the planned operations governance controls: role separation, RBAC/authentication, privileged access, change management, vulnerability/patch management, backup/restore, incident response, security/event monitoring, audit and access review.

## Next milestone

**M5 — Telegram Radar.**

Current M5 sequence:
- requirements and commercial/reuse review;
- security/supply-chain review and Top-100 threat coverage;
- donor verification;
- bounded TDLib and GramJS PoCs;
- common benchmark and security/operations review;
- ADR transport selection;
- acceptance/security tests before product-path implementation.

Later planned core milestones remain:
- M6 — generic Artifact/Ingestion layer;
- M7 — local-first transcription/extraction;
- M8 — Knowledge Gate foundation.

We choose by business value, security evidence and reusable capability, not by which technology is most interesting.

## Change policy

Before modifying the frozen baseline or adding a file, service, database, agent or dependency, answer:

1. Which approved requirement requires it?
2. Which commercial or non-commercial reuse scenarios could benefit from this block?
3. Which new security threat/Top-100 topics become applicable?
4. Is this a defect fix or a new capability?
5. Which architecture element owns it?
6. What enters it and what must leave it?
7. Why is it needed instead of a simpler existing mechanism?
8. Which acceptance/security test will prove it works?
9. Does it break a frozen invariant or add an external dependency?
10. What is the rollback/disable/replacement path?
11. Does the implementation remain reusable rather than embedding one product's domain logic into the core?

If these questions have no clear answers, the change is not implementation-ready.
