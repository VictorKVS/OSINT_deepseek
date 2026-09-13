# ADR-0002 — Preserve Source Observation Identity Separately from Raw Payload Reuse

Status: `ACCEPTED_RETROSPECTIVE`

Source decision: `ADR-CAND-011`, DEV semantic remediation and acceptance criteria.

## Context

The same bytes/text may appear at multiple source locators. Reusing one stored payload is useful, but deleting one of the observations would erase provenance about where/when the content was independently observed.

## Drivers

- provenance integrity;
- storage efficiency;
- auditability;
- source diversity analysis;
- future content propagation/reuse analysis.

## Options

### A — deduplicate complete Material observations by content hash

Storage/simple analysis is smaller, but independent source observations can disappear.

### B — store observation identity separately and reuse only raw payload object by hash

Preserves source observations while still avoiding duplicate payload storage.

## Decision

Select **B**.

A payload hash may reference one stored raw object. Multiple `Material` observations with distinct source locators remain separately traceable. `payloads_reused` reports storage reuse, not discarded observations.

## Consequences

Positive:
- no provenance loss from storage optimization;
- supports future propagation/source comparison;
- semantics are explicit.

Trade-offs:
- data model is slightly richer;
- observation count and raw-payload count are different metrics;
- downstream analytics must not confuse storage reuse with evidence independence.

## Verification

Acceptance evidence must include at least two distinct source observations containing equal content and demonstrate that both remain visible while one raw payload may be reused.

## Revisit triggers

Only a new evidence model with equivalent or stronger provenance guarantees may supersede this ADR.
