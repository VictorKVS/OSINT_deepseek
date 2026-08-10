# FATHER — Master Control Register

**Status:** ACTIVE / LIVING BACKLOG + TRACEABILITY INDEX  
**Owner:** Project/Product Governance  
**Rule:** this is the single compact index of material active/queued work. Detailed evidence stays in requirements, ADRs, threat registers, PoC reports and journal.

## States

`IDEA → QUEUED → READY → ACTIVE → VERIFY → DONE/FROZEN`

Alternative terminal states: `DEFERRED`, `REJECTED`, `SUPERSEDED`.

## Current WIP

| ID | Type | Title | Outcome / why | Depends on | Security / risk links | Evidence required | State | Next action |
|---|---|---|---|---|---|---|---|---|
| REQ-M5-001 | REQ | Live Telegram Radar | collect requested public Telegram material through replaceable transport with provenance and bounded failure | DEV v1 | S02,S06,S07,S14,S15,S16,S17 + Top-100 applicable topics | M5 acceptance contract + verified implementation | ACTIVE / SECURITY HOLD | clear pre-live security blockers |
| POC-M5-001 | POC | TDLib transport PoC | produce real operational/security evidence before transport ADR | REQ-M5-001 | session secrecy, rate handling, restart/checkpoint, upstream/supply chain | repeatable harness + raw observations + failure results | ACTIVE / LIVE RUN BLOCKED | remediate SEC-AUDIT-M5-001 before credentials |
| SEC-M5-001 | SEC | Telegram session / transport security gate | prove live credentials/session cannot leak and transport can be disabled/replaced safely | REQ-M5-001 | S06,S07,S15,S16 + agent/content threat model where applicable | threat-model review + log/session tests + upstream verification | ACTIVE | execute remediation waves A/B |
| SEC-AUDIT-M5-001 | SEC | Pre-M5 full project security audit | prevent real Telegram credentials/session from entering an unverified runtime | current repo + TDLib PoC | S02,S03,S06,S07,S13,S15,S16,S26,S29,S52 | `06_verification/17_PRE_M5_SECURITY_AUDIT_2026-08-10.md` + re-verification evidence | STOP / REWORK | close live-PoC blockers then re-audit |

WIP limit is currently full. Security audit remediation is an allowed interruption of the existing M5 security/PoC streams; it does not open a new product milestone.

## Active security findings from SEC-AUDIT-M5-001

| ID | Severity | Finding | Blocks | State | Required evidence |
|---|---|---|---|---|---|
| SEC-2026-001 | HIGH | default TDLib `.runtime/tdlib` path is not covered by current `.gitignore` | live auth | ACTIVE | ignore/outside-worktree control + test |
| SEC-2026-002 | HIGH | TDLib initialization/encryption flow is stale vs current upstream schema | live auth | ACTIVE | pinned schema + non-empty external DB key + tests |
| SEC-2026-003 | HIGH | `tdjson` native library loaded without recorded provenance/hash | live auth | ACTIVE | exact upstream/build/hash evidence |
| SEC-2026-004 | HIGH lifecycle | Dependabot vulnerability alerts disabled | M5 supply-chain readiness | ACTIVE | repository setting/control enabled and verified |
| SEC-2026-005 | MEDIUM-HIGH | unbounded TDLib pending update queue | live stress/reliability | ACTIVE | bounded queue/overflow policy + negative test |
| SEC-2026-006 | MEDIUM-HIGH | collector exception text persisted without centralized sanitization | live collector | ACTIVE | safe structured error/redaction tests |
| SEC-2026-007 | MEDIUM | DEV dependency is range-pinned, not reproducibly locked | M5 freeze | QUEUED | approved lock/update strategy |
| SEC-2026-008 | MEDIUM | repository has no declared license | external distribution/commercial posture | QUEUED | explicit project license/no-license decision |
| SEC-2026-009 | UNVERIFIED | secret scanning / push protection / branch rules not attestable via current connector | production/release; secret scan before auth | VERIFY OWNER SETTINGS | owner-side evidence |

## Next queued decisions

| ID | Type | Title | Outcome / why | Depends on | State | Promotion trigger |
|---|---|---|---|---|---|---|
| POC-M5-002 | POC | GramJS comparative PoC | preserve transport optionality only if TDLib evidence leaves a material decision gap | POC-M5-001 | QUEUED | Senior Council says comparison adds decision value |
| ADR-M5-001 | ADR | Telegram transport selection | choose/approve transport based on PoC, maintenance, security and operational evidence | POC-M5-001; POC-M5-002 if justified | QUEUED | sufficient comparable evidence |
| REQ-M5-AC | REQ | M5 acceptance/security test pack | executable product-path contract before implementation | ADR-M5-001 | QUEUED | transport ADR ready |
| REQ-M6-001 | REQ | Universal Artifact/Ingestion | preserve originals/hashes/types and safely normalize media/docs | M5 stable boundary | QUEUED | M5 baseline frozen |
| REQ-M7-001 | REQ | Local-first extraction/transcription | local processing path without mandatory third-party service | M6 | QUEUED | M6 baseline frozen |
| REQ-M8-001 | REQ | Knowledge Gate | governed evidence-backed publication/revision of knowledge | stable evidence/analysis contracts | QUEUED | M7/evidence contracts ready |

## Product opportunities — not implementation commitments

| ID | Type | Opportunity | Priority | Dependency | State |
|---|---|---|---|---|---|
| OPP-P1 | OPP | Competitive & Channel Intelligence | ★★★★★ | M5 + reporting | OPPORTUNITY |
| OPP-P2 | OPP | Content Origin & Propagation | ★★★★★ | M5; stronger with M6 | OPPORTUNITY |
| OPP-P3 | OPP | Brand / Reputation Monitoring | ★★★★★ | M5 + watchlist/reporting | OPPORTUNITY |
| OPP-P4 | OPP | Technology / Market Radar | ★★★★★ | M5 + M6 + later M8 | OPPORTUNITY |
| OPP-P5 | OPP | Consent-Based Risk Intelligence | ★★★★☆ | M5/M6 + identity/legal/access controls | CONTROLLED FUTURE |

## Technical debt

No technical-debt item is automatically active. Debt is added only when a current compromise is explicit and its repayment trigger is understood.

| ID | Type | Debt | Why acceptable now | Trigger to repay | State |
|---|---|---|---|---|---|
| DEBT-001 | DEBT | FixtureCollector search remains intentionally primitive | current purpose is deterministic DEV contract testing, not quality retrieval | production/research quality requires fixture search semantics | MONITOR |
| DEBT-002 | DEBT | `depth` / `stop_when_enough` semantics are not yet operational controls | no approved requirement currently depends on them | a live collector/Analyst contract requires them | MONITOR |

## Governance/process risk

| ID | Type | Risk | Control | State |
|---|---|---|---|---|
| RISK-PROC-001 | RISK | process overengineering delays executable evidence | seven living controls; DoR/DoD; WIP=1+1+1; council only at material gates; update existing docs before creating new ones | CONTROLLED / MONITOR |

## Traceability rule

A row becomes `DONE/FROZEN` only when its evidence links are known. When implemented, add links to:

```text
Requirement
→ Risks/Security findings
→ PoC/ADR
→ Acceptance tests
→ Code/component
→ Verification evidence
→ Journal/freeze
```

This register is an index, not the evidence itself.