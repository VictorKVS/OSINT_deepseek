# FATHER / OSINT_deepseek — Development Journal

**Purpose:** living engineering journal for the project.  
**Started:** 2026-08-09  
**Current stage:** **Stage 06 — Verification and Repository Rationalization**  
**Rule:** update this journal whenever a gate is passed, a material architectural decision changes, a defect changes the contract, a component is added/removed, or the next plan changes.

---

## 1. Why this journal exists

The project is deliberately being developed under the FATHER engineering principle:

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

The journal prevents the project from becoming a pile of code whose purpose is remembered only by its author. It records **what changed, why it changed, what evidence exists, what is still unverified, and what comes next**.

This is not a marketing changelog. Failed hypotheses, deferred experiments and deleted code are part of the engineering history and remain visible.

---

# 2. Executive status

## Current product boundary

```text
Analyst
  │ ResearchTask
  ▼
OSINTAgent
  │
  ├─ Collectors
  │    ├─ DEV FixtureCollector
  │    └─ TelegramCollector contract
  │
  ▼
Material / provenance
  ▼
MaterialStore
  ▼
MaterialPackage
  ▼
SimpleAnalyst       [DEV simulator]
  ▼
SimpleSocrates      [DEV simulator]
  │
  ├─ RESEARCH_MORE → ResearchTask → OSINT
  └─ PASS → DEV phase output

Future, NOT YET IMPLEMENTED:
Knowledge Gate → KB → FATHER → Expert Agents
```

## Current repository disposition

| Area | Status | Meaning |
|---|---|---|
| `father_osint/` | **CURRENT DEV PRODUCT** | canonical current development package |
| `tests/` | **CURRENT VERIFICATION ASSETS** | executable contract evidence |
| `scripts/run_dev_osint.py` | **KEEP** | direct DEV OSINT runner |
| `scripts/run_dev_pipeline.py` | **KEEP / CANONICAL DEV RUNNER** | bounded OSINT→Analyst→Socrates runner |
| `config/` | **DRAFT PROFILE/POLICY INPUTS** | not automatic runtime truth |
| `data/dev/` | **TEST FIXTURES ONLY** | deterministic test data, not verified intelligence |
| `core/` | **LEGACY** | old observability/runtime prototype |
| old root/runtime scripts | **LEGACY** | old Ollama/GPU/Windows prototype cluster |
| `services/llm-gateway/` | **FROZEN EXPERIMENTAL SUBPROJECT** | actually a cognitive policy prototype, not approved LLM gateway |
| `father_osint/transports/teleproto.py` | **EXPERIMENTAL / NOT APPROVED** | one transport hypothesis only |
| live Telegram / Node bridge | **DEFERRED** | excluded from current DEV acceptance |

---

# 3. Development history

## Phase A — Initial OSINT/FATHER concept

### Goal
Turn the earlier OSINT prototype into a worker inside a larger FATHER Knowledge Factory.

### Key separation adopted

```text
OSINT      = finds and preserves requested materials
Analyst    = interprets collected materials
Socrates   = challenges/weighs the analysis and requests more evidence
KB stage   = future controlled publication of reviewed knowledge
FATHER     = consumes/distributes knowledge; it is not the source collector itself
```

### Why
Earlier discussion was drifting toward a universal expert/superintelligence model. That created unnecessary identity graphs, causality theory and highly detailed epistemic machinery before the basic workflow existed. The architecture was deliberately cut back using an Occam-style minimum necessary for the actual task.

**Decision:** build a practical factory chain first; deepen any stage only when a concrete requirement justifies it.

---

## Phase B — First DEV implementation

### Added
- `father_osint/models.py`
- `father_osint/agent.py`
- `father_osint/storage.py`
- DEV collectors/fixtures
- Telegram collector boundary
- deterministic `SimpleAnalyst`
- deterministic `SimpleSocrates`
- bounded review pipeline
- DEV runner scripts
- tests

### Intended purpose
Prove handoffs and contracts without production infrastructure.

### DEV principle
No live Telegram credentials, Tor, proxy rotation, distributed databases, production scheduler or battle monitoring are required merely to prove the workflow.

---

## Phase C — Project governance correction: NO CODE BEFORE CONTRACT

### Problem discovered
Implementation was growing faster than the project specification. This would eventually create large debugging and refactoring debt.

### Decision
Feature development was paused and the project was reorganized around formal gates.

