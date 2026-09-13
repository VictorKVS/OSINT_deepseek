# Lesson 13 — Review / What Changed

Status: `CONDITIONAL_PASS / EXECUTION EVIDENCE PENDING`

## What Lesson 13 adds

Before this lesson the project had:

- deterministic acceptance tests;
- RAG/agent candidate architecture;
- model-stage policy;
- security threat register;
- hosting/CTO decision framework.

Lesson 13 adds the missing **semantic quality contract**:

- versioned Golden/Eval Dataset;
- retrieval metrics;
- Faithfulness / groundedness;
- Answer Relevancy / task usefulness;
- citation/provenance checks;
- security/adversarial evaluation;
- load/reliability/cost evaluation;
- fair Model A vs Model B comparison;
- CI/promotion quality gate.

## Current project state

```text
DETERMINISTIC TESTING   = EXISTING
GENAI TEST STRATEGY     = DOCUMENTED
GOLDEN/EVAL CONTRACT    = DOCUMENTED / DATASET NOT BASELINED
MODEL A vs MODEL B PLAN = READY FOR EXECUTION
GENAI CI QUALITY GATE   = CONTRACT DEFINED
MEASURED WINNER         = UNKNOWN
PRODUCTION THRESHOLDS   = TO_BE_BASELINED
```

## Gate interpretation

`LESSON_13_GENAI_QUALITY = CONDITIONAL_PASS`

Reason: the test/evaluation architecture is complete enough to execute, but no fake scores or model winner are claimed before a reviewed dataset and comparable runs exist.

## What should be improved

| Priority | Improvement | Why |
|---|---|---|
| P1 | Populate v1 Golden/Eval Dataset | architecture needs executable quality evidence |
| P1 | Calibrate automated judge/rubrics against human labels | LLM-as-judge must not become unverified authority |
| P1 | Select Model A / Model B candidates and run same-context comparison | Lesson 9 hosting ADR needs measured quality evidence |
| P1 | Define baseline thresholds from real measurements | avoid invented pass percentages |
| P0 | Add prompt-injection/retrieval-poisoning cases before agentic RAG | security gate |
| P1 | Integrate compact semantic regression into CI only after dataset/tooling is approved | automate without hiding flakiness |
| P2 | Feed model/judge acceptance and rework telemetry into Model Zoo routing | adaptive model portfolio |

## Relationship to FATHER automation

The same quality engine should later evaluate:

- generated requirements/documents;
- RAG answers;
- architecture review outputs;
- Model Zoo champion/challenger/judge behavior;
- automated document-review recommendations.

Thus Lesson 13 becomes a reusable verification layer for the **whole design-and-implementation factory**, not only one RAG demo.
