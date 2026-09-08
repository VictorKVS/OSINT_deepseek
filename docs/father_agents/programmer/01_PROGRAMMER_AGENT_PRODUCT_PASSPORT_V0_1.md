# Programmer Agent Product Passport v0.1

Status: **DRAFT FOR RESEARCH / NO IMPLEMENTATION AUTHORIZATION**  
Date: **2026-08-14**

## 1. Product goal

Create a professional software-engineering agent that can implement approved tasks and make material technical choices only through an auditable chain of evidence, alternatives, risk analysis and verification.

## 2. Inputs

Minimum input contract:

```text
EngineeringTask
- requirement_id
- business_goal
- functional_requirements
- nonfunctional_requirements
- constraints
- acceptance_criteria
- security_class / risk context if known
- target environment if fixed
- forbidden/required technologies if any
```

If important fields are unknown, the agent does not silently assume them. It records `OPEN_ASSUMPTION` and either requests resolution through the governing workflow or chooses a reversible safe default with explicit uncertainty.

## 3. Required outputs

```text
ImplementationPackage
- implementation_plan
- decision_records[]
- source_evidence_refs[]
- rejected_alternatives[]
- risk_register_delta[]
- code_changes[]
- tests[]
- verification_results[]
- security_results[]
- operational_notes[]
- residual_risks[]
- done_gate_status
```

## 4. Decision classes

Every choice is classified before the amount of evidence is chosen.

### D0 — trivial/reversible
Naming, formatting, obvious local refactor with unchanged behaviour. Source citation normally not required; tests/diff may be sufficient.

### D1 — local engineering choice
Library call, data structure, error-handling pattern, module boundary. Requires at least one relevant authoritative or consensus source when the choice is non-obvious, plus local tests.

### D2 — architectural/material
Language/runtime, database, framework, service boundary, protocol, concurrency model, persistence semantics, security mechanism. Requires alternatives, source evidence, context-fit analysis, explicit risks and acceptance evidence. Benchmark/PoC is required when the choice depends on performance, scalability, compatibility or operational behaviour.

### D3 — critical/high-impact
Security boundary, irreversible migration, high-availability design, sensitive-data processing, critical dependency/supply-chain decision. Requires independent critic review, counter-evidence search, stronger source diversity, failure-mode analysis and human/Principal approval where FATHER policy requires it.

## 5. Decision contract

For D1-D3 decisions the record SHALL answer:

1. What problem is being solved?
2. What constraints matter?
3. What alternatives were considered?
4. Which claims support each alternative?
5. Which sources support those claims?
6. Are the sources current and applicable to the actual version/environment?
7. What risks and trade-offs remain?
8. What observation would falsify the preferred option?
9. What experiment/test can discriminate between close alternatives?
10. Why is the selected option sufficient, not merely fashionable or possible?
11. Under what conditions must the decision be revisited?

## 6. Technology-selection rule

Technology is selected by context, not by popularity.

Candidate comparison may include:
- correctness guarantees;
- safety model;
- performance/latency/throughput;
- memory/resource footprint;
- concurrency model;
- ecosystem maturity;
- dependency/supply-chain exposure;
- observability;
- tooling and static analysis;
- portability;
- operations complexity;
- team competence and maintainability;
- licensing/support lifecycle;
- migration/rollback cost.

A literature/specification claim such as "technology X is suitable for high performance" is only a hypothesis for a context-specific choice. If performance materially drives the decision, the agent must produce reproducible local benchmark evidence.

## 7. Complexity rule

The default decomposition ladder is:

```text
function → module → package → process → service → microservice → distributed subsystem
```

The agent moves right only when requirements/evidence justify the added failure modes and operational cost.

## 8. Integration boundaries

```text
Architect / Analyst
      ↓ approved task
Programmer Researcher
      ↓ evidence bundle
Solution Planner
      ↓ candidates
Risk + Evidence Evaluator
      ↓
Engineering Critic
      ↓
Programmer Implementer
      ↓
Test / Security / Reliability Verifiers
      ↓
Principal Critic / acceptance gate when required
      ↓
ImplementationPackage
```

These may initially be logical roles inside one orchestrated agent. Separate services/agents are not authorized until workload, isolation or reliability evidence requires separation.

## 9. DONE gate

Generated code alone is never DONE.

Baseline material gate:

```text
requirements traceable            PASS
material decisions evidenced      PASS
alternatives recorded             PASS
unit/integration tests             PASS
static checks                      PASS
security checks appropriate        PASS
acceptance criteria                PASS
residual risks explicit            PASS
reproducible evidence preserved    PASS
```

## 10. MVP target

The first MVP is not "an agent that can code anything". It is an agent that can reliably solve a bounded set of Python/backend engineering tasks while producing auditable decisions and passing the same evidence gates every time. Language breadth is expanded only after the decision machinery is stable.
