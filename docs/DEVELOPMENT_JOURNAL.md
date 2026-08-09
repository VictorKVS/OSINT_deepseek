# FATHER / OSINT_deepseek — Development Journal

**Purpose:** living engineering journal for the project.  
**Started:** 2026-08-09  
**Current stage:** **Stage 06 — Verification and Repository Rationalization**  
**Current milestone:** **M2 — Dependency and legacy cleanup gate**  
**Rule:** update this journal whenever a gate changes, a material defect changes the contract, an architectural decision changes, a component is added/removed, or the roadmap changes.

---

# 1. Engineering principle

FATHER development follows this chain:

```text
REQUIREMENT / ТЗ
      ↓
REQUIREMENTS REVIEW
      ↓
BUSINESS + PROCESS ANALYSIS
      ↓
ARCHITECTURE
      ↓
ARCHITECTURE REVIEW
      ↓
ACCEPTANCE TEST DESIGN
      ↓
IMPLEMENTATION PLAN
      ↓
CODE
      ↓
TEST / RUN
      ↓
VERIFICATION
      ↓
EXPERIENCE / KB
```

> **NO CODE BEFORE CONTRACT.**

A component is not justified because it is interesting or already exists. It must have an approved purpose, owner, input/output contract, test and WHY.

The journal records failed hypotheses and deferred experiments as well as successful changes.

---

# 2. Current product boundary

```text
Analyst
  │ ResearchTask
  ▼
OSINTAgent
  │
  ├─ FixtureCollector          [DEV]
  └─ TelegramCollector         [transport-neutral boundary]
  │
  ▼
Material / provenance
  ▼
MaterialStore
  ▼
MaterialPackage
  ▼
SimpleAnalyst                  [DEV simulator]
  ▼
SimpleSocrates                 [DEV simulator]
  │
  ├─ RESEARCH_MORE → ResearchTask → OSINT
  └─ PASS → DEV phase output

NOT YET IMPLEMENTED:
Knowledge Gate → KB → FATHER → Expert Agents
```

Responsibilities remain deliberately narrow:

```text
OSINT      = collect and preserve requested material
Analyst    = interpret material
Socrates   = review/challenge and request more evidence
KB stage   = future controlled publication
FATHER     = future consumer/distributor of approved knowledge
```

---

# 3. Repository disposition

| Area | Status | Meaning |
|---|---|---|
| `father_osint/` | **CURRENT DEV PRODUCT** | canonical current development package |
| `tests/` | **CURRENT VERIFICATION ASSETS** | executable contract evidence |
| `scripts/run_dev_osint.py` | **KEEP** | direct fixture OSINT runner |
| `scripts/run_dev_pipeline.py` | **KEEP / CANONICAL DEV RUNNER** | bounded OSINT→Analyst→Socrates runner |
| `.github/workflows/dev-verification.yml` | **KEEP / ACTIVE CI** | clean-checkout DEV baseline verification |
| `config/` | **DRAFT PROFILE/POLICY INPUTS** | design inputs, not automatic runtime truth |
| `data/dev/` | **TEST FIXTURES ONLY** | deterministic test data, not verified intelligence |
| `core/` | **LEGACY** | old observability/runtime prototype |
| old root/Ollama/GPU/PowerShell scripts | **LEGACY** | historical local runtime cluster |
| `services/llm-gateway/` | **FROZEN EXPERIMENTAL SUBPROJECT** | cognitive-policy prototype, not approved LLM gateway |
| `father_osint/transports/teleproto.py` | **EXPERIMENTAL / NOT APPROVED** | transport hypothesis only |
| live Telegram / Node bridge | **DEFERRED** | excluded from DEV acceptance |

---

# 4. Development history and WHY

## A — Practical FATHER split

**Problem:** early design discussion was drifting toward a universal expert/superintelligence system before a basic workflow existed.

**Decision:** cut back to the minimum useful production chain: OSINT → Analyst → Socrates.

**WHY:** each role becomes understandable, replaceable and testable. Deep identity/causality/knowledge machinery is added only when a concrete requirement demands it.

**Result:** PASS.

---

## B — Simplified DEV mode

**Decision:** prove workflow using fixtures and simple/public sources before battle-grade integrations.

Deferred from current acceptance:
- Telegram credentials;
- Tor/dark-web gateway;
- proxy rotation;
- distributed queues/databases;
- production scheduler;
- monitoring infrastructure;
- live LLM gateway.

**WHY:** infrastructure must not obscure whether the basic contracts work.

