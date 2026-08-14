# PROGRAMMING_KB Evidence Model v0.1

Status: **DRAFT / RESEARCH BASELINE**  
Date: **2026-08-14**

## 1. Goal

PROGRAMMING_KB stores not only facts and patterns, but the conditions under which they are valid, the evidence that supports them, known counter-evidence, and the tests needed before applying them in a concrete project.

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

## 4. Knowledge Object schema

```yaml
knowledge_id: PKB-XXXX
status: DRAFT | VALIDATED | LIMITED | DEPRECATED | SUPERSEDED
claim: "..."
knowledge_domain: "..."
decision_classes: [D1, D2]
source_refs: [SRC-XXXX]
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

## 5. Decision Evidence Bundle

A material decision consumes multiple Knowledge Objects and produces an auditable bundle:

```yaml
decision_id: PDR-XXXX
requirement_refs: []
context: {}
constraints: []
candidates: []
claims_used: []
source_refs: []
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

## 6. Evidence sufficiency rules

### D0
Local diff/test evidence may be sufficient.

### D1
At least one directly relevant authoritative/consensus source OR strong E0 project evidence, plus local tests when behaviour changes.

### D2
Required:
- at least two credible candidate solutions;
- at least one E1/E2/E3 source supporting the decision basis;
- explicit applicability/version check;
- explicit risks/trade-offs;
- counter-evidence search;
- E0 experiment when the deciding claim is context-dependent (performance, scale, compatibility, reliability, operational cost).

### D3
Required:
- all D2 controls;
- independent review/Principal Critic;
- stronger source diversity, normally including independent sources;
- failure-mode/falsification analysis;
- security/supply-chain review where relevant;
- explicit residual-risk acceptance.

Exception: a single canonical specification may be the definitive source for a narrow semantic requirement, but local conformance still needs verification when implementation behaviour matters.

## 7. Freshness and knowledge decay

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

## 8. Counter-evidence rule

For D2/D3 decisions the system must ask:

> What evidence would make this recommendation wrong?

Counter-evidence is stored, not discarded. Rejected alternatives retain `revisit_conditions` so a future change in workload, cost, team competence, security posture or platform can reopen the decision.

## 9. Reliability over speed mode

When speed is explicitly not important, the agent increases depth rather than merely producing a longer answer:

1. expand source search to E1-E3 plus relevant E4;
2. search for counter-evidence;
3. compare at least three candidates when credible alternatives exist;
4. reproduce critical claims experimentally;
5. run failure-mode and security review;
6. ask Principal Critic to attack the preferred choice;
7. preserve all evidence and rejected alternatives.

## 10. Anti-patterns prohibited

- popularity = correctness;
- number of citations = evidence quality;
- five blogs outweigh one canonical specification;
- benchmark from another environment = guaranteed local result;
- newer technology = better technology;
- microservices = mature architecture;
- a passing SAST tool = secure code;
- LLM explanation = source evidence.
