# Full Project Audit — 2026-08-09

**Scope:** current `main` branch of `VictorKVS/OSINT_deepseek`  
**Stage:** 06 — Verification and Repository Rationalization  
**Mode:** requirements-first / no feature growth during audit  
**Purpose:** verify that code, tests, CI, documentation and repository structure still describe the same product after cleanup.

---

## 1. Executive verdict

The repository is materially healthier than the original prototype. The active runtime surface is now small:

```text
father_osint/
scripts/
tests/
config/
data/
docs/
.github/
requirements.txt
requirements-dev.txt
```

Recent clean-checkout GitHub Actions runs are green. The current DEV core is stdlib-only and verification uses pytest.

However, **Stage 06 is not ready to close yet**. The audit found one important pipeline semantics defect, two contract/implementation gaps, and substantial documentation drift caused by successful cleanup progressing faster than active control documents were updated.

**Audit gate:** `REWORK REQUIRED BEFORE DEV V1 FREEZE`.

No new product feature is justified by this audit. The work required is contract repair, missing acceptance tests, minimal fixes, and documentation reconciliation.

---

# 2. Findings by severity

## CRITICAL

### C-01 — Follow-up cycles do not accumulate evidence across research cycles

**Components:** `father_osint/review_pipeline.py`, `analysis.py`, `socrates.py`  
**Type:** architecture / implementation semantics  
**Status:** CONFIRMED BY STATIC TRACE

Current loop passes only the **current cycle package** to Analyst and Socrates.

Example:

```text
Initial task requests: telegram + github

Cycle 1
telegram material exists
github missing
→ follow-up asks only github

Cycle 2
github material exists
package contains only github
→ Analyst now sees telegram as missing
→ follow-up asks telegram

Cycle 3
telegram material exists
package contains only telegram
→ github appears missing again
```

The hard cycle bound prevents an infinite loop, but the loop can oscillate because evidence obtained in previous cycles is not part of the current review context.

**Why this matters:** the intended process is evidence accumulation, not stateless retries.

**Required chain:**

```text
Requirement clarification
→ acceptance test reproducing two-source partial coverage
→ failing test
→ implementation plan
→ minimal cumulative-evidence fix
→ regression
```

Do **not** patch the pipeline before the test contract is approved.

---

## IMPORTANT

### I-01 — `duplicates_skipped` no longer describes actual storage behavior

**Components:** `models.MaterialPackage`, `agent.OSINTAgent`, `storage.MaterialStore`, ТЗ  
**Type:** contract drift

`MaterialStore.save_material()` currently always returns `True`. Therefore `OSINTAgent` never increments `duplicates_skipped`.

At the same time raw payload files are actually reused by SHA-256 when identical text is observed from multiple sources.

Current semantics therefore are:

```text
source observations skipped = 0
raw payload blobs reused     = possible
```

but `MaterialPackage` exposes only:

```text
duplicates_skipped
```

This is ambiguous and can mislead callers into believing no duplication/reuse occurred.

**Decision required:** either:
1. redefine `duplicates_skipped` explicitly as observation-level duplicates and keep it zero until an observation identity rule exists; or
2. add a separate DEV metric such as `payloads_reused` / `raw_blobs_reused`.

No numeric metric should be added without first defining exactly what event increments it.

---

### I-02 — local-file Materials do not receive a content hash

**Components:** `models.Material`, `storage.MaterialStore`  
**Type:** requirement/implementation gap

The current ТЗ says a material observation includes `content hash when payload exists` and permits `raw_text and/or local raw file reference`.

Current storage hashes `raw_text`, but if a Material arrives only with `local_path`, no SHA-256 is computed and `content_hash` may remain `None`.

This becomes especially important for the planned reusable Artifact/ingestion layer, where original-file integrity is a first-class requirement.

**Required:** acceptance case for local-file payload hashing before implementation.

---

### I-03 — active traceability matrix is historically stale

**Document:** `docs/TRACEABILITY_MATRIX.md`  
**Type:** governance/documentation

It still states:
- Stage 04 test design pending;
- AC rows are `UNVERIFIED`;
- `storage.py` still rejects duplicate payload observations;
- `pipeline.py` still exists as retirement candidate;
- `teleproto.py`, `telegram_bridge/`, `core/`, `services/` still exist as active disposition items.

Those statements conflict with the current tree and successful Stage 06 CI evidence.

Because the project explicitly treats traceability as a control artifact, this is not cosmetic documentation debt. It can drive future engineering decisions in the wrong direction.

**Required:** rebuild the matrix from current requirements → current implementation → current tests → latest evidence.

