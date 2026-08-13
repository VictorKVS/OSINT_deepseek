# FATHER — Three-Pass Quality Ladder: MIN → MEDIUM → MAX

**Status:** ACTIVE EXECUTION POLICY  
**Effective:** 2026-08-13  
**Owner:** Project/Product Governance  
**Purpose:** make the whole product path work end-to-end at a minimal acceptable level first, then repeat the same path at medium quality, then harden it to maximum justified quality.

## 1. Governing rule

We do **not** maximize an isolated component while downstream/upstream stages are still absent or unproven.

Execution order is strictly:

```text
PASS 1 — MINIMUM: whole path from start to end works safely and repeatably
        ↓ only after end-to-end MIN PASS
PASS 2 — MEDIUM: whole path is useful, resilient and evidence-aware
        ↓ only after end-to-end MEDIUM PASS
PASS 3 — MAXIMUM: whole path is production-grade within approved scope
```

A stage may be redesigned, simplified or have its tests replaced if the existing approach cannot meet the active level efficiently. Architecture is subordinate to verified product behavior, safety invariants and evidence.

No level is promoted by documentation alone. Every promotion requires executable or directly observable evidence.

## 2. Whole-product path

The quality ladder covers the complete planned evidence-to-knowledge path:

```text
Mission / ResearchTask
  ↓
Live acquisition / Telegram Radar (M5)
  ↓
Artifact / universal ingestion (M6)
  ↓
Local-first extraction / transcription (M7)
  ↓
Evidence quality + sufficiency + counter-evidence
  ↓
Analyst
  ↓
Socrates / independent challenge
  ↓
Knowledge Gate (M8)
  ↓
Governed KB publication / rejection / revision
  ↓
Transparent report + lineage
```

Until M6-M8 exist, the MIN pass advances stage by stage but must preserve a runnable vertical slice after every new stage.

## 3. Global metrics by level

| Dimension | MINIMUM | MEDIUM | MAXIMUM |
|---|---|---|---|
| End-to-end completion | 1 bounded canonical scenario passes from available start to current approved end; after M8, full chain passes | ≥5 representative scenarios across normal + degraded inputs | approved evaluation suite covers major classes, edge cases and recovery paths |
| Determinism / repeatability | deterministic fixtures + bounded live run produce contract-valid results | repeated runs show stable contract behavior despite source variance | reproducibility policy, pinned/locked dependencies, controlled environments and release evidence |
| Negative tests | at least 1 meaningful failure test per stage | failure matrix covers invalid input, missing data, timeout, partial source failure, restart | adversarial/fault-injection suite covers security, corruption, concurrency, resource pressure and recovery |
| Provenance / lineage | 100% accepted materials/claims have source + hash/locator lineage | 100% claims trace to evidence assessments and acquisition attempts | end-to-end immutable/auditable lineage with revision history and integrity verification |
| Secrets / sensitive data | 0 secrets/session material committed; normal logs redact sensitive values | automated secret/session leakage tests + owner-setting review | release gate includes secret scanning, least privilege, rotation/recovery procedure and incident evidence |
| Availability / failure isolation | one source/stage failure does not silently corrupt successful outputs | bounded retries/timeouts/checkpoints; partial failures are explicit | tested recovery objectives, backpressure/resource limits, operational runbooks and observability |
| Evidence quality | separate evidence-quality records; no fake aggregate truth score | source independence/primary evidence/counter-evidence explicitly assessed | calibrated domain-specific scoring only where validation corpus supports it; otherwise qualitative policy remains |
| Research sufficiency | system can say INSUFFICIENT/MINIMUM and preserve unresolved gaps | GOOD achievable for suitable scenarios with explicit cross-source/counter-evidence work | DESIRABLE/MAX only when declared coverage/independence/counter-evidence criteria are actually met |
| Independent challenge | Socrates/verifier is logically separate from producer and can block/pass | challenge has explicit objections, rework loop and counter-evidence trigger | adversarial evaluation shows verifier catches seeded defects at approved target rate |
| CI | clean checkout + tests + canonical runners pass | CI covers unit + integration + security checks and representative scenarios | release-grade matrix, reproducibility, platform coverage and policy gates |
| Documentation/status truth | one authoritative current-state register | traceability from requirement → test → code → evidence | release/baseline manifests are generated or mechanically checked for drift |

