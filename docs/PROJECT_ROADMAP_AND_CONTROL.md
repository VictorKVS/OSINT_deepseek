# FATHER / OSINT_deepseek — Capability Roadmap & Project Control

**Status:** living project-management baseline  
**Current priority:** **P0 Knowledge Factory Conveyor**  
**Planning model:** capability/evidence driven; no invented completion percentages or dates  
**Purpose:** build one evidence-to-execution platform that turns trusted sources into governed knowledge, requirements, implementation choices, workforce decisions and auditable outcomes.

---

## 1. North-star product

The project is no longer defined as a Telegram/OSINT collector. OSINT is one acquisition capability inside a larger system.

The completed product idea is:

```text
SOURCE / LAW / ORDER / STANDARD / BOOK / TECHNICAL EVIDENCE
        ↓
KNOWLEDGE FACTORY
        ↓
WHAT IS TRUE / REQUIRED / APPLICABLE?
        ↓
REGULATION ENGINEERING
        ↓
WHAT MUST BE DONE AND HOW CAN IT BE VERIFIED?
        ↓
COMPLIANCE / IMPLEMENTATION DESIGN
        ↓
WHAT VALID IMPLEMENTATION OPTIONS EXIST?
        ↓
ROLE & RESPONSIBILITY ENGINEERING
        ↓
WHO MUST DO IT?
        ↓
WORKFORCE & COMPETENCY ENGINEERING
        ↓
WHAT SKILLS / LEVEL / CAPACITY ARE REQUIRED?
        ↓
SOURCING DECISION
        ↓
KEEP INTERNAL / TRAIN / HIRE / OUTSOURCE / HYBRID / AUTOMATE
        ↓
COST / TIME / QUALITY / RELIABILITY / RISK COMPARISON
        ↓
DECISION + IMPLEMENTATION PLAN
        ↓
EVIDENCE OF EXECUTION / AUDIT
        ↓
OBSERVED OUTCOME / EXPERIENCE
        ↓
GOLDEN SOLUTION / REUSABLE PATTERN
        ↓
REGULATORY DIGITAL TWIN
```

The system must answer not only **“what does the document say?”**, but eventually:

1. What applies to this organization/system/process?
2. What exactly must be done?
3. What are valid implementation alternatives?
4. Which alternative is cheaper/faster/more reliable/lower-risk under current constraints?
5. Which roles are responsible?
6. Do current people have the required competence and capacity?
7. Is it better to train, hire, outsource, use a hybrid model or automate part of the work?
8. What evidence proves implementation?
9. What happened in practice and which solution should be reused next time?

---

## 2. Permanent engineering principles

- **NO CODE BEFORE CONTRACT.**
- Evidence/provenance survives every transformation.
- Exact-original status requires actual bytes and computed SHA-256.
- Knowledge objects are typed; FACT, REQUIREMENT, CLAIM, HYPOTHESIS, OPINION and RECOMMENDATION are not interchangeable.
- Reuse before rediscovery/re-extraction/reimplementation.
- Differences become conflict candidates before being declared contradictions.
- Applicability is explicit and contextual.
- No single opaque “truth”, “quality”, “employee reliability” or “best solution” percentage.
- Cost, time, quality, reliability, operational burden and risk remain separate measurable dimensions.
- Every recommendation exposes alternatives, assumptions, evidence and reasons.
- Role separation is preserved: User / Analyst / OSINT Expert / Knowledge Curator / Reviewer / Administrator / Security Administrator / System Owner.
- Human/critic gates remain where legal, security, publication or high-impact decisions require them.

---

## 3. Integrated capability roadmap