**Result:** PASS.

---

## C — Governance correction: NO CODE BEFORE CONTRACT

**Trigger:** files were being added faster than the technical specification and architecture were being validated.

**Decision:** stop feature expansion and introduce formal gates.

Added:
- project governance;
- OSINT ТЗ;
- business/process analysis;
- architecture views;
- formal architecture review;
- test design pack;
- implementation-review pack;
- traceability matrix;
- repository audits;
- directory READMEs.

**WHY:** avoid years of debugging a pile of mutually inconsistent files.

**Result:** PASS / permanent project rule.

---

## D — Architecture review found provenance defect

**Old behavior:** two sources containing identical text could collapse into one Material because content hash was treated as observation identity.

```text
Source A ─ same bytes X ─┐
                         ├─ WRONG → one observation
Source B ─ same bytes X ─┘
```

**Correct contract:** source observation and raw payload are different objects.

```text
Source A observation ─┐
                      ├─ hash X → raw/X.txt
Source B observation ─┘
```

**WHY:** repeated publication by independent sources is itself evidence/provenance and must not disappear.

**Process followed:** requirement correction → test correction → failing test → implementation plan → minimal fix.

**Result:** PASS.

---

## E — Test-before-fix storage correction

Initial focused run after correcting the test contract:

```text
7 tests
5 passed
2 failed
```

Both failures reproduced the expected storage/provenance defect.

Minimal implementation changed `father_osint/storage.py` only:
- preserve every Material/source observation;
- SHA-256-address raw text;
- reuse equal raw blobs;
- no database or semantic deduplication yet.

Regression:

```text
7/7 PASS
```

Later reconstructed current DEV slice:

```text
15/15 PASS
```

**Result:** PASS.

---

## F — Pipeline rationalization

**Problem:** two overlapping orchestration paths existed.

- old `pipeline.py` — OSINT↔Analyst;
- `review_pipeline.py` — OSINT→Analyst→Socrates.

**Process:** compare architecture → migrate runner → migrate tests → search dependencies → delete only after proof.

**Decision:** `review_pipeline.py` is canonical; old `pipeline.py` removed.

**WHY:** one bounded orchestration path is easier to verify and maintain.

**Result:** PASS.

---

## G — Legacy core/runtime audit

Reviewed old:
- `core/agent_tracker.py`;
- `core/logger.py`;
- `run.py`;
- Windows/PowerShell crash and stress tools;
- Ollama/RTX/local smart-agent scripts.

Useful concepts retained for future requirements:
- explicit agent execution traces;
- health checks;
- runtime supervision;
- crash evidence;
- resource protection;
- metrics/logging.

**Decision:** implementation remains legacy; concepts may later be redesigned behind explicit observability/runtime contracts.

Hidden model reasoning is not an observability requirement. Future traces record explicit inputs/actions/tool events/outputs/errors/timing/formal WHY only.

**Result:** AUDITED / cleanup pending M2.

---

## H — Experimental `services/llm-gateway` audit

**Finding:** despite the name, this is currently a cognitive-policy prototype:

```text
FastAPI
   ↓
Sphinx intent/risk heuristics
   ↓
Enigma YAML rules
   ↓
Judge
   ↓
ALLOW / DENY / QUARANTINE / SIMULATE
```

Problems:
- uncalibrated hand-written risk numbers;
- regex-based semantic judgments;
- duplicated policy engines;
- no true LLM provider routing/cost/fallback/token gateway behavior.

Useful future pattern:

```text
interpretation
   ↓
versioned deterministic policy
   ↓
decision + matched rule + reason + audit trail
```

**Decision:** FROZEN EXPERIMENT / NO CURRENT INTEGRATION.

**Result:** PASS as classification.

---

## I — Config/data audit

`high_technology_watchlist.yaml` mixes mission, topics, source classes, routing, escalation and governance.

**Decision:** treat it as a draft design/profile artifact, not one executable truth source.

Numbers such as `1.0`, `0.95`, `0.75` are **not confidence/trust values** until a calibration method and benchmark exist.

`data/dev/` is fixture data only.

> Fixture data proves program behavior, not truth about the external world.

**Result:** PASS as boundary definition.

---

## J — Component traceability review

Created `docs/06_verification/09_COMPONENT_TRACEABILITY_MAP.md`.

Current classification:

