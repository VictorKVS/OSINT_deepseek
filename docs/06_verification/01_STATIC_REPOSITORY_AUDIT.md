# Stage 06 — Static Repository Audit

**Date:** 2026-08-09  
**Status:** IN PROGRESS / NO DELETIONS YET

## 1. Audit objective

Determine what belongs to the approved FATHER OSINT DEV chain before full local runtime verification.

Approved logical path:

```text
ResearchTask
   ↓
OSINTAgent
   ↓
Collector
   ↓
Material + provenance
   ↓
MaterialStore
   ↓
MaterialPackage
   ↓
SimpleAnalyst [DEV harness]
   ↓
SimpleSocrates [DEV harness]
   ↓
PASS or bounded ResearchTask follow-up
```

Anything outside this path must be explicitly justified before it becomes part of FATHER OSINT v1.

## 2. Disposition vocabulary

- `KEEP` — justified part of the current approved DEV path.
- `KEEP DEV ONLY` — useful verification/harness asset, not production architecture.
- `CHANGE` — required by approved contract but needs adjustment.
- `DEFER` — potentially useful later; excluded from current DEV acceptance.
- `LEGACY` — belongs to the earlier OSINT_deepseek prototype; not a dependency of the current architecture.
- `DELETE CANDIDATE` — appears redundant/unneeded, but deletion waits for full-checkout dependency verification.

## 3. `father_osint/` audit

| Path | Decision | Owner / role | WHY | Next verification |
|---|---|---|---|---|
| `models.py` | KEEP | shared contracts | defines ResearchTask, Material, MaterialPackage boundaries | field validation + serialization tests |
| `agent.py` | KEEP | OSINT orchestration | selects eligible collectors, bounds collection, isolates errors, returns package without analysis | AC-01/03/04/05 |
| `storage.py` | KEEP | DEV persistence | inspectable append-only observation storage and reusable content-addressed raw blobs | restart/provenance regression |
| `collectors/dev.py` | KEEP DEV ONLY | fixture acquisition | deterministic source input without PROD secrets/infrastructure | repeatability test |
| `collectors/telegram.py` | KEEP AS CONTRACT | source adapter boundary | maps transport-neutral Telegram messages into Material without analysis | contract mapping test |
| `analysis.py` | KEEP DEV ONLY | Analyst harness | proves generic MaterialPackage handoff and follow-up research request | AC-06/07 only |
| `socrates.py` | KEEP DEV ONLY | review harness | proves bounded PASS/RESEARCH_MORE flow; not final epistemic engine | AC-09 only |
| `review_pipeline.py` | KEEP DEV ONLY / PRIMARY LOOP CANDIDATE | DEV orchestration | contains complete OSINT→Analyst→Socrates bounded loop | full-loop test + local run |
| `pipeline.py` | DELETE CANDIDATE | older DEV orchestration | subset of review_pipeline behavior; second orchestration path increases ambiguity | prove no required caller after full checkout |
| `transports/` | DEFER | protocol adapters | live transport is outside current DEV proof | PROD transport ADR later |
| `__init__.py` | KEEP | package API | exports current core collection contracts | import smoke test |
| `README.md` | KEEP / UPDATE AS NEEDED | maintenance | explains package responsibility and boundaries | documentation consistency review |

### Key finding: duplicate orchestration

`pipeline.py` implements `OSINT → Analyst → follow-up`, while `review_pipeline.py` implements the same chain plus Socrates. The current architecture needs only one canonical DEV orchestration path. Therefore `review_pipeline.py` is the primary candidate and `pipeline.py` is frozen as a deletion candidate until runtime/import inspection proves no required dependency remains.

## 4. `scripts/` audit

Current directory contains new DEV runners beside earlier prototype/experiment scripts.

| Path/group | Decision | WHY |
|---|---|---|
| `run_dev_osint.py` | KEEP DEV ONLY | direct collection smoke runner |
| `run_dev_pipeline.py` | CHANGE / MIGRATE | currently imports older `DevResearchPipeline`; should not define the canonical path if `review_pipeline.py` is approved |
| `deepseek_safe.py` | LEGACY / DEFER | predates current contract; no approved requirement currently depends on it |
| `hello_agent.py` | LEGACY | prototype/learning runner outside current FATHER chain |
| `monitor.py` | LEGACY / DEFER | operational monitoring not required for DEV contract proof |
| `rtx3060_agent.py` | LEGACY | hardware/model experiment outside current OSINT contract |
| `smart_agent.py` | LEGACY | earlier agent experiment; not an approved current dependency |
| other old scripts | LEGACY UNTIL PROVEN | explicit inclusion requires requirement + test |

