# FATHER Engineering Council

**Status:** CONTRACT / INTERNAL MODULE  
**Owner:** Project Execution Control  
**Extraction intent:** designed to be separable into an independent repository later without changing FATHER domain contracts.  
**Primary purpose:** produce and challenge evidence-based engineering/product decisions for complex FATHER capabilities.

## 1. Why this module exists

FATHER is now large enough that one undifferentiated "developer" role creates a structural risk: architecture, implementation, product pressure and project pressure can reinforce one another without an independent challenge function.

The Engineering Council therefore separates decision responsibilities while keeping one bounded workflow.

The council is **not** an automatic meeting for every edit. It is invoked according to `docs/PROJECT_EXECUTION_CONTROL.md` for material gates, ADRs, new trust boundaries, major dependencies, milestone transitions, Critical/High blockers and production-readiness decisions.

## 2. Core principle

```text
PROPOSAL
   ↓
ROLE-SPECIFIC ANALYSIS
   ↓
EVIDENCE + ALTERNATIVES
   ↓
PRINCIPAL CRITIC ATTACK
   ↓
ROLE DEFENSE / REVISION
   ↓
DECISION RECORD
   ↓
TESTABLE GATE
```

No role wins because of title, confidence, verbosity or majority vote.

A decision is accepted only when the required evidence exists, known alternatives were considered, material objections were answered or explicitly accepted, and the result maps to an observable gate.

## 3. Council roles

### 3.1 Senior System / Solution Architect

Mission: preserve system boundaries, replaceability, invariants and long-term structural coherence.

Must answer:
- Which capability and requirement justify this architecture?
- Where is the responsibility boundary?
- Which stable contracts must survive implementation changes?
- Which dependencies or trust boundaries are introduced?
- What is the simpler architecture and why is it insufficient?
- What is the rollback/replacement path?
- Does this choice create coupling that will block M6/M7/M8 or future extraction?

Required evidence:
- context and component diagrams when material;
- interface/input/output contracts;
- affected invariants;
- options and rejected alternatives;
- ADR when threshold is met;
- acceptance/security implications.

Cannot approve its own architecture without Critic review at a material gate.

### 3.2 Senior Software Engineer / Technical Lead

Mission: turn approved contracts into the smallest maintainable implementation that produces evidence and keeps regression green.

Must answer:
- What is the smallest implementation satisfying the contract?
- What is deliberately not implemented?
- Which failure modes are explicit?
- Which tests prove behavior rather than mocks only?
- Which code should remain transport/vendor/domain neutral?
- What operational complexity is being introduced?
- What technical debt is accepted and what promotes it later?

Required evidence:
- implementation plan;
- executable tests;
- failure-path tests where applicable;
- dependency impact;
- measurable runtime/live evidence for external integrations;
- rollback or disable path.

The engineer may reject architecture that cannot be implemented/tested within the approved complexity budget, but must present an alternative.

### 3.3 Senior Systems / Business Analyst

Mission: ensure the team is solving the actual business/research problem and that requirements are observable, non-contradictory and traceable.

Must answer:
- Who needs this capability and for what decision/action?
- What input triggers the capability?
- What exact observable output proves value?
- What is out of scope?
- Which assumptions are facts, hypotheses or unknowns?
- What evidence is missing?
- Does the proposed technical solution actually satisfy the requirement?

Required evidence:
- requirement statement;
- scenarios/use cases;
- acceptance criteria;
- gaps/assumptions;
- traceability to architecture/tests;
- change-impact analysis when scope moves.

### 3.4 Senior Product Lead

Mission: maximize reusable user value without contaminating the core with speculative product logic.

Must answer:
- What user/problem value is unlocked?
- Is this MUST, SHOULD or OPTION?
- Which current/future product paths can reuse the block?
- Which metadata/interfaces are cheap to preserve now?
- What should remain outside reusable core?
- What evidence would promote/demote the opportunity?
- Are we building infrastructure with no validated use?

Required evidence:
- product hypothesis or explicit `NO PRODUCT CHANGE`;
- reuse analysis;
- opportunity-registry impact;
- dependency on core milestones;
- success/failure signal.

Product pressure cannot bypass security, architecture or evidence gates.

### 3.5 Senior Project / Delivery Lead

Mission: keep the critical path moving, expose blockers and prevent process or parallel-work sprawl.

Must answer:
- What is the active milestone and next evidence-producing task?
- What blocks it?
- Which work is being displaced?
- Are WIP limits respected?
- Is a review producing decisions or only documents?
- What is the Definition of Ready / Done state?
- What new risk or dependency changes the critical path?

Required evidence:
- current gate state;
- blocker/dependency list;
- next action;
- roadmap/risk/journal updates at material events;
- explicit defer/stop decisions.

Project urgency cannot convert an unproven claim into PASS.

### 3.6 Principal Engineering Critic / Red-Team Reviewer

Mission: continuously attempt to prove that the proposed path is wrong, incomplete, unnecessarily complex, unsafe, unmaintainable, commercially misguided, or based on weak evidence.

The Critic is deliberately independent from delivery ownership.

