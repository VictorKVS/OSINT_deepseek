# PROGRAMMING_KB Evidence Model v0.2

Status: **DRAFT / RESEARCH BASELINE**  
Date: **2026-08-15**

## 1. Goal

PROGRAMMING_KB stores not only facts and patterns, but the conditions under which they are valid, the evidence that supports them, known counter-evidence, and the tests needed before applying them in a concrete project.

A material Programmer decision must be auditable in both directions:

```text
DECISION
→ metric / criterion used
→ Knowledge Object / claim
→ exact source locator
→ source/version

SOURCE / REQUIREMENT
→ claim / Knowledge Object
→ metric or constraint derived from it
→ candidate comparison
→ decision affected
```

A human reviewer must be able to answer:

- what exactly was selected;
- which alternatives were considered;
- which source statement supports each material claim;
- where exactly that statement is located;
- which PROGRAMMING_KB object interprets it;
- which metrics were used;
- why each metric was relevant;
- where each threshold/target came from;
- what value each candidate produced;
- how those values changed the selection;
- which uncertainty, limitations and counter-evidence remain.

## 2. Evidence classes

Evidence classes are ordered by evidential role, not by popularity.

### E0 — Project reproducible evidence
Examples: repository tests, benchmark results, traces, incident records, profilers, fault-injection results, production metrics.

Use: strongest evidence for claims about **our actual environment** when the experiment is reproducible and correctly designed.

### E1 — Authoritative specification / standard / official normative guidance
Examples: language specifications, RFCs, ISO/IEC standards, NIST publications, OWASP verification standards, SLSA specification.

Use: semantics, requirements, security baselines, quality models, interoperability contracts.

### E2 — Peer-reviewed scientific evidence
Examples: systematic reviews, controlled studies, conference/journal papers with reproducible method and relevant scope.

Use: comparative claims, reliability/performance/security research, methods not fully settled by specifications.

### E3 — Consensus body of knowledge / established engineering textbook
Examples: IEEE SWEBOK and its curated reference set; established university/engineering texts.

Use: durable principles, terminology, design/test methods, educational grounding.

### E4 — Official engineering practice / vendor implementation evidence
Examples: official framework/runtime/database documentation, vendor architecture notes, upstream issue/release records, verified engineering case studies.

Use: version-specific implementation behaviour and operational constraints.

### E5 — Practitioner secondary source
Examples: reputable engineering articles, conference talks, technical blogs.

Use: hypothesis generation and practical examples; normally insufficient alone for D2/D3 decisions.

### E6 — Community/anecdotal source
Examples: forum answers, Q&A sites, social posts.

Use: discovery only. Must be independently verified before entering a material decision.

## 3. Source-quality dimensions

Each source record is scored/described separately on:

- `authority`
- `directness`
- `freshness`
- `version_match`
- `reproducibility`
- `independence`
- `context_fit`
- `known_limitations`

No single synthetic score is treated as truth until the weighting method is calibrated on real decisions.

## 4. Exact source locator contract

A source reference is incomplete for a material claim unless it identifies the exact part of the work that is being relied upon.

Minimum locator schema:

```yaml
source_ref: SRC-XXXX
source_version_ref: SRCV-XXXX|null
work_identity:
  author_or_owner: "..."
  title: "..."
  edition_or_version: "..."
  publication_date: YYYY-MM-DD|null
locator:
  locator_type: clause | paragraph | section | subsection | chapter | page | appendix | table | figure | anchor | path_line | commit_path_line | other
  locator_value: "e.g. § 9.2.2 / p. 417 / clause 5.3.1 / docs/x.md:L120-L137"
  parent_locator: "optional enclosing chapter/section"
  locator_verified: true|false
retrieved_at: YYYY-MM-DD
rights_state: "..."
content_fingerprint: "optional hash/fingerprint for locally preserved lawful excerpt or source snapshot"
notes: "..."
```

Required rules:

1. A book reference should identify edition/version and, where available, chapter/section plus page or exercise identifier.
2. A standard/RFC/specification reference should identify document version and exact clause/section/subsection.
3. A language/runtime claim should identify the exact language/runtime version and the relevant official documentation/specification section.
4. A repository/code source should identify commit or immutable revision, path and line/range where practical.
5. A scientific paper should identify the exact section/table/figure/result supporting the claim, not merely the paper title.
6. If the exact locator has not been verified, record `LOCATOR_UNVERIFIED`; the agent must not invent a clause, page or paragraph number.
7. Search snippets, LLM summaries and secondary descriptions never substitute for a verified locator in a D2/D3 decision.
8. The locator proves **where the source says something**; it does not by itself prove that the source is applicable to the current context.

### 4.1 Claim-to-source citation object

Each material claim used by a decision should be represented as a traceable citation object:

```yaml
citation_id: CIT-PROG-XXXX
knowledge_id: PKB-XXXX
claim_id: CLM-PROG-XXXX
source_ref: SRC-XXXX
source_locator_ref: LOC-XXXX
support_role: SUPPORTS | LIMITS | CONTRADICTS | DEFINES | SUPERSEDES
applicability_note: "why this source statement applies to this candidate/context"
interpretation_note: "what exact proposition is being taken from the source"
review_status: VERIFIED | LIMITED | LOCATOR_UNVERIFIED
```

