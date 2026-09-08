# PROGRAMMING_KB Coverage Matrix v0.1

Status: **INITIAL GAP MAP / NOT YET SUFFICIENT**  
Date: **2026-08-14**  
Primary profession map: **IEEE Computer Society SWEBOK Guide V4.0a**

## 1. Purpose

This matrix prevents the Programmer Agent knowledge base from becoming a random collection of Python/framework notes. SWEBOK V4.0a is used as the first profession-wide consensus map; FATHER keeps a smaller 12-domain operational map for retrieval, evaluation and measurable coverage.

`COVERED` below never means “complete”. At this stage it means only that the domain has an explicit place, source lane and planned validation path.

## 2. FATHER 12-domain operational map

| FATHER domain | Core questions the agent must answer | SWEBOK V4.0a anchors | Current state | P0 gap |
|---|---|---|---|---|
| D01 Requirements & specification | What exactly must be true? Which constraints and acceptance criteria exist? | Software Requirements; Models & Methods; Quality | SEED | Need requirement-card templates and ambiguity/assumption protocol examples |
| D02 Algorithms & data structures | What algorithm/data structure fits correctness, complexity and resource constraints? | Software Construction; Computing Foundations; Mathematical Foundations | GAP | Need canonical algorithms/complexity sources + evaluated examples |
| D03 Languages & runtimes | Why this language/runtime/version? What safety, concurrency, tooling and lifecycle properties matter? | Software Construction; Computing Foundations; Software Engineering Operations | GAP | Python canonical layer first; comparative Go/Rust/Java lane later |
| D04 API & interface design | What contract should components expose and how is compatibility preserved? | Software Architecture; Software Design; Software Construction; Requirements | GAP | Need HTTP/IETF, OpenAPI, schema/versioning and contract-test cards |
| D05 Data, storage & transactions | How is state represented, persisted, isolated, migrated and recovered? | Software Design; Software Construction; Computing Foundations; Quality | GAP | PostgreSQL/SQLite canonical source cards + transaction/isolation cases |
| D06 Concurrency & distributed systems | Where can races, ordering, partial failure, consistency and network uncertainty occur? | Software Architecture; Software Design; Construction; Computing/Engineering Foundations | GAP | Need concurrency memory-model sources, distributed failure/consistency evidence |
| D07 Architecture & decomposition | Why function/module/package/process/service? Where are boundaries and trade-offs? | Software Architecture; Software Design; Models & Methods; Economics | SEED | Need decision templates and measured anti-overengineering examples |
| D08 Testing & verification | What evidence proves correctness and catches regressions? | Software Testing; Quality; Construction; Models & Methods | SEED | Need unit/integration/property/mutation/contract/e2e evidence cards and test-quality metrics |
| D09 Security & secure coding | Which threats apply and which controls are testable? | Software Security; Quality; Professional Practice | SEED | ASVS/SSDF mapped requirements, language-specific secure-coding cards, threat-model handoff |
| D10 DevSecOps & supply chain | How is code built, reviewed, versioned, scanned, packaged and released safely? | Software Engineering Operations; Configuration Management; Process; Security | SEED | SLSA/OpenSSF mapping, CI policy, dependency acceptance and provenance scenarios |
| D11 Reliability, observability & operations | How does the system fail, degrade, recover and reveal its state? | Software Engineering Operations; Maintenance; Quality; Architecture | GAP | Need SLO/error-budget concepts, OpenTelemetry, failure-mode and recovery evidence |
| D12 Performance, profiling & capacity | What are the actual latency/throughput/resource limits and how were they measured? | Construction; Quality; Computing/Engineering Foundations; Economics | GAP | Need benchmark methodology, profiling, load-model and capacity-planning cards |

## 3. SWEBOK V4.0a → FATHER crosswalk

