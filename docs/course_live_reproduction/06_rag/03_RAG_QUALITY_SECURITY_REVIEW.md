# Lesson 06 — RAG Quality, Security and Review

Status: `CANDIDATE QUALITY/SECURITY CONTRACT`

## Quality dimensions

| Dimension | Example metric / evidence | Current state |
|---|---|---|
| retrieval coverage | Recall@k or judged coverage on versioned query set | BASELINE REQUIRED |
| ranking quality | nDCG/MRR or reviewer preference on labeled set | BASELINE REQUIRED |
| citation resolution | returned evidence refs resolve to exact source/version/span | REQUIRED |
| groundedness | claims supported by retrieved evidence | REQUIRED / eval method pending |
| conflict visibility | contradictory evidence retained/exposed | REQUIRED |
| freshness | selected evidence respects project freshness/version constraints | REQUIREMENT NEEDED |
| latency | retrieval + rerank + generation duration | BASELINE REQUIRED |
| cost | model/embedding/rerank/token/storage cost | BASELINE REQUIRED |
| reviewer rework | share of outputs returned for evidence correction | TELEMETRY CANDIDATE |

## Security threats linked to current project register

- indirect prompt injection from retrieved Telegram/web/PDF/file content;
- RAG/retrieval poisoning;
- memory/KB poisoning;
- external provider receives sensitive evidence;
- model/provider update changes behavior;
- cross-agent/tool action based on poisoned context if agentic tools are later enabled.

## Required controls before Production RAG

1. retrieved content remains data, not policy/instruction;
2. provenance-aware retrieval and resolvable citations;
3. corpus/index change audit;
4. data-classification filter before external provider use;
5. version inventory for embedding/reranker/generator models;
6. bounded retrieval/correction loops;
7. evidence conflict preservation;
8. independent review before KB promotion;
9. representative golden/eval query set;
10. rollback/reindex path when a corpus/model/index is poisoned or wrong.

## Lesson result

`RAG_DESIGN_READY = CONDITIONAL_PASS`

We have an evidence-grounded candidate architecture and evaluation order, but no claim of implemented/validated RAG.

## Improvement Review

| Priority | Improvement | Target |
|---|---|---|
| P1 | create versioned retrieval/eval query set with expected evidence refs | Lessons 6/13 |
| P1 | establish lexical baseline before adding vector/graph complexity | before RAG implementation |
| P0 | enforce untrusted-content boundary and provenance-aware retrieval | before agentic/Production RAG |
| P1 | version embedding/reranker/generator/index together in eval evidence | Lessons 6/19 |
| P1 | define freshness/index update SLO from product use case | Lessons 12/15 |
| P2 | expose retrieval trace in UI for analyst inspection | site/analyst UX pass |

## UNKNOWN

- approved vector DB;
- graph store technology;
- embedding/reranker/generator models;
- corpus volume/growth;
- required latency and cost ceiling;
- eval dataset size/coverage;
- first Product feature that actually requires RAG.