| ID | Capability outcome | Class | Depends on | Done when / evidence gate | State |
|---|---|---|---|---|---|
| B0 | Frozen DEV v1 semantic baseline | MUST | — | canonical runners and frozen behavior remain regression-green | **DONE / FROZEN** |
| KF0 | Source trust + exact acquisition D0-D3 | MUST | B0 | trusted source → exact bytes → MIME/size/SHA-256 → version → audit; BASIC/PRO/STRESS green | **ACTIVE P0** |
| KF1 | Document Compiler D4-D5 | MUST | KF0 | structure and chunks have stable IDs and exact source locators | PLANNED |
| KF2 | Knowledge Engineering D6-D12 | MUST | KF1 | concepts/definitions/requirements/entities/relations/conflicts extracted with provenance, competency questions, reuse and constraints | PLANNED |
| KF3 | Governed KB D13-D15 | MUST | KF2 | graph/table/document reconcile; expert review; no direct autonomous promotion; KB-ready package | PLANNED |
| KF4 | Change monitoring + bounded invalidation/reuse | MUST | KF3 | changed source/method invalidates only affected dependency subgraph; unchanged knowledge reused | PLANNED |
| UX1 | Role-based Web Shell | MUST | KF0 contracts | login/role routing, role dashboards, alerts, global search, My KB, Admin, Security and Owner workspaces | PLANNED / CONTRACT NEXT |
| UX2 | Knowledge Workspace | MUST | KF1/KF2 | synchronized Graph / Table / Document / Clause / Evidence / Timeline views | PLANNED |
| UX3 | “Find → verify → insert into my KB” workflow | MUST | KF2/KF3 | user can search global knowledge and REUSE / REFERENCE / CONTEXT MAP / DERIVE without duplicate truth models | PLANNED |
| RE1 | Requirement & Applicability Engineering | MUST | KF3 | source clauses become typed requirements with actor/action/object/condition/deadline/evidence/applicability | FUTURE CORE |
| RE2 | Requirement-to-Control mapping | MUST | RE1 | each requirement maps to verifiable control objectives and evidence expectations | FUTURE CORE |
| CD1 | Compliance / Implementation Pattern Library | MUST | RE2 | reusable implementation patterns linked to requirements/controls, prerequisites and evidence | FUTURE CORE |
| CD2 | Valid implementation alternatives | MUST | CD1 | system distinguishes prescriptive requirements from outcome-based requirements and enumerates only legally/technically permissible options | FUTURE CORE |
| DI1 | Cost / Time / Risk / Reliability comparison | MUST | CD2 | alternatives compared using explicit measured/estimated dimensions and assumptions; no opaque winner score | FUTURE CORE |
| RM1 | Role & Responsibility Matrix | MUST | RE2/CD1 | each control/process maps to accountable/responsible/review/security/admin roles with segregation-of-duties checks | FUTURE CORE |
| WC1 | Competency Model per Role | MUST | RM1 | each role has skills, levels, evidence, experience/capacity requirements and criticality | FUTURE CORE |
| WC2 | Person/Team Capability Matrix | SHOULD | WC1 | current staff capability/capacity mapped to required role profiles with explicit gaps and evidence | FUTURE CORE |
| WC3 | Workforce sourcing alternatives | MUST | WC1/WC2 | Internal / Train / Hire / Outsource / Hybrid / Automate options generated with constraints | FUTURE CORE |
| WC4 | Workforce cost/time/quality/reliability model | MUST | WC3 | TCO, time-to-competency, coverage, backup/bus-factor, SLA/vendor dependence, rework and observed quality compared separately | FUTURE CORE |
| DI2 | Decision Intelligence | MUST | DI1/WC4 | recommendation records selected/rejected options, assumptions, evidence, constraints, reviewer and revisit trigger | FUTURE CORE |
| EX1 | Implementation & Evidence Tracker | MUST | DI2 | selected solution moves through plan → execution → verification → evidence package → audit state | FUTURE CORE |
| EX2 | Outcome / feedback capture | SHOULD | EX1 | actual cost/time/incidents/rework/quality recorded against the decision hypothesis | FUTURE CORE |
| GS1 | Golden Solutions Library | MUST | EX2 | repeated verified patterns can become GOLDEN / LIMITED / REJECTED METHOD/SOLUTION through Champion/Challenger evidence | FUTURE CORE |
| RDT1 | Regulatory Digital Twin | OPTION→TARGET | KF3 + RE1 + DI2 + EX2 | simulate requirements/applicability/options/cost/workforce/implementation consequences and compare scenarios before changes | STRATEGIC TARGET |

