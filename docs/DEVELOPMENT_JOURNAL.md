# FATHER / OSINT_deepseek — Development Journal

**Purpose:** living engineering journal.  
**Started:** 2026-08-09  
**Current stage:** **Stage 07 — M5 Telegram Radar Requirements & Donor Verification**  
**Frozen baseline:** **DEV v1 / Stage 06 COMPLETE**  
**Current milestone:** **M5 — Telegram transport PoC preparation**  
**Rule:** update this journal whenever a gate, contract, architecture decision, material defect, component disposition, commercial/reuse opportunity or roadmap changes.

---

## 1. Permanent engineering rule

```text
REQUIREMENT / ТЗ
      ↓
COMMERCIAL + REUSE REVIEW
      ↓
REQUIREMENTS REVIEW
      ↓
BUSINESS + PROCESS ANALYSIS
      ↓
ARCHITECTURE
      ↓
COMMERCIAL + REUSE RECHECK
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
PRODUCT REGISTRY RECHECK
      ↓
EXPERIENCE / KB
```

> **NO CODE BEFORE CONTRACT.**

A component is not justified because it is interesting, fashionable or already present in the repository. It must have a concrete approved purpose, owner, input/output contract, acceptance evidence and WHY.

Commercial/reuse review is now a permanent gate. Before development starts we ask what other products can reuse the block, what low-cost metadata/interfaces should be preserved, what logic must remain product-specific, and whether a new commercial opportunity appears. The question is reopened during architecture review and after verification. A valid answer may be "no commercial change"; we do not add complexity merely to preserve hypothetical products.

---

## 2. Frozen DEV v1 product boundary

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
  ├─ RESEARCH_MORE → bounded follow-up ResearchTask
  └─ PASS → DEV phase output

NOT YET IMPLEMENTED:
Knowledge Gate → KB → FATHER → Expert Agents
```

Responsibilities remain narrow:
- **OSINT** collects and preserves requested material;
- **Analyst** interprets material;
- **Socrates** reviews/challenges and requests more evidence;
- **Knowledge Gate / KB / FATHER** remain future separately approved stages.

---

## 3. Current repository disposition

| Area | Status | Meaning |
|---|---|---|
| `father_osint/` | **DEV v1 BASELINE** | canonical frozen product package |
| `tests/` | **VERIFIED CONTRACT EVIDENCE** | 21-test clean-CI baseline |
| `scripts/run_dev_osint.py` | **KEEP** | direct DEV OSINT runner |
| `scripts/run_dev_pipeline.py` | **KEEP / CANONICAL** | bounded OSINT→Analyst→Socrates runner |
| `.github/workflows/dev-verification.yml` | **KEEP / ACTIVE** | clean-checkout verification |
| `config/` | **DRAFT INPUTS** | mission/profile/policy ideas, not calibrated truth |
| `data/dev/` | **TEST FIXTURES ONLY** | behavior evidence, never intelligence evidence |
| `father_osint/transports/` | **M5 EXTENSION BOUNDARY** | live implementation unapproved pending PoC/ADR |
| `docs/PRODUCT_OPPORTUNITY_REGISTRY.md` | **LIVING PRODUCT CONTROL** | commercial possibilities + mandatory reuse review |
| removed legacy/runtime/VIP/gateway/Teleproto code | **GIT HISTORY / AUDIT ONLY** | not current architecture |

---

## 4. Completed engineering decisions

### J-001 — Practical ecosystem split
OSINT collects, Analyst interprets, Socrates reviews. FATHER itself is not an oracle and does not answer from raw collection output.

### J-002 — DEV before battle integrations
Fixtures and deterministic local behavior are used to prove contracts before Telegram credentials, Tor, proxy rotation, schedulers, distributed storage, production secrets or LLM routing.

### J-003 — Provenance invariant
Equal payload does not collapse independent source observations. The same raw bytes may reuse one SHA-256-addressed blob while observations remain separately traceable.

### J-004 — Analyst/Socrates remain DEV simulators
They prove handoffs, gaps and bounded review cycles. They are not expert systems yet.

### J-005 — One orchestration path
`review_pipeline.py` is canonical. The older duplicate pipeline was retired only after tests/runners were migrated and regression evidence existed.

### J-006 — Legacy cleanup by evidence
Old `core/`, workstation/Ollama/GPU/PowerShell runtime, VIP prototype, experimental policy/"llm-gateway" and Teleproto/Node bridge were audited, useful lessons documented, then removed only after clean CI proved no current dependency.

### J-007 — No transport winner by existence
`TelegramCollector` keeps a transport-neutral protocol boundary. TDLib, GramJS or another implementation must later pass donor review, PoC, benchmark, security review and ADR.

### J-008 — Config values are not confidence
Uncalibrated numeric priorities in configuration cannot silently become trust/confidence scores.

### J-009 — Fixtures are not facts
Prepared fixture content proves program behavior only. It never becomes KB evidence automatically.

### J-010 — Cumulative research evidence
Follow-up review cycles analyze accumulated evidence from earlier cycles instead of forgetting prior source coverage.

### J-011 — Explicit payload reuse semantics
The misleading `duplicates_skipped` concept was replaced by payload-reuse semantics: observations survive; raw storage may be reused.

### J-012 — File provenance
File-only `Material` receives SHA-256 from original file bytes; missing file references fail explicitly.

### J-013 — Future reusable ingestion
Planned future Artifact/ingestion layer must support original preservation, pre-normalization hashing, real MIME/signature checks, audio/video/image/document routing and local-first processing. It is a roadmap item, not DEV v1 code.

### J-014 — Local-first transcription roadmap
Future FATHER must be capable of local transcription without third-party servers. External transcription services remain optional controlled fallbacks and require privacy review; sensitive/evidence material defaults to local processing.

### J-015 — M5 capability selection
After DEV v1 freeze, Telegram Radar was selected before Artifact/Ingestion, local transcription and Knowledge Gate because it converts the proven fixture-based OSINT contract into a useful live acquisition worker with the smallest architecture expansion.

Approved planning order:

```text
M5 Telegram Radar
      ↓
