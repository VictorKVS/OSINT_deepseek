# GenAI Test Strategy

Status: `DRAFT_FROM_CURRENT_EVIDENCE`

## 1. Purpose

Define how FATHER evaluates semantic/RAG/LLM behavior without confusing fluent output with correctness.

The strategy separates five quality layers:

1. retrieval quality;
2. answer quality;
3. grounding / faithfulness;
4. security / robustness;
5. operational quality: latency, throughput, reliability and cost.

## 2. System under evaluation

The candidate semantic flow is:

```mermaid
flowchart LR
    Q[Question / Research Need] --> R[Retriever]
    R --> C[Evidence Context]
    C --> M[Model / Analyst Candidate]
    M --> A[Answer / Finding]
    A --> V[Verifier / Judge]
```

The current OSINT collector remains outside the semantic quality claim. It supplies provenance-rich evidence; Lesson 13 evaluates what later retrieval/model stages do with that evidence.

## 3. Evaluation dimensions

| Dimension | Question | Candidate metrics |
|---|---|---|
| Retrieval | Did we retrieve the evidence needed to answer? | Recall@K, Precision@K, MRR/NDCG where meaningful, evidence coverage |
| Faithfulness | Is the answer supported by retrieved evidence? | Faithfulness / groundedness, unsupported-claim rate |
| Answer relevance | Does the answer address the question? | Answer Relevancy, task-specific rubric |
| Completeness | Did the answer omit material expected facts? | expected-evidence coverage, rubric score |
| Citation/provenance | Can claims be traced to resolvable evidence refs? | citation resolution rate, evidence coverage |
| Safety/security | Can untrusted content alter policy/tool behavior? | prompt-injection pass/fail, tool-policy violations |
| Consistency | Does repeated execution remain within acceptable variance? | variance/disagreement rate |
| Latency | Is response time acceptable? | p50/p95/p99 |
| Throughput | Can the route handle expected concurrency? | req/s, tokens/s, queue time |
| Reliability | Does the route fail/recover predictably? | error rate, timeout rate, retry/recovery success |
| Cost | What does accepted quality cost? | cost/query, cost/accepted answer, monthly scenario |

## 4. Metric hierarchy

No single metric is authoritative.

```text
Hard safety / evidence gates
        ↓
Retrieval sufficiency
        ↓
Faithfulness / unsupported claims
        ↓
Answer relevance / usefulness
        ↓
Latency / throughput / cost
```

A model that is cheaper or faster but fails evidence/safety gates cannot win the comparison.

## 5. Evaluation classes

### Deterministic checks

Prefer code/schema checks for:

- citation/reference resolution;
- required output fields;
- source-id existence;
- tool allowlist compliance;
- budget/cycle limits;
- structured output validity.

### Reference-based semantic evaluation

Use curated expected evidence/answers when a stable reference exists.

### Rubric / LLM-as-judge evaluation

May be used for dimensions that are difficult to encode deterministically, but:

- judge model/version is recorded;
- judge is independent from the candidate route where material;
- rubric is versioned;
- a human-labeled calibration subset is maintained;
- close/disputed results escalate to human review.

### Human review

Required for:

- evaluation-set creation/changes;
- material false-positive/false-negative findings;
- close model comparisons;
- legal/security correctness;
- acceptance of residual quality risk.

## 6. Tools

OTUS names `DeepEval` and `Ragas` as candidate automated evaluation frameworks. They are **tool candidates**, not required architecture dependencies.

Selection criteria:

- metrics needed by this project;
- ability to work with custom evidence IDs/rubrics;
- reproducibility;
- CI integration;
- offline/local execution needs;
- provider/data-policy constraints;
- maintenance/license/supply-chain review.

## 7. Baseline strategy

Every semantic improvement must be compared against a baseline.

Examples:

- lexical-only retrieval vs hybrid retrieval;
- no reranker vs reranker;
- Model A vs Model B with the same retrieval context;
- current prompt/policy vs candidate prompt/policy;
- hosted model vs local model on the same dataset.

## 8. Regression principle

A release must not be promoted only because average quality improves.

Check:

- critical-case regressions;
- security regressions;
- unsupported claims;
- subgroup/source-class regressions;
- latency/cost regressions;
- new UNKNOWN or evidence gaps.

## 9. Current status

The project has candidate semantic architecture and model-stage policy, but the versioned Golden/Eval dataset and measured comparison results are not yet baselined.

Therefore:

`GENAI_QUALITY_STATUS = DESIGN_READY / MEASUREMENT_PENDING`.
