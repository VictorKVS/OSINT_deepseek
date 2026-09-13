# Lesson 06 — RAG Applicability and Option Set

Status: `CANDIDATE DECISION INPUT`

## Problem

The OSINT worker already returns provenance-rich evidence packages. As the knowledge corpus grows, downstream Analyst/Knowledge Factory needs a controlled way to retrieve relevant evidence and relations without scanning the entire corpus manually.

RAG is therefore evaluated as a **downstream evidence-retrieval and context-building mechanism**, not as a replacement for OSINT acquisition or Knowledge Gate review.

## Options

### Option A — lexical / deterministic retrieval baseline

Use metadata filters, exact terms, BM25/full-text or equivalent deterministic retrieval.

Strengths:
- explainable baseline;
- low semantic ambiguity;
- easy to audit;
- inexpensive.

Weaknesses:
- synonym/concept mismatch;
- weaker semantic recall;
- limited cross-document relation discovery.

### Option B — vector RAG

Embed evidence chunks and retrieve by semantic similarity.

Strengths:
- semantic recall;
- useful for paraphrases and related concepts.

Weaknesses:
- retrieval score is not truth;
- index/model/version lifecycle;
- possible semantic false positives;
- requires eval data.

### Option C — hybrid lexical + vector + reranking

Combine lexical and vector candidates, normalize/fuse them and rerank.

Strengths:
- balances exact terminology with semantic recall;
- supports measurable retrieval comparison;
- fits current M7 relation-discovery candidate stack.

Weaknesses:
- more moving parts;
- latency/cost;
- tuning/evaluation complexity.

### Option D — hybrid retrieval + Knowledge Graph

Use lexical/vector retrieval plus traversal of evidence-grounded entities/relations.

Strengths:
- explicit relation navigation;
- useful for definitions, contradictions, requirements, entities and cross-document dependencies;
- can expose WHY one item was included.

Weaknesses:
- graph construction/review cost;
- relation errors can amplify bad context;
- requires provenance-preserving graph model.

## Current candidate direction

`Option C` is the simplest advanced candidate to evaluate first, with `Option D` added only for queries where graph traversal demonstrably improves retrieval or traceability.

This is not a final ADR. It is an evaluation order:

```text
lexical baseline
   ↓ compare
vector retrieval
   ↓ compare
hybrid + reranker
   ↓ only if justified
KG-assisted retrieval
```

## Advanced patterns

### Self-RAG style behavior

Useful only if the system can decide when retrieval is needed and then verify its own evidence use. It must not become an uncontrolled autonomous loop.

### CRAG style correction

Candidate when retrieval confidence/coverage is insufficient: widen/narrow query, request new source evidence or fall back to an explicit gap. Correction must remain bounded.

### Cache Augmented Generation

Candidate only for stable, approved context. Cache keys must include corpus/model/version scope; stale context cannot silently override fresher evidence.

## Decision criteria

- retrieval recall/precision on a representative set;
- evidence citation resolution rate;
- groundedness/faithfulness;
- latency;
- compute/token cost;
- corpus freshness behavior;
- index/update complexity;
- poisoning resistance;
- explainability / provenance visibility;
- rework rate after reviewer challenge.

## Required evidence before adoption

- versioned evaluation/golden query set;
- baseline lexical results;
- comparable candidate runs;
- failure examples;
- security review;
- operational cost/latency evidence;
- architecture review and ADR if a new persistent component/provider is introduced.
