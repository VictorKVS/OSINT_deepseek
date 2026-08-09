# Stage 03 — Formal Architecture Review

**Status:** OPEN  
**Decision:** PASS is not granted yet.

This document is the architecture gate. It is deliberately stricter than a design note: every significant component and information flow must be justified by approved requirements and business value before test design starts.

## 1. Review dimensions

| Dimension | Question | Current assessment |
|---|---|---|
| Business fit | Does the structure solve the stated research-supply problem? | PARTIAL PASS |
| Role separation | Are OSINT, Analyst and Socrates responsibilities distinct? | PASS conceptually |
| Contract completeness | Are inputs/outputs sufficient and explicit? | REVIEW REQUIRED |
| Simplicity | Is anything present without demonstrated need? | REVIEW REQUIRED |
| Failure behavior | Are failures visible and bounded? | PARTIAL PASS |
| DEV/PROD separation | Is production complexity deferred? | PASS conceptually |
| Traceability | Can every component be mapped to requirement/test? | INCOMPLETE |
| Legacy isolation | Is old code prevented from becoming implicit architecture? | PARTIAL PASS |
| Technology neutrality | Are unapproved technologies avoided in logical design? | PASS with exceptions |
| Operability | Can a maintainer understand what happens and why? | IMPROVING |

## 2. Component review

### `models.py`

**Purpose:** stage contracts.  
**Architecture question:** does it contain only information needed across stage boundaries?

Review actions:

- validate every `ResearchTask` field against ТЗ;
- classify each field as REQUIRED / OPTIONAL / REMOVE;
- confirm `Material` does not contain Analyst/Socrates judgments;
- confirm `MaterialPackage` exposes collection gaps and stop cause.

**Gate status:** OPEN.

### `agent.py`

**Purpose:** bounded collector orchestration.  
**Required behaviors:** collector eligibility, item limits, error isolation, packaging, storage handoff.

**Concern:** orchestration must not silently evolve into source analysis or production scheduler logic.

**Gate status:** REVIEW AGAINST TESTABLE REQUIREMENTS.

### `collectors/`

**Purpose:** source acquisition boundary.

`FixtureCollector` is justified by DEV strategy. `TelegramCollector` is a contract experiment. No production source transport is required for Stage 3 acceptance.

**Gate status:** KEEP DEV fixture; DEFER production transport decision.

### `storage.py`

**Purpose:** inspectable DEV persistence and exact deduplication.

**Questions:**

- why must task/package records also be stored here, if they are?
- which data is canonical versus derived?
- what is the expected behavior after process restart?

**Gate status:** OPEN.

### `analysis.py` / `socrates.py`

These exist to prove handoffs, not to establish final expert algorithms.

**Architecture risk:** repository scope creep from "OSINT worker" into the whole Knowledge Factory.

**Decision candidate:** retain as DEV harness, clearly mark as non-production and outside core OSINT ownership.

### `pipeline.py` / `review_pipeline.py`

**Problem:** overlapping orchestration paths are already visible.

Before any extension:

```text
KEEP one / MERGE / DELETE one / justify two separate use cases
```

No decision is allowed based merely on which file was written first.

### `transports/` and `telegram_bridge/`

Experimental. Architecture review does not approve Teleproto, Node.js, MTProto session management or production Telegram integration.

**Gate status:** DEFER / FROZEN.

### legacy `core/`, `services/`, old scripts

Must remain outside FATHER OSINT v1 unless a requirement and acceptance test explicitly pull them in.

**Gate status:** LEGACY / NOT IN CURRENT ARCHITECTURE.

## 3. Flow review

Each flow must be explainable as `source → object → destination → reason`.

| Flow | Object | Why it exists | Review |
|---|---|---|---|
| Analyst → OSINT | ResearchTask | bounded explicit research order | KEEP, verify fields |
| OSINT → Collector | ResearchTask / source scope | execute source-specific acquisition | KEEP |
| Collector → OSINT | Material / error | normalize acquisition result | KEEP |
| OSINT → Store | Material | preserve inspectable research material | KEEP, verify ownership |
| OSINT → Analyst | MaterialPackage | complete delivery incl. errors/gaps | KEEP |
| Analyst → OSINT | follow-up ResearchTask | fill material gaps | KEEP, bounded |
| Analyst → Socrates | Analysis | independent review | DEV harness / wider factory boundary |
| Socrates → OSINT | targeted follow-up via ResearchTask | collect missing evidence | KEEP conceptually, ownership review |

## 4. Architecture anti-pattern checks

The review must reject the architecture if it finds:

- a component with no requirement owner;
- a database/framework chosen before workload/contract evidence;
- two modules doing the same job without explicit use cases;
- hidden context required to understand an interface;
- production credentials/infrastructure needed to run DEV acceptance;
- analysis/truth logic embedded in source collectors;
- silent collector failures;
- infinite or unbounded agent loops;
- undocumented legacy dependencies;
- "future flexibility" used as the only reason for extra abstraction.

## 5. Risk register for this gate

| ID | Risk | Severity | Required action before PASS |
|---|---|---|---|
| AR-01 | contracts may reflect code rather than approved need | HIGH | field-by-field contract review |
| AR-02 | duplicate pipeline implementations | MEDIUM | choose/justify/merge after behavior comparison |
| AR-03 | Analyst/Socrates scope may blur repository ownership | MEDIUM | document package boundary |
| AR-04 | experimental Telegram code may be mistaken for approved | HIGH | keep frozen/deferred labels |
| AR-05 | traceability incomplete | HIGH | map each KEEP component to requirement + planned test |
| AR-06 | legacy components may be accidentally reused | MEDIUM | explicit inclusion rule |
| AR-07 | DEV storage semantics not fully specified | MEDIUM | define persistence/dedup/restart expectations |

## 6. Required decisions before Stage 3 PASS

- [ ] approve or change the business boundary;
- [ ] approve the actor/responsibility matrix;
- [ ] review `ResearchTask` field by field;
- [ ] review `Material` field by field;
- [ ] review `MaterialPackage` field by field;
- [ ] decide fate of `pipeline.py` vs `review_pipeline.py`;
- [ ] decide whether Analyst/Socrates code remains here as DEV harness;
- [ ] define exact DEV storage responsibility;
- [ ] update Traceability Matrix with all components marked KEEP/CHANGE/DELETE/DEFER;
- [ ] ensure every KEEP item has a Stage 4 acceptance test to be written.

## 7. Stage 3 exit criterion

Architecture review passes only when:

```text
Approved business need
        ↓
Approved information flows
        ↓
Approved component responsibilities
        ↓
Approved contracts
        ↓
Known risks + deferred decisions
        ↓
Traceable test obligations
```

At that point Stage 4 may design tests. Until then, no new feature code should be added.
