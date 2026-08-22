# Knowledge Factory Conveyor — Task Ledger

**Status:** ACTIVE / single P0 execution ledger

## P0 critical path

| Task | Lane | State | Exit evidence |
|---|---|---|---|
| KF-P0-001 Reconcile M1 contracts | E | IN_PROGRESS | common schemas/IDs/stages frozen |
| KF-P0-002 SourcePolicy registry | A | IN_PROGRESS | machine-readable approved source registry; current seed still requires live verification |
| KF-P0-003 Exact acquisition service | A | DONE / CI VERIFIED | `father_osint/acquisition.py`; exact bytes + MIME + size + SHA-256 + bounded/policy failures; PR #11 CI run `32573038699` |
| KF-P0-004 Artifact/version store | A/E | DONE / CI VERIFIED | content-addressed originals, append-only acquisition events, repeated-byte reuse and new-version preservation tests green |
| KF-P0-005 D0-D3 BASIC fixtures | A/E | IN_PROGRESS | exact legal-like artifact + stage ordering + frozen regression green; BOOK-profile acquisition fixture still missing |
| KF-P0-006 D0-D3 PROFESSIONAL fixtures | A/E | IN_PROGRESS | unchanged reuse and changed-version tests green; independent-source same-payload acquisition fixture still to add |
| KF-P0-007 D0-D3 STRESS fixtures | A/E | IN_PROGRESS | unverified/off-policy/redirect/fetch-failure/RBAC/corrupt-blob tests green; malformed-response fixture still to add |
| KF-P0-008 Structure parser contract | B | TODO | stable structure schema + parser version |
| KF-P0-009 Chunk compiler | B | TODO | traceable stable chunks |
| KF-P0-010 Knowledge object schemas | C | TODO | typed D6-D9 objects |
| KF-P0-011 Extraction implementation | C | TODO | concepts/definitions/atomic rules/entities with provenance |
| KF-P0-012 Relation taxonomy/engine | D | TODO | D10-D11 typed relations |
| KF-P0-013 Conflict/applicability engine | D | TODO | D12 classifications with evidence |
| KF-P0-014 Projection reconciliation | E | TODO | graph/table/document/clause views agree |
| KF-P0-015 Analyst review package | D | TODO | traceable PASS/REWORK/INCONCLUSIVE |
| KF-P0-016 Socrates/Critic gate | D | TODO | challenge/dependency/promotion checks |
| KF-P0-017 D15 KB-ready package | D/E | TODO | one bounded corpus reaches reviewed D15 |
| KF-P0-018 Change monitoring/invalidation | A/D/E | TODO | changed version causes bounded downstream impact |
| KF-P0-019 Reuse regression | C/D/E | TODO | unchanged objects reused, not recomputed |
| KF-P0-020 Second-profile reuse proof | all | TODO | same conveyor works without bespoke architecture |

## Current verification evidence — 2026-08-22

PR #11 DEV verification evidence:

```text
GitHub Actions run: 32573038699
job: verify / 97031244083
Python: 3.12.14
collected: 144 tests
result: 144 passed, 2 skipped
run_dev_osint.py: PASS
run_dev_pipeline.py: PASS
```

New D0-D3 acquisition coverage included in the green run:

- exact byte preservation and computed SHA-256;
- MIME and byte-length metadata;
- content-addressed original storage;
- append-only acquisition/audit observations;
- repeated unchanged artifact/version reuse without losing a new acquisition observation;
- changed bytes creating a new version while retaining old original bytes;
- unverified source block;
- off-policy host block before network call;
- redirect/final host outside policy rejection;
- explicit fetch failure;
- RBAC acquisition block;
- corruption detection before reusing an existing content-addressed blob.

This evidence closes the implementation core of KF-P0-003 and KF-P0-004, but does **not** yet close BASIC/PROFESSIONAL/STRESS as complete suites because their remaining named fixtures are still explicit above.

## Rule for updating the ledger

A task changes state only with a concrete evidence reference: commit, test, runner output, registry snapshot, artifact manifest or reviewed decision. “Started”, “almost done” and percentage estimates do not count as evidence.

## Current bottleneck

Complete D0-D3 acceptance as a mixed-profile corpus rather than adding downstream features:

1. BOOK-profile exact acquisition fixture;
2. independent-source same-payload acquisition fixture;
3. malformed/mismatched response fixture;
4. machine-readable acceptance runner/reconciliation report;
5. live-verification path for at least one approved SourcePolicy entry without weakening the exact-bytes/hash gate.

Only after this set is green may Lane B become the critical-path implementation lane.
