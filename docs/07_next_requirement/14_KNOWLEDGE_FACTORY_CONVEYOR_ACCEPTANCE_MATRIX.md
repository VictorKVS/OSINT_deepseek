# Knowledge Factory Conveyor — Acceptance Matrix

**Status:** ACTIVE / P0 TEST CONTRACT  
**Parent:** `13_KNOWLEDGE_FACTORY_CONVEYOR_P0_EXECUTION.md`

| ID | Scenario | Required evidence | Gate |
|---|---|---|---|
| KF-FX-001 | approved official source, exact document | bytes preserved, MIME, size, SHA-256, source/version/audit | D0-D3 BASIC |
| KF-FX-002 | book/non-legal material | bibliographic metadata, original, hash; no legal lifecycle fields promoted as truth | D0-D3 BASIC |
| KF-FX-003 | repeated unchanged acquisition | artifact reused by hash, new acquisition/provenance event preserved | D0-D3 PROFESSIONAL |
| KF-FX-004 | changed bytes/new version | new version created, old version retained, current pointer explicit | D0-D3 PROFESSIONAL |
| KF-FX-005 | same payload from independent observations | one blob may be reused; observations/source events remain distinct | D0-D3 PROFESSIONAL |
| KF-FX-006 | unavailable source | explicit failure/retry exhaustion; no D2/D3 false success | D0-D3 STRESS |
| KF-FX-007 | unapproved/misleading mirror | policy blocks or marks discovery-only; no VERIFIED source | D0-D3 STRESS |
| KF-FX-008 | malformed/non-matching response | validation failure and audit; bytes not promoted as intended artifact | D0-D3 STRESS |
| KF-FX-009 | invalid stage transition | deterministic rejection; no partial silent mutation | all |
| KF-FX-010 | structure parse | every structure node maps to artifact locator | D4 |
| KF-FX-011 | chunking | stable chunks map to structure + exact source locator | D5 |
| KF-FX-012 | term mention vs definition | mention and definition remain distinct typed objects | D6-D7 |
| KF-FX-013 | atomic requirement | one compound clause decomposes with source locator and method provenance | D8 |
| KF-FX-014 | uncertainty / missing value | explicit UNKNOWN/GAP, never fabricated field/fact | D6-D12 |
| KF-FX-015 | internal relation | typed edge has from/to IDs, evidence locator and method version | D10 |
| KF-FX-016 | amendment/supersession | version edge preserves old/new documents and legal context | D11-D12 |
| KF-FX-017 | competing definitions | difference becomes CONFLICT_CANDIDATE first, then explicit classification | D12 |
| KF-FX-018 | context-dependent rules | CONTEXT_SPLIT_REQUIRED rather than false contradiction | D12 |
| KF-FX-019 | circular/dependent evidence | dependency recorded; not counted as independent corroboration | D12-D14 |
| KF-FX-020 | hypothesis/claim presented as fact | review/promotion boundary rejects implicit cast | D14-D15 |
| KF-FX-021 | graph/table/document projection | same node/relation IDs and evidence refs reconcile across views | D13 |
| KF-FX-022 | Analyst review | PASS/REWORK/INCONCLUSIVE with reasons and affected object IDs | D14 |
| KF-FX-023 | direct autonomous publish attempt | blocked before KB publication boundary | D15 |
| KF-FX-024 | source version update | only affected dependency subgraph invalidated/reprocessed | monitoring/reuse |
| KF-FX-025 | parser/method version update | reprocessing trigger explicit and old method provenance retained | monitoring/reuse |
| KF-FX-026 | run budget reached | deterministic bounded stop with explicit reason | all |
| KF-FX-027 | registry/audit mismatch | run gate fails; mismatch surfaced and counted | all |
| KF-FX-028 | frozen DEV v1 regression | canonical baseline runners/tests remain behaviorally unchanged | all |

## Acceptance levels

### BASIC
Must include `KF-FX-001`, `002`, `009`, `028`.

### PROFESSIONAL
Adds `003-005`, `010-016`, `021-022`.

### STRESS / RED TEAM
Adds `006-008`, `017-020`, `023-027`.

## Evidence bundle per fixture

Each fixture must provide:

```text
fixture ID
input task + source/material profile
initial registry snapshot
expected events/state transitions
expected artifacts/knowledge objects
expected review result
expected metrics delta
protected invariant
actual test/run reference
status PASS / FAIL / REWORK
```

Volatile timestamps and generated IDs must be injected/frozen or excluded from golden comparisons where appropriate.

## Gate rule

A maturity gate is not complete because code exists. It is complete only when the required fixture set is reproducibly green and the telemetry/registry/audit counts reconcile.
