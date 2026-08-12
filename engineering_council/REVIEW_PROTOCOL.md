# Engineering Council — Adversarial Review Protocol

**Status:** CONTRACT  
**Applies to:** material council invocations defined by `docs/PROJECT_EXECUTION_CONTROL.md`  
**Goal:** prevent premature consensus and convert disagreement into testable evidence.

## 1. Inputs

A review starts only with a bounded decision question and the currently available evidence.

Minimum input:

```text
Decision ID
Requirement / problem
Scope / exclusions
Known evidence
Known constraints
Known risks
Decision deadline/gate if real
```

If the question is vague, the Systems/Business Analyst returns `REWORK` before architectural debate begins.

## 2. Round A — Independent positions

Before reading one another's recommendations, the following roles produce short independent positions where practical:

- Architect;
- Technical Lead;
- Systems/Business Analyst;
- Product Lead;
- Project/Delivery Lead;
- Principal Critic.

Each position MUST state:

```text
Recommendation
Evidence relied on
Assumptions
Unknowns
Strongest alternative
What would falsify this recommendation
Material risk introduced
Confidence: HIGH / MEDIUM / LOW, with reason
```

Confidence without an evidence reason is ignored.

## 3. Round B — Principal Critic attack

The Critic builds the strongest case against the leading proposal.

Attack checklist:

1. Does the proposal solve the approved requirement or a different problem?
2. Is there a simpler existing mechanism?
3. Which assumption has the weakest evidence?
4. Is test evidence fixture-only, mocked, stale or environment-specific?
5. What happens on restart, partial failure, timeout, rate limit and corrupted state?
6. What becomes hard to replace later?
7. What security/privacy/supply-chain boundary changes?
8. What operational burden is hidden?
9. What product/project pressure is biasing the choice?
10. What second-order effect hits later milestones?
11. What credible alternative dominates on simplicity, risk or reversibility?
12. Under what observable condition should we abandon the proposal?

The Critic must classify every material objection:

```text
BLOCKER
HIGH
MEDIUM
LOW
QUESTION
```

A `BLOCKER` must cite a hard constraint, failed gate, Critical/High unresolved risk, or missing evidence required by contract.

## 4. Round C — Defense and revision

The proposal owners answer each `BLOCKER` and `HIGH` point separately.

Allowed responses:

```text
AGREE_AND_FIX
DISAGREE_WITH_EVIDENCE
ACCEPT_RISK
RESEARCH_MORE
CHANGE_OPTION
```

`DISAGREE_WITH_EVIDENCE` must point to actual evidence, not authority or preference.

`ACCEPT_RISK` requires named owner, impact, revisit trigger and authorization when risk acceptance exceeds the role's mandate.

## 5. Round D — Alternative comparison

For a material ADR, compare at least:

```text
Option A — proposed path
Option B — strongest credible alternative
Option C — do nothing / defer / keep existing mechanism, when meaningful
```

Comparison dimensions are selected by the decision but usually include:

- requirement fit;
- implementation complexity;
- reversibility;
- operational burden;
- testability;
- security/privacy;
- supply-chain/maintenance health;
- performance only where required;
- migration cost;
- future coupling;
- reuse/product impact;
- evidence quality.

Do not invent numeric weights unless they are justified and calibrated. Qualitative comparison is preferable to fake precision.

## 6. Round E — Gate decision

The council result is one of:

```text
PASS
PASS_WITH_RISK
REWORK
RESEARCH_MORE
REJECT
NO_MATERIAL_CHANGE
```

A valid result includes:

```text
Decision
WHY
Evidence that carried the decision
Rejected alternatives and WHY
Residual risks
Required acceptance evidence
Rollback/replacement path
Revisit trigger
Recorded dissent
Next action
```

## 7. Burden of proof

The burden is asymmetric:

- a new dependency must prove why the existing mechanism is insufficient;
- a new trust boundary must prove its control model;
- a more complex architecture must prove material benefit;
- an irreversible choice must prove stronger evidence than a reversible one;
- a production claim must prove live/operational evidence, not only fixtures;
- a security exception must prove explicit risk acceptance;
- a product-driven core change must prove reusable core value rather than one-customer convenience.

## 8. Stop rules

Council debate stops when any is true:

1. acceptance evidence clearly selects an option;
2. the decision is reversible and further research costs more than the expected downside;
3. a hard blocker requires new evidence before debate can continue;
4. no material change exists;
5. repeated arguments contain no new evidence.

When debate stops for lack of evidence, result is `RESEARCH_MORE`, not forced consensus.

## 9. Critic quality standard

A high-class Critic is judged by whether it finds real failure modes and better alternatives early, not by how many objections it raises.

Bad criticism:
- vague negativity;
- impossible perfection standards;
- repeating already answered points;
- inventing risks with no plausible mechanism;
- blocking reversible experiments that cheaply produce evidence;
- criticizing without offering a test, alternative or decision criterion.

Good criticism:
- identifies a hidden assumption;
- proposes a simpler path;
- shows how the current test can produce a false PASS;
- names a concrete failure/recovery scenario;
- reveals irreversible coupling;
- distinguishes current evidence from inference;
- defines the experiment that resolves disagreement.

## 10. First application — M5 Telegram Radar

Current decision question:

> What is the smallest replaceable Telegram transport path that can reliably produce canonical FATHER `Material` records while preserving provenance and operational safety?

Council must explicitly compare:
- continue TDLib primary investigation;
- adopt Telethon as verified fallback/reference and continue integration;
- run another candidate PoC only if it can change the decision;
- defer transport finality and proceed behind a protocol boundary where reversibility is preserved.

Principal Critic must challenge:
- whether TDLib debugging still lies on the critical path;
- whether live Telethon evidence is sufficient for a bounded fallback but insufficient for production approval;
- whether another donor PoC adds information rather than schedule cost;
- whether the next highest-value proof is Telegram → Material rather than transport refinement.