| Component | Status |
|---|---|
| `models.py` | DEV CORE |
| `agent.py` | DEV CORE |
| `storage.py` | DEV CORE |
| `collectors/dev.py` | TEST SUPPORT |
| `collectors/telegram.py` | DEV BOUNDARY |
| `analysis.py` | DEV SIMULATOR |
| `socrates.py` | DEV SIMULATOR |
| `review_pipeline.py` | DEV ORCHESTRATION |
| `transports/teleproto.py` | EXPERIMENTAL / NOT APPROVED |

**Conclusion:** the current risk is premature growth, not missing components.

**Result:** PASS.

---

## K — 2026-08-09: Clean-checkout Stage 06 verification

**Trigger:** previous 15/15 run proved a reconstructed DEV slice but did not prove actual clean repository checkout behavior.

**Stage:** Stage 06 / M1.

### CI infrastructure discovery

Earlier GitHub Actions runs failed before creating any job. The workflow was reduced to a minimal valid form. After correction, GitHub created and executed the job normally.

**Classification:** `ENV/CI`.

### First real clean-checkout execution

A fresh GitHub-hosted Ubuntu runner successfully completed:

```text
checkout                 PASS
Python 3.12              PASS
import father_osint      PASS
pytest collection        15 tests
pytest                   15/15 PASS
```

Then the runner failed:

```text
python scripts/run_dev_osint.py
ModuleNotFoundError: No module named 'father_osint'
```

**Classification:** `IMPL` — script entrypoint/import-path defect.

### Test-first response

Added `tests/test_runner_entrypoints.py` before correcting the scripts.

It permanently requires both canonical entrypoints to execute successfully from repository root:
- `scripts/run_dev_osint.py`;
- `scripts/run_dev_pipeline.py`.

### Minimal implementation correction

Both runner scripts now explicitly establish repository root before importing `father_osint`.

Static review also found an obsolete field reference in `run_dev_pipeline.py`:

```text
cycle.review.reasons   # stale / invalid
```

Current `SocratesReview` contract contains:

```text
issues
questions
```

The runner was corrected to the current domain contract rather than polluting the model with a compatibility field.

### Final clean-checkout result

Verified commit:

`aecbdbcf2dcb5bb9ea47d0edc6c0c670dc032b2c`

Environment:
- Ubuntu 24.04;
- CPython 3.12.13;
- pytest 9.1.1.

Evidence:

```text
father_osint import       PASS
17 tests collected
17 passed
0 failed
0 errors
run_dev_osint.py          PASS
run_dev_pipeline.py       PASS
```

DEV OSINT runner:

```text
materials=2
duplicates_skipped=0
errors=0
stop_reason=collectors_exhausted
```

Canonical review runner:

```text
pipeline_stop=review_passed
cycles=1
materials=2
socrates=PASS
```

The clean baseline required only Python + pytest. It did not require Ollama/GPU monitoring/Teleproto/Telegram credentials/Tor/legacy PowerShell/experimental LLM service.

Full evidence: `docs/06_verification/TEST_REPORT_004.md`.

**Decision:** **M1 PASS on a clean Linux checkout.**

**Not claimed:** production readiness, Windows-specific validation, live Telegram, Knowledge Gate or expert-quality Analyst/Socrates.

---

# 5. Decision register

| ID | Decision | WHY | Revisit when |
|---|---|---|---|
| J-001 | OSINT collects; Analyst interprets; Socrates reviews | narrow/testable responsibilities | concrete requirement proves boundary must change |
| J-002 | DEV before battle integrations | prove contracts without infrastructure noise | PROD requirements approved |
| J-003 | NO CODE BEFORE CONTRACT | prevent implementation-defined architecture | permanent governance rule |
| J-004 | Equal payload does not collapse observations | provenance must survive | stronger observation-identity contract approved |
| J-005 | Analyst/Socrates are DEV simulators | workflow proof precedes expert AI | evaluation data + expert requirements exist |
| J-006 | One canonical `review_pipeline.py` | reduce orchestration ambiguity | new orchestration requirement appears |
| J-007 | Teleproto is not approved by existence | transport requires donor/ADR/benchmark | live Telegram stage |
| J-008 | Legacy runtime is not current architecture | historical prototype solved different concerns | observability/runtime requirement appears |
| J-009 | `services/llm-gateway` frozen | not currently a justified LLM gateway | routing/control-plane requirement approved |
| J-010 | Config weights are not trust/confidence | values are uncalibrated | calibration methodology exists |
| J-011 | Fixtures never become KB evidence automatically | test data ≠ intelligence evidence | permanent provenance invariant |
| J-012 | Canonical runners must work from repo root | documented execution path must be reproducible | packaging model changes |
| J-013 | CI clean checkout is Stage 06 baseline evidence | reproducible fresh filesystem run removes reconstruction ambiguity | CI architecture changes |