---

## 4. Current critical path

All unrelated product expansion remains HOLD while the conveyor is being proven.

```text
B0 frozen baseline
   ↓
KF0 D0-D3 exact acquisition
   ↓
BASIC → PROFESSIONAL → STRESS
   ↓
KF1 structure/chunks
   ↓
KF2 knowledge objects/relations/conflicts
   ↓
KF3 reviewed KB-ready
   ↓
KF4 monitoring/reuse
```

The web skeleton may proceed in parallel only against stable contracts and must not create a second truth model.

Historical Telegram work remains useful as an acquisition adapter and regression asset, but it is **not** the current product critical path.

---

## 5. Role-based product architecture

The web product is intentionally role-oriented rather than one universal dashboard.

| Role | Primary workspace | Main metrics | Main alerts |
|---|---|---|---|
| User / Viewer | Search + My Knowledge Bases | searches, reused objects, watched KB freshness | changed knowledge, stale source, conflict affecting my KB |
| Analyst | Research / applicability / conflict workspace | CQs answered, gaps, conflicts, review queue, rework | unresolved applicability, conflict candidate, evidence gap |
| OSINT Expert | Sources / acquisition | sources verified, acquisition attempts/success/failures, version changes | source unavailable, hash/version change, policy violation |
| Knowledge Curator | Concepts / mappings / graph quality | duplicates, mappings, orphan rate, provenance/locator coverage | duplicate candidate, unsafe merge, shape violation |
| Reviewer / Critic | D14 review queue | PASS/REWORK/INCONCLUSIVE, review time, recurring defects | promotion request, unsupported claim, dependency/circularity |
| Administrator | Users/workspaces/jobs/storage/integrations | users, queues, job health, storage, API/worker state | runtime failure, queue backlog, capacity issue |
| Security Administrator | Security/audit/privileged actions | privileged events, policy violations, integrity mismatches, access reviews | privilege escalation, secret exposure, audit mismatch, publication attempt |
| System Owner | Factory/portfolio/decision dashboard | throughput, reuse, rework, cost, bottlenecks, unresolved critical gaps/risks | critical risk, degradation, cost/rework growth, role coverage gap |

Admin and Security Admin remain separate roles; one does not automatically inherit the other.

---

## 6. Regulation Engineering layer

### Goal

Convert governed knowledge into executable compliance engineering objects.

```text
SOURCE CLAUSE
   ↓
REQUIREMENT
   ↓
APPLICABILITY
   ↓
CONTROL OBJECTIVE
   ↓
VERIFICATION / EVIDENCE EXPECTATION
```

A requirement record should eventually include:

- source and exact locator;
- current/version status;
- actor;
- action/obligation/prohibition/permission;
- object/subject;
- conditions/exceptions;
- applicability guard;
- deadline/frequency where present;
- expected evidence;
- related controls;
- conflicts/context splits;
- review state.

Prescriptive requirements restrict implementation choices. Outcome-based requirements permit alternative implementation patterns subject to evidence.

---

## 7. Compliance Design / implementation alternatives

For each applicable control objective:

```text
REQUIREMENT
   ↓
CONTROL
   ↓
PATTERN CANDIDATES
   ├─ A
   ├─ B
   ├─ C
   └─ D
   ↓
LEGAL / TECHNICAL ELIGIBILITY FILTER
   ↓
COST / TIME / RELIABILITY / RISK / OPERATIONS / AUDITABILITY
   ↓
DECISION
```

Example solution dimensions:

- CAPEX;
- licenses/subscriptions;
- implementation/integration cost;
- operation/support cost;
- training cost;
- time-to-compliance;
- availability / RTO / RPO where applicable;
- failure modes / SPOF;
- human-error exposure;
- vendor dependency / exit cost;
- auditability / evidence quality;
- residual risk;
- maintenance/upgrade burden.

The platform may offer optimization preferences such as lowest cost, fastest, highest reliability, lowest operational burden or balanced, but must expose the trade-offs and must not hide mandatory requirements behind an optimization score.

---

