# Lesson 02 — OSINT Agent NFR Baseline

Status: `DRAFT / BASELINES INCOMPLETE`

## Current DEV qualities already evidenced

| NFR | Current intent | Verification/evidence | State |
|---|---|---|---|
| bounded collection | `max_items` and bounded cycles prevent uncontrolled work | contract/tests | CURRENT |
| failure visibility | collector errors and stop reason visible | MaterialPackage/tests | CURRENT |
| provenance integrity | source observation survives payload reuse | acceptance/semantic remediation | CURRENT |
| deterministic fixtures | repeatable DEV verification | tests/CI baseline | CURRENT |
| secrets hygiene | no secrets committed; safe error surface | repo/security controls | CURRENT / ongoing |
| source adapter replaceability | Collector/transport boundary | architecture/PoC path | CURRENT DESIGN |
| inspectability/auditability | local evidence + traceability/journal | project docs/storage | CURRENT DEV |

## Production NFR candidates requiring baseline/owner

| ID | Category | Metric / scenario | Target | Verification intent | State |
|---|---|---|---|---|---|
| NFR-P01 | Freshness | source event/document → available evidence | `TO_BE_BASELINED` | time-stamped E2E test | OPEN |
| NFR-P02 | Throughput | material observations processed per time unit | `TO_BE_BASELINED` | load/operational test | OPEN |
| NFR-P03 | Concurrency | parallel tasks/sources without unacceptable degradation | `TO_BE_BASELINED` | concurrency test | OPEN |
| NFR-P04 | Latency | task submission → first/complete package by task class | `TO_BE_BASELINED` | p50/p95 telemetry | OPEN |
| NFR-P05 | Availability | service/task acceptance and processing availability | `TO_BE_BASELINED` | SLO monitoring | OPEN |
| NFR-P06 | Recovery | restart without evidence/checkpoint loss | requirement exists conceptually; target RTO/RPO unknown | restart/reconciliation test | PARTIAL |
| NFR-P07 | Evidence integrity | observation/provenance loss rate | zero silent loss intended | invariant tests/audit | CANDIDATE |
| NFR-P08 | Storage growth | bytes/observations per source/workspace/time | `TO_BE_BASELINED` | storage telemetry | OPEN |
| NFR-P09 | Semantic quality | retrieval/analysis quality for future RAG/LLM stages | `TO_BE_BASELINED` | versioned eval/golden set | FUTURE |
| NFR-P10 | Cost | cost/task or cost/useful evidence/semantic request | `TO_BE_BASELINED` | FinOps/TCO telemetry | OPEN |

## Rule

OTUS example values are not copied as OSINT project targets. Targets require Product/Operations/QA/Security/Data owners and measured baselines.

## Trace

`Product outcome -> NFR -> verification method -> architecture driver -> test/telemetry`.
