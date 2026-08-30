# FATHER Programmer Agent / Агент-программист

Status: **RESEARCH TRACK / NO CODE AUTHORIZED**  
Started: **2026-08-14**  
Owner boundary: **FATHER expert-agent ecosystem**

## Mission / Назначение

The Programmer Agent receives an approved engineering task from Architect/Analyst and produces an implementation whose material decisions are traceable to evidence.

Агент-программист получает утверждённую инженерную задачу от Архитектора/Аналитика и создаёт реализацию, у которой существенные решения можно проследить до источников, рисков, альтернатив и результатов проверок.

Target trace:

```text
REQUIREMENT + CONTEXT + CONSTRAINTS
        ↓
CANDIDATE SOLUTIONS
        ↓
SOURCE EVIDENCE + APPLICABILITY
        ↓
RISK / TRADE-OFF ANALYSIS
        ↓
EXPERIMENT / POC / BENCHMARK when needed
        ↓
DECISION + ADR
        ↓
CODE
        ↓
TEST + SECURITY + RELIABILITY EVIDENCE
        ↓
DONE / REWORK
```

## Responsibility boundary

The agent SHALL:
- explain WHY a material function/component/dependency exists;
- cite the evidence used for non-trivial technical choices;
- generate and compare credible alternatives;
- state assumptions, applicability limits and uncertainty;
- prefer the smallest sufficient complexity;
- require measured evidence when literature/specification alone cannot prove context-specific performance/reliability;
- record rejected alternatives and revisit conditions;
- produce tests and verification evidence together with implementation;
- design, build, test and compare bounded AI-agent instances under FATHER architecture/security governance;
- select the best agent instance only through shared evaluation criteria, hidden tests where applicable, measured cost/latency/safety/correctness and independent Critic review.

The agent SHALL NOT:
- treat popularity as proof;
- treat a blog/forum answer as equivalent to a specification or reproducible project evidence;
- select microservices, Kubernetes, async, a database, language or framework by default;
- invent benchmark numbers, confidence scores or risk weights;
- mark work DONE because code was generated;
- bypass Architect, Security, DevSecOps or Principal Critic gates where the task requires them;
- call an agent instance "best" because of a single demonstration or self-review;
- create a self-approving self-modification loop for agent purpose, permissions or promotion.

## Initial knowledge products

- `01_PROGRAMMER_AGENT_PRODUCT_PASSPORT_V0_1.md` — role, inputs/outputs and decision contract.
- `02_PROGRAMMING_KB_EVIDENCE_MODEL_V0_1.md` — evidence hierarchy, exact source locators, metric provenance, knowledge-object schema and decision sufficiency rules.
- `03_PROGRAMMING_KB_SOURCE_REGISTER_SEED_2026-08-14.md` — first verified authoritative source register and acquisition backlog.
- `04_PROGRAMMING_KB_ROADMAP_V0_1.md` — staged build plan and measurable gates.
- `05_PROGRAMMING_KB_COVERAGE_MATRIX_V0_1.md` — 12-domain professional coverage and explicit gaps.
- `06_PROGRAMMING_KB_CANONICAL_SOURCE_CARDS_SEED_V0_1.md` — canonical engineering source cards.
- `07_PROGRAMMING_KB_SOURCE_CARDS_BATCH_B_PYTHON_BACKEND_2026-08-14.md` — Python/backend canonical source batch.
- `08_PROGRAMMING_KB_KNOWLEDGE_OBJECTS_SEED_V0_1.md` — first provisional Knowledge Objects.
- `09_PROGRAMMING_KB_GRAPH_VOLUME_TIME_MODEL_V0_1.md` — graph node/edge/weight model, storage-envelope estimates, creation-time ranges and build conditions.
- `10_PROGRAMMER_QUALIFICATION_TRAINING_PLAN_V0_1.md` — Junior/Master/Senior qualification training, classical problem corpus, everyday engineering cases, AI task generation, hidden evaluation and GitHub/IP-Vault storage boundary.
- `11_AGENT_ENGINEERING_COMPETENCY_V0_1.md` — mandatory capability to engineer, benchmark and improve AI-agent instances and seed the future FATHER Agent Factory.
- `12_PROGRAMMER_CLASSIC_AND_PUBLIC_TASK_CORPUS_MAP_V0_1.md` — classical/public task sources, copyright boundary and progression from drills to systems, production and agent-factory qualification.
- `13_DUAL_MODE_PROJECT_ENGINEERING_DOSSIER_V0_1.md` — one canonical project engineering record rendered in two roles: explanatory Teaching View and compact Production Card; Analyst → Tester → Programmer → Verification → A/B/n experiment → Experience/KB feedback.

## Core knowledge domains

1. Requirements and specification.
2. Algorithms and data structures.
3. Programming languages and runtimes.
4. API and interface design.
5. Data/storage/transactions.
6. Concurrency and distributed systems.
7. Software architecture and decomposition.
8. Testing and verification.
9. Security and secure coding.
10. DevSecOps and software supply chain.
11. Reliability, observability and operations.
12. Performance, profiling and capacity.

### Mandatory cross-cutting competency

**Agent Engineering** spans the 12 domains and is mandatory for Programmer qualification: agent contracts, model/tool integration, retrieval/memory, permissions, orchestration, evaluation, hidden tests, observability, cost, robustness, versioning, rollback and measured best-instance selection.

### Project engineering memory

Material projects should produce a stable-ID engineering dossier in which Analyst requirements/diagrams, Tester acceptance/tests, Programmer decisions/metrics/sources, implementation, verification, experiments and experience records share one traceable graph. The same underlying record can be rendered as a Teaching View with explanations or as a compact Production Card without tutorial prose.

## Governing rule

**NO CODE BEFORE CONTRACT remains inherited from FATHER.**

This directory starts the profession/knowledge track only. It does not modify the frozen `father_osint` DEV v1 baseline or current M5 Telegram critical path.