The Programmer output may use compact visible markers such as:

```text
[KB:PKB-0042]
[SRC:SRC-RFC9110 §9.2.2]
[CIT:CIT-PROG-0187]
```

The marker is an index into the evidence bundle; the full bundle remains machine-readable and auditable.

## 5. Knowledge Object schema

```yaml
knowledge_id: PKB-XXXX
status: DRAFT | VALIDATED | LIMITED | DEPRECATED | SUPERSEDED
claim: "..."
knowledge_domain: "..."
decision_classes: [D1, D2]
claim_refs: [CLM-PROG-XXXX]
citation_refs: [CIT-PROG-XXXX]
source_refs: [SRC-XXXX]
source_locator_refs: [LOC-XXXX]
source_classes: [E1, E3]
source_versions: []
retrieved_at: YYYY-MM-DD
valid_from: YYYY-MM-DD|null
review_after: YYYY-MM-DD|null
applies_when: []
does_not_apply_when: []
assumptions: []
alternatives: []
known_risks: []
counter_evidence_refs: []
verification_method: "..."
project_evidence_refs: []
confidence_state: UNCALIBRATED | PROVISIONAL | SUPPORTED | CONTESTED
supersedes: null
superseded_by: null
notes: "..."
```

## 6. Metric provenance and purpose contract

A decision metric is not merely a number. Every metric used to compare candidates must state **why it is being used and where its target/threshold came from**.

Metric schema:

```yaml
metric_id: MET-PROG-XXXX
name: "..."
category: correctness | security | reliability | performance | compatibility | maintainability | complexity | cost | operability | reversibility | evidence_quality | other
decision_question: "What decision question does this metric answer?"
purpose: "Why this metric matters for this requirement/context"
derived_from:
  requirement_refs: []
  knowledge_refs: []
  citation_refs: []
definition: "precise definition"
unit: "ms | req/s | count | bool | % | currency | score-component | ..."
measurement_method: "..."
measurement_environment_ref: "..."
direction: LOWER_IS_BETTER | HIGHER_IS_BETTER | PASS_FAIL | RANGE
role: HARD_GATE | SOFT_COMPARISON | OBSERVATION_ONLY
threshold_or_target:
  value: null
  source: "requirement | standard | benchmark baseline | calibrated project history | none"
  provenance_ref: null
weight:
  value: null
  state: NOT_USED | UNCALIBRATED | CALIBRATED
  calibration_ref: null
known_limitations: []
uncertainty_method: "none | CI | repeated-runs | measurement-error | ..."
revisit_condition: "..."
```

### 6.1 Metric-selection rules

For every D2/D3 decision:

- each metric must be connected to at least one requirement, constraint, risk, Knowledge Object or explicit product objective;
- an arbitrary threshold is prohibited; if no defensible threshold exists, record `NO_DEFENSIBLE_THRESHOLD` and compare raw observations without pretending there is a pass line;
- a metric weight may not be invented to force a preferred winner;
- composite scores are prohibited until the weighting/calibration method has held-out evidence;
- hard gates are evaluated before soft comparison metrics;
- raw measurements remain visible even if a later calibrated composite score is used;
- metrics that were considered but deliberately excluded should be recorded with an exclusion reason when their omission could materially change the decision;
- the agent must distinguish `MEASURED`, `DERIVED`, `ESTIMATED`, `SOURCE_STATED` and `UNKNOWN` values.

### 6.2 Candidate measurement record

```yaml
measurement_id: MEAS-PROG-XXXX
metric_id: MET-PROG-XXXX
candidate_id: CAND-PROG-XXXX
value: null
value_state: MEASURED | DERIVED | ESTIMATED | SOURCE_STATED | UNKNOWN
sample_size: null
run_refs: []
result_evidence_refs: []
uncertainty: null
pass_gate: true|false|null
notes: "..."
```

### 6.3 Metric effect on the decision

The final bundle must show not just metric values but the decision effect:

```yaml
metric_effect:
  metric_id: MET-PROG-XXXX
  candidate_comparison: "..."
  effect: ELIMINATED | FAVORED | DISFAVORED | TIE | NO_EFFECT | INCONCLUSIVE
  reason: "..."
  evidence_refs: []
```

This prevents post-hoc statements such as "candidate A was faster and therefore better" when speed was not a material requirement or when candidate A failed a safety gate.

## 7. Decision Evidence Bundle

A material decision consumes multiple Knowledge Objects and produces an auditable bundle:

```yaml
decision_id: PDR-XXXX
requirement_refs: []
context: {}
constraints: []
candidates: []
claims_used: []
knowledge_refs: []
citation_refs: []
source_refs: []
source_locator_refs: []
metrics_used: []
metrics_considered_but_excluded: []
measurements: []
metric_effects: []
risks_by_candidate: {}
unknowns: []
counter_evidence: []
experiment_plan: null
experiment_results: []
selected_candidate: null
selection_reason: "..."
rejected_candidates: []
revisit_conditions: []
residual_risks: []
review_status: DRAFT
```