### Added project-control artifacts
- `docs/PROJECT_GOVERNANCE.md`
- `docs/OSINT_AGENT_TZ_V1.md`
- architecture review pack
- business/process analysis
- acceptance-test pack
- implementation plan pack
- traceability matrix
- repository audit documentation
- README files for major directories

### Engineering rule adopted

> **NO CODE BEFORE CONTRACT.**

A new component must answer:
1. Which requirement needs it?
2. Which architecture boundary owns it?
3. What enters it?
4. What leaves it?
5. Why is the simpler existing mechanism insufficient?
6. Which acceptance test proves it?

---

## Phase D — Stage 03: Architecture and business-process review

### What was reviewed
The system was analyzed as a business/information process rather than only as Python classes:
- actors;
- inputs and outputs;
- SIPOC/value-chain reasoning;
- system context;
- sequence/data flows;
- failure paths;
- DEV/PROD boundary;
- responsibilities and WHY for each stage.

### Core architecture retained

```text
ResearchTask
   ↓
OSINTAgent
   ↓
Collectors
   ↓
Material
   ↓
MaterialStore
   ↓
MaterialPackage
   ↓
Analyst
   ↓
Socrates
```

### Major architecture defect discovered
The original storage behavior treated identical content hashes as if they represented the same source observation.

Example:

```text
Source A ── same text X ─┐
                         ├─ old behavior → one Material
Source B ── same text X ─┘
```

That destroyed provenance.

### Contract correction
A **source observation** and a **raw payload** are different things.

Correct model:

```text
Source A observation ─┐
                      ├─ content_hash X → raw/X.txt
Source B observation ─┘
```

Equal bytes may share one raw blob, but separate observations must remain separate records.

### Why this mattered
This became the first practical demonstration of the FATHER process: architecture review changed the requirement before implementation was patched.

---

## Phase E — Stage 04: Test design before fix

### Work completed
Existing tests were reviewed against acceptance criteria before production code was changed.

### Important finding
An old test encoded the same incorrect assumption as the old storage implementation: identical text from two sources was expected to collapse to one Material.

### Decision
The test contract was corrected first.

### Added/clarified acceptance behavior
- preservation of provenance across identical payloads;
- restart semantics;
- collector isolation;
- `max_items` behavior;
- missing collector behavior;
- deterministic fixtures;
- bounded OSINT→Analyst→Socrates loop;
- transport-neutral Telegram collector boundary.

### First focused run

```text
7 tests
5 passed
2 failed
```

Both failures reproduced the storage/provenance defect expected from the reviewed architecture.

---

## Phase F — Stage 05: Minimal implementation correction

### Alternatives considered
The storage fix was treated as an implementation decision, not an improvised patch.

### Selected minimal solution
- preserve every Material/source observation;
- content-address raw text by SHA-256;
- reuse an existing raw blob when bytes are equal;
- do not introduce a database or semantic-dedup engine yet.

### Production file changed
`father_osint/storage.py` only.

### Focused regression

```text
7 tests
7 passed
0 failed
```

### Later reconstructed DEV slice verification

```text
15 tests collected
15 passed
0 failed
```

**Important limitation:** this was not yet a complete local checkout verification of every historical repository asset. It proved the current DEV slice, not the entire legacy repository environment.

---

## Phase G — Pipeline rationalization

### Problem
Two overlapping orchestration paths existed:
- older `pipeline.py` — OSINT↔Analyst loop;
- `review_pipeline.py` — OSINT→Analyst→Socrates loop.

### Process followed
1. architecture comparison;
2. test comparison;
3. migrate `run_dev_pipeline.py`;
4. migrate pipeline tests;
5. search for remaining canonical references;
6. only then delete the redundant pipeline.

### Result
`father_osint/pipeline.py` was removed.

`father_osint/review_pipeline.py` is now the canonical bounded DEV orchestration path.

### Why
This was the first cleanup performed through evidence rather than aesthetic preference.

---

## Phase H — Legacy core audit

### `core/agent_tracker.py`
Useful ideas found:
- trace ID;
- agent/tool activity;
- failures;
- duration;
- result statistics.

### Decision
Legacy implementation is not part of current FATHER OSINT. The concept is retained for a future explicit observability contract.

Do **not** preserve or attempt to expose hidden model reasoning. Future traces should record explicit inputs, actions, tool events, outputs, errors, timing and formal WHY fields only.

### `core/logger.py`
Found to mix system CPU/RAM/GPU monitoring with logging.

### Decision
Legacy implementation is deferred/cleanup candidate. Future logs/metrics must be designed separately from OSINT domain behavior.

