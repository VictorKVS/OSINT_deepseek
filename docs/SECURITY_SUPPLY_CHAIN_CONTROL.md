# FATHER / OSINT_deepseek — DevSecOps & Software Supply-Chain Governance

**Status:** ACTIVE CROSS-CUTTING CONTROL  
**Owner:** Security / Project Governance  
**Applies to:** every current and future milestone, dependency, GitHub Action, container, binary, model, external API/SDK and donor-derived component.  
**Principle:** security is not a final review. It is a permanent engineering gate from requirement to retirement.

## 1. Purpose

FATHER must remain maintainable and trustworthy as dependencies, upstream projects, CI actions, operating systems, models and external services change over time.

The security function therefore owns a continuously reviewed **software supply-chain threat register** and must be able to answer at any material gate:

- what third-party components do we depend on?
- who maintains them and is the upstream still healthy?
- which version/commit are we using?
- what license and security posture does it have?
- are known vulnerabilities present?
- is a safer/newer supported version available?
- can a compromised upstream, package, Action, binary or model poison our build or runtime?
- can secrets, evidence or sessions leak through code, logs, CI artifacts or external services?
- can we replace the component without redesigning the product?
- what evidence proves the control is working?

## 2. Standards baseline

The project uses the following as guidance, not as compliance theatre:

- **NIST SP 800-218 SSDF v1.1** — final baseline for secure software development.
- **NIST SP 800-218 Rev.1 / SSDF v1.2 draft** — monitored for future changes; not treated as final until finalized.
- **SLSA** — supply-chain integrity patterns for source/build/provenance.
- **OpenSSF Scorecard** — supplemental donor/upstream security signal, never a substitute for engineering review.
- **GitHub native security controls** — dependency alerts/review where available, code scanning, secret scanning/push protection where available.

## 3. Permanent DevSecOps gate

```text
REQUIREMENT / ТЗ
      ↓
SECURITY + SUPPLY-CHAIN REVIEW
      ├── data/secrets classification
      ├── trust boundaries
      ├── dependency impact
      ├── donor/upstream health
      ├── abuse/failure modes
      └── rollback/replacement path
      ↓
ARCHITECTURE
      ↓
THREAT MODEL / SECURITY REQUIREMENTS
      ↓
ACCEPTANCE + SECURITY TESTS
      ↓
IMPLEMENTATION
      ↓
SAST / SCA / SECRET / CONFIG CHECKS
      ↓
BUILD / CI INTEGRITY
      ↓
VERIFICATION
      ↓
SBOM / DEPENDENCY RECORD / RISK REGISTER UPDATE
      ↓
BASELINE
      ↓
CONTINUOUS REASSESSMENT
```

No new dependency or external execution surface becomes APPROVED merely because it works.

## 4. Supply-chain inventory classes

Every non-trivial external component must belong to one of these classes:

| Class | Examples | Required record |
|---|---|---|
| Package dependency | Python/npm libraries | name, exact version/range, direct/transitive, license, upstream, security state, replacement path |
| Source donor | TDLib, GramJS, donor project | upstream URL, activity, license, security posture, PoC/benchmark, decision state |
| CI/CD dependency | GitHub Actions | owner, action, pinned reference policy, permissions, update policy |
| Binary/tool | ffmpeg, browser, OCR engine | source, version, checksum/package source, update path |
| Container/base image | future runtime images | digest/tag, registry, provenance, CVEs, rebuild policy |
| AI model | future local/remote models | source, version/hash, license, data/privacy implications, update/evaluation policy |
| External API/service | transcription/LLM/search | provider, data sent, retention/privacy, auth secrets, fallback/replacement |

## 5. Dependency lifecycle

```text
DISCOVERED
   ↓
SOURCE_VERIFIED
   ↓
SECURITY_REVIEWED
   ↓
POC / BENCHMARKED
   ↓
APPROVED + PINNED
   ↓
MONITORED
   ├── UPDATE_AVAILABLE
   ├── VULNERABLE
   ├── UPSTREAM_STALE
   ├── LICENSE_CHANGED
   ├── COMPROMISE_SUSPECTED
   └── SUPERSEDED
   ↓
UPGRADE / REPLACE / RETIRE
```

