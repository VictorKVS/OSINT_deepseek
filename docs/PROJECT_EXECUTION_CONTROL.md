# FATHER — Project Execution Control

**Status:** APPROVED / ACTIVE  
**Purpose:** keep FATHER professionally governed without turning governance into a second product.  
**Primary rule:** one active core milestone, evidence before claims, and the smallest control set that materially reduces delivery/security risk.

## 1. Seven living control objects

The project is governed through seven primary living objects. New permanent control documents require an explicit reason why these seven are insufficient.

1. **ROADMAP** — where the project is going and which capability is active next.
2. **BACKLOG / MASTER CONTROL REGISTER** — what must be done next and its traceability.
3. **REQUIREMENTS** — why a capability exists and what observable outcome is required.
4. **ADR** — why a material technical/architectural choice was made and how to revisit it.
5. **THREAT / RISK REGISTERS** — what can fail, be attacked, become unsafe or derail delivery.
6. **PRODUCT OPPORTUNITY REGISTRY** — which reusable blocks unlock lawful product/commercial paths.
7. **DEVELOPMENT JOURNAL** — what actually happened, what changed and WHY.

Supporting documents (PoC reports, benchmarks, test evidence, threat models, council reports) are evidence attached to these controls, not additional competing governance systems.

## 2. Master Control Register model

Every material work item gets a stable ID and a type. Types MUST NOT be conflated:

- `REQ` — requirement/capability;
- `DEFECT` — behavior violates an approved contract;
- `RISK` — uncertain event/exposure that may cause harm;
- `SEC` — security finding/control;
- `DEBT` — known maintainability/design compromise that does not currently violate the contract;
- `ADR` — material decision;
- `POC` — bounded evidence-producing experiment;
- `OPP` — product/commercial opportunity.

Traceability pattern:

```text
REQ-M5-001
   ↓
RISK / SEC findings
   ↓
POC / ADR
   ↓
Acceptance Criteria
   ↓
Implementation
   ↓
Tests / Security evidence
   ↓
Baseline / Operation
```

### Required work-item fields

```text
ID
Type
Title
Capability / business outcome
Owner / decision role
State
Depends on
Blocks / blocked by
Affected components
Affected requirements / products
Security / risk links
Acceptance evidence required
Next action
WHY
```

## 3. Definition of Ready

A material implementation task is `READY` only when all applicable items are true:

- [ ] business/capability outcome is explicit;
- [ ] owner is known;
- [ ] scope and exclusions are explicit;
- [ ] inputs/outputs and responsibility boundary are understood;
- [ ] commercial/reuse review completed ("no change" is valid);
- [ ] security/threat/supply-chain review completed for new attack surfaces;
- [ ] architecture owner/boundary is known;
- [ ] acceptance criteria are observable and testable;
- [ ] blocking disagreement/risk is resolved, removed, or explicitly accepted;
- [ ] simpler existing mechanism was considered;
- [ ] rollback/disable path is understood where failure can affect a baseline or external system.

No READY → no product-path code.

## 4. Definition of Done

A material work item is `DONE` only when all applicable evidence exists:

- [ ] implementation matches approved contract;
- [ ] acceptance tests pass;
- [ ] relevant regression remains green;
- [ ] security checks/threat controls required for this surface are evidenced;
- [ ] dependency/supply-chain inventory is updated if changed;
- [ ] affected documentation/traceability is updated;
- [ ] risk/security registers reflect the new state;
- [ ] product opportunity registry has been rechecked;
- [ ] operational/rollback implications are recorded;
- [ ] journal contains the outcome and WHY;
- [ ] no in-scope unresolved Critical blocker remains without named acceptance.

`Code merged` is not Definition of Done.

## 5. WIP limit

Until measured delivery capacity justifies change, FATHER operates with this default WIP limit:

```text
1 ACTIVE core milestone
1 ACTIVE security workstream attached to that milestone
1 ACTIVE research/PoC stream attached to that milestone
```

Current approved WIP:

