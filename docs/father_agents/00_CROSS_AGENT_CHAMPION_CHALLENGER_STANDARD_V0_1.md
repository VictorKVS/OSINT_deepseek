# FATHER Cross-Agent Champion / Challenger Evaluation Standard v0.1

Status: **DESIGN BASELINE / CROSS-AGENT REQUIREMENT**  
Date: **2026-08-15**

## 1. Purpose

Every FATHER professional agent must be able to compare credible alternatives rather than silently commit to its first plausible answer.

The governing pattern is:

```text
TASK / REQUIREMENT
      ↓
CURRENT CHAMPION OR BASELINE
      +
ONE OR MORE CHALLENGERS
      ↓
COMMON HARD GATES
      ↓
COMMON ROLE-SPECIFIC METRICS
      ↓
SAME TEST / EVIDENCE CONDITIONS
      ↓
INDEPENDENT EVALUATION
      ↓
WINNER / TIE / INCONCLUSIVE / NO DOMINATING CANDIDATE
      ↓
EXPERIENCE RECORD
      ↓
FUTURE CHAMPION + KB FEEDBACK
```

The goal is not to run an expensive A/B experiment for every trivial action. The goal is to make material choices falsifiable, comparable and reusable.

## 2. Decision-class policy

### D0 — trivial/local/reversible

No mandatory challenger. Use an approved pattern and normal tests.

### D1 — standard engineering choice

A challenger is optional unless:
- the current pattern has weak evidence;
- the context materially differs from prior cases;
- regression/failure history indicates uncertainty;
- periodic sampling is required to detect stagnation.

### D2 — material choice

Required:
- >=2 credible candidates when alternatives exist;
- common acceptance gates;
- explicit metrics selected before final selection where practical;
- per-candidate evidence;
- rejected alternative retained with reason;
- result may be `NO DOMINATING CANDIDATE`.

### D3 — architecture/security/high-cost/irreversible choice

Required:
- normally >=3 candidates when three credible alternatives exist;
- independent Principal Critic/evaluator;
- failure/falsification testing;
- security/reliability/cost review as applicable;
- no candidate promoted if it violates a hard gate;
- residual-risk acceptance and revisit trigger.

The number of candidates may be lower only when the search space is genuinely narrower, and that limitation must be recorded.

## 3. Separation of author and judge

A professional agent may generate candidate outputs, but it must not be the sole authority that declares its own preferred candidate the winner.

Minimum separation:

```text
AUTHOR AGENT
  → candidate A/B/C

VERIFIER / TESTER / EVALUATOR
  → measurements + gate results

PRINCIPAL CRITIC for D3
  → attempts to falsify preferred candidate and metric choice

FATHER ORCHESTRATOR / governed decision step
  → promotion decision
```

Self-evaluation may be recorded as one signal, never as final proof for material decisions.

## 4. Universal comparison record

Each comparison uses a stable comparison ID.

```yaml
comparison_id: CMP-XXXX
project_record_id: PED-XXXX
agent_role: ANALYST | ARCHITECT | TESTER | PROGRAMMER | SECURITY | DEVSECOPS | RESEARCH | OSINT | OTHER
decision_class: D0 | D1 | D2 | D3
objective_refs: []
requirement_refs: []
risk_refs: []
baseline_or_champion_ref: null
candidate_refs: []
hard_gate_refs: []
metric_refs: []
test_or_eval_refs: []
measurement_refs: []
critic_ref: null
result: A_WINS | B_WINS | C_WINS | TIE | INCONCLUSIVE | NO_DOMINATING_CANDIDATE | ALL_REJECTED
selected_candidate_ref: null
rejected_candidate_refs: []
selection_reason: "..."
revisit_conditions: []
experience_ref: null
```

Candidates use stable IDs such as `CAND-XXXX` and must differ in a meaningful variable. Cosmetic rewordings are not separate candidates.

## 5. Hard gates before soft metrics

No weighted score may rescue a candidate that fails a mandatory safety/correctness/compliance gate.

Evaluation order:

```text
1. contract / requirement conformance
2. safety / security / permission gates
3. correctness / integrity gates
4. reliability / recoverability gates where mandatory
5. only then comparative soft metrics
6. cost / latency / complexity / maintainability / convenience
```

A cheaper or faster candidate is not better if it is wrong or unsafe.

## 6. Universal metric families

Not every metric applies to every agent. Each used metric must have provenance and purpose under the FATHER metric contract.

Common families:

- `CORRECTNESS` — acceptance/property satisfaction;
- `EVIDENCE_QUALITY` — traceability, source applicability, exact locator quality;
- `SAFETY_SECURITY` — policy/permission/security compliance;
- `ROBUSTNESS` — malformed, adversarial or incomplete input handling;
- `RELIABILITY` — failure/recovery/retry/consistency behaviour;
- `COST` — tokens, compute, tools, infrastructure, human review;
- `LATENCY` — end-to-end and stage latency distributions;
- `COMPLEXITY` — introduced components, coupling, operational burden;
- `MAINTAINABILITY` — change effort, testability, clarity, dependency burden;
- `REPRODUCIBILITY` — repeatability under controlled conditions;
- `HUMAN_INTERVENTION` — operator corrections/approvals/rework;
- `REVERSIBILITY` — rollback/change risk;
- `COVERAGE` — required domain/scenario/test coverage;
- `NOVELTY_VALUE` — whether a challenger tests a genuinely different hypothesis rather than duplicating the champion.

