# Lesson 13 — GenAI Quality & Testing

Status: `DOCUMENTATION / QUALITY-GATE DESIGN`

OTUS Lesson 13 requires a test plan for GenAI/RAG quality, including semantic metrics such as Faithfulness and Answer Relevancy, automated evaluation tooling and load testing.

For FATHER OSINT Agent this lesson adds a separate quality layer on top of existing deterministic acceptance testing.

## Existing test layer

`docs/04_testing/` already covers requirement-driven acceptance behavior of the OSINT DEV baseline.

Lesson 13 does **not** replace it. It adds evaluation for non-deterministic semantic components:

```text
Deterministic acceptance tests
        +
Versioned GenAI evaluation dataset
        +
Retrieval quality
        +
Generation quality
        +
Security / robustness
        +
Latency / throughput / cost
        ↓
GENAI_QUALITY_GATE
```

## Artifacts

- `01_GENAI_TEST_STRATEGY.md` — what is evaluated and why.
- `02_GOLDEN_EVAL_DATASET_CONTRACT.md` — versioned evaluation set and evidence-ground truth.
- `03_RAG_LLM_COMPARISON_TEST_PLAN.md` — fair comparison of two model routes on the same RAG task.
- `04_QUALITY_GATE_AND_CI_CONTRACT.md` — promotion/regression rules.
- `05_LOAD_RELIABILITY_SECURITY_TESTS.md` — performance, cost and adversarial test layers.
- `06_LESSON_13_REVIEW.md` — lesson result, UNKNOWNs and improvements.

## Core rule

```text
A model is not "better" because it sounds better.
It wins only if it passes the same versioned dataset,
retrieval context, security constraints and operational SLO gates.
```

No model/product is declared the winner in this documentation pass because comparable measured results do not yet exist.
