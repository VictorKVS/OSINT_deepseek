# M5 Telegram Radar — Completion Plan

**Status:** ACTIVE  
**Purpose:** close Telegram as the first complete OSINT Expert proving ground before opening another source/tool family.

## Product objective

Prove that FATHER can accept an Analyst research need, let OSINT Expert design and execute a bounded Telegram acquisition strategy, preserve evidence/provenance, assess search coverage and evidence quality, and return a package that Analyst/Socrates can use without Telegram-specific reasoning logic.

## End-to-end target

```text
Analyst Research Request
        ↓
OSINT Expert decomposition
        ↓
Telegram search strategy
        ↓
reconnaissance sample
        ↓
plan refinement / source selection
        ↓
bounded collection
        ↓
durable save → checkpoint
        ↓
Material / provenance / SHA
        ↓
MaterialPackage
        ↓
evidence assessment
        ↓
research sufficiency
        ↓
Analyst claims
        ↓
Socrates
        ↓
PASS / CHALLENGE / RESEARCH_MORE
```

## Acceptance gates

### G1 — Network and transport
- Telegram reachable in approved live environment.
- authorized local session outside source control.
- replaceable transport boundary.
- bounded global/per-channel collection.

**Status:** PASS.

### G2 — Canonical evidence ingestion
- Telegram message → canonical Material.
- stable source/message identity.
- provenance preserved.
- SHA-256 content addressing.
- repeated raw payload reused without collapsing observation history.

**Status:** PASS, including live repeat-run evidence.

### G3 — Reasoning boundary
- MaterialPackage → evidence-backed claims.
- every claim cites package material IDs.
- Socrates detects foreign/missing evidence references.
- live Telegram package reaches Socrates.

**Status:** PASS for deterministic DEV reasoning boundary.

### G4 — Reliability
Required:
- save-before-checkpoint;
- checkpoint survives restart;
- bounded FloodWait/retry;
- per-channel failure isolation;
- live checkpoint/restart/reconciliation proof;
- provenance/evidence not lost across restart.

**Status:** PASS. Contract tests cover save-before-checkpoint, restart persistence, bounded FloodWait/retry and channel isolation. Live Windows/VPN runs proved checkpoint creation, process restart, existing checkpoint detection (`resumed_sources=1`), raw-payload reuse (`payloads_reused=10`, `new_raw_payload_files=0`), new observation append, and continued Analyst→Socrates PASS. Evidence: `docs/journal/J-022_M5_LIVE_RESTART_RECONCILIATION_PASS_2026-08-12.md`.

### G5 — OSINT Expert search planning
Required:
- Analyst specifies what must be established;
- OSINT decomposes into observable indicators/questions;
- source/channel strategy is explicit;
- Analyst may suggest sources but does not own acquisition tactics;
- search plan records scope, exclusions, limits and failure/reporting behavior.

**Status:** PASS for deterministic Telegram baseline and live protocol proof. A real live run completed `ResearchRequest → SearchPlan → ACCEPT → COLLECTING → EvidencePackage → ANALYSIS → CLOSED` with `protocol_passed=true`, explicit KB/algorithm lineage and an auditable distinction between requested `GOOD` and achieved `MINIMUM` sufficiency. Evidence: `docs/journal/J-023_M5_G5_LIVE_SEARCH_PLAN_PROTOCOL_PASS_2026-08-13.md`.

### G6 — Reconnaissance and refinement
Required:
- first bounded reconnaissance sample;
- summary of source landscape and gaps;
- refinement of search plan before expensive/deep collection;
- ability to stop when added collection has low marginal value.

**Status:** NEXT / OPEN.

### G7 — Evidence quality assessment
Required dimensions (initial non-calibrated policy model):
- reliability;
- relevance;
- independence;
- recency;
- directness;
- corroboration;
- provenance quality.

Rules:
- dimensions remain distinct;
- no single score is treated as truth probability without calibration evidence;
- tool/source labels do not automatically confer reliability.

**Status:** OPEN.

### G8 — Research sufficiency
Required levels:
- MINIMUM;
- GOOD;
- DESIRED.

Assessment must consider coverage, diversity, independence, primary evidence, counter-evidence and critical gaps rather than raw material count.

Must support explicit result:

```text
INSUFFICIENT
reason: ...
critical gaps: ...
recommended next search: ...
```

**Status:** OPEN.

### G9 — Counter-evidence / alternative search
For material analytical questions, OSINT search plan must include a deliberate attempt to find evidence inconsistent with the leading hypothesis or record why such search is not applicable.

**Status:** OPEN.

### G10 — Transparent acquisition report
Analyst receives not only materials but also:
- what was searched;
- sources/channels attempted;
- bounds/limits;
- source failures;
- unresolved gaps;
- sufficiency target and achieved level;
- recommended follow-up search.

**Status:** OPEN.

### G11 — M5 closure
Before M5 DONE:
- all blocking gates above pass by tests and required live evidence;
- CI stays green;
- secrets/session hygiene passes;
- final Engineering Council review is recorded;
- transport/reference ADR is updated to reflect measured evidence;
- deferred generic ToolRegistry/Lead/Kali layer remains explicitly deferred unless a new approved requirement changes priority.

## Immediate execution order

```text
1. Live checkpoint/restart/reconciliation   PASS
2. Telegram SearchPlan contract             PASS
3. Reconnaissance → refinement cycle        NEXT
4. EvidenceAssessment model
5. ResearchSufficiency MINIMUM/GOOD/DESIRED
6. Counter-evidence behavior
7. AcquisitionReport to Analyst
8. Full live scenario
9. Council final review / M5 DONE
```

## Scope guard

Do not add a generic external-tool platform, multi-host scheduler, distributed queue, or broad LLM integration merely because it may be useful later. Telegram M5 is the proving ground. New infrastructure requires a concrete blocking requirement and Council review.
