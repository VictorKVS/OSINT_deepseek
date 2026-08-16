# OSINT Research & Hypothesis Engine

**Document ID:** OSINT-RES-0001  
**Status:** ARCHITECTURE / RESEARCH CONTRACT — IMPLEMENTATION NOT YET APPROVED  
**Method binding:** EDKBCM / KBRE  
**Purpose:** extend the OSINT worker from evidence acquisition into a controlled uncertainty-reduction loop without allowing hypotheses or model opinion to masquerade as verified knowledge.

## 1. Governing principle

OSINT remains an evidence supplier. It may generate and rank hypotheses for research planning, but it must never publish a hypothesis as FACT merely because it is plausible or highly scored.

Canonical loop:

`UNKNOWN → HYPOTHESES → EVIDENCE SEARCH → DISCRIMINATING TEST → UPDATE → CONVERGENCE / REMAIN UNKNOWN`

The system must distinguish at minimum:

- `FACT` — directly supported observation/claim at the required evidence tier;
- `INFERENCE` — conclusion derived from identified facts/rules;
- `HYPOTHESIS` — testable explanation or version;
- `ALTERNATIVE_HYPOTHESIS` — competing explanation;
- `OPINION` — reasoned synthesis not promoted to fact;
- `RECOMMENDATION` — proposed action;
- `UNKNOWN` — missing information;
- `CONFLICT` — credible evidence is inconsistent;
- `REJECTED_HYPOTHESIS` — hypothesis contradicted beyond the current acceptance rule.

## 2. Research object model

Every research question receives a stable `RQ-*` identifier.

Minimum entities:

- `RQ-*` research question;
- `FACT-*` evidence-backed fact;
- `SRC-*` source observation;
- `HYP-*` hypothesis;
- `ALT-HYP-*` alternative hypothesis;
- `TEST-*` discriminating research test;
- `RESULT-*` test result;
- `GAP-*` missing evidence;
- `REC-*` recommendation;
- `DEC-*` research decision;
- `COST-*` research effort/cost observation.

Every hypothesis must record:

- statement;
- scope/context;
- created_at;
- evidence_for;
- evidence_against;
- missing_discriminating_evidence;
- competing hypotheses;
- current status;
- confidence model/version if any;
- next best test candidates;
- provenance of the hypothesis generation event.

## 3. Evidence and provenance contract

Source observations must retain URI/identity, acquisition timestamp, source class, author/publisher where known, content hash where feasible, extraction/normalization provenance and freshness.

A hypothesis may cite evidence but must not modify the truth status of that evidence.

Search snippets, summaries and model-generated statements remain discovery aids unless independently promoted under the evidence policy.

## 4. Hypothesis lifecycle

`PROPOSED → UNDER_TEST → SUPPORTED / WEAKENED / CONFLICTED / REJECTED / INCONCLUSIVE`

`SUPPORTED` is not equivalent to `FACT`.

Promotion from hypothesis-derived conclusion to knowledge requires the destination Knowledge Gate / domain proof-floor.

No hypothesis is deleted merely because it lost. Rejected hypotheses are research assets because they prevent repeated dead ends.

## 5. Discriminating-test selection

Research should prefer evidence or tests that most efficiently distinguish competing hypotheses rather than simply maximize document volume.

Candidate utility dimensions:

- expected uncertainty reduction;
- acquisition cost;
- elapsed time;
- source authority/reliability;
- independence from existing evidence;
- legal/ethical availability;
- freshness;
- reversibility/safety of the research action.

Research-efficiency concept:

`RESEARCH_EFFICIENCY = uncertainty_reduction / (human_time + machine_cost + acquisition_cost)`

This is a research metric, not a universal normative formula. The exact uncertainty model must be versioned and empirically validated before numeric scores are treated as calibrated probabilities.

## 6. Confidence rules

Do not emit false precision such as `confidence=0.83` unless the confidence mechanism is defined, versioned, calibrated and exposes its evidence/sample assumptions.

Before calibration, prefer ordinal states such as:

`VERY_LOW / LOW / MEDIUM / HIGH / VERY_HIGH`

with explicit reasons.

