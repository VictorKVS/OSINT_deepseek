# Documentation Packs

This directory is the project control plane. Implementation must follow the document chain rather than invent requirements in code.

## Living project record

Start with **[DEVELOPMENT_JOURNAL.md](DEVELOPMENT_JOURNAL.md)** for the current checkpoint, development history, WHY decisions, open risks and forward plan.

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
COMPONENT / DEPENDENCY / LEGACY AUDIT
        ↓
FULL LOCAL CHECKOUT + PYTEST/RUNNERS
        ↓
FULL TEST REPORT
        ↓
EVIDENCE-BASED CLEANUP / REGRESSION
        ↓
DEV V1 BASELINE
```

## Current project stage

**Stage 06 — Verification and Repository Rationalization / ACTIVE.**

The first complete FATHER engineering cycle has already been exercised on storage/provenance semantics: requirement correction → architecture review → test correction → failing evidence → implementation plan → minimal fix → focused regression.

Repository rationalization has also advanced materially:
- `father_osint/review_pipeline.py` is the canonical DEV orchestration path;
- the redundant old `father_osint/pipeline.py` was migrated away from canonical runners/tests and then deleted;
- legacy `core/` and old Ollama/GPU/Windows runtime assets were audited;
- `services/llm-gateway/` was identified as a frozen experimental cognitive-policy subproject, not an approved current gateway dependency;
- `config/` and `data/dev/` boundaries were reviewed;
- the current `father_osint/` package has a formal component traceability map.

The next major evidence gate is a complete clean local checkout verification followed by dependency/legacy cleanup based on that evidence.

Main pack: [06_verification/README.md](06_verification/README.md)

## Active documents

- `DEVELOPMENT_JOURNAL.md` — **living history, WHY decisions, current checkpoint and roadmap.**
- `PROJECT_GOVERNANCE.md` — engineering lifecycle and gates.
- `OSINT_AGENT_TZ_V1.md` — current technical specification and acceptance criteria.
- `03_architecture/` — business analysis, architecture views, architecture review and decision register.
- `04_testing/` — acceptance test specification, existing-test review, execution plan and report format.
- `05_implementation/01_STORAGE_SEMANTICS_PLAN.md` — approved minimal storage correction plan.
- `05_implementation/02_IMPLEMENTATION_REVIEW.md` — implementation gate evidence.
- `06_verification/01_STATIC_REPOSITORY_AUDIT.md` — repository disposition work.
- `06_verification/02_FULL_RUN_PLAN.md` — exact local verification sequence and failure classification.
- `06_verification/04_DEPENDENCY_AUDIT.md` — dependency evidence and pipeline rationalization.
- `06_verification/05_LEGACY_CORE_AUDIT.md` — old core analysis and retained concepts.
- `06_verification/06_LEGACY_RUNTIME_AUDIT.md` — old runtime/Ollama/GPU/Windows cluster analysis.
- `06_verification/07_LLM_GATEWAY_AUDIT.md` — frozen experimental policy-subproject analysis.
- `06_verification/08_CONFIG_DATA_AUDIT.md` — configuration/data boundaries.
- `06_verification/09_COMPONENT_TRACEABILITY_MAP.md` — current `father_osint/` component → responsibility → input/output → tests → status map.
- `TEST_PLAN_V1.md` — project-level verification strategy.
- `TRACEABILITY_MATRIX.md` — requirement → architecture → test → code → evidence map.
- `REPOSITORY_AUDIT_2026-08-09.md` — earlier inventory snapshot; Stage 06 audit supersedes it for current disposition decisions.

## Current repository view

- `father_osint/` — canonical current DEV package.
- `review_pipeline.py` — canonical bounded OSINT→Analyst→Socrates orchestration.
- `tests/` — current executable contract evidence.
- `scripts/run_dev_osint.py` and `scripts/run_dev_pipeline.py` — canonical DEV execution paths.
- `core/` and old runtime scripts — audited legacy, not current implicit dependencies.
- `services/llm-gateway/` — frozen experimental subproject, no current integration.
- live Telegram transport/Node bridge — deferred and not required for current DEV acceptance.
- root dependency separation remains an open Stage 06 task.

## Research/history

- `DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md` — donor research, not an implementation approval.
- `FATHER_OSINT_AGENT_STANDARD_V0_1.md` — historical broad standard.
- `FATHER_OSINT_AGENT_STANDARD_V1.md` — simplified standard; subordinate to approved ТЗ.
- `OSINT_AGENT_MVP_V1.md` — earlier MVP notes; reconcile rather than silently overwrite.

A document can be useful without being an approved implementation contract. Status must remain visible.
