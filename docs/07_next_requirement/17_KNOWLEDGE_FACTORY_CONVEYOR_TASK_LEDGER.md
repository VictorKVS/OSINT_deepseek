# Knowledge Factory Conveyor — Task Ledger

**Status:** ACTIVE / single P0 execution ledger

## P0 critical path

| Task | Lane | State | Exit evidence |
|---|---|---|---|
| KF-P0-001 Reconcile M1 contracts | E | IN_PROGRESS | common schemas/IDs/stages frozen |
| KF-P0-002 SourcePolicy registry | A | IN_PROGRESS | machine-readable approved source registry; 152-FZ official source profile added; live acquisition still required |
| KF-P0-003 Exact acquisition service | A | DONE / CI VERIFIED | `father_osint/acquisition.py`; exact bytes + MIME + size + SHA-256 + bounded/policy failures |
| KF-P0-004 Artifact/version store | A/E | DONE / CI VERIFIED | content-addressed originals, append-only acquisition events, repeated-byte reuse and new-version preservation tests green |
| KF-P0-005 D0-D3 BASIC fixtures | A/E | IN_PROGRESS | exact LEGAL path green; BOOK-profile acquisition fixture still missing |
| KF-P0-006 D0-D3 PROFESSIONAL fixtures | A/E | IN_PROGRESS | unchanged reuse and changed-version tests green; independent-source same-payload fixture still to add |
| KF-P0-007 D0-D3 STRESS fixtures | A/E | IN_PROGRESS | unverified/off-policy/redirect/fetch-failure/RBAC/corrupt-blob tests green; malformed-response fixture still to add |
| KF-P0-008 Structure parser contract | B | DONE / CI VERIFIED | `father_osint/document_compiler.py`; deterministic DOCUMENT/CHAPTER/SECTION/ARTICLE structure; parser version `legal-preliminary-v1`; run 32575073589 |
| KF-P0-009 Chunk compiler | B | DONE / CI VERIFIED | stable D5 chunks carry document/version/structure locator + exact artifact SHA-256; semantic extraction remains blocked |
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
| KF-P0-021 Evidence-based Knowledge Engineering method | B/C/D/E | DONE / CONTRACT | Ontology 101 + Competency Questions + METHONTOLOGY + NeOn + PROV-O + SKOS + SHACL principles + FAIR + OQuaRE mapped to D0-D15 |
| KF-P0-022 Multidimensional quality metrics | C/D/E | DONE / CI VERIFIED | P/R/F1, provenance/locator coverage, CQ metrics, constraints, reuse/rework and metric provenance |
| KF-P0-023 KnowledgeScope + Competency Question executable model | C/D | IMPLEMENTED / CI PENDING | `father_osint/knowledge_method.py`; stable `KS-*`, `CQ-*`, answer states and pre-D6 gate |
| KF-P0-024 Shape/constraint validation layer | C/D/E | IMPLEMENTED / CI PENDING | `father_osint/knowledge_constraints.py`; machine-verifiable common KB-ready shape |
| KF-P0-025 Gold/evaluation corpus + annotation policy | C/D/E | TODO | versioned gold sets for extraction/conflict/CQ method evaluation |
| KF-P0-026 PDn 152-FZ live D0-D5 MVP | A/B/E | READY FOR LIVE RUN | `RUN_PDN_152FZ_MVP.cmd` downloads configured official `ips.pravo.gov.ru` artifact, computes SHA-256 and emits manifest/structure/chunks; live machine evidence required |

## Current verification evidence — 2026-08-22

Latest green PR #11 DEV verification for the PDn D0-D5 increment:

```text
GitHub Actions run: 32575073589
job: verify / 97036091693
Python: 3.12.14
collected: 158 tests
result: 158 passed, 2 skipped
run_dev_osint.py: PASS
run_dev_pipeline.py: PASS
```

New `tests/test_document_compiler_pdn_mvp.py` proves a deterministic vertical with synthetic official-like bytes:

- verified official source/policy → acquisition → D3;
- exact original SHA-256 remains lineage anchor;
- legal HTML visible-text extraction;
- chapter/article structure detection;
- stable structure/chunk IDs for same version/parser;
- D5 chunks carry article/structure/version/artifact lineage;
- tampered original blocks D4;
- unauthorized role blocks pipeline advancement;
- preliminary splitting never silently advances D6/D8 semantic states.

The configured live anchor is Federal Law No. 152-FZ on the official `pravo.gov.ru` integrated legal-information bank. The exact artifact hash/MIME are intentionally not hard-coded and must be produced by the live run.

## Rule for updating the ledger

A task changes state only with a concrete evidence reference: commit, test, runner output, registry snapshot, artifact manifest or reviewed decision. “Started”, “almost done” and percentage estimates do not count as evidence.

Methods obey the same rule: a method becomes GOLDEN only after same-corpus Champion/Challenger evidence, not because it is popular or academically cited.

## Current bottleneck

**Run KF-P0-026 on the workstation and capture the actual 152-FZ D0-D5 evidence.**

Expected success status:

```text
PASS_D0_D5_PRELIMINARY
```

Expected output root:

```text
data/knowledge_factory/pdn_mvp/
```

After the live PASS, start the first controlled D6-D8 PDn semantic pass on the produced 152-FZ chunks: terms/concepts, explicit definitions, actors and atomic requirements with exact article/chunk provenance.