## 4. Stage metrics

### A. Mission / ResearchTask

**MIN**
- explicit bounded objective;
- allowed sources/scope recorded;
- stop condition exists;
- invalid/unbounded request rejected or constrained.

**MEDIUM**
- materiality/risk level selects evidence depth;
- expected outputs and acceptance criteria machine-readable where practical;
- task decomposition preserves parent/child lineage.

**MAX**
- policy-driven planning validated against scenario corpus;
- budget/time/source constraints enforced and measured;
- plan changes are auditable.

### B. M5 Live acquisition / Telegram Radar

**MIN**
- bounded live public-source acquisition PASS;
- provenance + content hash preserved;
- checkpoint/restart PASS;
- per-source failure explicit;
- secrets/session hygiene PASS;
- hypothesis-driven G9 counter-evidence attempt proven when REQUIRED;
- intended multi-source behavior either demonstrated or explicitly accepted as a limitation;
- transport ADR records primary/fallback/revisit triggers.

**MEDIUM**
- ≥3 independent observable source contexts in representative scenario where available;
- rate-limit/timeout/restart/isolation tests pass repeatedly;
- metadata needed for edit/forward/reply/source lineage preserved;
- acquisition report exposes attempts, misses and gaps.

**MAX**
- sustained bounded runs under representative load;
- fault injection for network loss, rate limits, malformed payloads, session failure;
- operational metrics and recovery behavior verified;
- transport replacement test proves interface independence.

### C. M6 Artifact / universal ingestion

**MIN**
- original bytes preserved;
- SHA-256 before normalization;
- type detection does not trust extension alone;
- unsupported/corrupt artifact fails explicitly;
- one document + one image/audio/video representative path is accepted or explicitly routed as unsupported.

**MEDIUM**
- MIME/signature routing coverage for approved formats;
- metadata extraction and normalized artifact lineage;
- duplicate payload reuse without collapsing observations;
- resource/size/time limits.

**MAX**
- adversarial parser corpus, decompression/resource-bomb controls, corrupted/truncated files;
- sandbox/isolation policy where required;
- measured throughput and recovery.

### D. M7 Local-first extraction / transcription

**MIN**
- at least one fully local extraction/transcription route;
- no mandatory third-party upload;
- raw artifact → extracted text lineage preserved;
- failure/unsupported language/media is explicit.

**MEDIUM**
- representative language/audio-quality corpus;
- confidence/quality metadata kept distinct from factual truth;
- optional external fallback requires explicit policy and provenance.

**MAX**
- domain evaluation corpus with error-rate thresholds;
- privacy/security tests and offline operation verification;
- resource budgeting and model/version reproducibility.

### E. Evidence quality / sufficiency / counter-evidence

**MIN**
- each evidence item gets a separate quality assessment;
- sufficiency can remain MINIMUM/INSUFFICIENT;
- leading hypothesis forces a real G9 counter-evidence attempt;
- unresolved gaps survive into final report.

**MEDIUM**
- cross-source independence, primary/secondary status and temporal relevance assessed;
- GOOD requires explicit positive criteria, not merely item count;
- competing evidence is surfaced to Analyst/Socrates.

**MAX**
- calibrated scoring only with validation data;
- sensitivity/ablation testing of sufficiency policy;
- seeded confirmation-bias scenarios demonstrate counter-evidence behavior.

### F. Analyst

**MIN**
- claims are separated from evidence;
- every material claim has evidence lineage or is marked unsupported;
- no synthetic fixture is labelled verified domain truth.

**MEDIUM**
- competing interpretations and assumptions recorded;
- confidence language follows evidence/sufficiency policy;
- seeded unsupported-claim tests fail correctly.

**MAX**
- domain evaluation corpus with precision/recall or equivalent task metrics where meaningful;
- contradiction handling and temporal revision tests;
- expert benchmark and error taxonomy.

### G. Socrates / independent verifier

**MIN**
- independent assignment/role from producer;
- can PASS, REWORK/RESEARCH_MORE or FAIL;
- at least one seeded defect is detected;
- self-review is not accepted as independent verification.

**MEDIUM**
- challenge categories cover evidence gaps, contradiction, overclaim, scope and missing counter-evidence;
- bounded rework cycle;
- seeded defect set with measured detection rate.

