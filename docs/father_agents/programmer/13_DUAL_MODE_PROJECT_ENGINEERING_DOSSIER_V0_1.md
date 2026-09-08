# FATHER Project Engineering Dossier — Dual-Mode Development Record v0.1

Status: **DESIGN BASELINE / TRAINING + PRODUCTION TRACEABILITY**  
Date: **2026-08-15**

## 1. Purpose

Every non-trivial FATHER software project should accumulate not only source code, but a structured engineering record explaining how the solution was derived, how it was tested, which evidence and metrics affected the choice, and what experience should be reused later.

The record has **one canonical data model and two views**:

```text
CANONICAL PROJECT ENGINEERING DOSSIER
        ├─ TEACHING VIEW
        │    explanations, rationale, source notes, metric meaning,
        │    diagrams, examples, why alternatives were rejected
        │
        └─ PRODUCTION CARD VIEW
             compact machine-readable engineering card:
             IDs, requirements, diagrams, decisions, metrics,
             tests, evidence, code refs, results, status
```

The two views MUST be rendered from the same underlying records. They must not be manually maintained as independent documents because that would create drift.

It is acceptable and expected that the dossier is longer than the program code. The dossier is not documentation overhead for its own sake: it is the reusable engineering memory from which FATHER learns how projects were analysed, designed, implemented, tested and improved.

## 2. Two roles of the same record

### Role A — Teaching / explanatory mode

Used for:
- training people;
- training/evaluating professional agents;
- explaining FATHER-owned projects;
- code review and mentoring;
- reconstruction of why a historical decision was made;
- generation of future courses and practice material.

The Teaching View expands every material stage with:
- what the stage does;
- why it exists;
- which inputs it consumes;
- which outputs it produces;
- which sources/KB objects justify the method;
- which metrics are used and why;
- common mistakes and counterexamples;
- interpretation of diagrams and tests;
- implications for later stages.

### Role B — Production engineering card

Used during normal project execution and machine processing.

It contains no tutorial prose unless a clarification is materially required. It stores compact structured fields and stable references so FATHER can reconstruct the full reasoning when requested.

Example:

```yaml
project_record_id: PED-0042
requirement_bundle: ANL-REQ-0042
analysis_refs: [ANL-0042]
diagram_refs: [DGM-0112, DGM-0113]
test_plan_ref: TPL-0042
programmer_decisions: [PDR-0171, PDR-0172]
metric_refs: [MET-PROG-0021, MET-TEST-0014]
implementation_refs: [IMP-0042]
verification_refs: [VER-0088]
experiment_refs: [EXP-0031]
experience_refs: [EXPREC-0177]
status: VERIFIED
```

## 3. Canonical lifecycle

```text
BUSINESS / USER NEED
        ↓
ANALYST INTAKE + REQUIREMENT MODEL
        ↓
SCHEMES / FLOWS / STATES / CONSTRAINTS
        ↓
TESTER ACCEPTANCE + TEST MODEL
        ↓
PROGRAMMER CANDIDATES + EVIDENCE + METRICS
        ↓
IMPLEMENTATION
        ↓
TEST / SECURITY / RELIABILITY VERIFICATION
        ↓
A/B OR MULTI-CANDIDATE EXPERIMENT WHEN MATERIAL
        ↓
RESULT + FAILURE RECORDS
        ↓
EXPERIENCE / KNOWLEDGE UPDATE
        ↓
FUTURE FATHER DECISIONS
```

Each stage receives a stable ID and may contain child IDs for decisions, metrics, diagrams, tests and evidence.

## 4. Stage A — Analyst project card

The Analyst creates the first project record. Programmer work does not start from an unstructured chat message when a material project is involved.

Minimum Analyst output:

```yaml
analysis_id: ANL-XXXX
project_record_id: PED-XXXX
request_source: "..."
problem_statement: "..."
business_goal: "..."
users_or_actors: []
current_state: "..."
target_state: "..."
functional_requirements: []
nonfunctional_requirements: []
constraints: []
assumptions: []
unknowns: []
data_classes: []
external_dependencies: []
risks_known_at_intake: []
acceptance_intent: []
diagram_refs: []
source_refs: []
knowledge_refs: []
```

### 4.1 Analyst diagrams

The Analyst should create only diagrams that reduce material ambiguity. Diagram type is chosen by information need, not fashion.

Candidate diagram IDs:

- `DGM-CONTEXT-XXXX` — system/context boundary;
- `DGM-FLOW-XXXX` — information/data flow;
- `DGM-SEQUENCE-XXXX` — interaction sequence;
- `DGM-STATE-XXXX` — state/lifecycle transitions;
- `DGM-DATA-XXXX` — data entities/relationships where useful;
- `DGM-DEPLOY-XXXX` — deployment/topology;
- `DGM-SEC-XXXX` — trust/security boundary;
- `DGM-PROCESS-XXXX` — business/process flow.

Each diagram must have:

```yaml
diagram_id: DGM-XXXX
purpose: "what ambiguity/question this diagram resolves"
notation: "..."
source_model_refs: []
requirement_refs: []
assumptions: []
version: "..."
```

The Teaching View explains how to read the diagram and why it was selected. The Production Card stores the diagram plus its IDs and purpose.

## 5. Stage B — Tester card before implementation

The Tester receives the Analyst record and writes the schematic verification model before or alongside implementation design.

The purpose is to make acceptance conditions visible before code optimizes toward an accidental interpretation of the requirement.

Minimum Tester output:

```yaml
test_plan_id: TPL-XXXX
project_record_id: PED-XXXX
analysis_ref: ANL-XXXX
requirement_test_map: []
test_cases: []
negative_cases: []
boundary_cases: []
security_cases: []
reliability_cases: []
performance_cases: []
recovery_cases: []
test_metric_refs: []
source_refs: []
knowledge_refs: []
unknown_testability: []
```

Each material test has a stable ID:

```yaml
test_id: TST-XXXX
requirement_refs: [REQ-XXXX]
purpose: "what property is being verified"
preconditions: []
action_or_stimulus: "..."
expected_property: "..."
verifier: "..."
metric_refs: []
evidence_expected: []
source_locator_refs: []
knowledge_refs: []
why_this_test_exists: "..."
```

### 5.1 Tester explanations mirror Programmer explanations

In Teaching View, the Tester explains:
- why this property needs verification;
- where the expected behaviour came from;
- whether the test is requirement-derived, source-derived, risk-derived or regression-derived;
- which metric is used and why;
- why a threshold exists;
- what false positive/false negative risk remains;
- which important property cannot yet be tested and why.

Thus the test layer has the same evidence discipline as the implementation layer.

## 6. Stage C — Programmer decision and implementation card

The Programmer consumes the Analyst and Tester records.

For every D2/D3 decision, the Programmer records:

```text
requirement/context
→ candidate solutions
→ exact source/KB basis
→ criteria/metrics
→ measurements or expected properties
→ risks/counter-evidence
→ selected candidate
→ rejected alternatives
→ code/implementation refs
→ revisit conditions
```

The detailed source-locator and metric-provenance rules are inherited from `02_PROGRAMMING_KB_EVIDENCE_MODEL_V0_1.md`.

Minimum implementation record:

```yaml
implementation_id: IMP-XXXX
project_record_id: PED-XXXX
analysis_ref: ANL-XXXX
test_plan_ref: TPL-XXXX
decision_refs: [PDR-XXXX]
code_refs: []
configuration_refs: []
dependency_refs: []
metric_refs: []
source_refs: []
knowledge_refs: []
known_deviations: []
known_debt: []
```

The Teaching View expands each material decision into human-readable rationale such as:

```text
Decision: use candidate B
Because: REQ-021 requires bounded recovery time
Knowledge: [KB:PKB-0108]
Source: [SRC:SRC-XXXX §5.3.1]
Metric: [MET:MET-PROG-REL-014]
Why this metric: measures the requirement property directly
A = ... / B = ... / C = ...
Effect: A eliminated, B favored, C acceptable but more complex
Test coverage: [TST:TST-0182, TST-0183]
Code: [IMP:IMP-0042 path/ref]
Revisit when: workload or requirement changes
```

## 7. Stage D — Verification record

After implementation, Tester/Security/other verifier agents attach results rather than replacing the original plan.

```yaml
verification_id: VER-XXXX
project_record_id: PED-XXXX
implementation_ref: IMP-XXXX
test_plan_ref: TPL-XXXX
executed_test_refs: []
pass_count: 0
fail_count: 0
blocked_count: 0
measurement_refs: []
failure_refs: []
security_review_refs: []
critic_refs: []
acceptance_state: PASS | CONDITIONAL_PASS | FAIL | BLOCKED
```

Planned expectation and observed result remain separate so FATHER can learn from incorrect assumptions.

## 8. Stage E — A/B and multi-candidate engineering tests

A/B tests are not limited to UI/product experiments. FATHER may use controlled comparative experiments to evaluate competing engineering approaches.

Experiment record:

```yaml
experiment_id: EXP-XXXX
project_record_id: PED-XXXX
question: "..."
hypothesis: "..."
candidates: [CAND-A, CAND-B]
controlled_variables: []
changed_variable: "..."
metric_refs: []
hard_gates: []
run_plan: "..."
run_refs: []
results: []
uncertainty: "..."
conclusion: A_WINS | B_WINS | TIE | INCONCLUSIVE | NO_DOMINATING_CANDIDATE
critic_ref: null
revisit_conditions: []
```

Rules:
- the decision question and metrics are declared before inspecting results where practical;
- candidates receive comparable workload/resources unless resource difference is the variable under study;
- hard correctness/security gates dominate soft performance/cost preferences;
- raw results remain inspectable;
- no winner is forced when the evidence is inconclusive;
- failed candidates are retained as experience, not deleted.

For more than two candidates, the same record becomes an A/B/n or tournament comparison.

## 9. Stage F — Experience record and FATHER learning

Every project should produce experience objects that may later influence FATHER decisions without silently becoming universal truth.

```yaml
experience_id: EXPREC-XXXX
project_record_id: PED-XXXX
stage_refs: []
context_signature: "..."
what_worked: []
what_failed: []
root_causes: []
metric_outcomes: []
counterexamples: []
regression_test_refs: []
candidate_knowledge_updates: []
review_status: DRAFT | LIMITED | VALIDATED
reuse_conditions: []
do_not_generalize_when: []
```

Learning chain:

```text
PROJECT
→ DECISION
→ TEST
→ RESULT
→ FAILURE / SUCCESS
→ EXPERIENCE RECORD
→ repeated independent evidence
→ reviewed Knowledge Object
→ future retrieval/decision support
```

A single project result cannot automatically change a global Knowledge Object. Promotion requires the normal evidence and review gates.

## 10. Stable ID families

Initial ID namespace:

```text
PED-       Project Engineering Dossier
ANL-       Analyst record
REQ-       Requirement
DGM-       Diagram
TPL-       Test plan
TST-       Test case
PDR-       Programmer Decision Record
CAND-      Candidate solution
SRC-       Source
SRCV-      Source version
LOC-       Exact source locator
CIT-       Claim-to-source citation
PKB-       Programming Knowledge Object
MET-       Metric
MEAS-      Measurement
IMP-       Implementation
VER-       Verification
EXP-       Controlled experiment / A-B-n test
FAIL-      Failure record
EXP-REC-   Experience record (implementation may normalize exact prefix)
CRIT-      Principal Critic review
```