No legacy script is deleted during static audit.

## 5. Root execution assets

| Path | Decision | WHY |
|---|---|---|
| `README.md` | KEEP | repository navigation and engineering governance entry point |
| `requirements.txt` | REVIEW BEFORE LOCAL RUN | may include dependencies for legacy and current code; current DEV minimum must be distinguished |
| `run.py` | LEGACY / DEFER | large earlier entry point, not part of approved FATHER OSINT DEV path |
| `start.ps1` | LEGACY / DEFER | earlier runtime launcher |
| `crash_analyzer.ps1` | LEGACY / DEFER | diagnostic utility not required by current acceptance criteria |
| `system_stress_test.ps1` | LEGACY / DEFER | old stress test not evidence for current contract |
| `system_test_results.txt` | HISTORICAL EVIDENCE | keep as historical artifact; must not be presented as current acceptance evidence |

## 6. `core/` audit

`core/` contains only the earlier prototype package: `agent_tracker.py`, `logger.py`, package init and README.

Decision: **LEGACY / NOT AN IMPLICIT DEPENDENCY**.

Potential reuse is not rejected forever, but current FATHER OSINT v1 has no approved requirement that needs these components. Reuse would require an explicit architecture decision rather than importing them because they already exist.

## 7. `services/llm-gateway/` audit

The service contains a substantially broader experimental LLM system (`api`, `core`, `enigma`, `simulation`, `sphinx`, policies and other assets).

Decision: **DEFER / SEPARATE EXPERIMENTAL SUBSYSTEM**.

Reason:

- OSINT DEV acceptance does not require an LLM gateway;
- Analyst and Socrates are deterministic DEV harnesses at this stage;
- pulling this service into the current path would reintroduce infrastructure and reasoning complexity before a requirement proves the need.

The service may become a donor/standalone component later, but it is not part of FATHER OSINT v1 acceptance.

## 8. `telegram_bridge/` and live transports

Decision: **DEFER / FROZEN**.

The logical `TelegramCollector` contract remains useful, but Node/MTProto/session/secrets infrastructure is explicitly outside current DEV acceptance. The bridge must not be required to run the current acceptance suite.

## 9. `data/` and `config/`

- `data/dev/*fixture*` → `KEEP DEV ONLY`: deterministic acceptance inputs.
- runtime-generated `data/osint*` → local execution output; should not become source-of-truth project documentation.
- legacy config/watchlists → `DEFER/LEGACY` until a current requirement references them.

## 10. Static dependency risks before cleanup

| Risk | Consequence | Required proof |
|---|---|---|
| old runner imports `pipeline.py` | deleting file breaks script | inspect/migrate runner, then local smoke run |
| hidden legacy imports from root scripts | cleanup breaks historical execution | full checkout import/search before deletion |
| requirements mix current and legacy libs | local environment becomes unnecessarily heavy | derive minimal DEV dependency set |
| experimental service looks production-ready due to directory size | accidental scope expansion | keep explicit DEFER labels |
| historical test results confused with current evidence | false confidence | current reports must name environment/date/commit |

## 11. Proposed canonical DEV runtime after verification

```text
scripts/run_dev_review_pipeline.py
        ↓
DevReviewPipeline
        ↓
OSINTAgent
        ↓
FixtureCollector(s)
        ↓
MaterialStore
        ↓
SimpleAnalyst
        ↓
SimpleSocrates
```

This is a proposal for cleanup, not permission to create the runner yet. First confirm Stage 04 tests and full-checkout dependency map.

## 12. Exit criteria for static audit

Before asking for local checkout:

- [x] identify canonical FATHER OSINT package;
- [x] classify main package files;
- [x] identify duplicate pipeline path;
- [x] isolate live Telegram transport from DEV acceptance;
- [x] classify legacy core/root/service groups;
- [ ] inspect complete test directory after latest changes;
- [ ] inspect requirements and determine DEV-minimum dependencies;
- [ ] inspect runner/import references to `pipeline.py` and `review_pipeline.py`;
- [ ] update repository navigation with Stage 06 status;
- [ ] write exact full local run plan.

No deletion occurs until these remaining items are closed and a full local run confirms the dependency picture.
