# ROLE MATRIX v1 — Analyst ↔ OSINT Expert

Status: ACCEPTED BASELINE

## Principle

At the current stage FATHER OSINT has exactly two substantive expert roles:

1. `ANALYST` — owns the research question, hypotheses, analytical claims and conclusions.
2. `OSINT_EXPERT` — owns search strategy, collection, curation, verification preparation, provenance and evidence delivery.

Collector, curator, verifier and tool planner are capabilities of OSINT_EXPERT, not independent roles yet.

No significant datum, score, status, claim or decision may appear without provenance and a DecisionRecord.

## Role matrix

| Area | ANALYST | OSINT_EXPERT |
|---|---|---|
| Primary question | What must be established and what follows from evidence? | How can sufficient evidence be found and prepared? |
| Owns | ResearchRequest, Hypothesis, Claim, Conclusion, ResearchGap | SearchPlan, Lead, Material, EvidencePackage, Coverage |
| Knowledge base | Analytical KB | Search Intelligence KB |
| Select source classes | may recommend | owns decision |
| Select methods/tools | no | yes |
| Collect RAW | no | yes |
| Preserve provenance | consumes | owns |
| Deduplicate/normalize | no | yes |
| Assess actual search coverage | reviews | owns |
| Build hypotheses/conclusions | owns | prohibited |
| Request more research | owns | may recommend |
| Explain significant decisions | mandatory | mandatory |

## ANALYST contract

### Purpose
Transform a human problem into explicit research requirements and transform delivered evidence into bounded analytical claims and conclusions.

### Required inputs
- user/task context;
- prior ResearchRequests and ResearchGaps when present;
- EvidencePackages returned by OSINT_EXPERT.

### Required knowledge references
Every non-trivial analytical decision must cite one or more applicable entries/methods from `Analytical KB`, or explicitly record `knowledge_gap=true`.

### Decision algorithm
1. Define objective.
2. Decompose into research questions.
3. Identify entities, events, geography and time window.
4. Record hypotheses as hypotheses, never facts.
5. Set required sufficiency: `MINIMUM`, `GOOD`, or `DESIRABLE`.
6. Define acceptance/answer criteria.
7. Issue ResearchRequest.
8. Review SearchPlanProposal: `ACCEPT`, `AMEND`, or `REJECT` with reasons.
9. Review returned EvidencePackage, contradictions, gaps and coverage.
10. Create/update Claims and Hypotheses with evidence references.
11. If insufficient, issue ResearchGap; otherwise produce bounded Conclusion.

### Prohibitions
ANALYST must not silently choose collection transport, rewrite raw provenance, promote a lead to evidence without OSINT evidence lineage, or invent confidence/weights without a declared assessment method.

## OSINT_EXPERT contract

### Purpose
Convert an approved information need into a reproducible search strategy and a provenance-preserving EvidencePackage suitable for analysis.

### Required inputs
- ResearchRequest or ResearchGap;
- scope/constraints;
- requested sufficiency.

### Required knowledge references
Every material search/tool/verification choice must cite applicable `Search Intelligence KB` entries, method/runbook identifiers, or record `knowledge_gap=true` and treat the method as experimental.

### Decision algorithm
1. Parse the information need.
2. Determine known facts versus missing information.
3. Identify candidate source classes.
4. Consult Search Intelligence KB for methods, tools, limitations and known failure modes.
5. Select strategy and alternatives.
6. Produce SearchPlanProposal with expected coverage and limitations.
7. Await approval where required.
8. Collect while preserving RAW and source lineage.
9. Normalize, deduplicate and classify as Lead/Material/Evidence candidate.
10. Record corroboration, independence, contradictions and failed sources.
11. Assess achieved coverage/sufficiency using declared rules.
12. Return EvidencePackage and recommended follow-up.

### Prohibitions
OSINT_EXPERT must not declare the research hypothesis true, create final analytical conclusions, hide contradictory material, destroy provenance, or invent reliability/confidence values without an explicit assessment record.

## Shared formal rule

All significant decisions create a `DecisionRecord` containing at minimum:

- decision_id, case_id, role_id;
- input_refs;
- knowledge_refs and method_refs;
- decision and reason_codes;
- alternatives considered where material;
- uncertainties and limitations;
- output_refs;
- algorithm_version;
- knowledge_version;
- policy_version when applicable;
- created_at.

The system must support backward lineage from Conclusion → Claim → Evidence → Material → RAW → Collection → SearchPlan → ResearchRequest and forward impact tracing from any source material to every claim/conclusion that used it.
