# J-032 — Three-pass quality execution started — 2026-08-13

## Decision

Project execution is switched to a three-pass quality model:

1. MINIMUM — make the complete approved product path work safely end-to-end;
2. MEDIUM — repeat the complete path with stronger usefulness, resilience and evidence quality;
3. MAXIMUM — repeat the complete path with production-grade hardening for justified scope.

The controlling metrics and promotion gates are defined in `docs/QUALITY_LADDER_MIN_MED_MAX.md`.

## Active level

**MINIMUM**.

No MEDIUM/MAX optimization is allowed while a required MIN vertical-slice stage is absent, except immediate security remediation or a small architectural change required to preserve the MIN path.

## Current MIN status

| Stage | Current evidence | MIN status | Next gate |
|---|---|---|---|
| DEV baseline / contracts | clean deterministic DEV path already proven | PASS | regression protect |
| M5 live Telegram acquisition | live G6-G10 exploratory integrated PASS exists | PARTIAL | G11 required counter-evidence live scenario |
| M5 multi-source behavior | one observable source surfaced in bounded run | OPEN | explain/configure/prove intended multi-source behavior or accept limitation explicitly |
| M5 security/session | earlier controls exist; final live-path review remains | OPEN | final secret/session/log hygiene evidence |
| M5 transport decision | Telethon live fallback exists; TDLib remains candidate | OPEN | ADR with primary/fallback/revisit triggers |
| M6 Artifact/Ingestion | planned only | NOT STARTED | MIN original/hash/type/failure vertical slice after M5 MIN freeze |
| M7 local extraction/transcription | planned only | NOT STARTED | MIN local route after M6 MIN |
| Evidence/counter-evidence | G6-G10 exists; G9 REQUIRED live path unproven | PARTIAL | actual hypothesis-driven counter-evidence attempt |
| Analyst | DEV/live observation claims proven in current bounded path | PARTIAL MIN | preserve claim/evidence separation through later M6-M8 slice |
| Socrates | current integrated path produced PASS | PARTIAL MIN | independent defect/negative path must remain regression-protected |
| M8 Knowledge Gate | planned only | NOT STARTED | MIN publish/reject/revise + no synthetic-to-production path |
| Transparent report | G10 acquisition report proven for current live path | PARTIAL MIN | carry lineage/gaps through final full MIN chain |

## Immediate sequence

```text
M5 MIN closure:
G11 live hypothesis/counter-evidence
  → source coverage resolution
  → final secrets/session/log review
  → transport ADR/Critic review
  → M5 MIN freeze

then
M6 MIN
  → M7 MIN
  → M8 MIN
  → FULL MIN E2E acceptance

only then
MEDIUM from beginning to end

only then
MAXIMUM from beginning to end
```

## Change policy

If an existing approach or test prevents the active metric from being met efficiently, changing it is permitted after recording:

- failed metric/assumption;
- whether requirement, architecture, implementation or test was wrong;
- smallest justified change;
- new regression evidence;
- rerun of the whole active-level vertical slice.

Tests may not be weakened merely to obtain green CI.

## Result

**MINIMUM EXECUTION STARTED.**

The next product-changing gate is G11 live hypothesis-driven counter-evidence. Documentation-only progress cannot promote the level.