---

### I-04 — active documentation index still describes deleted repository areas

**Documents:** `docs/README.md`, parts of `DEVELOPMENT_JOURNAL.md`, root `README.md`  
**Type:** documentation drift

Examples observed during audit:
- `docs/README.md` still describes `services/llm-gateway/`, old `core/` and live bridge cleanup as current/recent repository state;
- root README still references `requirements-legacy.txt`, while the current root tree no longer contains that file;
- the living journal still contains repository-disposition/open-issue entries from before completed cleanup.

Historical audit reports may retain historical paths. **Living control documents may not present deleted components as current state.**

---

### I-05 — current ТЗ header is stale relative to actual project gate

**Document:** `docs/OSINT_AGENT_TZ_V1.md`

The header says implementation remains `PROTOTYPE / UNVERIFIED until Stage 03 and Stage 04 are completed`, although Stage 03/04 are complete and Stage 06 clean-checkout verification has succeeded.

The requirements themselves are mostly still useful, but the implementation-status statement must be corrected so readers know which acceptance evidence exists and which gaps remain.

---

## CLEANUP / QUALITY

### Q-01 — `tests/README.md` says tests are not yet accepted as evidence

The current test README predates successful clean CI and says tests should only be run after mapping review. This conflicts with established 17-test clean-checkout evidence.

Update it to separate:
- verified current tests;
- known missing acceptance cases discovered by this audit.

---

### Q-02 — `.gitignore` ignores the entire `data/` directory

Current `.gitignore` contains `data/`.

Existing tracked fixtures remain in Git, but new fixture files under `data/dev/` will normally be ignored unless explicitly forced. That is awkward for a project whose deterministic fixture corpus is an intentional verification asset.

**Recommended policy:** ignore runtime data while explicitly allowing versioned DEV fixtures, e.g. conceptual separation:

```text
data/runtime/     ignored
data/osint/       ignored
data/dev/         versioned fixtures
```

Do not change this until actual data directory layout is reviewed.

---

### Q-03 — future secret/session ignore policy is incomplete

Current ignore rules cover `.env`, `*.key`, `*.pem`, but the future Telegram/transport plans mention session files and external credentials.

Before live transport work, add a reviewed secret-artifact policy for patterns such as environment variants and transport session files. This is **DEFERRED** until the live transport requirement is opened; it is not a current DEV blocker.

---

### Q-04 — `FixtureCollector` uses whole-question substring matching

`FixtureCollector` searches the full `task.question` string plus topics. With no topics, natural-language questions may fail to match fixtures unless the whole question appears in the fixture text.

This is acceptable as a tiny deterministic harness only if documented. If fixtures are intended to simulate realistic keyword retrieval, test design should define token/keyword behavior instead of allowing implementation-defined matching.

**Status:** DEFER unless a test/use case demonstrates pain.

---

### Q-05 — `depth` and `stop_when_enough` are contract fields but are not operational in DEV

`ResearchTask` validates `depth` and stores `stop_when_enough`, but current DEV orchestration does not make decisions from either value.

This is not necessarily a bug because DEV scope is intentionally simplified, but documentation must state they are **carried contract fields, not implemented control semantics** in DEV v1.

---

# 3. What is currently strong

The audit confirmed several good boundaries.

## S-01 — narrow OSINT responsibility

`OSINTAgent` selects compatible collectors, collects, persists, isolates collector errors and returns `MaterialPackage`. It does not perform analysis or KB promotion.

## S-02 — provenance correction remains sound

Distinct source observations survive even when text bytes are identical. Raw text can reuse one SHA-256-addressed blob without collapsing observations.

## S-03 — transport abstraction remains clean

`TelegramCollector` depends on the minimal `TelegramTransport` protocol rather than a concrete TDLib/GramJS/Teleproto implementation. The current repository has no accidentally approved transport backend.

## S-04 — hard loop bound works

`DevReviewPipeline(max_cycles=N)` prevents unbounded follow-up loops. The newly found problem is evidence accumulation, not loop boundedness.

## S-05 — current dependency surface is small

`father_osint` is stdlib-only. `requirements-dev.txt` contains pytest. Historical dependencies have been removed from the active dependency surface.

## S-06 — clean CI is meaningful

Current GitHub Actions performs:

```text
clean checkout
Python 3.12
install DEV verification dependency
import father_osint
pytest collect
pytest run
run_dev_osint.py
run_dev_pipeline.py
```

Recent workflow runs are successful.

---

# 4. Test coverage audit

## Covered reasonably well