Future research may benchmark Bayesian updating, likelihood ratios, evidence-weighting, argumentation frameworks or other statistically justified approaches.

## 7. Analyst and Socrates roles

OSINT:
- discovers and acquires evidence;
- records provenance;
- detects gaps/conflicts;
- proposes researchable hypotheses and discriminating tests;
- returns evidence packages.

Analyst:
- normalizes facts and competing explanations;
- evaluates applicability/context;
- decides which hypothesis/test enters the research queue;
- prepares candidate conclusions.

Socrates / Red Team:
- attacks assumptions;
- searches for alternative explanations;
- checks circular evidence and source dependence;
- challenges confidence and missing-data handling;
- returns `PASS / RESEARCH_MORE / INCONCLUSIVE`.

Knowledge Gate:
- alone may promote candidate conclusions into the target knowledge base according to its proof-floor.

## 8. Safety and legality

The research loop is for lawful OSINT and research. Acquisition methods remain subject to project legal, ethical, privacy, security and platform constraints. A high expected information gain never authorizes an otherwise prohibited collection action.

## 9. Telemetry required for KBRE / EDKBCM

Every research run should emit:

- number of research questions;
- hypotheses proposed;
- alternatives considered;
- hypotheses rejected;
- evidence items acquired;
- evidence items promoted/rejected;
- conflicts detected/resolved;
- acquisition attempts and failures;
- human review minutes;
- machine/tool cost;
- time to first useful evidence;
- time to hypothesis discrimination;
- repeated/dead-end searches avoided;
- reuse of prior acquisition recipes;
- final uncertainty state;
- lessons returned to EDKBCM.

This telemetry feeds the Knowledge Factory research program so later OSINT missions become faster and cheaper without lowering evidence quality.

## 10. Knowledge Factory integration

Output contract:

`OSINT MATERIAL/EVIDENCE PACKAGE → ANALYST → SOCRATES → KNOWLEDGE GATE → DOMAIN KB`

Research feedback:

`DOMAIN KB GAP → RQ → OSINT RESEARCH LOOP → RESULT → KB UPDATE / REMAIN UNKNOWN`

Method feedback:

`OSINT RUN METRICS → KBRE/EDKBCM → METHOD EXPERIMENT → GOLDEN/REJECTED METHOD`

Therefore OSINT is both a collector and an experimental sensor for the Knowledge Factory.

## 11. MVP progression

### R0 — Contract only
Define entity states, interfaces and test cases. No autonomous hypothesis promotion.

### R1 — Manual hypothesis ledger
Analyst creates hypotheses and evidence links; OSINT records source packages.

### R2 — Assisted hypothesis generation
Model proposes alternatives and gaps; human/Analyst selects tests.

### R3 — Evidence-aware research planner
Rank next research actions by quality-adjusted expected information gain and cost.

### R4 — Automated bounded research loop
Execute approved collectors within hard limits, update evidence state, stop on budget/gate.

### R5 — Cross-domain research engine
Reuse the same loop for Security, architecture, programming, electronics, robotics, medicine, agriculture and later domains, with domain-specific proof floors.

## 12. Mandatory regression scenarios before implementation

At minimum test:

1. one source repeated by ten mirrors does not become ten independent confirmations;
2. absence of evidence does not become evidence of absence;
3. a search failure does not reject a hypothesis;
4. a plausible model explanation remains HYPOTHESIS;
5. contradictory authoritative sources produce CONFLICT;
6. new evidence can weaken a previously favored hypothesis;
7. rejected hypotheses remain preserved;
8. research stops at configured time/cost/tool limits;
9. numeric confidence is blocked when no calibrated model exists;
10. Knowledge Gate rejects hypothesis-only output presented as FACT;
11. the chosen next test must expose why it was selected;
12. provenance survives every transformation from collector to analyst.

## 13. Current architectural decision

Adopt this research loop as a planned OSINT capability, but do not implement autonomous decision publication yet. First integrate telemetry and research object contracts with the existing DEV baseline and existing Analyst/Socrates loop, then add tests, then code.

This preserves the repository's governing rule: **NO CODE BEFORE CONTRACT**.