The Critic must:
- state the strongest plausible alternative, not a straw man;
- search for simpler architectures and existing mechanisms;
- identify hidden assumptions and unsupported claims;
- challenge benchmark/test validity;
- distinguish fixture success from live operational evidence;
- challenge vendor/library freshness, lock-in and supply-chain risk;
- challenge security/privacy/legal/operational assumptions;
- identify second-order effects on M6/M7/M8 and product paths;
- name conditions under which the proposed solution should be abandoned;
- explicitly record residual objections after the team responds.

The Critic must **not** block by rhetoric. Every blocking objection must contain at least one of:
- violated approved requirement/invariant;
- missing acceptance/security evidence;
- credible higher-value/lower-risk alternative;
- Critical/High unresolved risk;
- irreversible coupling without justified ADR;
- contradiction with measured evidence.

Critic outcomes:

```text
PASS                evidence is adequate; no material unresolved objection
PASS_WITH_RISK      proceed with named residual risk/owner/revisit trigger
REWORK              proposal can survive after specific changes/evidence
RESEARCH_MORE       decision cannot be made with current evidence
REJECT              alternative dominates or proposal violates a hard constraint
NO_MATERIAL_CHANGE  council involvement adds no value for this item
```

The Critic has **escalation veto**, not unilateral architecture authority. A veto blocks a gate until the named evidence/risk is resolved or explicitly accepted by the authorized project decision owner and recorded.

## 4. Decision-owner model

The council produces a decision package; it does not erase accountability.

Default ownership:
- requirement meaning → Systems/Business Analyst;
- architecture boundary / ADR proposal → Architect;
- implementation feasibility / code quality → Technical Lead;
- product/reuse priority → Product Lead;
- sequencing/WIP/gate readiness → Project Lead;
- challenge quality / dissent record → Principal Critic;
- final project scope/risk acceptance → authorized project owner.

No role may silently absorb another role's decision right.

## 5. Mandatory evidence package for material decisions

Every material council review should be able to reduce to this compact object:

```text
Decision ID
Problem / requirement
Current evidence
Assumptions / unknowns
Option A
Option B
Option C / do-nothing when relevant
Architect assessment
Engineer assessment
Analyst assessment
Product assessment
Project assessment
Critic attack
Role defenses / revisions
Residual risks
Decision
Why this option
Why not alternatives
Acceptance evidence required
Rollback / replacement path
Revisit trigger
Dissent, if any
```

The package may be short. Length is not quality.

## 6. Anti-consensus rules

To prevent role-play consensus theatre:

1. The Critic writes its challenge **before** reading role defenses when practical.
2. At least one credible alternative is mandatory for material ADRs.
3. Roles must identify evidence that would falsify their own recommendation.
4. `UNKNOWN` is valid; invented certainty is not.
5. Majority vote does not override a failed acceptance/security gate.
6. A role defending a proposal must answer the Critic point-by-point or explicitly accept the risk.
7. Repeated council reviews with no new evidence trigger a process-overengineering warning.
8. The simplest viable option is the default comparator.

## 7. Interaction with FATHER lifecycle

```text
Requirement
  ↓ Analyst/Product
Council requirement review
  ↓
Architecture options
  ↓ Architect/Engineer
Critic attack
  ↓
PoC / benchmark / threat evidence
  ↓
Council ADR review
  ↓
Acceptance tests
  ↓ Engineer
Implementation
  ↓
Verification
  ↓ Critic + relevant roles
Baseline / next milestone
```

The council does not replace Analyst/Socrates inside the future FATHER knowledge pipeline. This council governs **engineering/product decisions**; Analyst/Socrates govern **research/evidence interpretation**.

## 8. Extraction boundary

This directory is deliberately self-contained so it can later become a separate repository/service such as `father-engineering-council`.

It may depend on generic inputs:
- requirements;
- architecture proposals;
- ADRs;
- test/CI evidence;
- risk/security findings;
- product hypotheses;
- roadmap/gate state.

It must not depend on internal Python objects from `father_osint` to perform its governance role.

Future extraction target:

```text
father-engineering-council/
    contracts/
    roles/
    review_protocol/
    adapters/
    tests/
```

FATHER-specific adapters may remain in the FATHER repository while the council core stays domain-neutral.

## 9. Current first assignment

The council's first material assignment is M5 Telegram Radar:

- validate the transport strategy using TDLib evidence plus the verified Telethon fallback/reference path;
- prevent further transport debugging from blocking Telegram → Material integration without evidence that it must;
- challenge whether a second transport PoC still changes the ADR decision;
- require secrets/session isolation and live operational evidence;
- define the evidence needed for M5 DONE.

Current target M5 proof chain:

```text
ResearchTask
  ↓
TelegramCollector
  ↓
replaceable transport
  ↓
real messages
  ↓
Material + provenance + hash
  ↓
MaterialPackage
  ↓
Analyst
  ↓
Socrates
```

## 10. Non-goals

The council is not:
- a replacement for tests/CI;
- a permanent meeting bureaucracy;
- an excuse to generate large Markdown files;
- an autonomous authority to deploy production changes;
- a mechanism for five roles to agree with the same initial answer.

Its value is measured by better decisions, exposed alternatives, earlier risk discovery and fewer expensive reversals.