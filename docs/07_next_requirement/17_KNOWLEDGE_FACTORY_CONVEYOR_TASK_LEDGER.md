# Knowledge Factory Conveyor — Task Ledger

**Status:** ACTIVE / single P0 execution ledger

## P0 critical path

| Task | Lane | State | Exit evidence |
|---|---|---|---|
| KF-P0-001 Reconcile M1 contracts | E | IN_PROGRESS | common schemas/IDs/stages frozen |
| KF-P0-002 SourcePolicy registry | A | IN_PROGRESS | machine-readable approved source registry |
| KF-P0-003 Exact acquisition service | A | TODO | exact bytes + MIME + size + SHA-256 + bounded failures |
| KF-P0-004 Artifact/version store | A/E | TODO | originals preserved; repeated/versioned runs safe |
| KF-P0-005 D0-D3 BASIC fixtures | A/E | TODO | KF-FX-001,002,009,028 PASS |
| KF-P0-006 D0-D3 PROFESSIONAL fixtures | A/E | TODO | KF-FX-003..005 PASS |
| KF-P0-007 D0-D3 STRESS fixtures | A/E | TODO | KF-FX-006..008 PASS |
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

## Rule for updating the ledger

A task changes state only with a concrete evidence reference: commit, test, runner output, registry snapshot, artifact manifest or reviewed decision. “Started”, “almost done” and percentage estimates do not count as evidence.

## Bottleneck selection

At the end of every run select exactly one next bottleneck from this ledger. Parallel lanes may continue only if they do not depend on unresolved upstream semantics.
