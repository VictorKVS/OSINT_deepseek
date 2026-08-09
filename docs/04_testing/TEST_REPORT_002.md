# TEST_REPORT_002 — Storage Semantics Regression

**Date:** 2026-08-09  
**Stage:** 05 implementation verification / Stage 04 regression evidence  
**Status:** FOCUSED REGRESSION PASS

## 1. Change under test

Only `father_osint/storage.py` was changed.

Purpose: preserve every source observation while reusing identical raw payload blobs by SHA-256.

## 2. Execution environment

As in TEST_REPORT_001, outbound network access prevented a direct repository clone. The focused regression was executed against a local reconstruction of the current reviewed GitHub modules plus the committed storage change.

This is strong behavioral evidence for the changed slice, but final repository verification still requires an exact checkout/CI run.

## 3. Focused suite

```text
7 tests executed
7 passed
0 failed
```

Covered behavior:

- AC-02: same payload from different source observations is preserved;
- AT-04: same behavior remains after store/process restart;
- AC-03: missing collector is explicit;
- AC-04: max_items bounds collection;
- AC-05: collector failure is isolated and visible;
- AC-08: full DEV pipeline is hard bounded;
- AC-09: full DEV review path can reach Socrates PASS.

## 4. Defect status

| Defect | Result |
|---|---|
| DEF-001 provenance loss on identical payload | RESOLVED IN FOCUSED REGRESSION |
| DEF-002 restart provenance loss | RESOLVED IN FOCUSED REGRESSION |

## 5. Architecture check

The fix stayed within the approved Stage 05 boundary:

```text
source observation -> Material JSONL record
payload bytes      -> hash-addressed raw blob
```

No new database, dependency, framework, collector contract or production transport was introduced.

## 6. Gate decision

```text
Storage fix: ACCEPTED FOR DEV
Focused regression: PASS
Whole-repository acceptance: NOT YET VERIFIED
PROD readiness: NOT CLAIMED
```

## 7. Next required action

Run the exact repository test suite from a real checkout or CI environment and record `TEST_REPORT_003`. Only then should Stage 04/05 be closed globally and repository cleanup decisions (`pipeline.py` etc.) be executed.
