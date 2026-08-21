# Knowledge Factory M1 — Scope Freeze

Status: ACTIVE
Branch: agent/knowledge-factory-m1

## Goal
Deliver one complete, testable Knowledge Factory vertical before expanding scope.

## Included in first cycle
1. Users / minimal RBAC / Admin and Security Admin separation.
2. OfficialSourceRegistry with explicit source class and trust basis.
3. LEGAL material profile with lifecycle/version/date/change metadata.
4. BOOK material profile with bibliographic/edition/structure metadata, without legal-status semantics.
5. Acquisition: locate -> acquire -> preserve original -> SHA-256 -> provenance -> register.
6. Document pipeline state D0-D15; first executable gate is D0-D3.
7. Interactive document-card contract with DONE / IN_PROGRESS / NOT_DONE / FAILED / NOT_APPLICABLE states.
8. Shared projections: Graph <-> Table <-> Documents <-> Clauses.
9. Day / Night / System visual theme contract.
10. Append-only audit and production counters with reconciliation checks.
11. BASIC -> PROFESSIONAL -> STRESS acceptance tests.

## Explicitly deferred
- Investigation Engine;
- broad OSINT tool expansion;
- adaptive agents;
- deep/reinforcement learning;
- production-scale UI polish;
- semantic D4-D15 automation beyond what is needed to preserve contracts.

## First acceptance target
A bounded list containing several legally significant documents and several books can be processed without mixing profile semantics. Every acquired item has source/provenance, preserved original, integrity hash, profile-specific metadata, registry state and audit trace. Counters reconcile to the registry.

## Change-control rule
Any new idea that does not block this acceptance target is recorded for a later maturity level and does not expand M1 scope.
