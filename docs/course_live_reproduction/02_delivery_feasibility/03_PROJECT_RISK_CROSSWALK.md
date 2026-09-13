# Lesson 02 — Project Risk Crosswalk

Status: `CROSS-LINK MODEL / DO NOT COLLAPSE RISK TYPES`

The project already has project/delivery and security threat views. This document links them without pretending they are the same thing.

## Crosswalk

| Delivery/project risk | Related security/technical risk | Delivery impact | Treatment/evidence |
|---|---|---|---|
| technology-first transport choice | stale/compromised upstream, session/rate failures | rework, delay, wrong dependency | PoC → donor review → ADR |
| live behavior differs from fixtures | tests prove mocks but not operation | false readiness | bounded real-source PoC + restart/failure tests |
| provenance semantics regress | checkpoint/data/provenance loss | unusable investigation evidence | invariants + regression + durable save/reconciliation |
| external AI service becomes mandatory | sensitive-data/provider/model supply-chain threats | privacy block, cost/vendor dependence | provider abstraction + data classification + local path |
| scope grows across source/media/product options | attack surface + unbounded collection | schedule/cost/security growth | MUST/SHOULD/OPTION + CR/change gate |
| user/customer data arrives before governance | privacy/legal/secret risks | production gate blocked | data inventory/legal applicability before expansion |
| many agents/tools are added for novelty | excessive agency/prompt/tool threats | complexity/rework/cost | prove use-case value, bounded tools, security gate |
| architecture docs diverge from code | controls/tests no longer prove stated design | rework/false assurance | traceability + verification/freeze review |

## Risk rule

Project risk answers: **what uncertain event can derail delivery/value?**

Security threat answers: **what adversarial/failure condition can harm confidentiality/integrity/availability/authority?**

They may reference each other, but owners/scoring/closure evidence can differ.

## Quantitative scoring

Probability/impact numbers are estimates unless calibrated from evidence. No numeric score is promoted to FACT solely because a spreadsheet formula produced it.

## Risk-to-estimate relationship

A risk affects Estimate v0 only when:
- the risk is in-scope;
- treatment requires work/cost/time;
- owner agrees on treatment;
- estimate impact is explicit.

A risk allocated by contract is not erased; it moves to contractual assumption/dependency and retains a trigger.
