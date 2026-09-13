# Lesson 12 — Review

Status: `DOCUMENTATION_LAYER_COMPLETE / PRODUCTION STORAGE TECHNOLOGIES REMAIN CANDIDATE`

## What Lesson 12 added

- one end-to-end data pipeline from source observation to reviewed knowledge candidate;
- stream and batch source convergence after acquisition;
- raw-first evidence-preservation rule;
- role-based storage selection for raw, metadata, retrieval, graph, analytics and datasets;
- data governance/lineage/version/retention model;
- explicit Feature Store applicability and training-serving-skew controls;
- retrieval/index consistency rules for RAG.

## What is already supported by current project evidence

The current project already separates source observations from raw payload reuse, preserves SHA-256 identity, and models staged progression from source acquisition through parsing/chunking/semantic extraction/review toward KB readiness. Lesson 12 turns those existing semantics into an explicit AI data architecture.

## Storage decisions

No product is approved merely for appearing in a reference stack.

```text
Raw evidence             → object/Data Lake class candidate
Operational metadata     → relational/catalog candidate
Lexical search           → search index candidate
Semantic retrieval       → Vector DB/index only after RAG eval
Relations                → graph store only when graph queries justify it
Analytics/telemetry      → warehouse/lakehouse when scale justifies it
Feature Store            → conditional, only for shared offline/online ML features
```

## Feature Store conclusion

`FEATURE_STORE = NOT_REQUIRED_FOR_CURRENT_CORE`

The current verified OSINT core does not serve structured ML features online. Revisit is mandatory when an approved trained model uses the same feature definitions offline and online.

## What remains UNKNOWN

- Production data volumes/growth and query profile;
- retention periods per data class/legal purpose;
- Production metadata/object/index availability/SLO;
- chosen vector/graph technologies, if ever promoted;
- first trained model requiring a Feature Store;
- deletion/retraction obligations by data class;
- Production data residency/region constraints.

## Result

```text
LESSON_12_DATA_ARCHITECTURE = CONDITIONAL_PASS
```

The end-to-end architecture and governance rules are defined. Exact Production storage technologies remain evidence-dependent.

## Improvement Review

| Priority | Improvement | Target |
|---|---|---|
| P0 | Finalize Production data classification, retention, deletion and external-processing matrix | 12–14 |
| P1 | Define dataset/index version registry and migration/rebuild procedure | 12–19 |
| P1 | Add lineage validation: raw → chunk → embedding/claim → review → knowledge | 12–18 |
| P1 | Define data quality telemetry per pipeline stage | 12–15 |
| P1 | Benchmark lexical/vector/graph layers before selecting Production stores | 12–17 |
| P2 | Add dataset manifests for eval/training corpora | 12–19 |
