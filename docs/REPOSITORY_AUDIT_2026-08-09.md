# Repository Audit — 2026-08-09

**Purpose:** separate legacy prototype assets, current FATHER DEV code, experiments and documentation before further development.

## Status vocabulary

- **CURRENT-DEV** — belongs to current simplified FATHER OSINT path.
- **PROTOTYPE-UNVERIFIED** — written before requirements gate or not yet executed against current ТЗ.
- **LEGACY** — belongs to earlier OSINT_deepseek implementation; preserve until migration decision.
- **EXPERIMENTAL** — candidate/integration research; not part of accepted DEV contract.
- **DOC** — project knowledge/governance.

## Root

- `.gitignore` — CURRENT-DEV/support.
- `requirements.txt` — LEGACY/needs reconciliation; currently reflects old runtime rather than the new DEV package alone.
- `run.py`, `start.ps1` — LEGACY entry points.
- `crash_analyzer.ps1`, `system_stress_test.ps1`, `system_test_results.txt` — LEGACY diagnostics/evidence; preserve until reviewed.

## `father_osint/`

All current files are **PROTOTYPE-UNVERIFIED** until the test plan is executed, but they are the intended CURRENT-DEV implementation family.

- `models.py` — contracts: ResearchTask, Material, MaterialPackage.
- `agent.py` — OSINT orchestration.
- `storage.py` — local DEV persistence/dedup.
- `analysis.py` — deterministic DEV Analyst.
- `socrates.py` — deterministic DEV Socrates.
- `pipeline.py` — bounded OSINT↔Analyst pipeline.
- `review_pipeline.py` — bounded OSINT→Analyst→Socrates pipeline; overlap with `pipeline.py` requires review.
- `collectors/dev.py` — DEV fixture collector.
- `collectors/telegram.py` — Telegram collector contract/mapping.
- `transports/teleproto.py` — EXPERIMENTAL, not required for DEV acceptance.

## `tests/`

Five test files exist. They are **TEST SPEC PROTOTYPES** until executed and linked to acceptance criteria in `TRACEABILITY_MATRIX.md`.

## `data/dev/`

Fixture data for simplified development. CURRENT-DEV.

## `telegram_bridge/`

EXPERIMENTAL production-transport research. Freeze during requirements/test normalization. It must not become a prerequisite for DEV acceptance.

## `docs/`

Contains historical donor research and OSINT standards plus the new requirements-first project pack. `FATHER_OSINT_AGENT_STANDARD_V0_1.md` is historical; `FATHER_OSINT_AGENT_STANDARD_V1.md` is closer to current scope but subordinate to approved ТЗ/governance.

## `core/`, `scripts/`, `services/`, `config/`

These predate the current FATHER requirements-first architecture and are treated as LEGACY or EXPERIMENTAL until individually reviewed. They are not deleted because they may contain useful behavior, diagnostics, configuration or donor code.

## Migration decision process

After the first test run every implementation file receives one decision:

`KEEP` — matches requirements and architecture.  
`CHANGE` — useful but contract mismatch exists.  
`DELETE` — unnecessary duplicate/dead path after evidence.  
`DEFER` — production/future capability outside current scope.

No bulk cleanup occurs before this evidence-producing pass.
