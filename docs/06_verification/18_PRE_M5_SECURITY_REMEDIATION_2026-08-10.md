# FATHER / OSINT_deepseek — Pre-M5 Security Remediation Evidence

**Date:** 2026-08-10  
**Parent audit:** `17_PRE_M5_SECURITY_AUDIT_2026-08-10.md`  
**Scope:** remediation of findings that can be closed in repository code before the first live TDLib authorization.  
**Gate:** **CODE-SIDE REMEDIATION PASS / LOCAL PROVENANCE EVIDENCE STILL REQUIRED**

## Executive result

The repository-side blockers found by the pre-M5 security audit were remediated and regression-tested. The current code no longer permits the original unsafe defaults for TDLib runtime storage, database encryption, native library resolution, unbounded pending-update buffering, or persistence of raw collector exception text.

The first live Telegram authorization is still conditional on local operator evidence: an explicitly approved TDLib build, exact `tdjson` path and SHA-256, a non-empty database-encryption key, and local credential handling outside Git.

## Remediation matrix

| Finding | Change | Evidence state |
|---|---|---|
| SEC-2026-001 | `.runtime/` is ignored by Git; documented external runtime remains preferred | CONTROLLED |
| SEC-2026-002 | current `setTdlibParameters` includes mandatory non-empty `database_encryption_key`; obsolete encryption-key auth path removed; current phone/email/code/password states handled | CONTROLLED |
| SEC-2026-003 | `TdJsonBridge` requires explicit `TDJSON_LIBRARY` + `TDJSON_SHA256`, verifies SHA-256 before `ctypes.CDLL`, and refuses PATH-only implicit loading | CODE CONTROLLED / LOCAL HASH EVIDENCE REQUIRED |
| SEC-2026-004 | `dependabot.yml` remains present, but repository vulnerability alerts are still disabled in GitHub settings | OPEN OWNER SETTING |
| SEC-2026-005 | pending update buffer is bounded; overflow is observable through `dropped_pending_updates` | CONTROLLED |
| SEC-2026-006 | persisted collector errors no longer include raw `str(exc)`; stable type-only summary is used | CONTROLLED |
| SEC-2026-007 | exact dependency/lock strategy remains queued for M5 freeze | QUEUED |
| SEC-2026-008 | project license decision remains queued before external distribution/commercial release | QUEUED |
| SEC-2026-009 | GitHub connector cannot attest all settings; official GitHub documentation states secret scanning runs automatically for public repositories. Repository-level Dependabot alerts and branch/ruleset controls still need owner-side verification/configuration | PARTIAL / OWNER ACTION |

## Security implementation details

### Native TDLib boundary

Live PoC startup now requires all of:

```text
TDJSON_LIBRARY
TDJSON_SHA256
TELEGRAM_API_ID
TELEGRAM_API_HASH
FATHER_TDLIB_DB_KEY
```

The binary hash is checked before the library is loaded. A malformed or mismatching digest stops execution.

### TDLib database state

The database encryption key is mandatory in the current request builder. Empty-key fallback is forbidden. The key is not written into repository configuration or ordinary log output.

### Error handling

Collector/package errors contain only collector name and exception type. Raw exception payloads are not persisted into the MaterialPackage path because third-party exceptions can contain request/account/session details.

### Resource limits

The synchronous PoC facade uses a bounded update queue. Overflow is not silent: a counter records dropped pending updates for reliability analysis.

## Automated evidence

New/updated tests cover:

- non-empty TDLib database-encryption key;
- current TDLib email/code authorization contract;
- fail-closed account-registration behavior;
- native `tdjson` hash verification and mismatch rejection;
- current credential-field redaction;
- collector exception payload non-disclosure;
- bounded TDLib pending-update queue and observable overflow.

The latest reviewed repository state after these changes completed both DEV Verification and CodeQL successfully.

## External/platform controls

GitHub official documentation currently states that secret scanning runs automatically for public repositories. This repository is public. This is platform-level evidence that ordinary secret scanning is present, but the current connector cannot list secret-scanning alerts or attest repository-specific advanced settings.

Dependabot vulnerability alerts are independently confirmed **disabled** by the repository API and must be enabled by the repository owner under GitHub Settings → Advanced Security. The presence of `.github/dependabot.yml` does not enable vulnerability alerts by itself.

## Remaining gate before first live authorization

The code-side Wave A/B remediation is complete enough to prepare a local run, but **do not enter Telegram credentials until local native-library provenance is recorded**:

1. build/install TDLib from the selected official upstream revision;
2. record the exact upstream tag/commit;
3. compute SHA-256 of the exact `tdjson.dll`/`libtdjson.so` used;
4. set `TDJSON_LIBRARY` to that exact file;
5. set `TDJSON_SHA256` to the recorded digest;
6. provide a strong non-empty `FATHER_TDLIB_DB_KEY` outside Git;
7. confirm `git status` remains clean/does not expose runtime state;
8. enable Dependabot alerts before M5 supply-chain readiness/freeze.

## Gate decision

```text
Repository code-side security remediation: PASS
Live TDLib credential authorization: CONDITIONAL / WAITING FOR LOCAL PROVENANCE
M5 production approval: NOT GRANTED
```

No product milestone or production transport has been approved by this remediation report.
