# EC-001 — M5 Telegram transport strategy

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Council result:** PASS_WITH_RISK  
**Decision owner:** Project owner  
**Revisit trigger:** new measured evidence showing TDLib/another transport is required for an M5 acceptance criterion that Telethon cannot satisfy.

## Problem

Should M5 continue to spend its critical path on TDLib/GramJS transport PoCs, or freeze a transport-neutral boundary and proceed with the already live-proven Telethon path to canonical FATHER `Material` integration?

## Current evidence

Measured evidence recorded in J-018:

- direct Telegram TCP/HTTPS connectivity failed before VPN;
- Telegram reachability passed through AmneziaVPN;
- the recovered authorized Telethon session successfully acquired public-channel data;
- a 100-object request scale was demonstrated across configured channels;
- 356 text-bearing messages were processed in the observed run;
- TDLib reached `authorizationStateWaitPhoneNumber` but did not yet complete operational authorization in the previously failing network condition;
- Telegram → canonical FATHER `Material` and end-to-end M5 acceptance remain unproven.

## Options

### Option A — Keep TDLib as the M5 critical path

Continue TDLib authorization/debugging until it becomes the primary working transport, then integrate it into FATHER.

### Option B — Freeze transport contract; use Telethon for the M5 integration path

Define a minimal transport-neutral `TelegramTransport`/`TelegramMessage` boundary, adapt the live-proven Telethon path behind it, and immediately prove Telegram → `Material` → `MaterialPackage` → Analyst → Socrates. Keep TDLib as a replaceable candidate adapter and revisit only when evidence shows it changes an acceptance or production decision.

### Option C — Add GramJS/another transport PoC before integration

Run another candidate PoC before selecting/integrating a transport.

## Senior System / Solution Architect

**Recommendation:** Option B.

The stable architectural asset is not Telethon. It is the boundary between Telegram-specific acquisition and FATHER's canonical evidence model. M5 should therefore freeze the smallest contract that lets transports be replaced without changing `Material`, provenance, Analyst or Socrates.

Required boundary:

```text
TelegramCollector
      ↓
TelegramTransport
      ↓
TelegramMessage DTO
      ↓
MaterialFactory
      ↓
Material + provenance + raw hash
```

The transport contract must not expose Telethon entity/message classes or TDLib JSON objects. Vendor/library-specific state stays inside adapters.

**Why not A:** it makes an unproven implementation candidate a prerequisite for proving the actual M5 capability.

**Why not C:** no current requirement demonstrates that a third PoC answers a decision that cannot be answered by the existing Telethon + TDLib evidence.

**Falsification condition:** choose another path if an approved M5 requirement requires a capability unavailable through the Telethon adapter or if the neutral contract cannot represent required Telegram semantics without leaking vendor-specific types.

## Senior Software Engineer / Technical Lead

**Recommendation:** Option B, implemented minimally.

The next executable proof should not be another login. It should convert real acquired Telegram messages into canonical materials with stable source/message identity, timestamps, locator/provenance and raw-content hash.

Implementation order:

1. define `TelegramMessage` DTO and `TelegramTransport` protocol;
2. create `TelethonTransport` adapter around the proven path;
3. map DTO → canonical `Material` through one factory/mapper;
4. add fixture/unit contract tests;
5. run live Windows/VPN acceptance for real messages;
6. prove persistence/checkpoint ordering and source-failure isolation;
7. only then spend effort on another adapter if an acceptance gap exists.

Do not move PyYAML/Telethon into the frozen core dependency surface merely to support the optional adapter. Optional transport dependencies remain isolated.

**Falsification condition:** stop if the adapter requires invasive changes to canonical FATHER contracts or cannot meet bounded collection/failure behavior.

## Senior Systems / Business Analyst

**Recommendation:** Option B.

The observable M5 outcome is acquisition of Telegram evidence into the FATHER research pipeline, not successful operation of a particular Telegram library.

Current requirement gap is downstream: live Telegram data has not yet become canonical `Material` and has not traversed the complete evidence/review path.

Acceptance must therefore be written in transport-independent terms wherever possible: real source acquisition, stable identity, provenance, bounded collection, explicit failures, durable save/checkpoint behavior, restart/reconciliation and downstream package processing.

**Unknown:** final production requirements may later make TDLib-specific capabilities relevant. They are not presently proven to be M5 blockers.

**Falsification condition:** an approved requirement explicitly depends on a semantic/operational capability that the chosen adapter cannot supply.

## Senior Product Lead

**Recommendation:** Option B.