---

## Phase I — Legacy runtime audit

Reviewed:
- `run.py`
- `start.ps1`
- `crash_analyzer.ps1`
- `system_stress_test.ps1`
- old `scripts/smart_agent.py`
- `monitor.py`
- `rtx3060_agent.py`
- `deepseek_safe.py`
- `hello_agent.py`

### Finding
These form an older local Ollama/RTX3060/Windows runtime experiment. They are not the present OSINT product architecture.

### Useful experience retained
- health checks;
- runtime supervision;
- crash evidence;
- resource protection;
- observability.

### Decision
Preserve as legacy until final cleanup gate; do not allow them to drive current dependencies or architecture.

---

## Phase J — `services/llm-gateway/` audit

### Finding
Despite the name, the subsystem is not currently an LLM provider gateway. It is a cognitive policy prototype:

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

### Risks found
- manually assigned, uncalibrated risk values;
- regex-driven semantic claims;
- duplicated policy logic (`Enigma` and another policy engine);
- no real provider routing/cost/fallback/token-management gateway behavior.

### Useful pattern retained

```text
interpretation
   ↓
deterministic versioned policy
   ↓
decision + reason + matched rule + audit trail
```

### Decision
**FROZEN EXPERIMENTAL SUBPROJECT / NO CURRENT INTEGRATION.**

---

## Phase K — Config and data audit

### `config/high_technology_watchlist.yaml`
Found to combine several concepts:
- mission profile;
- topic priorities;
- source classes;
- signal classes;
- future KB routing;
- escalation policy;
- output governance.

### Decision
Treat as a design/profile artifact, not one executable truth source.

The numeric values such as `1.0`, `0.95`, `0.75`, source priorities, etc. are **not calibrated confidence/trust scores**. They may represent provisional attention priorities only until a requirement and measurement method exist.

### `data/dev/`
Confirmed as deterministic fixture data.

### Invariant

> Fixture data proves software behavior, not truth about the external world.

DEV fixture content must never silently enter a future Knowledge Base as verified intelligence.

---

## Phase L — Current `father_osint/` component traceability review

A formal component map was created in:

`docs/06_verification/09_COMPONENT_TRACEABILITY_MAP.md`

### Current classification

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

### Current architectural conclusion
The current core is sufficiently small. The largest near-term risk is **premature growth**, not lack of components.

---

# 4. Important decisions and reasons

| ID | Decision | WHY | Revisit when |
|---|---|---|---|
| J-001 | OSINT collects; Analyst interprets; Socrates reviews | keeps responsibilities narrow and testable | concrete evidence requires boundary change |
| J-002 | DEV before battle-grade integrations | proves contracts without secrets/infrastructure noise | DEV acceptance passes and PROD requirements exist |
| J-003 | No code before contract | prevents architecture from being invented in implementation | never; this is project governance |
| J-004 | Preserve source observations even for equal payloads | provenance is intelligence evidence | only if a stronger observation identity model is specified |
| J-005 | Analyst/Socrates remain deterministic DEV simulators | current goal is workflow proof, not expert AI | expert requirements and evaluation datasets exist |
| J-006 | `review_pipeline.py` is canonical; old `pipeline.py` deleted | one bounded orchestration path is simpler | only if a new orchestration requirement appears |
| J-007 | Teleproto is not approved by existence | transport must pass donor/ADR/benchmark process | live Telegram stage |
| J-008 | Legacy core/runtime is not current architecture | old prototype addressed different local runtime concerns | future observability/runtime-supervision requirements |
| J-009 | `services/llm-gateway` frozen | current code is policy prototype, not justified gateway dependency | approved LLM routing/control-plane requirement |
| J-010 | Config weights are not confidence/trust | values are uncalibrated | benchmark/calibration methodology exists |
| J-011 | Fixtures never become KB evidence automatically | test data and intelligence evidence are different classes | never; provenance separation remains mandatory |

---

# 5. Known open issues / uncertainties

## V-01 — Full local repository verification still required
Focused/current DEV-slice tests have passed, but a complete clean local checkout must still prove:
- imports;
- test collection;
- full `pytest`;
- canonical DEV runners;
- absence of accidental legacy dependencies;
- behavior after legacy cleanup.

## V-02 — GitHub Actions currently unreliable/unresolved
Earlier CI attempts failed before useful Python job evidence was produced. Treat this as CI configuration/environment work, not as proof that the DEV code fails.