Composite scores remain prohibited until weights are calibrated. Raw dimensions remain visible.

## 7. Role-specific comparison examples

### Analyst

Compare alternative requirement interpretations, decomposition strategies or process/data-flow models.

Typical metrics:
- requirement coverage;
- contradiction count;
- unresolved ambiguity count;
- stakeholder acceptance;
- traceability completeness;
- downstream rework caused;
- time/cost to clarify.

A visually attractive diagram is not a winning analysis if it omits requirements or creates downstream ambiguity.

### Architect

Compare architecture candidates.

Typical metrics:
- requirement/NFR conformance;
- failure isolation;
- security boundary quality;
- deployability/operability;
- complexity;
- cost;
- reversibility;
- measured performance where relevant;
- change impact.

### Tester / QA

Compare verification strategies, test sets or verifier implementations.

Typical metrics:
- requirement/risk coverage;
- defect detection rate on seeded/known failures;
- false positive/false negative behaviour;
- execution cost/time;
- determinism/flakiness;
- reproducibility;
- regression value.

A larger test suite does not win merely because it has more tests.

### Programmer

Compare implementation, library, language, concurrency, persistence, service-boundary or agent-instance candidates.

Typical metrics:
- correctness;
- security;
- latency/throughput/resources where relevant;
- reliability/recovery;
- dependency/supply-chain risk;
- maintainability;
- complexity;
- total operating cost;
- testability;
- rollback/reversibility.

### Security

Compare controls/mitigations/architectural security measures.

Typical metrics:
- risk reduction against explicit threat scenarios;
- coverage;
- bypass/failure cases;
- residual risk;
- operational burden;
- false-positive impact;
- recovery impact;
- compliance/applicability;
- cost.

Security must not optimize a single security metric while ignoring unacceptable business or reliability damage unless the control is a mandatory legal/safety gate.

### DevSecOps / Operations

Compare build/deploy/rollback/monitoring approaches.

Typical metrics:
- deployment success;
- rollback time/success;
- reproducibility;
- change failure rate;
- recovery time;
- supply-chain evidence;
- operator effort;
- infrastructure cost.

### Research / OSINT

Compare acquisition/research plans, source mixes, hypotheses or evidence routes.

Typical metrics:
- source independence;
- provenance completeness;
- contradiction discovery;
- coverage;
- freshness;
- research sufficiency;
- cost/time;
- counter-evidence yield.

More sources alone is not a winning result.

## 8. Offline evaluation vs live A/B

The phrase "A/B test" covers several modes and must not be restricted to production traffic experiments.

### Offline bake-off

Preferred default for agents and engineering alternatives:
- same task/evaluation corpus;
- same allowed tools/data where applicable;
- repeated runs;
- hidden cases;
- deterministic verifiers when possible.

### Shadow evaluation

Candidate runs against real or replayed work without affecting production decisions.

### Canary / live A/B

Allowed only when product, legal, privacy, safety and operational controls permit it. User/customer-impacting experiments require explicit authorization and rollback.

### Tournament / A/B/n

Used when >=3 candidates are credible. Pairwise elimination is allowed, but all comparison conditions and stopping rules must be recorded.

## 9. Champion lifecycle

A winner becomes `CHAMPION` only for a bounded context.

```yaml
champion_id: CHAMP-XXXX
candidate_ref: CAND-XXXX
role: PROGRAMMER
scope: "..."
promoted_from_comparison: CMP-XXXX
valid_for_versions: []
known_limits: []
review_after: YYYY-MM-DD|null
rechallenge_triggers:
  - source/runtime change
  - repeated failure
  - cost/latency drift
  - new credible alternative
  - security finding
  - requirement/context shift
```

`CHAMPION` never means universally best.

## 10. Preventing benchmark gaming

Required controls for qualification-critical comparisons:
- hidden held-out cases;
- no leakage of expected answers/states;
- variant generation around the same competency;
- periodic replacement of overexposed tasks;
- explicit contamination status;
- separate training and evaluation history;
- independent verifier where practical;
- no optimization against one scalar score alone.

## 11. Experience feedback

Every material comparison produces experience, including losses.

```text
CMP result
→ candidate strengths/weaknesses
→ failed gates
→ metric effects
→ critic findings
→ context
→ EXPREC
→ repeated evidence
→ candidate KB update
```

A losing candidate may become the future champion when context changes. Therefore rejected candidates are retained with `revisit_conditions`.

## 12. Minimum FATHER-wide adoption gate

Before claiming that champion/challenger comparison is operational across FATHER:

- implement the common `CMP` schema;
- run at least one D2 comparison for Analyst, Tester, Programmer and Security/Architecture lane;
- use >=3 explicit metrics in each comparison;
- prove hard-gate-before-soft-score behaviour;
- produce at least one `NO_DOMINATING_CANDIDATE` or `INCONCLUSIVE` case without forcing a winner;
- save results into Engineering Memory;
- render the comparison in Teaching View and Production Card;
- prove that one later task can retrieve and reuse a prior comparison without treating it as universal truth.

## 13. Governing principle

**FATHER agents do not merely generate answers; they generate hypotheses/variants, test them under a declared objective, preserve losses, and improve the current champion from measured evidence.**