## 8. Role & Workforce / Competency Engineering

This is a planned core layer, not a side HR feature.

### 8.1 Requirement-to-role chain

```text
Requirement
   ↓
Control
   ↓
Process / Activity
   ↓
Role
   ↓
Competency
   ↓
Required level / capacity
```

### 8.2 Role profile

Each role will contain:

- responsibilities;
- required decisions/actions;
- required technical/domain/legal skills;
- required skill level;
- experience/certification evidence where meaningful;
- required availability/capacity/FTE;
- critical functions;
- prohibited role combinations / segregation of duties;
- backup/continuity requirements.

### 8.3 Person/team profile

Where lawful and appropriate, compare current capability to role demand using explicit evidence rather than subjective labels.

Possible dimensions:

- skill coverage by required level;
- verified experience;
- task/review history;
- rework/error rate in comparable work;
- certifications/training;
- availability/capacity;
- backup person availability;
- single-person dependency / bus factor.

No opaque “employee reliability 87%” score.

### 8.4 Sourcing alternatives

For every material competency/capacity gap, compare:

1. keep current staff;
2. train/upskill;
3. hire;
4. outsource;
5. hybrid internal + external;
6. automate part of the function where legally/operationally appropriate.

### 8.5 Workforce economics

Internal TCO may include:

```text
salary + taxes + recruiting/onboarding + training + certification
+ tooling + management + backup coverage + replacement/downtime risk
```

Outsource TCO may include:

```text
contract + SLA + integration + vendor control + audit
+ dependency + transition/exit cost + retained internal oversight
```

Training decisions additionally require `time_to_competency`; an otherwise cheap training path is not sufficient when the role must be covered before the person can realistically reach the required level.

---

## 9. Decision Intelligence and experience loop

Every significant implementation/workforce choice becomes a reusable Decision Record:

```text
DECISION
- requirement/control
- organization/system context
- alternatives considered
- selected option
- rejected options
- constraints
- estimated cost/time/risk/quality/reliability
- evidence/method versions
- approver/reviewer
- revisit trigger
```

After implementation, estimates are compared with observed results:

```text
estimated vs actual cost
estimated vs actual time
incidents/failures
review/rework burden
SLA/availability
control verification results
human effort
maintenance burden
```

This closes the learning loop:

```text
DECISION
   ↓
IMPLEMENTATION
   ↓
OBSERVED OUTCOME
   ↓
METHOD/SOLUTION EVALUATION
   ↓
GOLDEN / LIMITED / REJECTED
   ↓
REUSE IN NEXT PROJECT
```

The system therefore accumulates organizational experience rather than repeatedly starting projects from zero.

---

## 10. Regulatory Digital Twin strategic target

Once requirements, implementation patterns, workforce profiles, cost/risk models and outcome history exist in a common graph, the platform can model alternative scenarios before changing the real organization.

Examples:

- a new regulation enters into force;
- a requirement changes applicability;
- a certified product is replaced;
- an internal specialist leaves;
- outsourcing cost increases;
- a deadline is shortened;
- a control is automated;
- a new system enters scope.

The Digital Twin should answer:

```text
What changes?
Which requirements/controls/roles are affected?
What becomes non-compliant?
What implementation alternatives exist?
What skills/capacity are missing?
What will each scenario cost?
How long will it take?
What new risks/dependencies appear?
What evidence will be required?
```

This remains a strategic target and must be built only after the underlying Knowledge/Requirement/Decision data is trustworthy.

---

## 11. Quality and production metrics

Metrics are multidimensional and retain provenance.

### Knowledge Factory

- source verification coverage;
- exact-original acquisition success/failure;
- bytes and artifact reuse;
- provenance/locator coverage;
- precision/recall/F1 on reviewed gold sets;
- competency-question coverage;
- constraint conformance;
- conflict/gap classifications;
- reuse/rework ratio;
- time to D15;
- human review minutes;
- cost where measurable.

### Regulation / Compliance Design

- requirements with explicit applicability;
- requirements mapped to controls;
- controls with verification evidence model;
- valid implementation patterns per control;
- unhandled requirement gaps;
- decision rework after review;
- estimate-vs-actual variance after implementation.