M6 Artifact / universal ingestion
      ↓
M7 Local transcription
      ↓
M8 Knowledge Gate
```

### J-016 — Fresh Telegram transport donor shortlist
Fresh official-source verification on 2026-08-10 replaced assumptions from the old donor matrix.

Current PoC shortlist:

```text
TDLib   → POC-1 / primary
GramJS  → POC-2 / explicit activity-risk comparison
```

Non-finalists:
- **Telethon:** GitHub upstream archived 2026-02-21 and points to a new upstream; the new upstream still requires separate SOURCE_VERIFIED review before it can return to the shortlist.
- **Pyrogram:** archived and explicitly no longer maintained/supported.
- **Hydrogram:** not shortlisted because the verified release evidence found was too old for a 2026 production shortlist without deeper freshness/security proof.

Important correction: the earlier donor notes claimed a 2026 GramJS release cadence including `3.0.0`. Fresh official GitHub verification did **not** reproduce that claim; the retrieved repository page lists GitHub release `v2.17.4` dated 2023-05-14. Therefore GramJS remains useful for a PoC because its MTProto/session/API model is simple, but carries a material maintenance/freshness question.

Detailed evidence: `docs/07_next_requirement/03_TELEGRAM_TRANSPORT_DONOR_RESEARCH_2026-08-10.md`.

### J-017 — Commercial/reuse review becomes a permanent engineering gate
Every requirement and material architecture change must now be reviewed for reusable product value **before implementation**, then revisited during architecture review and after verification/baseline freeze.

Questions include:
- which current/future products can reuse this block;
- what low-cost metadata or interfaces are worth preserving now;
- what domain-specific logic must remain outside reusable core;
- whether technology choice creates commercial lock-in;
- whether a new opportunity should be added to the product registry;
- whether existing star priorities should be raised, lowered or retired.

This does **not** authorize speculative overengineering. Primary requirement and simplicity remain dominant.

Control document: `docs/PRODUCT_OPPORTUNITY_REGISTRY.md`.

---

## 5. DEV v1 verification result

Clean GitHub-hosted Linux checkout proves:

```text
checkout                  PASS
Python 3.12               PASS
import father_osint       PASS
21 tests collected        PASS
21 tests executed         PASS
run_dev_osint.py          PASS
run_dev_pipeline.py       PASS
```

Semantic acceptance includes provenance preservation, payload reuse without dropping observations, file SHA-256, explicit missing-file failure, cumulative bounded follow-up research, collector failure isolation and a transport-neutral Telegram collector.

Detailed evidence lives in `docs/06_verification/` and `docs/journal/`.

---

## 6. Stage 06 closure

- **M1 Clean repository verification — PASS**
- **M2 Dependency and legacy cleanup — PASS**
- **M3 Documentation consistency — PASS**
- **M4 DEV v1 baseline freeze — PASS**

The baseline remains frozen while M5 extends it through a separately reviewed requirement.

---

## 7. Current Stage 07 / M5 — Telegram Radar

Planning records:
- `docs/07_next_requirement/01_M5_CAPABILITY_PRIORITY.md`
- `docs/07_next_requirement/02_TELEGRAM_RADAR_REQUIREMENTS_V0_1.md`
- `docs/07_next_requirement/03_TELEGRAM_TRANSPORT_DONOR_RESEARCH_2026-08-10.md`
- `docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`
- `docs/07_next_requirement/05_TELEGRAM_IMPLEMENTATION_PATTERN_REVIEW_2026-08-10.md`

M5 business requirement:

> FATHER OSINT shall collect requested public Telegram channel material through a replaceable approved transport and return provenance-preserving `Material` records with bounded execution and explicit failures.

Commercial/reuse implications already identified for M5 include Competitive & Channel Intelligence, Content Origin & Propagation Analytics, Brand/Reputation Monitoring, Technology/Market Radar, Source/Channel Quality Analytics and later controlled Risk Intelligence. These opportunities justify preserving stable IDs, timestamps, edit/forward/reply metadata, source locator and content hashes where doing so does not complicate the primary collection contract.

Current gate:

```text
requirements              PASS / draft approved direction
   ↓
