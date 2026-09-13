# Lesson 01 / Product — Assumption / UNKNOWN Log

Status: `ACTIVE`

| ID | Type | Statement | Owner | Validation trigger | Downstream impact |
|---|---|---|---|---|---|
| AU-01 | ASSUMPTION | preserving provenance materially improves downstream analytical trust and reuse | Product / Analyst | repeated-investigation comparison | Product KPI / architecture priorities |
| AU-02 | ASSUMPTION | bounded research loops are preferable to open-ended autonomous research | Product / Analyst | pilot investigations | orchestration and cost controls |
| AU-03 | UNKNOWN | first external/commercial user segment | Product Owner | product decision | UX, packaging, SLA, pricing |
| AU-04 | UNKNOWN | production legal basis and constraints for each live-source class | Legal/Compliance | before source activation | source enablement / security / retention |
| AU-05 | UNKNOWN | production data classification and retention matrix | Data Owner | before production persistence | storage/security/backup |
| AU-06 | UNKNOWN | target production throughput, latency and concurrency | Product + Operations | telemetry / workload forecast | sizing / architecture / NFR |
| AU-07 | UNKNOWN | production availability objective and support hours | Service Owner | service-model decision | HA/DR/operations |
| AU-08 | UNKNOWN | approved production LLM hosting model | Architecture decision | lessons 8–9 / TCO + CTO challenge | privacy/cost/latency/support |
| AU-09 | UNKNOWN | acceptable monthly operating cost / TCO envelope | Business Owner / Finance | budget decision | provider/runtime options |
| AU-10 | FUTURE_DECISION | automatic KB publication | Product + Governance | later maturity gate | authority/security/audit |

## Rule

An UNKNOWN may block a later gate, but it must never be silently converted into a fact because code or an experimental component already exists.
