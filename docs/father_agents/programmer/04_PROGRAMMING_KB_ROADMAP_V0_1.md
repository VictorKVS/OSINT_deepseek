# PROGRAMMING_KB Roadmap v0.1

Status: **DRAFT EXECUTION PLAN**  
Date: **2026-08-14**

## 1. Objective

Build a source-grounded programming knowledge base that allows the Programmer Agent to answer not only **what to implement**, but also:

- why this design/function/dependency is justified;
- which alternatives exist;
- what risks each alternative adds;
- what evidence is strong enough for the decision class;
- what must be measured locally;
- when the decision should be revisited.

## 2. Delivery strategy

The KB is built breadth-first to a minimum professional working level, then deepened. We do not spend months perfecting one language while other critical engineering domains remain empty.

```text
MINIMUM PROFESSIONAL COVERAGE
        ↓
MEDIUM DEPTH / MORE CASES
        ↓
MAXIMUM DEPTH / SPECIALIST + PRINCIPAL LEVEL
```

## 3. Phase gates

### P0 — Governance and evidence contract
Deliver:
- source hierarchy;
- Knowledge Object schema;
- Decision Evidence Bundle;
- freshness/supersession rules;
- counter-evidence and revisit rules.

Gate: one sample D2 decision can be reconstructed from requirement to source, risk, experiment and result.

### P1 — Profession map and coverage matrix
Use SWEBOK V4.0a as the first consensus map and map it to 12 FATHER Programmer domains.

Deliver a matrix:

```text
domain → subdomain → required competencies → source coverage → card count → validation state → gaps
```

Gate: every critical domain has explicit P0/P1/P2 gaps; no undefined word such as "many" or "enough" is used without a threshold.

### P2 — Canonical specification layer
Ingest/normalize official specifications and current product/runtime documentation for the first MVP stack.

First MVP stack:
- Python;
- FastAPI/backend HTTP APIs;
- PostgreSQL;
- Git/GitHub;
- Linux basics relevant to runtime;
- Docker only where deployment requires it;
- pytest/testing;
- observability baseline;
- secure-development baseline.

Gate: all version-sensitive cards identify exact source/version and review date.

### P3 — Fundamental engineering layer
Build durable cards for:
- algorithms/data structures;
- program design/modularity;
- error handling;
- state and side effects;
- concurrency basics;
- persistence/transactions;
- API contracts;
- testing methods;
- performance measurement.

Sources: SWEBOK-guided textbooks + scientific evidence + official specifications.

Gate: agent can solve bounded backend design tasks without defaulting to framework-specific folklore.

### P4 — Security + DevSecOps integration
Map PROGRAMMING_KB to:
- NIST SSDF;
- OWASP ASVS;
- SLSA;
- OpenSSF dependency/project signals;
- SECURITY_KB / DEVSECOPS_KB when those stores are connected.

Gate: every sample implementation produces security and supply-chain evidence appropriate to its risk class.

### P5 — Reliability / operations / performance
Add:
- timeout/retry/idempotency decisions;
- failure modes and degraded behaviour;
- logging/metrics/tracing;
- profiling;
- load/latency/resource benchmarks;
- rollback/recovery patterns.

Gate: context-dependent claims are measured, not merely cited.

### P6 — Architecture decision engine
Create comparison templates for recurring D2 decisions:
- function/module/service boundary;
- sync vs async;
- monolith/module/microservice;
- REST vs event/message interface where relevant;
- SQL vs alternative stores;
- language/runtime selection;
- library/framework adoption;
- cache introduction;
- consistency/availability trade-offs;
- build/deployment model.

Gate: each scenario records at least two credible alternatives, counter-evidence and revisit conditions.

### P7 — Evaluation corpus
Create benchmark tasks with known acceptance requirements and independently reviewed expected reasoning.

Task families:
- bug fix;
- small feature;
- refactor;
- API design;
- schema/transaction decision;
- performance bottleneck;
- security defect;
- dependency replacement;
- reliability failure;
- architecture choice.

Gate: repeated agent runs are scored on evidence correctness, source applicability, solution correctness, test quality, risk coverage and unnecessary complexity.

