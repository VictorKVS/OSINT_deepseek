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
04_testing/
        ↓
TEST DESIGN + FOCUSED EVIDENCE
        ↓
05_implementation/
        ↓
REVIEWED MINIMAL FIX
        ↓
06_verification/  ← CURRENT STAGE
        ↓
STATIC REPOSITORY AUDIT
        ↓
FULL LOCAL CHECKOUT + PYTEST/RUNNERS
        ↓
TEST_REPORT_003
        ↓
EVIDENCE-BASED CLEANUP / REGRESSION
```

## Current project stage

**Stage 06 — Verification and Repository Rationalization / ACTIVE.**

The focused storage defect was taken through requirement → architecture → test → implementation-plan → minimal fix → focused regression. The next task is not feature development: it is to prove the complete repository boundary, separate current FATHER OSINT DEV assets from legacy/experimental code, then perform the first full local-checkout verification.

Main pack: [06_verification/README.md](06_verification/README.md)

## Active documents

- `PROJECT_GOVERNANCE.md` — engineering lifecycle and gates.
- `OSINT_AGENT_TZ_V1.md` — current technical specification and acceptance criteria.
- `03_architecture/` — business analysis, architecture views, architecture review and decision register.
- `04_testing/` — acceptance test specification, existing-test review, execution plan and report format.
- `05_implementation/01_STORAGE_SEMANTICS_PLAN.md` — approved minimal storage correction plan.
- `05_implementation/02_IMPLEMENTATION_REVIEW.md` — implementation gate evidence.
- `06_verification/01_STATIC_REPOSITORY_AUDIT.md` — current KEEP / CHANGE / DELETE CANDIDATE / DEFER / LEGACY disposition map.
- `06_verification/02_FULL_RUN_PLAN.md` — exact local verification sequence and failure classification.
- `TEST_PLAN_V1.md` — project-level verification strategy.
- `TRACEABILITY_MATRIX.md` — requirement → architecture → test → code → evidence map.
- `REPOSITORY_AUDIT_2026-08-09.md` — earlier inventory snapshot; Stage 06 audit supersedes it for current disposition decisions.

## Current verified static findings

- `father_osint/` is the canonical current DEV package candidate.
- `review_pipeline.py` is the canonical full-loop candidate; `pipeline.py` is a deletion candidate pending full-checkout dependency proof.
- `run_dev_pipeline.py` still imports the older pipeline path and therefore requires migration after verification, not before.
- `core/`, root legacy runners/PowerShell tools and `services/llm-gateway/` are not implicit dependencies of FATHER OSINT v1.
- live Telegram transport/Node bridge remains deferred and must not be required for current DEV acceptance.
- root `requirements.txt` currently lists Ollama/monitoring/GPU-oriented dependencies; these are not justified as dependencies of the pure-Python FATHER OSINT DEV core and must not be installed automatically merely to satisfy legacy code.

## Research/history

- `DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md` — donor research, not an implementation approval.
- `FATHER_OSINT_AGENT_STANDARD_V0_1.md` — historical broad standard.
- `FATHER_OSINT_AGENT_STANDARD_V1.md` — simplified standard; subordinate to approved ТЗ.
- `OSINT_AGENT_MVP_V1.md` — earlier MVP notes; reconcile rather than silently overwrite.

A document can be useful without being an approved implementation contract. Status must remain visible.