| SWEBOK knowledge area | Primary FATHER destination(s) | Notes for PROGRAMMING_KB |
|---|---|---|
| Software Requirements | D01, D04 | Translate requirements into implementation/acceptance traceability; do not let the Programmer Agent silently invent product requirements |
| Software Architecture | D07, D04, D06, D11 | Architecture decisions become D2/D3 Decision Evidence Bundles |
| Software Design | D07, D04, D05, D06 | Design principles must be stored with applicability and counter-examples, not as universal slogans |
| Software Construction | D02, D03, D04, D08, D12 | Main coding knowledge lane; language-specific source cards attach here |
| Software Testing | D08 | Test technique, oracle quality, coverage limits and defect evidence |
| Software Engineering Operations | D10, D11, D12 | Build/release/runtime/observability/operations knowledge; exact operational scope must remain source-versioned |
| Software Maintenance | D07, D08, D11 | Changeability, regression, migration, repair, support lifecycle and deprecation |
| Software Configuration Management | D10 | Git/versioning/change control/build provenance/dependency state |
| Software Engineering Management | Cross-cutting | Task planning, estimation and control belong to FATHER governance; programmer uses only the portions required for engineering delivery |
| Software Engineering Process | D01, D08, D10; cross-cutting | Process evidence must scale with D0-D3 impact; no ceremony for its own sake |
| Software Engineering Models & Methods | D01, D07, D08 | Modeling, analysis and formal/semi-formal methods enter when they materially reduce decision risk |
| Software Quality | D01, D08, D09, D11, D12 | Mapped with ISO/IEC 25010:2023 to turn vague quality words into measurable acceptance properties |
| Software Security | D09, D10 | Maps to SECURITY_KB/DEVSECOPS_KB later; Programmer Agent must implement and prove controls, not own enterprise risk alone |
| Software Engineering Professional Practice | Cross-cutting | Ethics, communication, collaboration and review behavior affect handoffs and human approval rules |
| Software Engineering Economics | D07, D12; cross-cutting | Include build-vs-buy, complexity/operations cost, migration/rollback and performance-cost trade-offs |
| Computing Foundations | D02, D03, D05, D06, D12 | Algorithms, systems, networking, databases and platform foundations feed concrete design choices |
| Mathematical Foundations | D02, D06, D08, D12 | Complexity, probability/statistics, logic and quantitative verification where relevant |
| Engineering Foundations | D06, D11, D12; cross-cutting | Experiment design, measurement, systems thinking, reliability and engineering trade-offs |

## 4. P0 / P1 / P2 gap severity

The project avoids vague labels such as “little knowledge” or “many sources”.

- **P0 — blocking gap:** the agent cannot safely make a common material decision because the knowledge domain lacks a canonical source lane, decision rule or verification method.
- **P1 — material weakness:** the domain exists and routine decisions are possible, but important alternatives, counter-evidence or evaluated scenarios are missing.
- **P2 — enrichment gap:** useful depth, specialist cases or additional languages/tools are missing but the professional MVP remains functional.

### Initial P0 list

1. Python language/runtime canonical source layer.
2. HTTP/API contract canonical layer.
3. PostgreSQL transaction/data layer.
4. Test-method evidence beyond ordinary example-based unit tests.
5. Benchmark/profiling methodology.
6. Concurrency/distributed failure semantics.
7. Reliability/observability/failure-mode layer.
8. Dependency/framework adoption and rejection procedure.
9. One fully worked D2 decision showing source → applicability → alternatives → experiment → result.
10. Evaluation corpus that can fail an agent for citation theater, fabricated measurements or unnecessary complexity.

**P0 unresolved count at initiation: 10.**  
MIN gate requires: **0 unresolved P0 gaps.**

## 5. Minimum professional coverage metrics

A domain counts as `MIN-COVERED` only when all are true:

```text
canonical/authoritative source lane exists
AND >= 10 VALIDATED or LIMITED Knowledge Objects (unless a written exception is approved)
AND >= 1 evaluated decision/task scenario
AND applicability/version fields are populated where relevant
AND verification method is explicit
AND known counter-evidence/limitations are recorded where material
```

The whole PROGRAMMING_KB reaches MIN only when:

```text
12/12 domains MIN-COVERED
P0 gaps = 0
validated/limited cards >= 120
reviewable decision scenarios >= 20
end-to-end code + test + evidence scenarios >= 10
D2/D3 traceability = 100%
fabricated/untraceable acceptance claims = 0
```

Raw source or card count cannot override a failed domain or evaluation gate.

## 6. First acquisition order

The breadth-first order for the MVP is:

```text
D01 requirements/specification
  ↓
D03 Python language/runtime
  ↓
D08 testing/verification
  ↓
D04 HTTP/API contracts
  ↓
D05 PostgreSQL/transactions
  ↓
D09 security/secure coding
  ↓
D10 DevSecOps/supply chain
  ↓
D07 architecture/decomposition
  ↓
D12 performance/profiling
  ↓
D11 reliability/observability
  ↓
D06 concurrency/distributed systems
  ↓
D02 algorithms/data structures deepening
```

This order is not a claim that later domains are less important. It is an MVP sequencing decision: first make bounded Python/backend delivery traceable, then strengthen the failure/performance/distributed-system frontier.

## 7. Next controlled output

Create source cards for the first canonical Python/backend set, then create the first worked D2 case. Candidate case:

> For a bounded backend service requirement, decide whether a new operation should remain a synchronous function/module call, become async inside the process, or become an independent service. The result must be decided from constraints and measurements, not architecture fashion.
