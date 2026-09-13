# ADR-0001 — OSINT Worker Is an Evidence Supplier, Not Final Truth Authority

Status: `ACCEPTED_RETROSPECTIVE`

Source decision: existing project mission + `ADR-CAND-001`.

## Context

The Knowledge Factory needs source material for analysis. A collection component that also decides truth would combine acquisition, interpretation and approval, making provenance, challenge and accountability weaker.

## Drivers

- preserve role separation;
- source-neutral Analyst handoff;
- visible gaps/uncertainty;
- independent review before knowledge promotion;
- support multiple future analysis methods without rewriting collectors.

## Options considered

### A — OSINT returns final conclusion

Simpler surface, but collection and analytical authority collapse into one component. Harder to challenge and trace.

### B — OSINT returns provenance-rich `MaterialPackage`

Collection remains bounded and source-focused; Analyst/Reviewer remain separate.

## Decision

Select **B**. OSINT returns evidence observations/packages and visible collection errors/gaps. Final analytical conclusions and governed knowledge promotion remain downstream responsibilities.

## Consequences

Positive:
- clearer responsibility boundary;
- provenance survives downstream model changes;
- independent review is possible;
- acquisition tests remain deterministic.

Trade-offs:
- more handoff contracts;
- downstream Analyst/Reviewer components are required;
- user-facing result cannot come directly from collector without analysis layer.

## Verification

- `OSINT_AGENT_TZ_V1.md` output contract;
- `OSINTAgent` returns `MaterialPackage`;
- traceability/acceptance tests verify Analyst handoff;
- no collector API is treated as Knowledge Gate.

## Revisit triggers

Revisit only if product scope changes so radically that acquisition and interpretation become one intentionally accountable component; such change requires new architecture/security review and superseding ADR.
