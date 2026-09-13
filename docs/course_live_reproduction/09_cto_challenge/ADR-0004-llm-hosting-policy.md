# ADR-0004 — Use Hosted LLM API for Current PoC/MVP Semantic Work Behind a Replaceable Gateway

Status: `ACCEPTED_WITH_CONDITIONS / CURRENT STAGE POLICY`

Date: `2026-09-14`

Owners: Architecture / Product / Security / Data authority for applicability  
Supersedes: none  
Superseded by: none

## Context

The FATHER OSINT/Knowledge Factory project is expanding from deterministic evidence acquisition into semantic analysis, RAG and agent candidates. A hosting policy is needed before semantic model use becomes an accidental dependency.

The project does not yet have enough Production workload/TCO data to justify hardware procurement or a permanent on-prem/cloud-GPU decision. At the same time, the security register already identifies external AI services receiving sensitive evidence as a Critical-impact threat requiring classification, privacy review and explicit approval.

## Drivers

- learn quickly during PoC/MVP without premature infrastructure CAPEX;
- preserve a local/self-hosted migration path;
- prohibit uncontrolled external processing of sensitive/unclassified evidence;
- compare options at equal quality/SLO;
- collect real workload/TCO data before Production commitment;
- keep provider/model changes replaceable and reviewable.

## Options considered

1. hosted proprietary/model API;
2. self-hosted open model on cloud GPU;
3. self-hosted on-prem GPU;
4. hybrid/provider-neutral gateway supporting approved backends.

## Decision

For the **current PoC/MVP semantic-model phase**, use a **hosted model API behind a provider-neutral Model Gateway/policy boundary** when and only when the input data is explicitly classified as permitted for external processing.

Unclassified or sensitive evidence is **not** sent to an external provider by default. The request must fail closed, use a separately approved local path, or remain unresolved until an authorized path exists.

Do **not** purchase/commit to Production self-hosted GPU infrastructure based on speculative workload. Collect real quality, latency, token/volume, concurrency, privacy and cost telemetry first.

This ADR selects the current-stage policy/interface strategy, not a permanent vendor and not the final Production hosting topology.

## WHY

At current uncertainty, hosted API provides the highest reversibility and fastest comparable semantic evaluation while avoiding premature hardware commitment. The gateway boundary reduces provider lock-in. The classification gate prevents convenience from overriding privacy/security. Production self-hosting remains a serious alternative and must be reconsidered once the missing workload/quality/TCO evidence exists.

## Consequences

### Positive

- low initial infrastructure commitment;
- faster PoC/eval of semantic capabilities;
- real token/latency/quality telemetry can be collected;
- provider-neutral boundary preserves migration path;
- no need to operate GPU serving stack before it is justified.

### Negative / trade-offs

- external-provider dependency and terms/pricing risk;
- network/provider availability affects semantic stages;
- some evidence cannot be processed externally;
- gateway/policy layer adds design complexity;
- Production economics remain unresolved until telemetry exists.

### Risks retained

- accidental sensitive-data egress if classification/policy is bypassed;
- provider/model behavior changes;
- vendor-specific features leaking through gateway abstraction;
- cost growth with tokens/requests;
- external retention/privacy changes.

## Compliance / Verification

Before enabling an external model path:
- classify allowed input data;
- record provider/model/version;
- keep credentials outside prompts/evidence/repository;
- log model-stage telemetry needed for cost/quality comparison;
- run common evaluation/security cases;
- block prohibited data path;
- verify evidence/citation behavior for grounded use cases.

## Rollback / Replacement path

Disable hosted backend in gateway policy and route only to an approved local/self-hosted backend or return a visible unavailable/blocked state. Domain/evidence contracts must not depend on provider-specific payloads.

## Revisit triggers

Create a superseding ADR when any material trigger occurs:
- external processing becomes prohibited for required data;
- hosted API TCO materially exceeds a comparable self-hosted option;
- p95 latency/availability fails approved SLO;
- local model passes the same quality/security eval and stable workload supports economic utilization;
- provider terms/retention/region/security posture changes;
- offline/local operation becomes a hard requirement;
- Production use case and workload become approved.

## Traceability

`HD-01..HD-10 -> trade-off matrix -> TCO gaps -> ADR-0004 -> semantic PoC/MVP telemetry -> future Production ADR`