```text
CORE:      M5 Telegram Radar
SECURITY:  M5 session / transport / supply-chain controls
RESEARCH:  TDLib PoC
```

M6, M7, M8 and product MVPs remain QUEUED/OPPORTUNITY unless an explicit gate promotes them.

Urgent defects/security incidents may interrupt WIP; the interruption and displaced item are recorded.

## 6. Senior Council invocation rule

The Senior Council is mandatory for material gates, not routine edits.

**Invoke the full council for:**
- new milestone/capability;
- material requirements change;
- major ADR or donor/technology selection;
- new trust boundary or sensitive data class;
- new external dependency with material runtime/supply-chain impact;
- new product path that changes core interfaces;
- unresolved Critical/High architecture/security blocker;
- baseline freeze / production-readiness gate;
- material incident or post-incident redesign.

**Do not invoke the full council for:** formatting, typo fixes, refactors with unchanged observable contract, routine dependency PR triage, or small test additions unless they reveal a material issue.

A council member may return `NO MATERIAL CHANGE`. Dissent must be recorded when it affects a gate.

## 7. Change Impact Analysis

Before every material change, answer compactly:

```text
What changes?
Which approved requirement requires it?
Which modules/interfaces/data contracts are affected?
Which tests must change or remain green?
Which threat surfaces/trust boundaries change?
Which dependencies/supply-chain items change?
Which product opportunities become easier/harder?
Which roles/operational procedures are affected?
Can we roll back or disable it safely?
Does this create new TECH DEBT?
```

The result may be short. It exists to prevent hidden blast radius, not to create paperwork.

## 8. ADR threshold

Create/update an ADR only for a decision that is costly or risky to reverse, affects multiple components/products, introduces an external dependency/trust boundary, or would otherwise be repeatedly debated.

ADR minimum:

```text
Context
Options
Evidence / PoC
Security + operations + supply-chain impact
Decision
WHY
Rejected alternatives
Rollback / replacement path
Revisit triggers
```

Do not create ADRs for trivial implementation details.

## 9. Technical debt register rule

Technical debt is not a defect and not a future feature.

A `DEBT-*` item records:
- current compromise;
- why it is acceptable now;
- consequence if left indefinitely;
- trigger that promotes it into active work;
- affected tests/components;
- simplest repayment path.

Debt is reviewed at milestone freeze and when a change touches the affected area. It is not automatically scheduled merely because it exists.

## 10. Documentation hierarchy

To avoid Markdown sprawl:

```text
L1 — Living controls
README / ROADMAP / EXECUTION CONTROL / GOVERNANCE
RISK + SECURITY REGISTERS / PRODUCT REGISTRY / JOURNAL

L2 — Contracts and decisions
Requirements / ADR / threat models

L3 — Evidence
PoC / benchmark / verification / test reports / council reports

L4 — Journal entries
short event history linking to L1–L3
```

A new document must identify its level and owner. Prefer updating an existing living control over creating a new permanent file.

## 11. Governance complexity risk

`Process overengineering` is a first-class project risk.

Early warnings:
- more governance artifacts than evidence-producing work;
- repeated reviews that do not change a decision;
- full-council review of routine edits;
- multiple registers tracking the same fact independently;
- milestone progress measured by documents rather than executable evidence.

Treatment:
- seven-object control model;
- WIP limit;
- council threshold;
- evidence-first gate completion;
- `NO MATERIAL CHANGE` as a valid review result;
- periodically delete/merge obsolete governance artifacts after traceability is preserved.

## 12. Immediate approved execution path

No new governance mechanism is needed before M5 produces real evidence.

```text
TDLib PoC
   ↓
raw operational/security results
   ↓
Senior Council review
   ↓
GramJS comparison only if it still adds decision value
   ↓
Transport ADR
   ↓
M5 acceptance tests
   ↓
minimal implementation
   ↓
security + regression verification
   ↓
M5 baseline
```

This execution path is APPROVED. New process ideas go to backlog unless they address a concrete uncovered failure mode.