IDs are stable and never renumbered merely for cosmetic ordering.

## 11. Metric lineage across roles

Metrics must be traceable across the whole project, not recreated independently by each role.

Example:

```text
REQ-021: recovery <= agreed business tolerance
        ↓
ANL-0042: records business impact / target-state constraint
        ↓
MET-REL-014: recovery-time metric, definition + provenance
        ↓
TST-0182: fault/recovery test uses MET-REL-014
        ↓
PDR-0171: candidate comparison uses the same MET-REL-014
        ↓
MEAS-0311/0312/0313: candidate measurements
        ↓
VER-0088: final implementation measurement
        ↓
EXP-0031: A/B comparison if alternatives remain material
        ↓
EXPREC-0177: experience outcome
```

This allows a reviewer to ask either:

> Why was this architecture chosen?

or:

> Where did this metric come from and everywhere was it used?

and traverse the graph in either direction.

## 12. Teaching View rendering example

A future learner-facing rendering may look like:

```text
PROJECT PED-0042 — Add reliable import pipeline

1. ANALYST
   Requirement REQ-021 ...
   Diagram DGM-FLOW-0112 ...
   Explanation: why the flow is separated this way ...

2. TESTER
   TST-0182 Recovery after interruption
   Based on REQ-021 + PKB-...
   Metric MET-REL-014
   Explanation: why recovery is measured and how ...

3. PROGRAMMER
   PDR-0171 compares A/B/C
   Sources: exact clauses/sections ...
   Metrics: correctness, recovery, cost ...
   Explanation: why each metric matters ...

4. CODE
   IMP-0042 ...

5. VERIFICATION
   TST-... PASS / FAIL
   measured values ...

6. EXPERIMENT
   EXP-0031 A/B result ...

7. WHAT FATHER LEARNED
   EXPREC-0177 ...
   candidate KB updates ...
```

This can become course material automatically without rewriting the project from scratch.

## 13. Production Card rendering example

```yaml
ped: PED-0042
analysis: ANL-0042
diagrams: [DGM-FLOW-0112]
test_plan: TPL-0042
decisions: [PDR-0171]
metrics: [MET-REL-014, MET-COST-006]
implementation: IMP-0042
verification: VER-0088
experiments: [EXP-0031]
experience: [EXPREC-0177]
state: VERIFIED
```

No explanatory text is required during routine machine processing because every ID resolves to the same underlying graph. A human may request the Teaching View at any time.

## 14. Consequences for FATHER knowledge development

The dossier turns ordinary project work into a continuously growing evidence corpus:

- Analyst experience accumulates patterns of requirements, ambiguity and diagrams;
- Tester experience accumulates test methods, failure modes and metric usefulness;
- Programmer experience accumulates candidate decisions, source-backed rationale and implementation outcomes;
- Security/Architecture/Critic findings become linked cross-role evidence;
- A/B/n experiments calibrate which approaches dominate under which contexts;
- repeated results may later calibrate metric thresholds/weights;
- courses and exercises may be generated from real sanitized project traces;
- professional agents are evaluated against the same traceability expectations.

Thus the project repository becomes not only a collection of programs, but a **development knowledge base with reconstructable engineering lineage**.

## 15. First implementation gate

Before building a generic runtime for this dossier, prove the schema on one real or representative project.

Required proof:

1. one `PED-*` record;
2. one Analyst record with at least two diagrams;
3. at least five requirement IDs;
4. Tester map with >=10 tests including negative/boundary cases;
5. Programmer comparison with >=2 credible candidates;
6. exact source/KB references for material claims;
7. >=3 explicit metrics with provenance/purpose;
8. one implementation reference;
9. one verification record;
10. one A/B or A/B/n experiment where a real decision question exists;
11. one Experience Record;
12. render both Teaching View and Production Card from the same underlying data.

Only after this pass should FATHER choose the concrete storage/rendering implementation.