# FATHER / OSINT_deepseek — Development Journal

**Purpose:** living engineering journal.  
**Started:** 2026-08-09  
**Current stage:** **DEV v1 BASELINE FROZEN**  
**Previous stage:** **Stage 06 — Verification and Repository Rationalization / COMPLETE**  
**Current milestone:** **M5 — choose the next approved business requirement**  
**Rule:** update this journal whenever a gate, contract, architecture decision, material defect, component disposition or roadmap changes.

---

## 1. Permanent engineering rule

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

A component is not justified because it is interesting, fashionable or already present in the repository. It must have a concrete approved purpose, owner, input/output contract, acceptance evidence and WHY.

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
| `father_osint/` | **DEV v1 BASELINE** | canonical current product package |
| `tests/` | **VERIFIED CONTRACT EVIDENCE** | 21-test clean-CI baseline |
| `scripts/run_dev_osint.py` | **KEEP** | direct DEV OSINT runner |
| `scripts/run_dev_pipeline.py` | **KEEP / CANONICAL** | bounded OSINT→Analyst→Socrates runner |
| `.github/workflows/dev-verification.yml` | **KEEP / ACTIVE** | clean-checkout verification |
| `config/` | **DRAFT INPUTS** | mission/profile/policy ideas, not calibrated truth |
| `data/dev/` | **TEST FIXTURES ONLY** | behavior evidence, never intelligence evidence |
| `father_osint/transports/` | **FUTURE BOUNDARY** | no live Telegram transport approved |
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
Follow-up review cycles now analyze accumulated evidence from earlier cycles instead of forgetting prior source coverage.

### J-011 — Explicit payload reuse semantics
The misleading `duplicates_skipped` concept was replaced by payload-reuse semantics: observations survive; raw storage may be reused.

### J-012 — File provenance
File-only `Material` receives SHA-256 from original file bytes; missing file references fail explicitly.

### J-013 — Future reusable ingestion
Planned future Artifact/ingestion layer must support original preservation, pre-normalization hashing, real MIME/signature checks, audio/video/image/document routing and local-first processing. It is a roadmap item, not current DEV v1 code.

### J-014 — Local-first transcription roadmap
Future FATHER must be capable of local transcription without third-party servers. External transcription services remain optional controlled fallbacks and require privacy review; sensitive/evidence material defaults to local processing.

---

## 5. Stage 06 verification result

Clean GitHub-hosted Linux checkout currently proves:

```text
checkout                  PASS
Python 3.12               PASS
import father_osint       PASS
21 tests collected        PASS
21 tests executed         PASS
run_dev_osint.py          PASS
run_dev_pipeline.py       PASS
```

Semantic acceptance includes:
- source provenance survives equal payloads;
- raw payload reuse is explicit;
- local files are hashed from original bytes;
- missing files fail visibly;
- evidence accumulates across bounded follow-up cycles;
- loops remain hard bounded;
- collector failure is isolated and visible;
- Telegram collector remains transport-neutral.

Detailed evidence lives in `docs/06_verification/` and `docs/journal/`.

---

## 6. Stage 06 closure

### M1 — Clean repository verification
**PASS.** Clean Linux checkout, tests and canonical runners verified.

### M2 — Dependency and legacy cleanup
**PASS.** Active runtime is stdlib-only; DEV verification uses pytest. Legacy and unrelated experimental implementations were removed from the active tree after audits and regression.

### M3 — Documentation consistency
**PASS.** Root README, documentation index, test README, traceability, component map and Stage 06 control documents were reconciled with the current repository.

### M4 — DEV v1 baseline freeze
**PASS.** Current contracts and verified implementation are frozen as the reference baseline. Freeze does not mean production readiness; it means future work must start from a new approved requirement instead of silently extending the baseline.

---

## 7. Open future requirements — not current defects

1. **Live Telegram transport** — donor review + benchmark + security review + ADR required.
2. **Reusable Artifact/Ingestion layer** — file/media/document normalization and evidence preservation.
3. **Local transcription engine** — offline/local-first acceptance scenario; external service registry as controlled fallback.
4. **Knowledge Gate / KB publication** — separate domain model, review semantics and tests.
5. **Expert Analyst/Socrates** — requires evaluation corpus, quality metrics and explicit expert requirements.
6. **Production observability/runtime supervision** — redesign from retained lessons, not restoration of old legacy code.
7. **Windows-specific verification** — desirable before claiming cross-platform DEV baseline.

---

## 8. Current roadmap

**M5 — NEXT APPROVED BUSINESS REQUIREMENT.**

The next step is deliberately not “add another technology”. We first choose one concrete capability and pass it through the full engineering chain.

Candidate next requirements currently recorded:
- live Telegram Radar transport;
- generic Artifact/Ingestion layer;
- local transcription;
- Knowledge Gate foundation.

Selection criteria:
1. immediate value to the FATHER workflow;
2. dependency on the frozen DEV v1 core;
3. testability with bounded acceptance criteria;
4. minimum unnecessary infrastructure;
5. reusable value for later agents.

Until one is approved, **DEV v1 remains frozen**.

---

## 9. Journal update template

For every material change record:

```text
Date
Stage / milestone
Trigger / problem
Decision
WHY
Files/components affected
Acceptance test / evidence
Result: PASS / PARTIAL / REWORK / DEFERRED
New risks
Next action
```

Small formatting-only commits do not require a separate architectural journal entry.