An APPROVED component can return to REVIEW at any time.

## 6. Mandatory security registers

The project maintains four linked records:

1. **Project Risk Register** — delivery/architecture/product risks.
2. **Security & Supply-Chain Threat Register** — technical threats to source, dependencies, build, runtime and secrets.
3. **Donor KB** — upstream project evidence and freshness.
4. **Dependency/SBOM inventory** — what is actually used by a frozen baseline.

A finding must link to the affected component/milestone and to remediation evidence.

## 7. Minimum controls by stage

### NOW / DEV

MUST:
- keep runtime dependency surface minimal;
- no secrets/session material in Git;
- clean CI from a fresh checkout;
- exact dependency declarations where practical;
- review every new external dependency before adoption;
- record upstream URL/license/maintenance state;
- secret scanning for the public repository;
- SCA/dependency vulnerability scanning;
- lightweight SAST for Python changes;
- pin third-party CI actions to reviewed immutable revisions when the automation baseline is introduced;
- least-privilege GitHub Actions permissions;
- maintain a security threat register.

### BEFORE LIVE TELEGRAM / M5 FREEZE

MUST additionally:
- threat model Telegram sessions/credentials;
- ensure session material never appears in normal logs or CI artifacts;
- verify dependency and transport upstream state immediately before ADR/freeze;
- test hostile/invalid source responses and bounded failure behavior;
- define emergency transport-disable/replacement procedure.

### BEFORE ARTIFACT INGESTION / M6 FREEZE

MUST additionally:
- treat all files as untrusted input;
- validate type/signature independently of filename;
- constrain parsers/converters and resource use;
- define archive/decompression policy;
- scan/contain dangerous active content where applicable;
- preserve original hash/provenance.

### BEFORE PRODUCTION DISTRIBUTION

MUST additionally:
- reproducible or traceable build strategy;
- SBOM generated for release artifact;
- release provenance/attestation strategy;
- signed/tagged release policy;
- production secret management;
- dependency update SLA by severity;
- vulnerability disclosure/incident handling process;
- backup/rollback/recovery validation.

## 8. Security gates

A milestone cannot freeze when an in-scope **CRITICAL** threat lacks one of:

- verified mitigation;
- explicit architectural removal of the threat;
- documented risk acceptance by the project owner with WHY.

`"scanner is green"` is not sufficient evidence by itself. Tool findings, architecture, exploitability and actual exposure must be reviewed together.

## 9. Update policy

Dependency freshness is not equivalent to blindly installing the newest version.

For every update:

```text
new release / advisory
      ↓
impact assessment
      ↓
changelog + security + compatibility review
      ↓
test in isolated branch/harness
      ↓
regression
      ↓
approve / defer with WHY / replace
```

We prefer **supported and security-maintained** over merely **newest**.

## 10. Security automation backlog

### SEC-01 — Governance baseline
**MUST / ACTIVE**
- this policy;
- security/supply-chain threat register;
- roadmap integration;
- journal integration.

### SEC-02 — Repository security automation
**MUST / NEXT**
- verify GitHub secret-scanning state;
- add SAST for Python;
- add dependency/SCA scan appropriate to the current stdlib + pytest surface;
- add dependency update automation with review, not blind merge;
- apply least-privilege workflow permissions;
- review/pin third-party Actions.

### SEC-03 — SBOM / release inventory
**SHOULD now, MUST before product release**
- machine-readable dependency inventory;
- baseline/release SBOM;
- store provenance with release evidence.

### SEC-04 — Continuous upstream watch
**SHOULD**
- periodically re-evaluate APPROVED donor/upstream state;
- flag archive/staleness/security/license changes;
- reopen ADR when a material change occurs.

### SEC-05 — Security regression packs
**MUST as attack surfaces appear**
- secrets/logging;
- Telegram session handling;
- untrusted files/parsers;
- external services;
- auth/RBAC when introduced;
- prompt/content injection when LLM-driven tooling becomes executable.

## 11. Security owner behavior

The security role is expected to challenge the project continuously:

> What changed upstream? What dependency became vulnerable? What new trust boundary did this feature create? What can an attacker poison? What can leak? What can fail open? What is no longer supported? How do we disable or replace it?

This challenge is part of normal delivery, not an audit performed after development.
