# FATHER Engineering Governance

**Status:** ACTIVE PROJECT RULE

## Primary principle

**NO CODE BEFORE CONTRACT.**

FATHER development follows an evidence-producing engineering chain. Code is an implementation of an approved contract, not the place where requirements are invented.

The operational execution rules (Definitions of Ready/Done, WIP limit, Senior Council threshold, Change Impact Analysis, ADR threshold, technical-debt classification and documentation hierarchy) are defined in:

**[Project Execution Control](PROJECT_EXECUTION_CONTROL.md)**

## Mandatory chain

```mermaid
flowchart LR
    I[Idea / Business Need] --> R[ТЗ / Requirements]
    R --> CR[Commercial + Reuse Review]
    CR --> SR[Security / Threat Review]
    SR --> RR[Requirements Review]
    RR --> A[Architecture]
    A --> AR[Architecture Review]
    AR --> T[Acceptance Test Specification]
    T --> IP[Implementation Plan]
    IP --> C[Code]
    C --> TR[Test + Security Runs]
    TR --> AC[Acceptance]
    AC --> OP[Operation]
    OP --> EX[Experience / KB]
```

## Gates

### G0 — Requirements Ready
Must define purpose, scope, actors, inputs, outputs, constraints, exclusions, DEV/PROD boundary and acceptance criteria. Material items must also satisfy the current **Definition of Ready**.

### G1 — Architecture Ready
Must show responsibility boundaries, data flow, external dependencies, trust/failure boundaries and WHY for material decisions. Commercial/reuse and security implications must be explicit.

### G2 — Tests Ready
Acceptance tests must exist before further feature code. A test should prove externally observable behavior, not merely call an internal class. Security acceptance tests are required where a new attack surface exists.

### G3 — Development Allowed
Only requirements traceable through G0-G2 may be implemented.

### G4 — Verified
Existing tests have been executed; failures are recorded and classified; implementation matches the approved contract; in-scope security findings are treated according to policy; Definition of Done evidence is complete where applicable.

### G5 — Operational Candidate
Production integrations, credentials, schedulers, hardening, monitoring and battle collectors may be introduced only here. Operational roles, rollback/disable path, logging/audit, secrets and vulnerability management must be defined before production claims.

## Project modes

- **DEV / SIMPLIFIED:** fixtures, deterministic workers, local storage, small bounded loops.
- **PROD / BATTLE:** live connectors, secrets, schedulers, isolation, monitoring, retry/rate-limit strategy, legal/security controls.

The DEV model must prove the profession and interfaces before PROD infrastructure is added.

## Occam rule

Do not add an agent, service, datastore, protocol, metric, abstraction or governance mechanism unless a concrete approved requirement or uncovered risk needs it. Future capability is documented, not pre-built.

The same Occam rule applies to project management: governance exists to reduce risk and improve decisions, not to produce documents.

## WIP rule

Default project WIP is limited to:

- **1 active core milestone**;
- **1 active security workstream attached to it**;
- **1 active research/PoC stream attached to it**.

Current approved WIP is M5 Telegram Radar + M5 security/supply-chain review + TDLib PoC. Other milestones/products remain queued unless explicitly promoted by a gate.

## Senior Council rule

The full Senior Council is invoked for material milestone, ADR, trust-boundary, external-dependency, high/critical security, product-path and freeze decisions. Routine edits and low-risk implementation details use normal engineering review rather than full council ceremony.

## Change request rule

Every material change must be traceable as:

`Need -> Requirement -> Risk/Security Review -> Architecture/ADR -> Test -> Implementation -> Test/Security Evidence -> Decision/Experience`.

A compact Change Impact Analysis is required for material changes.

If a discovered implementation predates the contract, it is marked **PROTOTYPE / UNVERIFIED** and is reviewed with `KEEP / CHANGE / DELETE` after requirements approval.

## Work-item classification

Do not conflate:

- `DEFECT` — violates approved behavior;
- `RISK` / `SEC` — uncertain exposure or security finding;
- `DEBT` — accepted maintainability/design compromise;
- `REQ` — approved capability;
- `OPP` — opportunity, not an implementation commitment.

This distinction is mandatory in planning and reviews.

## Evidence rule

Documents alone do not prove capability. Gate completion must ultimately rely on appropriate executable/operational evidence: tests, PoC results, benchmark data, security findings/mitigations, restart/recovery evidence, or other observable proof appropriate to the requirement.