# Knowledge Factory Conveyor — Unified Stream Board

**Status:** ACTIVE / P0  
**Rule:** all lanes feed the same conveyor; unrelated work is HOLD.

## Lane A — Source Trust & Acquisition

**Objective:** make D0-D3 real and repeatable.

- [ ] reconcile `SourcePolicy` implementation and seed registry
- [ ] approved/discovery source modes
- [ ] exact locator resolution
- [ ] bounded HTTP/file acquisition adapter contract
- [ ] exact-byte preservation
- [ ] MIME/signature/size metadata
- [ ] SHA-256
- [ ] DocumentVersion creation/reuse
- [ ] legal lifecycle metadata adapter
- [ ] acquisition/audit counters
- [ ] KF-FX-001..009 green

**Blocking output:** verified `OriginalArtifact + DocumentVersion` objects.

## Lane B — Document Compiler

**Objective:** turn immutable originals into stable traceable structure and chunks.

- [ ] parser profile registry
- [ ] parser/method versioning
- [ ] structure-node schema
- [ ] profile-specific locator schema
- [ ] deterministic structure parse
- [ ] stable chunk IDs
- [ ] chunk-to-original locator preservation
- [ ] parser failure states
- [ ] KF-FX-010..011 green

**Input gate:** D3 artifact.  
**Blocking output:** D4-D5 compiler package.

## Lane C — Knowledge Extraction

**Objective:** create reusable typed knowledge objects instead of rereading originals.

- [ ] concept/term schema
- [ ] definition schema
- [ ] atomic fact/requirement/rule/claim schema
- [ ] entity/actor/control/method schema
- [ ] extraction provenance schema
- [ ] object equivalence/reuse policy
- [ ] explicit UNKNOWN/GAP semantics
- [ ] KF-FX-012..014 green

**Input gate:** D5 chunks.  
**Blocking output:** D6-D9 typed objects.

## Lane D — Relations, Conflicts, Analyst & Socrates

**Objective:** convert isolated objects into reviewed knowledge.

- [ ] typed relation taxonomy
- [ ] internal relation builder
- [ ] cross-document relation builder
- [ ] version/amendment/supersession edges
- [ ] applicability/context edges
- [ ] duplicate/equivalence candidate classifier
- [ ] conflict/overlap/context-split/gap classifier
- [ ] evidence-dependence/circularity check
- [ ] Analyst review package
- [ ] Socrates/Critic review contract
- [ ] promotion-request boundary
- [ ] KF-FX-015..020, 022..023 green

**Input gate:** D6-D9 objects.  
**Blocking output:** D10-D15 reviewed KB-ready package.

## Lane E — Platform, QA, Audit, Metrics & Projections

**Objective:** make every lane deterministic, inspectable and regressable.

- [ ] stable ID envelope
- [ ] registry/store reconciliation
- [ ] append-only audit enforcement
- [ ] RBAC/action boundaries
- [ ] graph/table/document/clause projection reconciliation
- [ ] BASIC/PROFESSIONAL/STRESS runner
- [ ] production telemetry schema
- [ ] reuse/rework counters
- [ ] change propagation/invalidation
- [ ] frozen DEV v1 regression
- [ ] KF-FX-021, 024..028 green

**Blocking output:** evidence that the conveyor is a system, not a collection of scripts.

## Integration gates

```text
G-A  Lane A → verified D3 artifact
G-B  Lane B → traceable D5 chunks
G-C  Lane C → typed D9 knowledge objects
G-D  Lane D → reviewed D15 KB-ready package
G-E  Lane E → reconciled tests/metrics/audit across A-D
```

No lane can declare DONE while its integration gate is red.

## HOLD queue

Preserve but do not actively expand:

- Telegram transport competition not required for acquisition unblock;
- M6 evidence worklog as an independent track;
- Programmer Agent standalone feature work;
- Research/Hypothesis R1+ autonomous behavior;
- specialist KB expansion beyond first acceptance corpus;
- UI cosmetic work;
- RL/deep training;
- speculative infrastructure/product features.

## Daily/Run reporting format

Every execution report should answer:

```text
1. Which lane/gate moved?
2. What artifact/test evidence was produced?
3. What failed or was reworked?
4. Which object counts changed?
5. What was reused instead of recomputed?
6. What is the single next bottleneck?
```

No percentage speedup or completion date is reported without measured comparable telemetry.
