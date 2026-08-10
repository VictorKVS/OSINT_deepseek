# 2026-08-10 — Lean Execution Control Approved

**Stage:** 07 / M5 Telegram Radar  
**Result:** APPROVED / ACTIVE

## Trigger

Project review identified a new mirror risk: after reducing architecture overengineering, governance itself could become overengineered and delay executable evidence.

## Decision

Approve a lean execution-control model and stop inventing new process layers unless a concrete uncovered failure mode requires them.

## Approved controls

1. Seven living project-control objects: Roadmap, Master Control Register/Backlog, Requirements, ADR, Risk/Security Registers, Product Opportunity Registry, Development Journal.
2. Material work-item classification: `REQ / DEFECT / RISK / SEC / DEBT / ADR / POC / OPP`.
3. Definition of Ready before product-path code.
4. Definition of Done before a material item is closed/frozen.
5. Default WIP limit: one active core milestone + one attached security stream + one attached research/PoC stream.
6. Full Senior Council only at material gates; routine edits use normal engineering review.
7. Compact Change Impact Analysis before material changes.
8. ADR only for costly/risky-to-reverse decisions.
9. Technical debt kept separate from defects, risks, features and opportunities.
10. Documentation hierarchy L1 living controls → L2 contracts/decisions → L3 evidence → L4 journal.
11. `Process overengineering` becomes an explicit monitored project risk.

## Current WIP

```text
CORE:      M5 Telegram Radar
SECURITY:  M5 session / transport / supply-chain controls
RESEARCH:  TDLib PoC
```

M6, M7, M8 and product MVPs remain queued.

## WHY

Governance is useful only when it improves decisions and prevents expensive mistakes. The project now has enough governance machinery; the next priority must be operational evidence. The approved model keeps traceability/security/product discipline while preventing review ceremony and Markdown growth from replacing delivery.

## Files

- `docs/PROJECT_EXECUTION_CONTROL.md`
- `docs/MASTER_CONTROL_REGISTER.md`
- `docs/PROJECT_GOVERNANCE.md`
- `README.md`

## Next action

No further governance design before the current evidence task unless a real blocker proves a gap.

```text
TDLib PoC
→ raw results
→ Senior Council review
→ GramJS comparison only if justified
→ Transport ADR
→ M5 acceptance/security tests
→ implementation
```

**Next gate:** TDLib PoC evidence review.