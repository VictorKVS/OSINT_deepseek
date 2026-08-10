# 2026-08-10 — Pre-M5 Security Remediation

## WHY

The pre-M5 security audit blocked live TDLib authorization until repository-side credential/session, native-library and resource-boundary weaknesses were corrected.

## DONE

- ignored `.runtime/` so the default TDLib PoC state cannot be staged accidentally;
- aligned TDLib initialization with current `database_encryption_key` semantics;
- removed the obsolete empty encryption-key authorization path;
- added current email/code auth handling and fail-closed new-account registration behavior;
- required exact `tdjson` path + SHA-256 verification before native library loading;
- expanded credential redaction;
- stopped persisting raw collector exception strings;
- bounded TDLib pending updates and made overflow observable;
- added/updated regression tests for all of the above;
- updated PoC operator instructions and Master Control Register.

## EVIDENCE

`docs/06_verification/18_PRE_M5_SECURITY_REMEDIATION_2026-08-10.md`

The reviewed post-remediation repository state completed DEV Verification and CodeQL successfully before this journal update. Subsequent documentation commits must retain the same regression/security checks.

## REMAINING BEFORE LIVE AUTH

- select/build exact official TDLib revision;
- record `tdjson` binary SHA-256 and use it as `TDJSON_SHA256`;
- provide non-empty local DB encryption key outside Git;
- confirm local runtime remains untracked;
- owner-side GitHub security setting check; Dependabot vulnerability alerts are currently disabled and must be enabled before M5 supply-chain readiness/freeze.

## GATE

Repository code remediation: **PASS**.  
Live TDLib authorization: **CONDITIONAL — local provenance required**.  
Production/M5 freeze: **NOT APPROVED**.
