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
| KF-P0-021 Evidence-based Knowledge Engineering method | B/C/D/E | DONE / CONTRACT | Ontology 101 + Competency Questions + METHONTOLOGY + NeOn + PROV-O + SKOS + SHACL principles + FAIR + OQuaRE mapped to D0-D15 in `docs/03_architecture/12_EVIDENCE_BASED_KNOWLEDGE_ENGINEERING_METHOD.md` |
| KF-P0-022 Multidimensional quality metrics | C/D/E | DONE / CI VERIFIED | `father_osint/knowledge_quality.py`; P/R/F1, provenance/locator coverage, CQ metrics, constraints, reuse/rework and metric provenance; PR #11 run `32573607002`: 152 passed, 2 skipped |
| KF-P0-023 KnowledgeScope + Competency Question executable model | C/D | TODO | stable `scope_id`, `CQ-*`, answer states and pre-D6 gate |
| KF-P0-024 Shape/constraint validation layer | C/D/E | TODO | machine-verifiable object/relation shapes; mandatory D15 conformance |
| KF-P0-025 Gold/evaluation corpus + annotation policy | C/D/E | TODO | versioned gold sets for extraction/conflict/CQ method evaluation |

## Current verification evidence — 2026-08-22

Latest PR #11 DEV verification evidence including the Knowledge Engineering metrics increment:

```text
GitHub Actions run: 32573607002
job: verify / 97032600010
Python: 3.12.14
collected: 152 tests
result: 152 passed, 2 skipped
run_dev_osint.py: PASS
run_dev_pipeline.py: PASS
previous CodeQL run: 32573038727 / PASS
current CodeQL run for this increment: 32573606956 / running at last observation
```

D0-D3 acquisition coverage remains green:

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

The Knowledge Engineering increment adds verified metric semantics:

- established methodology anchors rather than ad-hoc graph construction;
- competency questions as domain acceptance requirements;
- mandatory reuse/alignment check before new concept creation;
- PROV-style lineage semantics;
- SHACL-style constraint validation contract;
- FAIR-oriented stable IDs/metadata/provenance/reuse requirements;
- separate accuracy/completeness/consistency/freshness/trust/interoperability dimensions;
- executable metric primitives in `father_osint/knowledge_quality.py`;
- tests forbidding fabricated undefined ratios and opaque composite truth/quality scores;
- explicit metric provenance and raw confusion/coverage counts.

## Rule for updating the ledger

A task changes state only with a concrete evidence reference: commit, test, runner output, registry snapshot, artifact manifest or reviewed decision. “Started”, “almost done” and percentage estimates do not count as evidence.

Methods obey the same rule: a method becomes GOLDEN only after same-corpus Champion/Challenger evidence, not because it is popular or academically cited.

## Current bottleneck

Complete D0-D3 acceptance as a mixed-profile corpus rather than skipping upstream evidence gates:

1. BOOK-profile exact acquisition fixture;
2. independent-source same-payload acquisition fixture;
3. malformed/mismatched response fixture;
4. machine-readable acceptance runner/reconciliation report;
5. live-verification path for at least one approved SourcePolicy entry without weakening the exact-bytes/hash gate.

In parallel, only contract/test-design work that cannot invalidate D0-D3 may prepare KF-P0-023/024/025. D6 semantic extraction cannot become the critical implementation lane before the mixed-profile D0-D3 gate is green.