**MAX**
- adversarial benchmark and blind evaluation set;
- false-pass and false-block rates tracked;
- verifier disagreement/review escalation policy.

### H. M8 Knowledge Gate / KB

**MIN**
- publication requires evidence lineage + Analyst output + verifier PASS;
- rejection/revision path exists;
- synthetic/test evidence cannot enter production KB;
- version and timestamp recorded.

**MEDIUM**
- claim-level revisions preserve prior versions and reasons;
- expiry/revalidation trigger for time-sensitive knowledge;
- conflicting claims coexist with status rather than destructive overwrite.

**MAX**
- domain-specific authority policies, review SLAs and revalidation automation;
- audit/replay of why a knowledge claim was published at a given time;
- drift/staleness metrics and controlled rollback.

### I. Reporting / operational closure

**MIN**
- transparent final report contains source attempts, evidence refs, unresolved gaps, sufficiency and verifier verdict;
- no unsupported claim of VERIFIED status.

**MEDIUM**
- report distinguishes fact/claim/inference/unknown/counter-evidence;
- machine-readable summary plus human-readable narrative;
- completeness checks against task contract.

**MAX**
- signed/baselined release evidence where justified;
- report reproducibility from stored lineage;
- policy/compliance export formats as product requirements demand.

## 5. Promotion gates

### PASS 1 — MINIMUM

The entire product is MIN-PASS only when every currently approved stage has MIN evidence and, after M8 exists, at least one bounded scenario executes:

`ResearchTask → live acquisition → ingestion → extraction → evidence/counter-evidence → Analyst → Socrates → Knowledge Gate → report`.

Current starting point on 2026-08-13:
- DEV v1 baseline: PASS;
- M5 exploratory G6-G10 live path: PASS/PARTIAL toward MIN;
- remaining M5 MIN blockers: G11 required-counter-evidence live proof, multi-source behavior resolution, final secret/session review, transport ADR;
- M6: NOT STARTED;
- M7: NOT STARTED;
- M8: NOT STARTED.

Therefore **active level = MINIMUM**. MEDIUM and MAXIMUM work is blocked except where a security defect must be fixed immediately or a tiny change is required to keep MIN architecture viable.

### PASS 2 — MEDIUM

Starts only after full MIN vertical slice PASS. All MIN evidence remains regression-protected. Medium work is performed again from the beginning of the chain to the end; no stage may be called MEDIUM if an upstream stage remains MIN-only for the same scenario class.

### PASS 3 — MAXIMUM

Starts only after full MEDIUM vertical slice PASS. MAX means maximum **justified** quality for approved scope, not infinite complexity. A metric with no business/security value may be explicitly capped at MEDIUM by an ADR.

## 6. Test-change rule

Tests are not sacred if they encode the wrong requirement. When evidence shows the approach is poor:

1. record the failed metric/assumption;
2. state whether requirement, architecture, implementation or test is wrong;
3. change the smallest justified layer;
4. add a regression that would have caught the discovered failure;
5. rerun the whole active-level vertical slice, not only the changed unit;
6. preserve negative evidence and unresolved limitations.

Changing a test merely to make CI green without changing an invalid contract is prohibited.

## 7. Hourly reporting metrics

Each hourly status report must contain only measurable deltas:

- current active quality level: MIN / MEDIUM / MAX;
- current stage and gate;
- completed gates since previous report;
- tests/CI: pass/fail/total when available;
- live scenarios executed and their result;
- provenance/lineage failures count;
- secret/session leakage findings count;
- unresolved P0 blockers;
- approach/test changes and why;
- regression status;
- next single critical action;
- explicit `NO MATERIAL CHANGE` when nothing changed.

Reports must not inflate progress from commits/documentation alone.

## 8. Current execution sequence

```text
MINIMUM PASS
  M5: G11 → source coverage → security → ADR → MIN freeze
  M6: artifact ingestion MIN vertical slice
  M7: local extraction/transcription MIN vertical slice
  M8: Knowledge Gate MIN vertical slice
  FULL MIN end-to-end acceptance
        ↓
MEDIUM PASS
  repeat chain from ResearchTask to governed KB/report
        ↓
MAXIMUM PASS
  repeat chain from ResearchTask to governed KB/report
```

This document overrides any local sequencing that attempts to start MEDIUM/MAX hardening before the complete active-level vertical slice is proven.