### 7.1 Mandatory human-readable decision explanation

For D2/D3, the Programmer must be able to render a compact audit view like:

```text
DECISION PDR-0041
Selected: Candidate B

Reason 1 — semantic correctness
  Based on: [KB:PKB-0042]
  Source: [SRC:SRC-XXXX §x.y.z]
  Metric: [MET:MET-PROG-CORR-003] contract conformance
  Why metric used: required by REQ-017
  A = FAIL, B = PASS, C = PASS
  Effect: Candidate A eliminated by hard gate

Reason 2 — retry behaviour under target workload
  Based on: [KB:PKB-0108]
  Source: [SRC:SRC-YYYY §a.b]
  Metric: [MET:MET-PROG-REL-014] failed-operation recovery rate
  Why metric used: RISK-023 + REQ-021
  A = 98.7%, B = 99.98%, C = 99.90% across RUN-... 
  Effect: B favored; difference remains context-specific E0 evidence

Reason 3 — operational cost
  Metric: [MET:MET-PROG-COST-006]
  Threshold source: no hard threshold; raw comparison only
  A = ..., B = ..., C = ...
  Effect: B favored only after correctness/reliability gates passed

Rejected: A — failed correctness gate; C — higher operational burden with no measured compensating benefit.
Unknowns: ...
Revisit when: ...
```

The rendered explanation must never imply that a metric was causal in the selection if the evidence bundle records `NO_EFFECT` or `INCONCLUSIVE`.

## 8. Evidence sufficiency rules

### D0
Local diff/test evidence may be sufficient.

### D1
At least one directly relevant authoritative/consensus source OR strong E0 project evidence, plus local tests when behaviour changes.

### D2
Required:
- at least two credible candidate solutions;
- at least one E1/E2/E3 source supporting the decision basis;
- exact source locator for each material source-derived claim, or explicit `LOCATOR_UNVERIFIED` blocking promotion where locator verification is material;
- explicit PROGRAMMING_KB/claim/citation IDs for material reasoning;
- explicit applicability/version check;
- explicit metrics/criteria and why each was selected;
- threshold/target provenance or explicit `NO_DEFENSIBLE_THRESHOLD`;
- per-candidate measurements/evidence for material comparative claims;
- explicit risks/trade-offs;
- counter-evidence search;
- E0 experiment when the deciding claim is context-dependent (performance, scale, compatibility, reliability, operational cost).

### D3
Required:
- all D2 controls;
- independent review/Principal Critic;
- stronger source diversity, normally including independent sources;
- failure-mode/falsification analysis;
- review for metric cherry-picking and arbitrary weights/thresholds;
- security/supply-chain review where relevant;
- explicit residual-risk acceptance.

Exception: a single canonical specification may be the definitive source for a narrow semantic requirement, but local conformance still needs verification when implementation behaviour matters.

## 9. Freshness and knowledge decay

Every version-sensitive claim carries:

```text
source_date
retrieved_at
product/runtime version
valid_from
review_after
superseded_by
last_project_verification
```

A knowledge object becomes `STALE_REVIEW_REQUIRED` when its review date expires, a referenced dependency/runtime reaches end-of-life, the authoritative source is superseded, or project evidence contradicts it.

Source locators must also be revalidated when the source version changes. A locator from version N must not be silently reused for version N+1.

## 10. Counter-evidence rule

For D2/D3 decisions the system must ask:

> What evidence would make this recommendation wrong?

Counter-evidence is stored, not discarded. Rejected alternatives retain `revisit_conditions` so a future change in workload, cost, team competence, security posture or platform can reopen the decision.

Counter-evidence should use the same exact locator and citation rules as supporting evidence.

## 11. Reliability over speed mode

When speed is explicitly not important, the agent increases depth rather than merely producing a longer answer:

1. expand source search to E1-E3 plus relevant E4;
2. verify exact locators for deciding claims;
3. search for counter-evidence;
4. compare at least three candidates when credible alternatives exist;
5. declare metric purpose and threshold provenance before reading candidate results where practical;
6. reproduce critical claims experimentally;
7. run failure-mode and security review;
8. ask Principal Critic to attack the preferred choice and the metric selection itself;
9. preserve all evidence and rejected alternatives.

## 12. Anti-patterns prohibited

- popularity = correctness;
- number of citations = evidence quality;
- a citation without a verified exact locator is treated as sufficient for D2/D3;
- invented paragraph/page/clause identifiers;
- five blogs outweigh one canonical specification;
- benchmark from another environment = guaranteed local result;
- a metric is used merely because it is easy to measure;
- an arbitrary threshold is presented as an engineering requirement;
- metric weights are tuned after seeing results to produce a desired winner;
- a composite score hides a failed hard safety/correctness gate;
- newer technology = better technology;
- microservices = mature architecture;
- a passing SAST tool = secure code;
- LLM explanation = source evidence.