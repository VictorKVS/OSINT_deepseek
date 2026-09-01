# FATHER Team Knowledge Materials Matrix

Status: ACTIVE / post-Architect pilot

The successful Architect Telegram acquisition is the proven reference for the next team roles. The reference run observed 31 numbered lessons, 24 lessons without a primary source artifact, 45 queries, 204 search hits, 9 media candidates, 7 new downloads, 2 payload reuses, 0 errors, and 23,836,395 downloaded bytes in 128.4248056 seconds. `speedup_vs_1_stream_pct` remains unknown because no same-queue 1-stream baseline has been measured.

## Five-stream role allocation

| Stream | Cluster | Roles | First goal |
|---|---|---|---|
| 1 | Engineering Core | Programmer, QA Tester, DevOps/SRE | Build implementation, testing and operations evidence layers |
| 2 | Analysis & Product | System Analyst, Business Analyst, Product/UX | Build requirements, process, product and usability evidence layers |
| 3 | Security & Legal | Security Engineer, Legal/Compliance | Reuse active Security KB pipeline and add legal/compliance competence layer |
| 4 | Data & AI | Data Engineer, ML/LLM Engineer | Build data, RAG, model, evaluation and LLMOps evidence layers |
| 5 | Economics & Research | FinOps/Economist, OSINT/Research Analyst | Build cost/business-case and research-method/evidence layers |

Architect remains the `PROVEN_REFERENCE` role rather than consuming one of the five active expansion streams.

## Role material lists

### Programmer / PROGRAMMING_KB — P0

Collect and structure material for Python/runtime semantics, software design, refactoring, algorithms and data structures, HTTP/REST, OpenAPI, FastAPI/backend, PostgreSQL transactions, pytest/testing, concurrency/async, packaging/dependencies, secure coding, OpenTelemetry, profiling, code review, patterns and anti-patterns.

Preferred evidence order: official Python/standards/project documentation → primary framework/database documentation → author/publisher material → reputable reference implementations → Telegram/community material as candidate evidence only.

### QA Tester / TESTING_KB — P0

Collect test strategy, test levels, risk-based testing, test-design techniques, property-based and contract testing, API/UI testing, performance/security testing, test data, defect taxonomy, regression strategy, quality gates, CI orchestration and observability-for-testing materials.

Required outputs include checklists, test catalogs, reference suites and traceable acceptance criteria rather than only theory.

### DevOps/SRE / DEVSECOPS_KB — P0

Collect Linux operations, Docker, Kubernetes, Terraform, GitOps, ArgoCD, CI/CD, SRE, SLI/SLO/SLA, incidents, observability, OpenTelemetry, Prometheus/Grafana, capacity planning, autoscaling, backups/DR, secrets and supply-chain-security materials.

Operational runbooks and postmortem examples are first-class knowledge objects.

### System Analyst / SYSTEM_ANALYSIS_KB — P0

Collect requirements engineering, functional/non-functional requirements, use cases, user stories, BPMN, UML, C4, DFD, integration analysis, API contracts, event-driven systems, domain modeling, traceability, acceptance criteria, impact analysis, quality attributes and system boundaries.

Every mature topic should ultimately support a reusable template/checklist plus source-backed examples.

### Business Analyst / BUSINESS_ANALYSIS_KB — P1

Collect business goals, stakeholder analysis, process modeling, value streams, business rules, KPIs, cost-benefit analysis, risk registers, prioritization, workshops/interviews, process improvement, operating models and business cases.

### Product/UX / PRODUCT_KB — P1

Collect product discovery, problem framing, JTBD, user research, information architecture, interaction design, usability testing, accessibility, design systems, product analytics, A/B testing, roadmaps, prioritization, product-market-fit signals, UX writing and service design.

### Security Engineer / SECURITY_KB — P0

Continue the separate active Security/Regulatory pipeline. Competence material should cover threat modeling, secure architecture, AppSec, DevSecOps, OWASP, cloud security, IAM, network security, SIEM/logging, incident response, vulnerability management, cryptography, KII, PDN, regulated/GIS security and LLM security.

Legal/currentness material keeps its stricter A0/A1 evidence boundary; Telegram never promotes legal truth.

### Legal/Compliance / LEGAL_KB — P0

Collect legal-source hierarchy, applicability, effective dates, amendment chains, contracts, privacy/data protection, information-security law, intellectual property, software licensing, AI governance, evidence/auditability, regulatory change, policy drafting and legal traceability.

Official legal sources dominate. Commentary and community material remain reference-only unless independently supported.

### Data Engineer / DATA_KB — P1

Collect data modeling, SQL/PostgreSQL, ETL/ELT, data quality, lineage, batch/streaming, Kafka, lakehouse/warehouse, vector databases, metadata catalogs, schema evolution, data contracts, orchestration, privacy engineering, backup and retention.

### ML/LLM Engineer / AI_AGENTS_KB — P0

Collect transformers, embeddings, RAG, retrieval evaluation, prompts, tool use, agent orchestration, structured outputs, fine-tuning/adapters, quantization, serving, LLM evaluation, guardrails, LLM security, observability, model routing, context management, multimodal models and MLOps/LLMOps.

Papers, official documentation, model cards, reference implementations, evaluation datasets and benchmarks are distinct evidence classes and must not be collapsed into one confidence score.

### FinOps/Economist / FINOPS_KB — P1

Collect unit economics, TCO, CAPEX/OPEX, cloud cost models, FinOps, LLM inference cost, GPU sizing economics, budgeting/forecasting, scenario analysis, ROI/NPV, allocation/showback/chargeback, vendor comparison, procurement economics, project business cases and sensitivity analysis.

### OSINT/Research Analyst / RESEARCH_KB — P0

Collect research-question formulation, source discovery, reliability, provenance, triangulation, counter-evidence, uncertainty, timeline reconstruction, entity resolution, graph analysis, Telegram/web research, evidence sufficiency, hypotheses, structured analytic techniques, report writing and red-team/Socratic critique.

This role is also responsible for evaluating the acquisition method itself: which queries produce useful source artifacts, where false positives occur, and when marginal search value has fallen enough to stop.

## Maturity gates

**MIN** means topic inventory exists; every P0 topic cluster has an authoritative-source seed; every cluster has at least one reviewable artifact or explicit GAP; provenance/SHA-256 are preserved.

**MEDIUM** adds independent source classes for important decisions, templates/checklists/examples, conflict and counter-evidence representation, and competency questions answerable with source lineage.

**MAX** adds change monitoring, benchmark/evaluation corpus, measured reuse/regression metrics, versioned challengeable golden decisions, and the existing human-review promotion boundary.

## Next execution order

1. Programmer, System Analyst, Security/Legal and ML/LLM Engineer profiles first (P0 role cores).
2. QA Tester, DevOps/SRE and OSINT/Research Analyst next (operational quality and research reliability).
3. Business Analyst, Product/UX, Data Engineer and FinOps/Economist after the P0 cores have a working MIN layer.
4. Do not launch unrestricted Telegram scraping for every role at once. Generate bounded query sets from each role registry, measure usefulness, then expand only where gaps remain.
