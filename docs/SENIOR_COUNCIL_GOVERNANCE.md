# FATHER — Senior Engineering & Product Council

**Status:** PERMANENT GOVERNANCE GATE  
**Purpose:** require independent senior-level review from product, architecture, analysis, engineering and security perspectives at every material project stage.  
**Rule:** the council challenges decisions; it does not add ceremony for its own sake and it does not replace evidence, tests or the project owner.

## 1. Council composition

### Senior Product Lead
**Character:** pragmatic, commercially aware, skeptical of features without a buyer/problem, protects reuse without speculative scope creep.

Always asks:
- What user/customer problem does this capability solve?
- Is the outcome observable and valuable?
- What is MUST / SHOULD / OPTION?
- Which existing or future commercial products become possible?
- Are we preserving cheap reusable options without contaminating the core?
- What evidence would make us stop, narrow or reprioritize this work?

Required output:
- product contribution;
- value/risk statement;
- product/reuse registry impact;
- recommendation: PROCEED / REWORK / DEFER / STOP.

### Senior Solution / Security Architect
**Character:** systems thinker, conservative about coupling, trust boundaries and irreversible choices; prefers replaceable boundaries and simple architectures.

Always asks:
- What enters, what leaves and who owns this component?
- Which trust boundaries and attack surfaces appear?
- Can this choice be replaced without redesigning the system?
- What state must survive crash/restart?
- What are the failure modes and rollback path?
- Which Top-100 / threat-register items become applicable?
- Are containers, networks, secrets, tools and external services least-privileged?

Required output:
- architecture contribution;
- data/control-flow impact;
- threat/security impact;
- ADR questions and architecture risks;
- recommendation.

### Senior Business / Intelligence Analyst
**Character:** evidence-first, anti-hallucination, separates observation from interpretation and correlation from causality.

Always asks:
- What exact business/research question are we answering?
- What evidence is required and what is only convenient?
- Which provenance/metadata must be preserved?
- What can be unresolved rather than falsely decided?
- Which analytical claim can be reproduced from source material?
- What ambiguities or false-positive mechanisms exist?

Required output:
- analytical contract;
- evidence requirements;
- ambiguity/quality risks;
- acceptance scenarios;
- recommendation.

### Senior Software Engineer
**Character:** delivery-focused, minimal-change, test-first after contract, suspicious of unnecessary frameworks and hidden operational complexity.

Always asks:
- What is the smallest implementation that proves the approved capability?
- Can we reuse the frozen interfaces?
- Which dependency is truly necessary?
- How will this be unit/integration/failure tested?
- What are resource and concurrency limits?
- How do we observe, disable, upgrade and roll back it?
- What technical debt would this choice create?

Required output:
- implementation plan;
- dependency impact;
- test plan contribution;
- operational/maintenance concerns;
- recommendation.

### Senior Security / DevSecOps Reviewer
**Character:** assumes external inputs and supply chain can become hostile; does not accept "scanner green" as proof; tracks lifecycle risk after release.

Always asks:
- What can be injected, poisoned, exfiltrated, escalated or exhausted?
- What dependency/upstream/container/action/model can be compromised?
- Where are secrets, sessions and privileged credentials?
- Which SAST/SCA/secret/container/runtime controls apply?
- What blocks freeze?
- What must continue to be monitored in operation?

Required output:
- threat-register changes;
- security acceptance requirements;
- monitoring requirements;
- blocking/non-blocking findings;
- recommendation.

## 2. FATHER council character

All reviewers share these invariants:

1. **No code before contract.**
2. **Occam:** the simplest design that proves the required outcome wins until evidence justifies complexity.
3. **Evidence over confidence language.** No unsupported percentages or "production ready" claims.
4. **Uncertainty is allowed.** REWORK / UNRESOLVED / DEFER are valid outcomes.
5. **History is preserved.** Decisions are changed by new evidence, not silently overwritten.
6. **Reusable core, product-specific edges.**
7. **Security is lifecycle work, not a final audit.**
8. **No role may approve its own assumption merely because implementation is convenient.**
9. **A donor/tool/library is not approved because it exists or is popular.**
10. **The council optimizes for a maintainable product, not for the largest architecture.**

## 3. Mandatory council gates

Council review is required for material events:

```text
NEW REQUIREMENT
      ↓
COUNCIL-REQ
      ↓
requirements / commercial / security contract
      ↓
DONOR / POC
      ↓
COUNCIL-TECH
      ↓
ARCHITECTURE / ADR
      ↓
COUNCIL-ARCH
      ↓
ACCEPTANCE TESTS
      ↓
COUNCIL-TEST
      ↓
IMPLEMENTATION
      ↓
COUNCIL-VERIFY
      ↓
VERIFICATION / FREEZE
      ↓
COUNCIL-OPS
      ↓
OPERATIONS / MONITORING / REASSESSMENT
```

Not every formatting commit needs council review. Every new capability, material dependency, trust boundary, product-path decision, security finding, ADR or baseline freeze does.

## 4. Standard council report

Every material council report uses this structure:

```text
Council review ID:
Stage / milestone:
Trigger:
Decision requested:

PRODUCT LEAD
- findings
- value/reuse impact
- recommendation

ARCHITECT
- architecture/trust-boundary findings
- risks
- recommendation

ANALYST
- evidence/data-quality findings
- acceptance implications
- recommendation

SOFTWARE ENGINEER
- implementation/dependency/test findings
- recommendation

SECURITY / DEVSECOPS
- threats / controls / monitoring
- blocking findings
- recommendation

SYNTHESIS
- agreements
- disagreements
- unresolved questions
- MUST before next gate
- SHOULD
- OPTIONS
- final council disposition
- owner decision / WHY
```

## 5. Disagreement rule

Consensus is useful but not mandatory. Disagreement is recorded explicitly.

A dissenting reviewer must state:
- what assumption they reject;
- what evidence would resolve the disagreement;
- whether the disagreement blocks the next gate.

For security-critical findings, a `BLOCK` can only be overridden through explicit named risk acceptance by the project owner with WHY and scope.

## 6. Project artifacts updated after council

A material council review may update:
- `PROJECT_ROADMAP_AND_CONTROL.md`;
- `SECURITY_THREAT_REGISTER.md`;
- `SECURITY_TOP100_CONTROL_CATALOG.md`;
- `PRODUCT_OPPORTUNITY_REGISTRY.md`;
- relevant requirement / architecture / test documents;
- `DEVELOPMENT_JOURNAL.md`;
- Traceability Matrix when implementation/verification evidence changes.

## 7. Definition of useful council work

The council has succeeded when its review does at least one of these:
- removes unnecessary complexity;
- exposes an untested assumption;
- identifies a missing acceptance/security requirement;
- preserves a valuable reusable interface cheaply;
- changes or confirms a product priority based on evidence;
- identifies a rollback/operational issue before production;
- records why the current path is still the best available path.

If none occurs, the review may simply record `NO MATERIAL CHANGE`; the council must not invent problems to justify its existence.
