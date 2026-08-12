# EC-002 — M5 reliability before LLM-backed Analyst

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Council result:** PASS_WITH_RISK  
**Decision:** close operational ingestion reliability gates before introducing an LLM-backed Analyst on the M5 critical path.

## Question

The live path Telegram → Material → MaterialPackage → DeterministicEvidenceAnalyst → DeterministicSocrates has passed. Should the project now add an LLM-backed Analyst, or first complete checkpoint/restart/rate-limit/failure-isolation behavior?

## Evidence available

Measured live evidence now proves:

- Telegram acquisition through the Telethon reference adapter;
- canonical `Material` mapping;
- SHA-256 content-addressed raw storage;
- preservation of repeated observations/provenance;
- `MaterialPackage` creation;
- deterministic evidence claims that cite package-owned `material_id` values;
- deterministic Socrates package-consistency review returning PASS.

Not yet measured live:

- save-before-checkpoint ordering;
- restart/reconciliation behavior;
- duplicate replay after interruption;
- FloodWait/rate-limit behavior;
- per-channel failure isolation;
- bounded retry/backoff behavior.

## Senior System / Solution Architect

**Recommendation:** reliability first.

The reasoning boundary is now stable enough to accept a future LLM implementation without requiring source-specific changes. The larger architectural risk is losing or skipping evidence due to incorrect checkpoint semantics. An intelligent analyst cannot compensate for evidence that was never durably recorded.

The ingestion invariant should be:

```text
receive source observation
        ↓
map to canonical Material
        ↓
persist raw payload + provenance
        ↓
confirm durable save
        ↓
advance source checkpoint
```

Checkpoint advancement before durable save is forbidden.

## Senior Software Engineer / Technical Lead

**Recommendation:** implement deterministic reliability contracts before any LLM dependency.

Required engineering sequence:

1. introduce an explicit checkpoint abstraction independent of Telethon;
2. test save-before-checkpoint ordering with fakes;
3. test restart from last committed checkpoint;
4. test replay/reconciliation without content loss;
5. classify Telegram rate-limit errors and implement bounded retry/backoff policy;
6. isolate one channel failure from other configured channels;
7. run a live acceptance that records checkpoint evidence.

Only after these tests are green should the LLM adapter be introduced behind the already-existing `Analyst` protocol.

## Senior Systems / Business Analyst

**Recommendation:** reliability first.

The user-visible requirement is trustworthy evidence acquisition. Current reasoning PASS is structural rather than semantic. The next unmet functional risks concern completeness and repeatability of collection.

Acceptance requirements should be transport-independent where possible:

- no committed checkpoint without durable observation;
- restart does not skip uncommitted evidence;
- replay may create a new observation but may reuse identical raw payload bytes;
- one source failure is explicit and does not silently terminate unrelated sources;
- rate-limit conditions are surfaced and bounded rather than retried forever.

## Senior Product Lead

**Recommendation:** reliability first, then LLM.

Adding an LLM now would produce more impressive outputs but would not increase trust in the evidence supply chain. The next durable product value is reliable autonomous collection. Once that exists, LLM analysis can be improved independently behind the reasoning contract.

## Senior Project / Delivery Lead

**Recommendation:** keep the critical path narrow.

Current next milestone:

```text
Checkpoint contract
  → save-before-checkpoint tests
  → restart/reconciliation tests
  → FloodWait/backoff contract
  → per-source failure isolation
  → live reliability acceptance
```

LLM integration is a separate following milestone and must not run in parallel unless it has a strict non-blocking experiment budget.

## Principal Engineering Critic / Red-Team attack

### Attack 1 — This may postpone the first useful AI output too long

True. Reliability work can become endless infrastructure work.

**Constraint accepted:** only the four named reliability gates are blocking. Do not expand M5 into a general distributed-systems framework.

### Attack 2 — A local append-only DEV store is not a production database

True. Passing checkpoint semantics against the DEV store does not prove transactional guarantees for a future production datastore.

**Residual risk accepted:** define ordering and reconciliation contracts now; future storage backends must satisfy the same contract tests.

### Attack 3 — Telethon-specific FloodWait handling could leak into canonical architecture

**Constraint accepted:** canonical layer should model a bounded retryable-source condition, while Telethon exception types remain inside the adapter.

### Attack 4 — Replaying observations may inflate the evidence graph

True. Current architecture intentionally preserves observation history while deduplicating raw payload bytes. Future graph/query layers will need semantic grouping by stable source/message identity.

**Residual risk accepted:** do not collapse provenance at ingestion time merely to simplify downstream queries.

### Attack 5 — LLM reasoning could expose hidden contract gaps earlier

Possible, but current evidence-contract already provides a stable adapter point. LLM exploration may proceed later as a bounded experiment; it does not justify putting stochastic behavior onto the M5 acceptance path before ingestion reliability is known.

## Critic outcome

`PASS_WITH_RISK`

The decision is accepted only with a scope guard: complete exactly the named reliability gates, then proceed to LLM-backed reasoning. Do not invent broader reliability infrastructure unless a failing acceptance test requires it.

## Decision

**Reliability before LLM on the M5 critical path.**

The deterministic Analyst/Socrates layer is frozen as the current reasoning reference contract. The next implementation milestone is checkpoint/restart/rate-limit/failure-isolation reliability.

## M5 next acceptance gates

- checkpoint is advanced only after durable material save;
- restart resumes without skipping uncommitted evidence;
- replay preserves provenance and reuses identical raw payloads;
- retry behavior is bounded;
- Telegram FloodWait/rate-limit is translated to an explicit adapter outcome/policy;
- failure in one configured channel does not silently discard results from others;
- live acceptance proves checkpoint progression and restart behavior;
- CI remains green.

## Revisit trigger

After the above gates are measured PASS, open a new Council decision for selecting and evaluating an LLM-backed `Analyst` implementation, including hallucination, citation fidelity, calibration, privacy, latency and cost criteria.