### P8 — FATHER integration
Connect:

```text
Architect/Analyst task
  → Programmer evidence retrieval
  → decision package
  → implementation
  → Test/Security/DevSecOps gates
  → Principal Critic
  → Knowledge Gate
  → experience feedback into PROGRAMMING_KB
```

Gate: successful and failed decisions both feed structured experience records without converting runtime anecdotes directly into universal knowledge.

## 4. Concrete coverage targets

Raw card count is not a completeness proof; it is only a progress control. Coverage gates require both count and domain distribution.

### MIN — professional working MVP
- 12/12 critical domains represented;
- >= 120 VALIDATED or LIMITED knowledge cards total;
- >= 10 cards in each critical domain or an explicit justified exception;
- 0 unresolved P0 coverage gaps;
- >= 20 independently reviewable decision scenarios;
- >= 10 scenarios executed end-to-end with code + tests + evidence;
- 100% of D2/D3 sample decisions include alternatives, risks, source refs, applicability and revisit conditions;
- 0 invented benchmark values or untraceable source claims in acceptance corpus.

### MEDIUM — strong senior-working layer
- >= 500 validated/limited cards;
- >= 60 decision scenarios;
- >= 40 end-to-end evaluated implementations;
- Python/backend stack deep coverage plus at least one compiled language comparison lane;
- calibrated source-quality and decision-sufficiency metrics based on observed review results;
- automated stale-source detection for version-sensitive cards.

### MAX — principal/research expansion
- >= 1500 validated/limited cards across general + specialist domains;
- >= 150 decision scenarios;
- >= 100 end-to-end evaluated implementations;
- multiple language/runtime families;
- scientific-evidence synthesis for contested engineering questions;
- failure-injection, performance and security benchmark suites;
- cross-KB integration with Architecture, Security, DevSecOps, Reliability and Product knowledge;
- measured agent regression dashboard across versions.

These thresholds may be revised only through an evidence-backed roadmap record; changing the number to make a gate green is prohibited.

## 5. Work queue — next 10 controlled steps

1. Approve Programmer Agent passport and evidence schema.
2. Build the 12-domain coverage matrix from SWEBOK V4.0a.
3. Create source-card schema and first seven authoritative source cards.
4. Acquire canonical Python/PEP/CPython sources and version policy.
5. Acquire PostgreSQL, HTTP/IETF, OpenAPI and pytest canonical sources.
6. Build first 30 fundamental Python/backend Knowledge Objects.
7. Build first five D2 decision templates: sync/async, library adoption, DB transaction boundary, API boundary, module/service boundary.
8. Create 10 evaluation tasks and have Principal Critic review expected evidence requirements before agent implementation.
9. Run the Programmer Agent manually/semi-automatically through those tasks; capture failures and missing knowledge.
10. Only after gates are stable, design executable agent orchestration and KB retrieval code.

## 6. Risks

| Risk | Control |
|---|---|
| KB becomes a link dump | Knowledge Objects require claim, scope, applicability, risk and verification method |
| citation theater | source class + directness + local evidence + critic review |
| stale framework knowledge | version/status/review-after/superseded fields |
| overfitting to Python | use profession-wide domain map first; stack-specific cards second |
| microservice/tool fashion bias | smallest-sufficient-complexity rule and explicit alternatives |
| excessive process slows MVP | D0-D3 decision classes scale evidence depth to impact |
| source-count gaming | coverage and scenario gates, not card count alone |
| scientific papers misapplied | methodology/scope/applicability summary required before E2 use |
| agent copies insecure OSS code | OSS practice is E4/E5 evidence only after provenance and security review |
| incorrect confidence math | no synthetic confidence score until calibration dataset exists |

## 7. Current status

```text
P0 evidence contract       STARTED
P1 coverage matrix         NEXT
P2 canonical sources       STARTED / seed 7
P3 fundamentals            NOT STARTED
P4 security/devsecops      BASELINES IDENTIFIED
P5 reliability/performance NOT STARTED
P6 decision engine         DESIGN OUTLINE
P7 evaluation corpus       NOT STARTED
P8 executable integration  NOT AUTHORIZED
```
