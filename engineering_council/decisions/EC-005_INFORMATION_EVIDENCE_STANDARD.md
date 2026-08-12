# EC-005 — Adopt Information & Evidence Standard

**Date:** 2026-08-12  
**Result:** PASS_WITH_RISK  
**Applies to:** all expert-system evidence paths, beginning with M5 Telegram Radar.

## Decision

Adopt `docs/architecture/INFORMATION_EVIDENCE_STANDARD.md` as a foundational standard.

FATHER must not treat information as an opaque text blob. Source identity, temporal context, provenance, propagation, quality dimensions, coverage/sufficiency, contradictions and evidence-to-claim traceability become first-class architecture concerns.

## WHY

The system is being built as an expert system. Analyst quality is bounded by the quality and interpretability of what OSINT delivers. A strong Analyst cannot repair missing provenance, unknown source independence, collapsed timestamps or unmeasured search coverage after collection.

Therefore evidence semantics must be designed before expert reasoning grows more sophisticated.

## Principal Critic review

### Risk 1 — Metadata explosion
Attempting to require every possible field for every source will make adapters unusable.

**Constraint:** distinguish `required core`, `required when applicable`, and `optional enrichment` in implementation contracts. Missing unavailable metadata must be explicit, not invented.

### Risk 2 — False precision
Numeric reliability/confidence values without calibration can create pseudo-scientific certainty.

**Constraint:** preserve dimensions separately; no aggregate probability-of-truth score without calibration evidence.

### Risk 3 — Propagation graph overengineering
Full cross-platform diffusion mapping could become a separate product and block M5.

**Constraint:** Telegram M5 records only low-cost propagation metadata available from the source and enough structure to support future mapping. Cross-platform propagation is deferred.

### Risk 4 — Analyst/OSINT boundary blur
If OSINT starts drawing substantive conclusions, evidence acquisition and interpretation become conflated.

**Constraint:** OSINT may assess source/evidence quality, search coverage and acquisition sufficiency. Substantive domain conclusions remain Analyst responsibility.

### Risk 5 — Standard becomes documentation-only
A standard with no acceptance tests provides little value.

**Constraint:** G5–G10 must translate relevant parts into executable contracts/tests and live Telegram evidence.

## Required implementation order

Do not redesign all existing models at once. Apply the standard incrementally through Telegram M5:

1. SearchPlan / scope / requested evidence questions.
2. Reconnaissance and source coverage accounting.
3. EvidenceAssessment dimensions.
4. Sufficiency levels and critical gaps.
5. Counter-evidence branch.
6. AcquisitionReport for Analyst.
7. Low-cost temporal/propagation metadata extensions where supported by Telegram.
8. Final Council review of M5 against this standard.

## Revisit triggers

Revisit if:
- a source class cannot be represented without destructive loss;
- required metadata materially harms bounded collection;
- evidence-quality dimensions prove ambiguous in live use;
- Analyst cannot determine what a material supports from the delivered package;
- a later source requires new source-neutral dimensions.