## V-03 — Root dependency model is still polluted by legacy needs
Ollama/GPU/monitoring dependencies historically present in root requirements are not automatically justified for the current pure-Python DEV core.

## V-04 — Legacy deletion gate not complete
Legacy files have been classified but should not be mass-deleted until a full checkout dependency scan and archival decision are completed.

## V-05 — Production source transports not selected
Telegram live transport remains an experimental decision. TDLib/other candidates require their own current donor verification and benchmark before approval.

## V-06 — No Knowledge Gate yet
This is intentional. KB publication logic must not be added until its requirements, object model, review semantics and acceptance tests are approved.

---

# 6. Forward plan

## Milestone M1 — Complete Stage 06 repository verification

**Goal:** prove what the repository actually needs before further cleanup or features.

Sequence:

```text
clean local checkout
    ↓
record Python/environment snapshot
    ↓
python import check
    ↓
pytest --collect-only
    ↓
full pytest
    ↓
run_dev_osint.py
    ↓
run_dev_pipeline.py
    ↓
search imports/references to legacy cluster
    ↓
TEST_REPORT_004
```

**Exit criteria:** reproducible evidence showing which current components pass and which failures are code/test/environment/legacy issues.

---

## Milestone M2 — Dependency and legacy cleanup gate

Only after M1:

- separate current DEV requirements from legacy experimental dependencies;
- decide archive vs delete for `core/`;
- decide archive vs delete for old root/PowerShell/Ollama scripts;
- preserve useful engineering lessons in docs before deleting implementations;
- rerun full regression after each cleanup group.

**Exit criteria:** canonical project path can be understood and run without accidental legacy dependencies.

---

## Milestone M3 — Documentation consistency pass

- root README must reflect current stage, not historical Stage 03;
- docs index must match actual completed cleanup/migrations;
- every active directory README must identify owner, status, input/output and current gate;
- traceability matrix must point to current files only.

**Exit criteria:** a new engineer can determine the current product path without reading chat history.

---

## Milestone M4 — Freeze DEV v1 baseline

After Stage 06 passes:

- tag/record a DEV v1 baseline;
- create final DEV acceptance report;
- freeze canonical contracts (`ResearchTask`, `Material`, `MaterialPackage`);
- record explicit deferred items.

**Exit criteria:** we know exactly what DEV v1 proves and what it does not prove.

---

## Milestone M5 — Choose next requirement, not next technology

Possible next work must be selected by business need. Candidate directions include:
- real Web/GitHub collector;
- live Telegram transport;
- Analyst v1;
- Socrates v1;
- Knowledge Gate/KB contract;
- observability;
- production scheduling/security.

Before choosing, write the requirement and business reason. Do not activate a technology simply because code already exists.

---

# 7. Journal update protocol

For every material development event append an entry using this template:

```markdown
## YYYY-MM-DD — [short title]

**Stage:**  
**Trigger / problem:**  
**Decision:**  
**WHY:**  
**Files/documents affected:**  
**Tests/evidence:**  
**Result:** PASS / PARTIAL / REWORK / DEFERRED  
**New risks/open questions:**  
**Next action:**
```

A normal code commit does not need a journal entry unless it changes architecture, a contract, a gate, a major defect status or the roadmap.

---

# 8. Current journal checkpoint — 2026-08-09

**Stage:** Stage 06 — Verification and Repository Rationalization  
**Result:** **IN PROGRESS**

### Done
- FATHER responsibility split established.
- DEV simplified mode established.
- project governance and NO CODE BEFORE CONTRACT adopted.
- ТЗ and architecture/business-analysis packs created.
- storage/provenance defect discovered through architecture review.
- acceptance tests corrected before implementation.
- minimal storage fix implemented and focused regression passed.
- current DEV slice reached 15/15 focused tests in reconstructed verification.
- canonical review pipeline selected; redundant old pipeline removed after dependency migration.
- legacy `core/` audited.
- legacy runtime/Ollama/RTX scripts audited.
- experimental policy/"LLM gateway" subsystem audited and frozen.
- config/data boundaries audited.
- current `father_osint/` component traceability map created.

### Not done yet
- complete clean local checkout verification;
- final dependency split;
- evidence-based legacy archive/delete pass;
- stable CI;
- DEV v1 baseline/tag;
- PROD source transport selection;
- Knowledge Gate/KB implementation.

### Immediate next action
**Run/prepare the complete Stage 06 verification on a clean local checkout, produce the next full test report, then perform evidence-based dependency/legacy cleanup.**