- distinct source observations with same payload;
- raw blob reuse for identical text;
- restart provenance preservation;
- no eligible collector;
- max_items bound;
- collector failure isolation;
- deterministic Analyst gap detection;
- deterministic Socrates pass/research-more;
- hard max review cycles;
- canonical runner entrypoints;
- Telegram collector mapping boundary.

## Missing tests required before DEV v1 freeze

### AT-NEW-01 — cumulative evidence across follow-up cycles

Scenario:

```text
Task source types: telegram + github
Cycle 1 returns telegram only
Cycle 2 returns github only
Expected final review: PASS using cumulative evidence
Expected: no ping-pong back to telegram
```

This test should fail against current pipeline and is the highest-priority audit action.

### AT-NEW-02 — local file content hash

Scenario:

```text
Material(raw_text=None, local_path=<file>)
store material
Expected content_hash = SHA-256(original file bytes)
Expected original file not silently rewritten
```

Exact ownership/copy semantics must be decided before implementation.

### AT-NEW-03 — duplicate/reuse metric semantics

Only add after deciding what the metric means. The test must prove the exact increment event and prevent future semantic drift.

---

# 5. Documentation consistency model

From now on documents should be classified as either:

```text
LIVING CONTROL DOCUMENT
    must reflect current main

HISTORICAL SNAPSHOT / AUDIT RECORD
    may describe removed files, but must be explicitly historical
```

Living control documents include at minimum:
- root `README.md`;
- `docs/README.md`;
- `docs/DEVELOPMENT_JOURNAL.md`;
- `docs/OSINT_AGENT_TZ_V1.md`;
- `docs/TRACEABILITY_MATRIX.md`;
- current stage README.

Old audit reports should not be rewritten to erase history. Add superseded/current-state markers when necessary.

---

# 6. Required remediation sequence

The project rule remains unchanged:

```text
AUDIT FINDING
    ↓
classify
    ↓
requirement/contract correction if needed
    ↓
acceptance test first
    ↓
prove failure
    ↓
implementation plan
    ↓
minimal fix
    ↓
full regression
    ↓
living docs reconciliation
    ↓
DEV v1 freeze decision
```

## Gate A — pipeline cumulative evidence

1. clarify cumulative-package semantics in architecture/ТЗ;
2. add AT-NEW-01;
3. run and record expected failure;
4. implement smallest correct accumulation model;
5. full CI regression.

## Gate B — payload integrity / metrics contract

1. decide local-file hashing semantics;
2. decide duplicate/reuse metric vocabulary;
3. add tests;
4. implement only accepted behavior.

## Gate C — documentation reconciliation

Update living docs only after code/test contract is stable:
- `TRACEABILITY_MATRIX.md`;
- root README;
- docs README;
- tests README;
- ТЗ implementation-status header;
- Development Journal current disposition/open issues/roadmap.

## Gate D — final DEV v1 verification

- clean checkout;
- full pytest;
- both runners;
- current traceability matrix has no false/stale rows;
- no current README points to deleted files;
- open issues explicitly deferred or closed.

---

# 7. Audit decision register

| ID | Finding | Severity | Decision |
|---|---|---|---|
| A-001 | Follow-up evidence is not cumulative | CRITICAL | REWORK via test-first gate |
| A-002 | `duplicates_skipped` semantics drifted | IMPORTANT | redefine contract before code |
| A-003 | local-file payload not hashed | IMPORTANT | add acceptance contract/test |
| A-004 | traceability matrix stale | IMPORTANT | rebuild after semantic fixes |
| A-005 | living docs reference deleted state | IMPORTANT | reconcile in M3 |
| A-006 | ТЗ implementation status stale | IMPORTANT | update after current evidence mapping |
| A-007 | tests README stale | CLEANUP | update in M3 |
| A-008 | data/ ignore policy conflicts with future fixture growth | CLEANUP | review data layout before change |
| A-009 | future secret/session patterns incomplete | DEFER | live transport gate |
| A-010 | fixture whole-question matching is simplistic | DEFER | change only on explicit retrieval requirement |
| A-011 | depth/stop condition not operational | DEFER/CLARIFY | document DEV semantics |

---

# 8. Current milestone recommendation

Do **not** declare M2/M3/DEV v1 complete yet.

Recommended temporary status:

```text
Stage 06
  M2 repository cleanup      substantially complete
  Audit semantic gate        REWORK REQUIRED
  M3 documentation sync      pending
  M4 DEV v1 freeze           blocked by A-001/A-002/A-003
```

The next action is **not more OSINT features**. The next action is AT-NEW-01 and the cumulative-evidence contract.
