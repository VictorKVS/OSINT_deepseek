# Model-orchestrated Knowledge Pipeline

## Principle

Use models where semantic interpretation is required; keep evidence identity, provenance, hashes, offsets, versioning, gating and publication status deterministic.

The pipeline therefore uses two planes:

```text
EVIDENCE PLANE (deterministic)
bytes → SHA-256 → locator → page/offset → version → manifest → audit

SEMANTIC PLANE (model-assisted)
parse → translate → classify → extract → compare → reason → review → publish candidate
```

No model may overwrite or replace evidence-plane data.

## Stage map

| Stage | Purpose | Preferred model family | Deterministic gate |
|---|---|---|---|
| M0 | file identity / registry | none | bytes, MIME, SHA-256, source locator |
| M1 | document layout / OCR | document-layout / OCR models | page count, text coverage, block coordinates |
| M2 | tables / formulas / figures | table/layout parser + vision model when needed | cell/span geometry, figure/page locator |
| M3 | translation | specialized MT tournament + LLM challengers | aligned unit IDs, source hash, QC |
| M4 | semantic structure | classifier/LLM + rules | stable semantic IDs, parent/child structure |
| M5 | terminology / definitions | extraction LLM + embeddings | exact source span required |
| M6 | claims / principles / patterns / trade-offs | extractor LLM ensemble | candidate only, NEEDS_REVIEW |
| M7 | relation discovery | embeddings + reranker + relation classifier/LLM | relation endpoints must exist |
| M8 | contradiction / agreement | NLI / verifier LLM / judge | both evidence sides required |
| M9 | professor synthesis | stronger reasoning LLM with RAG | no unsupported claim publication |
| M10 | KB promotion QA | judge model + deterministic validator | schema, evidence coverage, review policy |

## Champion / challenger policy

Every semantic stage has a champion and optional challengers.

Calibration mode:

```text
same fixture set
   ├─ model A
   ├─ model B
   ├─ model C
   └─ specialized model
        ↓
metrics + blind judge + human sample review
        ↓
champion selected
```

Production mode:

```text
95–100% → champion
small canary sample → challenger(s)
quality regression → re-open tournament
```

This avoids running every large model on every page forever while preserving continuous improvement.

## Model roles

### Document parser

Responsibilities:
- reading order;
- headings;
- paragraphs;
- lists;
- table structure;
- formula/code blocks;
- figures/captions;
- page and bounding-box provenance.

A vision model is a fallback/helper for figures or difficult scanned regions, not the source of truth for ordinary machine-readable text.

### Translator

Responsibilities:
- EN→RU translation without summarization;
- terminology preservation;
- full-content preservation;
- aligned source/target units.

Translation candidates are selected by tournament. Specialized MT models should compete with general LLMs.

### Semantic structurer

Responsibilities:
- chapter/section hierarchy;
- paragraph role;
- example/list/table/callout classification;
- local topic boundaries.

Rules remain as a fallback and validation layer.

### Terminologist

Responsibilities:
- terms;
- aliases;
- definitions;
- abbreviations;
- English↔Russian terminology mapping;
- author-specific definitions.

Terminology objects keep evidence spans and are never promoted solely because a model emitted them.

### Knowledge extractor

Responsibilities:
- claims;
- principles;
- patterns;
- trade-offs;
- decision criteria;
- failure modes;
- examples;
- assumptions and applicability conditions.

Output is always candidate state first.

### Relation / contradiction analyst

Responsibilities:
- SUPPORTS;
- CONTRADICTS;
- REFINES;
- SPECIALIZES;
- GENERALIZES;
- ALTERNATIVE_TO;
- USES_DIFFERENT_DEFINITION;
- APPLIES_WHEN;
- FAILS_WHEN.

Embedding similarity alone may retrieve candidates but must not assert a semantic relation.

### Professor

Responsibilities:
- compare multiple books/documents;
- reconcile terminology;
- identify disagreements;
- distinguish context-dependent advice from universal-looking prose;
- build reasoned summaries and decision packets;
- state uncertainty and evidence gaps.

The professor must consume retrieved evidence objects, not raw unbounded corpus text.

### Judge / verifier

Responsibilities:
- independently score extraction fidelity;
- detect unsupported synthesis;
- reject missing evidence;
- compare champion/challenger outputs;
- trigger human review when margin/confidence is insufficient.

## Local hardware operating mode

On a single consumer GPU, heavyweight stages should run sequentially. Small embedding/reranking stages may be batched separately.

Suggested runtime pattern:

```text
parse/OCR
  ↓ unload
translation champion
  ↓ unload
embedding/index batch
  ↓ unload
extractor
  ↓ unload
verifier/judge
  ↓ unload
professor only for cross-source review
```

## Evidence contract for every model-produced object

Every semantic output must record at least:

- `stage_id`;
- `model_id`;
- `model_role`;
- `prompt_or_policy_version`;
- `source_object_ids`;
- `source_hashes`;
- `source_span_ids`;
- `output_hash`;
- `created_at`;
- `quality_status`;
- `review_status`;
- `judge_results` when used.

## Failure policy

Models fail closed.

Examples:
- OCR confidence insufficient → `NEEDS_OCR_REVIEW`;
- translation fails QC → `NEEDS_REVIEW`, not DONE;
- extraction has no evidence span → rejected;
- contradiction has only one source side → rejected;
- professor produces unsupported claim → rejected;
- judge disagreement above threshold → HUMAN_REVIEW_REQUIRED.

## Target architecture

```text
SOURCE
  ↓
Evidence Registry
  ↓
Document Model
  ↓
Translation Tournament
  ↓
Semantic Structure Model
  ↓
Terminology Model ──────┐
  ↓                     │
Knowledge Extractor     │
  ↓                     │
Embeddings / Retrieval ─┤
  ↓                     │
Relation + NLI Analyst  │
  ↓                     │
Professor / RAG ◀───────┘
  ↓
Independent Judge
  ↓
Deterministic Promotion Gate
  ↓
KNOWLEDGE_CORE
```