### Workforce Engineering

- role coverage;
- critical-function coverage;
- competency gaps by level;
- required vs available FTE/capacity;
- single-person dependency;
- backup coverage;
- time-to-competency;
- internal vs outsource TCO components;
- observed quality/rework/SLA outcomes by sourcing model.

Speedup, completion forecasts or comparative quality claims are published only when sufficient measured telemetry exists.

---

## 12. Current progress dashboard

| Workstream | Current state | Next evidence gate |
|---|---|---|
| Frozen DEV v1 | **DONE / FROZEN** | remain regression-green |
| Knowledge Factory D0-D3 | **ACTIVE P0** | mixed-profile BASIC/PRO/STRESS acceptance |
| Knowledge Engineering methodology/metrics | **CONTRACT + EXECUTABLE BASE** | complete KnowledgeScope/CQ/constraints/gold corpus |
| Document Compiler D4-D5 | QUEUED | structure/chunk contract after D0-D3 |
| Semantic D6-D12 | QUEUED | typed extraction/reuse/conflict fixtures |
| Governed D13-D15 | QUEUED | review/promotion/projection reconciliation |
| Role-based website | PLANNED | web shell + route/RBAC/navigation contract |
| Regulation Engineering | ROADMAP | requirement/applicability object model |
| Compliance Design | ROADMAP | implementation-pattern model |
| Workforce & Competency Engineering | **ROADMAP / APPROVED DIRECTION** | role→competency→capacity schema and sourcing decision model |
| Decision Intelligence | ROADMAP | multi-criteria decision record + comparison model |
| Golden Solutions | ROADMAP | observed-outcome evaluation loop |
| Regulatory Digital Twin | STRATEGIC TARGET | unlocked by trustworthy lower layers |

---

## 13. Immediate controlled backlog

1. **MUST:** finish mixed-profile D0-D3 BASIC / PROFESSIONAL / STRESS acceptance.
2. **MUST:** complete machine-readable SourcePolicy verification/reconciliation path.
3. **MUST:** preserve frozen DEV v1 regression and security checks.
4. **SHOULD/PARALLEL CONTRACT:** finish KnowledgeScope/Competency Question and shape-validation fixtures without bypassing D0-D3.
5. **MUST NEXT:** Document Compiler D4-D5.
6. **MUST AFTER:** D6-D15 through one bounded corpus.
7. **MUST UI:** build role-based web skeleton against stable contracts: User / Analyst / OSINT / Curator / Reviewer / Admin / Security Admin / Owner.
8. **MUST UI SCENARIO:** global search → verify source/applicability → reuse/reference/context-map into My KB → preview/review/audit.
9. **ROADMAP DESIGN:** define Requirement/Control/Implementation Pattern schemas.
10. **ROADMAP DESIGN:** define Role/Competency/Person-Team/Capacity/Sourcing option schemas and evidence rules.

No later layer may pull implementation capacity away from the current P0 conveyor until its required upstream data exists.

---

## 14. Definition of complete product idea

The project reaches its intended strategic form when a user can move through this entire evidence chain without losing provenance:

```text
“Что требует нормативный акт?”
        ↓
“Относится ли это ко мне?”
        ↓
“Что конкретно нужно сделать?”
        ↓
“Какими допустимыми способами это можно сделать?”
        ↓
“Что дешевле / быстрее / надёжнее / проще / менее рискованно?”
        ↓
“Какие роли должны это выполнить?”
        ↓
“Какие компетенции и мощности нужны?”
        ↓
“Есть ли они у нас?”
        ↓
“Обучить / нанять / аутсорс / hybrid / автоматизировать?”
        ↓
“Какой вариант выбран и почему?”
        ↓
“Как доказать выполнение?”
        ↓
“Что получилось фактически?”
        ↓
“Стоит ли это решение сделать GOLDEN и переиспользовать?”
```

That is the completed thought: **trusted knowledge → requirement → engineering solution → people/capability → decision → execution evidence → organizational learning**.
