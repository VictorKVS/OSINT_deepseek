# Lesson 09 — Review / CTO Challenge

Status: `PASS FOR HOMEWORK PACKAGE / PRODUCTION DECISION STILL CONDITIONAL`

## Homework criteria coverage

| Criterion | Coverage |
|---|---|
| Compare cost | TCO formulas/input gaps + qualitative current-stage cost trade-off |
| Privacy/security | explicit classification gate + external AI threat trace |
| Quality | common eval/quality gate required across options |
| Latency | p50/p95 listed as mandatory comparable evidence |
| Support complexity | managed API vs self-hosted/cloud/on-prem ops burden compared |
| Make a decision | ADR-0004 accepted with conditions for current PoC/MVP stage |
| ADR structure | Context, drivers, options, decision, consequences, verification, rollback, triggers |
| Honest trade-offs | provider dependency/privacy/cost uncertainty/gateway complexity preserved |
| CTO pitch | `04_CTO_CHALLENGE.md` |

## Project state after Lessons 1–9

```text
Product / Presale                 CONDITIONAL_PASS
Delivery Strategy                 CONDITIONAL_PASS
HLD / C4                          CONDITIONAL_PASS
LLD                               CONDITIONAL_PASS
RAG                               CANDIDATE / EVAL REQUIRED
Multi-Agent                       CANDIDATE / SECURITY+VALUE PROOF REQUIRED
ADR discipline                    READY
LLM hosting current-stage policy  ACCEPTED_WITH_CONDITIONS
CTO Challenge                     PASS FOR COURSE REVIEW
Production readiness              NOT CLAIMED
```

## Improvement Review

| Priority | Improvement | Target |
|---|---|---|
| P0 | complete data classification/legal approval matrix for external model processing | before real sensitive external LLM use |
| P1 | collect provider/model/version/token/latency/quality telemetry | first semantic PoC |
| P1 | build comparable local-model eval on same dataset | Lessons 13/17 |
| P1 | replace qualitative TCO with current quotes + measured load | before Production hosting ADR |
| P1 | define Model Gateway contract and compliance tests before provider becomes runtime dependency | architecture/integration pass |
| P1 | add independent reviewer sign-off to material ADRs | Lesson 9/10 governance |
| P2 | visualize ADR/driver/trade-off/TCO trace in FATHER site | site pass |

## What remains UNKNOWN

- final Production model/provider;
- final Production deployment;
- Production external-processing data classes;
- comparable TCO winner;
- quality winner on project eval set;
- final SLO/capacity envelope.

These gaps are intentional and visible. The current decision does not claim to resolve them.