Users receive no additional product value from a third transport PoC by itself. The value unlock occurs when Telegram becomes reusable evidence for FATHER analysis and later Telegram-dependent product paths.

The reusable asset is the transport-neutral acquisition contract plus canonical evidence mapping. That preserves future replacement while avoiding speculative infrastructure work.

No product path is promoted solely because Telethon works.

**Falsification condition:** a validated product requirement depends on transport-specific capabilities that materially alter the contract or economics.

## Senior Project / Delivery Lead

**Recommendation:** Option B and remove TDLib/GramJS from the M5 critical path.

Current critical path:

```text
contract → Telethon adapter → TelegramMessage → Material → persistence/checkpoint → live acceptance → pipeline proof → ADR
```

TDLib becomes a bounded side investigation only when it has a named decision question, time/effort budget and evidence target. GramJS is deferred until a concrete unresolved requirement justifies it.

This reduces WIP and moves effort toward the largest remaining M5 evidence gap.

**Falsification condition:** integration becomes blocked by a transport limitation rather than by FATHER mapping/persistence logic.

## Principal Engineering Critic / Red-Team attack

### Attack 1 — Telethon success may be an accident of an old authorized session

A recovered session proves acquisition, but not clean onboarding, credential lifecycle, production deployment or long-term operational reliability. Treating it as the final production winner would overclaim the evidence.

**Accepted.** The decision does not declare Telethon the permanent production winner. It declares it the currently evidence-backed adapter for proving the M5 integration contract.

### Attack 2 — A generic transport abstraction can become premature abstraction

If the interface is designed around imagined TDLib/GramJS needs, it may create unnecessary DTOs and adapter complexity.

**Accepted constraint.** The protocol must be derived only from canonical M5 evidence needs and the currently observed Telegram message fields. No speculative cross-library feature matrix is allowed.

### Attack 3 — Deferring TDLib may hide a future migration cost

Telethon and TDLib differ in authorization, updates, entity resolution, rate behavior and message/media representation. A shallow abstraction could fail later.

**Residual risk accepted.** Preserve raw transport metadata only where low-cost and useful for provenance/debugging, but do not leak transport objects. Add a contract test suite that any future adapter must pass. Revisit when production requirements are known.

### Attack 4 — Live reading is not evidence of restart-safe collection

The largest reliability risks remain checkpoint ordering, duplicate/reconciliation behavior, FloodWait/429 handling and partial source failure.

**Blocking for M5 DONE, not for Option B.** These become mandatory acceptance gates before M5 completion.

### Attack 5 — GramJS may be a cheaper deployment option than Python Telethon

Possible, but there is no measured evidence that Node/GramJS solves a current blocker or lowers total M5 cost enough to justify another PoC now.

**Decision:** defer. A new PoC requires a written decision question and success metric.

## Critic outcome

`PASS_WITH_RISK`

The critic does not find evidence supporting continued transport experimentation on the critical path. The strongest objection is that Telethon live success is insufficient for production selection; the council agrees and narrows the decision accordingly.

## Decision

Adopt **Option B**.

For M5, Telethon becomes the **reference/live integration adapter**, not the irrevocable production transport. The project immediately freezes the smallest transport-neutral contract needed for current canonical evidence requirements and moves to Telegram → FATHER `Material` integration.

TDLib remains a candidate adapter but is removed from the M5 critical path. It may resume only when a named acceptance/production question requires evidence from it. GramJS is deferred under the same rule.

## Mandatory acceptance evidence before M5 DONE

- real Telegram message maps to canonical `Material`;
- stable source/message identity and provenance are preserved;
- raw/original content hash is produced according to canonical FATHER rules;
- collection is bounded;
- per-source failure is explicit and isolated;
- durable save occurs before checkpoint advance;
- restart/reconciliation behavior is tested;
- rate/FloodWait behavior is explicit and bounded;
- secrets/session files remain outside source control and logs;
- live Windows/VPN run proves the adapter through the canonical mapping path;
- resulting `MaterialPackage` can traverse Analyst → Socrates;
- regression/CI baseline remains green.

## Rollback / replacement path

A future `TDLibTransport` or other adapter may replace Telethon by satisfying the same contract tests and live acceptance suite. Canonical `Material`, Analyst and Socrates must not require changes solely because the Telegram library changes.

## Next engineering task

Implement and test the minimal `TelegramTransport` + `TelegramMessage` contract and a Telethon adapter that maps live messages into the existing canonical `Material` model. Do not implement speculative multi-transport orchestration yet.
