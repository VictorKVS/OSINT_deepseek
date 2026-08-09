# Documentation Packs

This directory is the project control plane. Implementation follows the document chain rather than inventing requirements in code.

## Living project record

Start with **[DEVELOPMENT_JOURNAL.md](DEVELOPMENT_JOURNAL.md)** for the current checkpoint, development history, WHY decisions, open future requirements and roadmap.

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
ACCEPTANCE TESTS
        ↓
05_implementation/
        ↓
REVIEWED MINIMAL CHANGE
        ↓
06_verification/
        ↓
CLEAN CHECKOUT + AUDIT + REMEDIATION
        ↓
DOCUMENTATION CONSISTENCY
        ↓
DEV v1 BASELINE FREEZE
```

## Current status

**DEV v1 BASELINE FROZEN. Stage 06 is complete.**

Completed evidence includes:
- storage/provenance correction;
- one canonical `review_pipeline.py`;
- removal of old pipeline/runtime/core/VIP/experimental gateway/Teleproto bridge after audit;
- runtime/dev dependency separation;
- clean GitHub Actions checkout verification;
- full project audit;
- semantic remediation for cumulative follow-up evidence, explicit payload-reuse semantics and file-only SHA-256;
- documentation consistency pass;
- formal DEV v1 freeze.

The current clean CI baseline collects **21 tests**, passes all 21, then executes both canonical DEV runners.

## Active documents

- `DEVELOPMENT_JOURNAL.md` — living history, WHY decisions, current freeze state and next-requirement roadmap.
- `PROJECT_GOVERNANCE.md` — engineering lifecycle and gates.
- `OSINT_AGENT_TZ_V1.md` — current requirements and AC-01…AC-13.
- `03_architecture/` — business analysis, architecture views and review decisions.
- `04_testing/` — acceptance test design and execution rules.
- `05_implementation/` — reviewed implementation plans.
- `06_verification/09_COMPONENT_TRACEABILITY_MAP.md` — current package component map.
- `06_verification/10_DEPENDENCY_SPLIT.md` — dependency decision evidence.
- `06_verification/11_LEGACY_CLEANUP_REPORT.md` — evidence-based old runtime/core removal.
- `06_verification/12_TELEGRAM_EXPERIMENT_AUDIT.md` — why the concrete Teleproto bridge was removed.
- `06_verification/13_LLM_GATEWAY_DISPOSITION.md` — why the unrelated policy-control experiment was removed.
- `06_verification/14_FULL_PROJECT_AUDIT_2026-08-09.md` — full current-project audit.
- `06_verification/15_SEMANTIC_REMEDIATION_PLAN.md` — approved remediation contract.
- `06_verification/16_DEV_V1_BASELINE_FREEZE.md` — formal closure/freeze record.
- `TRACEABILITY_MATRIX.md` — current requirement → architecture → test → implementation → evidence map.

## Current repository view

- `father_osint/` — frozen DEV v1 package.
- `father_osint/review_pipeline.py` — cumulative bounded OSINT→Analyst→Socrates orchestration.
- `father_osint/transports/` — future transport boundary; no implementation is approved by existence.
- `tests/` — verified executable contract evidence.
- `scripts/run_dev_osint.py`, `scripts/run_dev_pipeline.py` — canonical DEV entrypoints.
- `requirements.txt` — current stdlib-only runtime declaration.
- `requirements-dev.txt` — current pytest verification dependency.
- `config/` — draft mission/profile/policy inputs, not calibrated truth.
- `data/dev/` — fixtures only, never automatic intelligence evidence.

Removed legacy/experimental implementations remain available in Git history and audit documents; they are not current architecture.

## Next engineering gate

**M5 — choose one next approved business requirement.**

Recorded candidates:
- live Telegram Radar transport;
- generic Artifact/Ingestion layer;
- local-first transcription;
- Knowledge Gate foundation.

The next cycle starts at business requirement and acceptance criteria, not at library selection or code.

## Research/history

- `DONOR_KB_TELEGRAM_INTELLIGENCE_V0_1.md` — donor research, not an implementation approval.
- `FATHER_OSINT_AGENT_STANDARD_V0_1.md` — historical broad standard.
- `FATHER_OSINT_AGENT_STANDARD_V1.md` — simplified standard; subordinate to current ТЗ.
- `OSINT_AGENT_MVP_V1.md` — earlier MVP notes; historical/supporting context.

A document can be useful without being an approved implementation contract. Its status must remain explicit.
