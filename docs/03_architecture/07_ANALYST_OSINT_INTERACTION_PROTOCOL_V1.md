# Analyst ↔ OSINT Expert Interaction Protocol v1

Status: ACCEPTED BASELINE

## Goal
Ensure that every handoff between ANALYST and OSINT_EXPERT is explicit, versioned, auditable and traceable to inputs, knowledge and decisions.

## Canonical workflow

`Task → ResearchRequest → SearchPlanProposal → PlanDecision → Collection/Processing → EvidencePackage → AnalyticalAssessment → ResearchGap OR Conclusion`

A ResearchGap starts another iteration while preserving the same case lineage.

## Protocol objects

### ResearchRequest
Required fields:
- request_id, case_id;
- objective;
- research_questions[];
- hypotheses[];
- entities_of_interest[];
- time_window/geography when relevant;
- required_sufficiency: MINIMUM|GOOD|DESIRABLE;
- constraints;
- known_context/evidence refs;
- acceptance criteria;
- created_by, created_at, schema_version.

### SearchPlanProposal
Required fields:
- search_plan_id, request_id, case_id;
- information_gaps[];
- source_classes[];
- methods[] and KB refs;
- tools/capabilities[] when known;
- search sequence;
- expected coverage;
- verification approach;
- alternatives considered;
- limitations/risks;
- expected sufficiency;
- algorithm_version, knowledge_version.

### PlanDecision
ANALYST returns exactly one status:
- `ACCEPT`;
- `AMEND` plus requested changes;
- `REJECT` plus reason codes.

No silent mutation of the proposal is allowed. An amended plan receives a new version while retaining the same search_plan_id lineage.

### EvidencePackage
Required fields:
- package_id, request_id, search_plan_id, case_id;
- materials[];
- evidence[];
- leads[];
- source/search attempts including failures;
- provenance refs;
- corroboration and independence observations;
- contradictions[];
- unverified_items[];
- source/time/geographic coverage where applicable;
- requested_sufficiency and achieved_sufficiency;
- limitations[] and critical_gaps[];
- recommended_follow_up[];
- decision_record_refs[];
- created_at, schema_version.

### AnalyticalAssessment
Required fields:
- assessment_id, package_id, case_id;
- claims[] with evidence refs;
- hypotheses updated/retained/rejected;
- contradictions considered;
- uncertainty/limitations;
- sufficiency acceptance decision;
- DecisionRecord refs.

### ResearchGap
Required fields:
- gap_id, case_id, parent_request_id;
- question;
- why_needed;
- related_claims/hypotheses[];
- missing_evidence_type;
- current_sufficiency;
- required_sufficiency;
- priority;
- created_at.

## State machine

ResearchRequest: `DRAFT → ISSUED → PLANNING → PLAN_REVIEW → APPROVED → COLLECTING → EVIDENCE_DELIVERED → ANALYSIS → CLOSED|RESEARCH_MORE`.

Invalid transitions must fail explicitly and be logged.

## Evidence states

Information must not jump directly from raw collection to analytical fact.

`RAW_OBSERVATION → LEAD → MATERIAL → EVIDENCE_CANDIDATE → EVIDENCE_ACCEPTED|EVIDENCE_REJECTED`

State changes require actor role, timestamp, reason code, input refs, method/KB refs and DecisionRecord.

## Sufficiency semantics

- `MINIMUM`: enough to provide a bounded preliminary answer, with material gaps explicitly listed.
- `GOOD`: key claims have appropriate corroboration/coverage and major known contradictions have been investigated.
- `DESIRABLE`: broader source/time/alternative-hypothesis coverage has been pursued beyond the minimum required for a defensible answer.

These labels are policy categories, not numeric confidence. Any numeric score requires its own named, versioned calculation/assessment method and inputs.

## Failure protocol

OSINT_EXPERT must report failed/blocked sources and tool failures rather than silently omitting them. ANALYST must not interpret absence of collected material as evidence of absence unless the EvidencePackage explicitly supports that inference and records the search coverage needed for it.

## Knowledge gaps

If either role lacks a suitable KB rule/method, it records `knowledge_gap=true`, describes the gap, and must not disguise an improvised judgment as established methodology. Experimental methods must be labeled and their outputs receive corresponding limitations.

## Audit invariant

For every conclusion the system must be able to answer:
1. What evidence supports it?
2. Where did that evidence originate?
3. How was it collected and transformed?
4. Which role made each material decision?
5. Which algorithm/method and KB version governed that decision?
6. What uncertainty, contradiction and missing coverage was known at the time?
