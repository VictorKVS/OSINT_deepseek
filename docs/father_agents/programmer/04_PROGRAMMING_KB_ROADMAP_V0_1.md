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
P1 coverage matrix         STARTED
P2 canonical sources       STARTED / 15 source cards
P3 fundamentals            STARTED / 7 provisional Knowledge Objects
P4 security/devsecops      BASELINES IDENTIFIED
P5 reliability/performance NOT STARTED
P6 decision engine         DESIGN OUTLINE
P7 evaluation corpus       NOT STARTED
P8 executable integration  NOT AUTHORIZED
```

## 8. Cross-FATHER agent evolution — captured future path

This section records high-value ideas that must not be lost, while explicitly keeping them **outside the current M5 critical path and outside Programmer runtime implementation**.

### F0 — Three flagship professional agents
Initial professional development focus:
- `PROGRAMMER`;
- `ARCHITECT`;
- `SECURITY`.

Other professional agents are added only after their knowledge bases and evaluation material reach a usable evidence threshold.

### F1 — Qualification levels are permissions, not separate agents
Use one professional agent with evidence-backed qualification states rather than cloning Junior/Master/Senior agents.

Initial model:
- **Junior** — follows approved instructions/contracts; no material autonomous design decisions;
- **Master** — may discover alternatives and propose improvements; material changes require approval;
- **Senior** — may select bounded engineering routes independently, but must produce strong evidence, alternatives, risks and validation.

Promotion must depend on measured performance history, not prompt wording or self-declaration.

### F2 — Independent Principal Critic
The Critic is independent from the authoring agent and attempts to falsify material decisions.

Required review dimensions:
- false or hidden assumptions;
- missing evidence;
- credible counterexamples;
- stronger/dominating alternatives;
- security and reliability failures;
- economic/cost errors;
- unnecessary complexity;
- unmeasured claims represented explicitly as `UNKNOWN` / `UNMEASURED`, never invented numbers.

### F3 — Experience / Failure / Counterexample memory
Successful and failed work both become structured experience:

```text
failure
→ normalized failure record
→ root cause
→ fix
→ regression test
→ candidate knowledge rule
→ independent review
→ trusted/limited KB object
```

A single successful anecdote must not automatically become universal knowledge.

### F4 — Agent Arena / Tournament system
After the KB and evaluation corpus are mature enough, create controlled competitions between multiple runs/versions/strategies of the same professional agent.

Minimum prerequisites:
- objective acceptance criteria;
- hidden or independently controlled evaluation tasks;
- reproducible sandbox/tool execution where applicable;
- scorecard separating speed from correctness, safety and evidence quality;
- tournament history and weakness map.

Arena progression should move from ordinary coverage tasks to weakness-driven, adversarial and novel-combination tasks rather than endlessly generating low-information repetitions.

### F5 — Adversarial Agent Researcher / FATHER immune system
In an isolated, authorized sandbox, research attacks against FATHER agents themselves, including prompt/tool/memory/data poisoning and permission-confusion classes.

Learning loop:

```text
attack scenario
→ observed failure
→ root cause
→ countermeasure
→ regression test
→ defensive rule
→ distribution to affected agents
```

This is a future security research capability, not authorization for uncontrolled external attack activity.

### F6 — Secure Knowledge / IP Vault
Do not assume a fixed per-agent storage size such as 1–5 TB before measurement.

Preferred logical model:

```text
SHARED KNOWLEDGE CORE
  ├─ PROGRAMMER delta
  ├─ ARCHITECT delta
  └─ SECURITY delta
```

Separate public/open material from proprietary material. Candidate protected IP includes:
- decision graphs and proprietary relation weights;
- calibrated source/decision coefficients;
- hidden evaluation corpus;
- tournament/failure corpus;
- routing and decision policies;
- proprietary mappings;
- customer-specific intelligence and results.

Actual LLM provider model weights are not to be confused with FATHER-owned decision/knowledge weights.

### F7 — Economics and cost instrumentation
Do not hard-code speculative prices. Build measurable cost models first.

Track at minimum:
- storage hot/warm/cold/backup/replication/egress;
- inference and retrieval cost;
- sandbox/tool/compute cost;
- critic/judge/human-review cost;
- `cost per task`;
- `cost per validated competence`;
- training/evaluation cost;
- support and risk reserve;
- commercial unit economics and ROI.

Real provider tariffs and measured usage are substituted only when the architecture and workload are known.

### F8 — Learning research only after evidence corpus exists
Tournament history and verified experience may later support:
- retrieval/policy improvement;
- supervised fine-tuning;
- preference tuning;
- distillation;
- reward modelling / reinforcement learning where justified.

RAG/history alone must not be mislabeled as model-weight training. Any deeper training path requires measurable gain over the simpler retrieval/policy baseline and an explicit economic case.

### Future execution order

```text
PROGRAMMER_KB + ARCHITECTURE_KB + SECURITY_KB
→ evidence contracts
→ qualification metrics
→ independent Critic
→ evaluation corpus
→ experience/failure memory
→ Mini Arena
→ tournament history / weakness maps
→ controlled adversarial-agent research
→ secure IP Vault at production-sensitive scale
→ learning-method research
→ measured commercial economics
```

**Current disposition:** CAPTURED / DEFERRED. These ideas are preserved as the post-KB evolution path and do not displace the current M5 product gate.