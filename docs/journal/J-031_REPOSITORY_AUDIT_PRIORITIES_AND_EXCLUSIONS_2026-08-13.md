# J-031 — Repository audit: priorities and exclusions — 2026-08-13

## Trigger

Full repository control audit after the integrated M5 G6-G10 live PASS.

## Finding

The repository has advanced faster than its management/control surfaces. Current live evidence proves an integrated Telegram exploratory path through G6-G10, but `MASTER_CONTROL_REGISTER.md` still described TDLib controlled authorization as the immediate next action. This creates a material risk of duplicate experimentation, wrong sequencing and inaccurate milestone reporting.

The latest live evidence is intentionally conservative: acquisition and integrated role/protocol behavior passed, while achieved research sufficiency remained `MINIMUM`, G9 was `NOT_APPLICABLE` because no leading hypothesis was supplied, and only one observable Telegram source was represented in reconnaissance.

## Decision

The critical path is reset to evidence gaps that can actually close M5:

1. G11 live hypothesis-driven scenario with G9 REQUIRED and an actual counter-evidence attempt;
2. explain and resolve the one-observable-source result, or explicitly accept/document the limitation;
3. final secrets/session/log hygiene review;
4. final transport ADR plus Engineering Council/Principal Critic review;
5. M5 acceptance/freeze;
6. only then promote M6 Artifact/Ingestion.

## Priority policy

P0 work closes an unproven M5 acceptance condition or prevents false project state. P1 work improves lifecycle/reproducibility/governance after the P0 product gate. P2 work is useful but explicitly non-critical.

## Explicit exclusions

Until P0 is closed:

- do not run GramJS or another donor PoC merely for completeness;
- do not continue TDLib debugging without a written decision-changing hypothesis;
- do not start M6/M7/M8 implementation;
- do not promote fixtures, DEV simulators or Telegram-only evidence into VERIFIED professional/domain knowledge;
- do not derive aggregate truth probability from evidence-quality scores without a separately approved calibrated model;
- do not restore removed legacy runtime/gateway/VIP code without a new requirement and reuse decision;
- do not add another governance/status layer when an existing control can carry the decision;
- do not blindly merge major Dependabot Action upgrades without CI/security compatibility evidence;
- do not make production/cross-platform claims without the applicable Windows/clean-host evidence.

## Dependency/CI observation

Open Dependabot PRs exist for major GitHub Action updates and pytest. Current workflows still use older pinned major generations. These are P1 lifecycle items: inspect/test deliberately, but they do not outrank M5 closure unless an existing action becomes unsupported or a security defect makes the upgrade blocking.

## Control update

`docs/MASTER_CONTROL_REGISTER.md` now contains the audit priority queue and exclusions. Its audit-reconciliation section is the temporary authoritative override for stale earlier M5 WIP rows until those rows are rewritten/closed during P0 reconciliation.

## Result

**AUDIT COMPLETE / PLAN UPDATED.**

Current proven capability:

`live acquisition + provenance/restart + G6-G10 integrated exploratory PASS`.

Still unproven for M5 closure:

`hypothesis-driven G9 execution + intended multi-source coverage + final transport/security decision + M5 freeze`.
