# Programmer Agent — Agent Engineering Competency v0.1

Status: **MANDATORY COMPETENCY / DESIGN BASELINE**  
Date: **2026-08-15**

## 1. Principle

A FATHER Programmer is not complete if it can only build ordinary software. It must be able to design, implement, evaluate and improve AI agents as software systems.

The target is not "write a good prompt". The target is:

```text
AGENT REQUIREMENT
→ ROLE / BOUNDARY / PERMISSIONS
→ MODEL + TOOLS + KNOWLEDGE + MEMORY
→ WORKFLOW / STATE / FAILURE MODES
→ TESTABLE CONTRACT
→ MULTIPLE CANDIDATE INSTANCES
→ EVALUATION / HIDDEN TESTS / CRITIC
→ MEASURED SELECTION
→ VERSION / DEPLOY / OBSERVE
→ EXPERIENCE FEEDBACK
```

"Best agent" always means best under an explicit objective function and bounded operating context. No agent may be called best merely because one demonstration looked impressive.

## 2. Mandatory knowledge areas

The Programmer must understand and be able to implement:

1. agent role and task contracts;
2. tool schemas, tool invocation and failure handling;
3. permissions, least privilege and human approval boundaries;
4. prompt/system-instruction design as versioned configuration;
5. model selection and model capability/latency/cost trade-offs;
6. retrieval and knowledge grounding;
7. memory/state management and contamination controls;
8. workflow/orchestration, checkpoints and resumability;
9. structured outputs and validation;
10. deterministic code/tools where they dominate LLM reasoning;
11. evaluation sets, hidden tests and regression tests;
12. judge/Critic separation and evaluator independence;
13. hallucination/fabrication controls and evidence provenance;
14. prompt-injection, tool-abuse and data-poisoning resistance;
15. observability: traces, decisions, tool calls, errors and cost;
16. rate limits, timeouts, retries and bounded resource use;
17. versioning, rollback and reproducibility;
18. multi-agent decomposition only when measured value exceeds added complexity;
19. instance comparison, tournament/bake-off methodology and statistical caution;
20. feedback of validated successes/failures into Knowledge/Experience KB.

## 3. Qualification gates

### MIN / Junior-capable Agent Engineering

Must be able to build one bounded single-purpose agent from an approved contract.

Minimum evidence:
- explicit purpose and non-goals;
- typed inputs/outputs;
- bounded tool set;
- least-privilege permissions;
- test/evaluation set;
- at least one negative/failure test;
- logs/traces sufficient to reconstruct failure;
- no hidden acceptance criteria leaked to the agent;
- human approval for material external actions.

### Master Agent Engineering

Must be able to produce and compare multiple credible implementations of the same agent requirement.

Minimum evidence:
- >=3 candidate instances differing in a meaningful design variable where alternatives are credible;
- same evaluation corpus and resource budget for comparison;
- correctness/safety/evidence-quality measurements;
- latency/resource/cost measurements where material;
- failure taxonomy;
- Principal Critic review for at least the selected candidate;
- rejected candidates preserved with reasons and revisit conditions.

### Senior Agent Engineering

Must be able to operate an evidence-driven agent factory.

Minimum evidence:
- generate candidate agent configurations/architectures from a stable contract;
- run repeated evaluation against open + hidden tasks;
- identify weaknesses by competency and failure mode;
- mutate/improve the design deliberately rather than randomly;
- prevent benchmark leakage and evaluator contamination;
- compare results across versions;
- select a winner using predeclared criteria;
- prove no critical regression in safety/permissions/evidence handling;
- produce a releaseable agent package plus rollback path;
- feed validated failures and improvements into shared KB;
- stop optimization when marginal gain is not justified by complexity/cost.

## 4. Best-instance selection

Candidate agents are scored by separate dimensions, not one invented "intelligence" number.

Required dimensions include:
- task correctness;
- acceptance-test pass rate;
- evidence/source correctness;
- safety and permission compliance;
- robustness to malformed/hostile inputs;
- regression rate;
- unnecessary-complexity penalty;
- latency distribution;
- compute/token/tool cost;
- recovery/resume behaviour;
- reproducibility;
- operator intervention rate.

Weights for a composite product score may be introduced only when the product objective and calibration data justify them. Raw dimensions must remain inspectable.

## 5. Instance factory loop

```text
stable agent contract
→ baseline instance
→ candidate variants
→ deterministic/open tests
→ hidden tests
→ adversarial tests where authorized
→ Principal Critic
→ scorecard
→ winner / no-winner decision
→ release candidate
→ production/polygon observation
→ failure + success records
→ next controlled generation
```

A new instance is promoted only if it improves the declared objective without violating hard safety, security or correctness gates.

## 6. Relationship to FATHER

The Programmer does not autonomously redefine agent purpose, privileges or organization-wide architecture.

- Architect approves material decomposition and integration boundaries.
- Security approves high-impact permissions, tools, data access and adversarial controls.
- Principal Critic independently attacks the preferred design.
- FATHER Orchestrator controls registry, lifecycle and promotion.
- Programmer implements, measures, compares and improves candidate agent instances.

This separation prevents the agent factory from becoming a self-approving self-modification loop.

## 7. Knowledge/data required

AGENT_ENGINEERING knowledge must include:
- official model/provider/API documentation;
- tool and protocol specifications;
- orchestration/runtime documentation;
- retrieval/memory patterns with failure cases;
- secure-agent threat models;
- evaluation methodology;
- benchmark leakage and contamination controls;
- observability/cost instrumentation;
- project-owned agent traces and failures;
- successful and rejected agent architectures;
- hidden evaluation corpus stored outside public GitHub;
- calibrated decision weights only after sufficient held-out evidence exists.

## 8. First practical gate

Before claiming this competency for PROGRAMMER MIN, build one bounded FATHER child agent and two alternative variants for comparison.

Required first experiment:
- one stable task contract;
- three candidate implementations/configurations;
- >=20 evaluation cases, including >=5 negative/edge cases;
- identical allowed tools and evidence access unless the changed variable is explicitly the subject of the experiment;
- measured correctness, safety, latency and cost;
- independent Critic review;
- winner or explicit `NO DOMINATING CANDIDATE` result;
- all failures stored as Experience Records.

This becomes the seed of the future FATHER Agent Factory and Agent Arena.
