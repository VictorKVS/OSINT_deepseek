# FATHER OSINT — Permanent ALINA Lab and B2B Product Boundary

Status: accepted architecture decision. Priority: Telegram first, Darknet second.

## Non-negotiable invariant
The existing FATHER OSINT system is the **permanent internal research and skill-building laboratory for ALINA Analyst**. It is not replaced, renamed into, or subordinated to a commercial client product. ALINA continuously researches authorized sources, learns techniques, tests candidate skills, tracks provenance and maintains its own knowledge graph and competency registry.

## Two distinct operational contexts on one common engineering core
1. **ALINA OSINT LAB (permanent):** Telegram research -> evidence -> method extraction -> skill candidates -> isolated testing -> verified reusable skills -> competency tracking. Darknet is a later, isolated research adapter after the Telegram milestone.
2. **FATHER OSINT B2B (client deployments):** requirements intake -> process design -> selection of reviewed reusable components -> client-specific agents and workflows -> controlled deployment -> customer-specific monitoring and reporting.

Both may reuse FATHER Analytical Core, ToolLab adapters, skill manifest schema, quality framework, workflow engine and interface components. Reuse is by explicit versioned packages/interfaces, **not shared operational databases**.

## Strict isolation
- ALINA research corpus, raw captures, account sessions, credentials, evidence, prompts, telemetry and experimental outputs remain in ALINA-controlled storage.
- Each client has its own tenant/project storage, keys, credentials, logs, access policy and retention settings.
- No client raw data, identifiable case materials, secrets or proprietary workflows flow into ALINA or other clients by default.
- Promote a generalized improvement only after authorization, review, de-identification where appropriate, licensing checks and a repeatable non-client test.
- Client deployments never alter ALINA's permanent laboratory, skill evaluations or knowledge graph automatically.

## Initial Telegram delivery milestones
T0: task catalog and transparent statuses (planned vs real).
T1: Telegram channel research workspace with per-channel tabs and provenance-first post view.
T2: authorized collection pipeline with checkpoints, rate limits, secure sessions and real storage.
T3: time-series waves, source comparison, evidence media and explicit uncertainty.
T4: candidate skill extraction, declarative skill registry and isolated test fixtures.
T5: evaluation dashboard and verified competency passport.
T6: reusable client workflow templates and separate B2B intake, without cross-tenant data reuse.
T7: Darknet adapter design and isolated rollout after Telegram is validated.

## Acceptance gates
- A successful Telegram demo must distinguish demo content from real collected material.
- No skill is 'verified' without a recorded fixture, result, version and review.
- No origin attribution based solely on first observed post; no causal claim based solely on similarity.
- No execution of commands sourced from untrusted posts without review and sandbox policy.
- No active collection or testing without authorization and required network policy.
- B2B may ship separately; the ALINA laboratory remains available and independent.

## User-facing product labels
ALINA OSINT LAB — Постоянная лаборатория
FATHER OSINT B2B — Автоматизация для заказчиков
Shared: FATHER Analytical Core / Skill Factory / ToolLab

## Immediate implementation
Expose the distinction in the Telegram-first task catalog; implement a separate client intake prototype without touching the existing ALINA research data or the main branch.
