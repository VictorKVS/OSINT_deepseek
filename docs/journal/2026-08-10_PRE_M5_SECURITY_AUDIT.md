# 2026-08-10 — Pre-M5 Security Audit

**Stage:** 07 / M5 Telegram Radar  
**Workstream:** Security / DevSecOps  
**Trigger:** before first real Telegram API credentials and TDLib session are used, Security was instructed to review the whole current project and issue a formal gate decision.

## Decision

**SECURITY GATE = STOP / REWORK BEFORE LIVE TDLib AUTHORIZATION.**

The DEV v1 baseline and CodeQL remain green, and the current product runtime is still small/std-lib-only. The audit nevertheless found concrete issues in the new TDLib PoC boundary that must be fixed before credentials/session data are introduced.

Primary blockers:

- `SEC-2026-001` — default `.runtime/tdlib` location is not ignored by Git;
- `SEC-2026-002` — TDLib initialization/encryption flow is stale against current upstream API;
- `SEC-2026-003` — native tdjson provenance/hash is not verified before loading;
- `SEC-2026-006` — generic collector error persistence can bypass secret redaction;
- secret-scanning/push-protection status must be owner-verified before credential use.

Additional before stress/freeze:

- bounded TDLib pending-update queue;
- Dependabot vulnerability alerts enabled;
- reproducible dependency-lock decision;
- repository licensing decision;
- branch/ruleset verification.

## WHY

A green unit-test/CodeQL run is not evidence that a live credential/session boundary is safe. The correct point to discover session-path, native-binary, encryption and error-redaction defects is before the first real authorization, not after a secret has entered runtime storage.

## Evidence

Primary report:

`docs/06_verification/17_PRE_M5_SECURITY_AUDIT_2026-08-10.md`

Master backlog updated:

`docs/MASTER_CONTROL_REGISTER.md`

## Commercial/reuse review

No product opportunity changes. These controls improve every future product using authenticated connectors, native libraries or locally persisted sessions without adding product-specific logic.

## Result

`REWORK REQUIRED`

## Next action

Execute remediation Wave A, add regression/security tests, re-run DEV verification + CodeQL, then Security re-verifies before authorizing POC-TD-01 local login.