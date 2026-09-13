# Lesson 12 — Data Architecture for AI Systems

Status: `DOCUMENTATION LAYER / CURRENT DATA SEMANTICS + CANDIDATE PRODUCTION STORES`

OTUS Lesson 12 asks for an end-to-end data pipeline, storage selection (Data Lake / Feature Store / Vector DB etc.), and Data Governance with attention to consistency between offline/training and online/inference paths.

For FATHER OSINT Agent the primary concern is **evidence lineage**: original source observations and raw payloads must remain traceable through parsing, chunking, retrieval, semantic extraction, review and later knowledge promotion.

## Artifacts

- `01_END_TO_END_DATA_PIPELINE.md` — source → raw → normalize → enrich → index → review/knowledge flow.
- `02_STORAGE_SELECTION.md` — role-based storage choices; technology names remain candidates until workload requirements exist.
- `03_DATA_GOVERNANCE_LINEAGE.md` — ownership, lineage, versions, retention, deletion/retraction and quality rules.
- `04_FEATURE_STORE_APPLICABILITY.md` — when Feature Store is actually required and how training-serving skew is prevented.
- `05_LESSON_12_REVIEW.md` — result, UNKNOWNs and improvement actions.

## Core principle

```text
Preserve original evidence first
→ transform with versioned lineage
→ build replaceable indexes/derivatives
→ promote knowledge only after review/gates
```

The project does not treat a Vector DB, Knowledge Graph, Data Lake or Feature Store as mandatory merely because they appear in an AI reference architecture.