---

# 6. Open issues

## V-01 — Windows-specific validation
Clean Linux checkout now passes. Windows-specific developer-machine behavior remains unverified. It is not currently a blocker for the logical DEV baseline, but should be checked before declaring cross-platform DEV v1.

## V-02 — Dependency model
Root `requirements.txt` still reflects legacy Ollama/GPU concerns. Current FATHER OSINT DEV baseline proved it needs only Python + pytest for verification.

## V-03 — Legacy cleanup
Legacy components are classified, but archive/delete actions must now be performed group-by-group with regression after each group.

## V-04 — CI maintenance warning
GitHub warns that third-party actions historically targeting Node 20 are being forced to Node 24. This is CI maintenance, not a FATHER application failure.

## V-05 — Production transports
No live Telegram transport is approved. Candidate selection requires current donor verification + ADR + benchmark.

## V-06 — Knowledge Gate
Intentionally absent. Its requirements, object model, review semantics and tests must be designed before implementation.

---

# 7. Roadmap

## M1 — Clean repository verification

**Status:** ✅ PASS on GitHub clean Linux checkout.

Evidence:
- import passes;
- 17 tests collect;
- 17/17 pass;
- both canonical DEV runners pass;
- legacy/experimental dependencies are not required.

Report: `docs/06_verification/TEST_REPORT_004.md`.

---

## M2 — Dependency and legacy cleanup gate

**Status:** ▶ CURRENT.

Sequence for each cleanup group:

```text
classify purpose
    ↓
search approved dependencies
    ↓
preserve useful requirement/experience
    ↓
archive/delete implementation
    ↓
clean-checkout CI regression
    ↓
journal result
```

Planned groups:
1. root dependency files;
2. `core/` legacy package;
3. old root/PowerShell runtime files;
4. old Ollama/GPU scripts;
5. frozen experimental services/transport placement review.

**Exit criterion:** current DEV product can be installed/read/run without accidental legacy dependencies or misleading launch paths.

---

## M3 — Documentation consistency

- all README files reflect actual post-cleanup structure;
- no deleted files remain in traceability/docs;
- dependency/install instructions show current DEV vs legacy separation;
- architecture diagrams and journal match the repository.

**Exit criterion:** a new engineer can understand the project without chat history.

---

## M4 — DEV v1 baseline freeze

- perform final clean checkout regression;
- optionally verify Windows developer execution;
- freeze current DEV contracts;
- record deferred items;
- create final DEV acceptance report;
- tag/record baseline.

**Exit criterion:** exact statement of what DEV v1 proves and does not prove.

---

## M5 — Select next requirement, not next technology

Possible future directions:
- Web/GitHub live collector;
- Telegram live transport;
- Analyst v1;
- Socrates v1;
- Knowledge Gate/KB contract;
- observability;
- production scheduling/security.

Selection requires a business need and ТЗ before implementation.

---

# 8. Journal update protocol

For each material event append/update using:

```markdown
## YYYY-MM-DD — [title]
**Stage:**
**Trigger/problem:**
**Decision:**
**WHY:**
**Files/documents affected:**
**Tests/evidence:**
**Result:** PASS / PARTIAL / REWORK / DEFERRED
**New risks/open questions:**
**Next action:**
```

Routine commits do not require an entry unless they change architecture, contract, gate, defect status or roadmap.

---

# 9. Current checkpoint — 2026-08-09

**Stage:** Stage 06  
**Milestone:** M2 — Dependency and legacy cleanup  
**Status:** **ACTIVE**

### Completed
- responsibility split;
- simplified DEV mode;
- governance and NO CODE BEFORE CONTRACT;
- ТЗ/business analysis/architecture/test packs;
- provenance contract correction;
- test-first storage fix;
- pipeline rationalization;
- legacy core/runtime audit;
- experimental policy service audit;
- config/data audit;
- current component traceability map;
- working GitHub clean-checkout CI;
- runner entrypoint acceptance tests;
- **17/17 clean-checkout tests PASS**;
- both canonical DEV runners PASS.

### Immediate next action
**Begin M2 with the dependency split: define minimal current DEV dependencies separately from legacy experimental dependencies, verify no current test/runner imports legacy packages, then rerun clean CI before any legacy deletion.**