commercial/reuse review   PASS / registry opened
   ↓
donor SOURCE_VERIFIED     PASS for shortlist
   ↓
TDLib PoC + GramJS PoC    ← NEXT
   ↓
identical benchmark
   ↓
security/operations review
   ↓
ADR transport selection
   ↓
commercial/reuse recheck
   ↓
acceptance tests
   ↓
implementation plan
   ↓
production-path code
```

No concrete Telegram transport is APPROVED yet.

### PoC acceptance focus

Both candidates must prove the same scenario:
- secrets/session material outside repository;
- tiny allow-listed public source set;
- stable source/message identifiers;
- restart/checkpoint behavior;
- explicit FloodWait/429 behavior;
- per-source isolation/timeouts;
- session data never emitted in normal logs;
- compatibility with existing `TelegramCollector` contract;
- frozen 21-test DEV v1 regression stays green.

---

## 8. Open future requirements — not current defects

1. **Artifact/Ingestion layer (M6)** — file/media/document normalization and evidence preservation.
2. **Local transcription (M7)** — offline/local-first acceptance; external service registry as controlled fallback.
3. **Knowledge Gate (M8)** — separate domain model, review semantics and tests.
4. **Expert Analyst/Socrates** — evaluation corpus, quality metrics and explicit expert requirements.
5. **Production observability/runtime supervision** — redesign from retained lessons, not legacy restoration.
6. **Windows-specific verification** — required before cross-platform production claims.

---

## 9. Current roadmap

Current action: **execute two bounded Telegram transport PoCs, starting with TDLib, without modifying frozen DEV v1 contracts.**

Every subsequent requirement starts with the commercial/reuse gate before architecture and code.

---

## 10. Journal update template

```text
Date
Stage / milestone
Trigger / problem
Decision
WHY
Commercial / reuse review
Files/components affected
Acceptance test / evidence
Result: PASS / PARTIAL / REWORK / DEFERRED
New risks
Registry changes
Next action / next reuse-review gate
```

Small formatting-only commits do not require a separate architectural journal entry.
