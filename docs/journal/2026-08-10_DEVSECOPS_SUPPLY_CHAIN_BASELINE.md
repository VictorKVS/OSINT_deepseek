# 2026-08-10 — DevSecOps / Supply-Chain Baseline

## Stage / milestone

Cross-cutting security workstream `SEC` introduced alongside active M5 Telegram Radar work.

## Trigger

The project now depends increasingly on external libraries, GitHub Actions, Telegram transports and later binaries/models/services. Security cannot remain a one-time audit after implementation. The project needs a permanent threat-management and supply-chain lifecycle.

## Decision

Introduce DevSecOps as a mandatory cross-cutting control for every milestone.

Created:
- `docs/SECURITY_SUPPLY_CHAIN_CONTROL.md`
- `docs/SECURITY_THREAT_REGISTER.md`
- `.github/workflows/security-codeql.yml`
- `.github/dependabot.yml`

Hardened:
- `.github/workflows/dev-verification.yml` with explicit read-only repository permission and immutable commit pins for third-party/first-party Actions.

## WHY

A component can become unsafe after approval because:
- a CVE appears;
- upstream becomes archived/stale;
- a maintainer/account/release is compromised;
- a license changes;
- a transitive dependency becomes vulnerable;
- a CI Action or binary changes;
- a secret leaks;
- an external provider changes privacy/retention behavior.

Therefore `APPROVED` is not a terminal state. Approved components enter `MONITORED` and may return to review.

## Security baseline

Security lifecycle:

```text
Requirement
  ↓
Security + supply-chain review
  ↓
Threat model
  ↓
Security acceptance tests
  ↓
Implementation
  ↓
SAST / SCA / secret / config controls
  ↓
Verification
  ↓
Inventory / SBOM / threat-register update
  ↓
Baseline
  ↓
Continuous reassessment
```

## Immediate security queue

1. Verify CodeQL workflow execution and triage any finding.
2. Verify GitHub secret-scanning / push-protection state available to this public repository.
3. Review current `requirements-dev.txt` and future runtime dependencies through SCA/dependency review.
4. Before TDLib PoC uses real credentials, complete Telegram session/secrets threat model.
5. Maintain donor freshness/security state for TDLib/GramJS and reopen ADR on material upstream change.
6. Introduce release SBOM/provenance before external product distribution.

## Result

`SEC-01 Governance baseline` — PASS / established.  
`SEC-02 Repository security automation` — PARTIAL / CodeQL + Dependabot + workflow hardening introduced; execution/config state still requires verification.

## Next gate

Security verification results must be reviewed before M5 transport baseline freeze.
