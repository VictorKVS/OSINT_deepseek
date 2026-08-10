# FATHER / OSINT_deepseek — Pre-M5 Security Audit

**Date:** 2026-08-10  
**Audit type:** pre-live-integration DevSecOps / security review  
**Scope:** current repository, DEV v1 baseline, GitHub Actions, dependency surface, secrets/session handling, TDLib PoC boundary, current storage/orchestration code, security governance and controls that become active before a real Telegram session.  
**Decision authority:** Security / DevSecOps Gate  
**Gate result:** **STOP / REWORK REQUIRED BEFORE LIVE TDLib AUTHORIZATION**

---

## 1. Executive verdict

The current DEV v1 core remains small and comparatively easy to secure. The production package currently has no third-party Python runtime dependencies, GitHub Actions are pinned to immutable commits, workflow permissions are explicit, CodeQL is active, and the latest reviewed DEV verification and CodeQL runs completed successfully.

However, the repository is **not yet authorized for a live Telegram credential/session run**. The audit found several concrete pre-PoC blockers in the new TDLib PoC path and one important GitHub security-control gap.

The most important findings are:

1. **SEC-2026-001 / HIGH — TDLib runtime default path is not covered by `.gitignore`.** `run_local.py` defaults to `.runtime/tdlib`, while `.gitignore` covers `.tdlib/`, `tdlib-data/`, `tdlib-files/`, `poc/tdlib/runtime/` and `poc/tdlib/session/`, but not `.runtime/`. A local TDLib database/session can therefore be created in a Git-visible path and accidentally staged.
2. **SEC-2026-002 / HIGH — Current TDLib initialization contract is stale against current upstream API.** Current official TDLib `setTdlibParameters` includes `database_encryption_key`; the PoC request builder does not send it. The PoC auth state machine instead relies on `authorizationStateWaitEncryptionKey`, which is not part of the current official getting-started authorization sequence. This is both a functional bootstrap risk and a local-data protection risk.
3. **SEC-2026-003 / HIGH — Native `tdjson` provenance is not verified before `ctypes.CDLL` loads it.** `TDJSON_LIBRARY` can point to any local shared library. This is acceptable only if the operator independently verifies provenance; current code has no version/hash/source verification gate. A replaced DLL/SO would execute native code inside the PoC process and receive Telegram credentials/session access.
4. **SEC-2026-004 / HIGH — Dependabot vulnerability alerts are disabled for the repository.** A Dependabot configuration file exists for version updates, but the GitHub API explicitly reports that Dependabot alerts are disabled. This weakens the intended continuous vulnerability-monitoring model.
5. **SEC-2026-005 / MEDIUM-HIGH — TDLib pending update queue is unbounded.** While a synchronous request waits for its correlated response, every unrelated TDLib update is appended to an unbounded deque. Under high update volume or delayed responses this can cause memory growth and process exhaustion.
6. **SEC-2026-006 / MEDIUM-HIGH — Collector exception strings are persisted without a security redaction boundary.** `OSINTAgent` stores `type(exc).__name__` and `str(exc)` directly in `collection_errors`. A future live transport exception containing credential/session/request detail could therefore be written to local evidence/state even though TDLib JSON payload redaction exists elsewhere.
7. **SEC-2026-007 / MEDIUM — Python DEV dependency is range-pinned, not reproducibly locked.** CI installs `pytest>=9.0,<10`; a later compatible release can enter a clean build without an explicit reviewed version/hash change. Current runtime risk is limited because the product core is stdlib-only, but this is not sufficient as the dependency graph grows.
8. **SEC-2026-008 / MEDIUM — Repository has no declared GitHub license.** GitHub repository metadata returns `license: null`. This is not a runtime exploit but is a material legal/supply-chain/commercialization risk and blocks a clean external reuse/distribution posture.
9. **SEC-2026-009 / UNVERIFIED CONTROL — secret-scanning alerts and branch protection could not be read through the current GitHub integration.** The API returned access/permission errors. This is not evidence that the controls are absent; it means the audit cannot currently attest them. They require owner-side verification in GitHub settings.

No live Telegram API credentials or session data were found in the reviewed current files. No current use of `eval`, `exec`, `subprocess`, `pickle` or shell-command execution was found through repository code search. These negative findings reduce current attack surface but do not replace future scanning.

---

## 2. Evidence reviewed

### Repository / CI

- `.github/workflows/dev-verification.yml`
- `.github/workflows/security-codeql.yml`
- `.github/dependabot.yml`
- `.gitignore`
- repository metadata / main branch metadata where accessible
- latest GitHub Actions history for DEV Verification and CodeQL

### Dependency surface

- `requirements.txt` — runtime currently stdlib-only
- `requirements-dev.txt` — current explicit third-party DEV dependency: pytest 9.x range
- no active Node/npm runtime in current product tree

### Current core

- `father_osint/models.py`
- `father_osint/storage.py`
- `father_osint/agent.py`
- `father_osint/collectors/telegram.py`
- current transport-neutral boundary

### TDLib PoC

- `poc/tdlib/tdjson_bridge.py`
- `poc/tdlib/requests.py`
- `poc/tdlib/auth.py`
- `poc/tdlib/client.py`
- `poc/tdlib/mapping.py`
- `poc/tdlib/run_local.py`
- current TDLib PoC tests

### Security governance

- `docs/SECURITY_THREAT_REGISTER.md`
- `docs/SECURITY_TOP100_CONTROL_CATALOG.md`
- `docs/SECURITY_SUPPLY_CHAIN_CONTROL.md`
- `docs/AI_AGENT_SECURITY_THREAT_MODEL.md`
- `docs/PROJECT_EXECUTION_CONTROL.md`
- `docs/MASTER_CONTROL_REGISTER.md`

### Upstream verification

Current official TDLib documentation was checked for initialization/authentication semantics. Current documentation states that local TDLib data is encrypted using a user-provided encryption key and the current `setTdlibParameters` schema contains `database_encryption_key`. The current getting-started flow begins with `authorizationStateWaitTdlibParameters` and does not rely on the older separate encryption-key authorization step.

---

## 3. Positive controls already evidenced

### P-01 — GitHub Actions pinning

`actions/checkout`, `actions/setup-python` and CodeQL actions are pinned to immutable commit SHAs rather than floating tags.

**Assessment:** good supply-chain control; retain.

### P-02 — Workflow permissions

DEV verification explicitly has `contents: read`; CodeQL has the narrow additional `security-events: write` permission required to upload findings.

**Assessment:** good least-privilege baseline.

### P-03 — CodeQL operational

The reviewed latest CodeQL run completed successfully on the latest TDLib PoC test commit.

**Assessment:** useful SAST evidence, but not approval by itself.

### P-04 — Small active dependency surface

The product runtime is currently Python stdlib-only. The DEV dependency surface contains pytest only.

**Assessment:** strong current risk reduction.

### P-05 — TDLib-specific objects do not currently leak into product domain contracts

The current `TelegramCollector` remains transport-neutral and maps `TelegramMessage` into `Material` without requiring TDLib classes.

**Assessment:** good replacement/containment boundary.

### P-06 — Secrets are not printed by the intended bootstrap path

`run_local.py` uses environment variables for API ID/hash and `getpass` for interactive code/2FA entry. Existing redaction logic covers several TDLib credential fields.

**Assessment:** good direction, but incomplete because storage path, encryption-key handling, native-library provenance and generic exception redaction remain blockers.

---

## 4. Detailed findings

## SEC-2026-001 — TDLib runtime path can enter Git

**Severity:** HIGH  
**Threat links:** S06, S07, S15  
**Component:** `poc/tdlib/run_local.py`, `.gitignore`

`run_local.py` defaults to:

```text
.runtime/tdlib
```

The current `.gitignore` does not ignore `.runtime/`.

### Attack / failure scenario

1. operator runs the PoC;
2. TDLib creates database/session material under `.runtime/tdlib`;
3. operator runs `git add .`;
4. session/cache material can be staged and potentially committed.

### Required remediation

- ignore `.runtime/` or use a default runtime root that is already ignored and outside the repository;
- preferably reject a runtime root located inside a Git worktree unless it is an explicitly ignored path;
- add an automated regression test that the documented/default session path matches ignore policy;
- before first live run, check `git status --ignored` and verify no session material is trackable.

**Gate:** blocks live authorization.

---

## SEC-2026-002 — TDLib initialization/encryption contract is stale

**Severity:** HIGH  
**Threat links:** S02, S15, S27  
**Component:** `poc/tdlib/requests.py`, `poc/tdlib/auth.py`

Current upstream TDLib places `database_encryption_key` in `setTdlibParameters`. The current PoC request builder omits that field and the auth flow still contains the older `authorizationStateWaitEncryptionKey` path with an empty-string default key.

### Security effect

TDLib states that local data encryption uses a user-provided encryption key. A PoC that sends no current-schema encryption key, or uses an empty default through an obsolete path, cannot yet be approved to hold a real user session.

### Functional effect

The PoC may fail or behave differently against the actual current TDLib build because the initialization contract is not aligned with current upstream documentation.

### Required remediation

- refresh PoC against one exact TDLib commit/version;
- generate/obtain a strong local database encryption key outside Git;
- inject it into current `setTdlibParameters` schema;
- remove obsolete authorization-state handling unless the pinned TDLib version actually requires it;
- never print/store the key in ordinary logs;
- document local key storage strategy; for later production use, move toward OS keychain/secret management.

**Gate:** blocks live authorization.

---

## SEC-2026-003 — Native tdjson library is trusted by path only

**Severity:** HIGH  
**Threat links:** S03, S13, S15  
**Component:** `poc/tdlib/tdjson_bridge.py`

`TdJsonBridge` resolves `TDJSON_LIBRARY` / `find_library("tdjson")` and directly calls `ctypes.CDLL`.

### Attack / failure scenario

If the local tdjson binary is replaced, downloaded from an untrusted build, or an unexpected loader path wins resolution, attacker-controlled native code executes with the same access as the PoC, including API credentials/session state.

### Required remediation

For PoC:
- pin exact TDLib upstream commit/tag;
- document trusted build source;
- record SHA-256 of built/downloaded tdjson binary in the PoC run report;
- display resolved library path and hash before authorization without leaking secrets;
- fail if operator has not explicitly approved the expected binary provenance.

For production later:
- SBOM/provenance/signature strategy;
- controlled package/build pipeline;
- version inventory and vulnerability lifecycle monitoring.

**Gate:** blocks live authorization until provenance is recorded.

---

## SEC-2026-004 — Dependabot alerts disabled

**Severity:** HIGH for intended lifecycle / currently lower exploit exposure  
**Threat links:** S01, S10, S26, S29  
**Surface:** GitHub repository security settings

`.github/dependabot.yml` exists, but the repository Dependabot alerts API returns:

```text
Dependabot alerts are disabled for this repository.
```

Version-update PR configuration is not equivalent to vulnerability alerting.

### Required remediation

Repository owner must enable the applicable GitHub dependency graph / Dependabot alerts settings and verify that security advisories can be surfaced. Automatic merge remains disabled; alerts/PRs require review and regression.

**Gate:** must be corrected before declaring M5 supply-chain monitoring ready. It does not by itself block local offline unit testing.

---

## SEC-2026-005 — Unbounded pending TDLib update queue

**Severity:** MEDIUM-HIGH  
**Threat links:** S16, S52  
**Component:** `poc/tdlib/client.py`

Unrelated updates received while waiting for a correlated response are appended to an unbounded `deque`.

### Failure scenario

A high-volume account/channel update stream plus a delayed request response can grow memory until the process becomes unstable.

### Required remediation

- explicit maximum pending-update count and/or memory/time policy;
- choose overflow behavior deliberately: spill-to-bounded local queue, process live updates concurrently, or fail explicitly;
- metric for dropped/deferred/queued updates;
- negative test with update burst.

**Gate:** must be fixed before multi-channel live stress/reliability testing.

---

## SEC-2026-006 — Exception text can bypass redaction

**Severity:** MEDIUM-HIGH  
**Threat links:** S07, S15  
**Component:** `father_osint/agent.py` and future live collectors

The orchestration layer persists:

```text
{collector.name}: {ExceptionType}: {str(exc)}
```

This is useful for debugging, but a third-party transport/library error may include request parameters, local paths, session identifiers, usernames, phone numbers or other sensitive values.

### Required remediation

- define structured collector failure objects or a centralized safe-error formatter;
- default user-facing/persisted error = stable category/code + sanitized message;
- raw diagnostics, if needed, stay local and access-controlled;
- add tests proving common Telegram credential fields are redacted if included in exception payload/message.

**Gate:** fix before live collector errors are persisted.

---

## SEC-2026-007 — DEV dependency builds are not reproducible

**Severity:** MEDIUM  
**Threat links:** S01, S03, S04, S10  
**Component:** `requirements-dev.txt`, CI

`pytest>=9.0,<10` allows an unseen new compatible version to enter a later clean CI run.

### Required remediation

Not urgent for current stdlib-only runtime, but before a broader dependency surface:
- adopt reviewed exact lock for CI/release baselines;
- optionally use hashes for high-assurance install paths;
- maintain a human-readable direct dependency declaration separately if desired;
- Dependabot proposes controlled lock updates.

**Gate:** SHOULD before M5 freeze; MUST before non-trivial runtime dependency set/release.

---

## SEC-2026-008 — No repository license declared

**Severity:** MEDIUM / legal-supply-chain  
**Threat links:** S14  
**Surface:** repository distribution/commercialization

GitHub repository metadata currently reports no detected license.

### Required remediation

Product owner/legal decision needed before external distribution/commercial reuse:
- choose project license or explicitly document proprietary/no-license intent;
- ensure donor-derived code/pattern usage remains compatible;
- maintain third-party notices/license inventory when external dependencies enter product baseline.

**Gate:** does not block TDLib technical PoC; blocks clean external product/reuse posture.

---

## SEC-2026-009 — GitHub security settings partly unverifiable from current integration

**Severity:** CONTROL GAP / UNVERIFIED  
**Threat links:** S06, S08, S26, S29  
**Surface:** GitHub repository settings

The current connector cannot attest:
- secret-scanning alert list/settings;
- push protection status;
- main branch protection/ruleset status.

The API returned permission/access errors. This must not be converted into a false claim that the features are either enabled or disabled.

### Required remediation

Repository owner verifies in GitHub UI/API with appropriate permissions:
- secret scanning;
- push protection where available;
- branch/ruleset protection for `main`;
- required status checks (DEV verification + CodeQL where appropriate);
- force-push/deletion policy;
- review requirement when team size grows.

**Gate:** verify before production/release baseline; secret-scanning status should be checked before first real credentials are used.

---

## 5. Current attack-surface assessment

| Surface | Current exposure | Audit state |
|---|---|---|
| Core Python runtime | stdlib-only, local deterministic | LOW / CONTROLLED DEV |
| GitHub Actions | two workflows; immutable action SHAs; least permissions visible | GOOD, monitor |
| Python dependency supply chain | pytest only, range pinned | SMALL but non-reproducible |
| Telegram live credentials | not yet used in approved run | **BLOCKED pending remediation** |
| TDLib native code | new PoC native trust boundary | **HIGH attention** |
| Telegram untrusted content | mapping only; no executable agent tools | LOW now / future HIGH |
| File parsers/OCR/media | not implemented | NOT YET APPLICABLE |
| LLM tool execution | not implemented | NOT YET APPLICABLE |
| Containers | not implemented | NOT YET APPLICABLE |
| External AI services | not active | NOT YET APPLICABLE |
| Knowledge Gate/KB | not implemented | NOT YET APPLICABLE |

---

## 6. Top-100 / threat-register reconciliation

Current M5 priority threats listed in the living register are appropriate. This audit materially changes the status/priority of:

- `S02` upstream/API freshness — **ACTIVE FINDING** via current TDLib API mismatch;
- `S03/S13` third-party/native provenance — **ACTIVE FINDING** for tdjson;
- `S06` credential/session in Git — **ACTIVE FINDING** due default runtime path mismatch;
- `S07` sensitive logs/errors — **ACTIVE FINDING** due generic exception persistence;
- `S15` Telegram transport/session security — **BLOCKED / ACTIVE**;
- `S16/S52` rate/resource exhaustion — **ACTIVE FINDING** due unbounded pending queue;
- `S26` findings tracked to closure — this report starts the evidence chain;
- `S29` post-baseline monitoring — **GAP** because Dependabot alerts are disabled.

Container, prompt-injection, SSRF, parser, RAG/KB and model-supply-chain controls remain monitored future controls and are not current defects because those surfaces do not yet exist.

---

## 7. Mandatory remediation order

### Wave A — before any real Telegram credentials/session

1. **SEC-2026-001** fix runtime path / ignore mismatch.
2. **SEC-2026-002** align TDLib initialization with pinned current upstream and require non-empty database encryption key.
3. **SEC-2026-003** pin and record tdjson binary provenance/hash before load/use.
4. **SEC-2026-006** sanitize persisted collector errors.
5. verify GitHub secret scanning / push protection status from owner settings.

### Wave B — before live multi-channel/restart/reliability tests

6. **SEC-2026-005** bound pending update memory.
7. enable **Dependabot alerts** and verify dependency monitoring.
8. re-run unit/regression/CodeQL.

### Wave C — before M5 freeze / product baseline

9. decide reproducible dependency lock approach.
10. decide repository/license posture.
11. verify main branch protection/ruleset and required checks.
12. generate first dependency/native binary inventory for M5 baseline.

---

## 8. Security Gate

```text
DEV v1 regression                 PASS
CodeQL                             PASS
Current core dependency surface    LOW
GitHub Action pinning              PASS
TDLib session-path safety          FAIL
TDLib current API/encryption       FAIL
Native tdjson provenance           FAIL
Generic error redaction            FAIL / incomplete
Pending-update resource bound      FAIL / incomplete
Dependabot vulnerability alerts    FAIL / disabled
Secret scanning / branch rules     UNVERIFIED

FINAL SECURITY GATE:
STOP → REMEDIATE → REVERIFY → THEN LIVE TDLib POC
```

No production/core redesign is required. The correct response is a small set of targeted security fixes at the PoC and repository-control boundaries.

---

## 9. Reverification evidence required

The gate can move to `CONDITIONAL PASS FOR LOCAL LIVE POC` only when evidence shows:

- default TDLib runtime location cannot be accidentally tracked;
- current pinned TDLib schema is implemented and database encryption key is non-empty and externally supplied/generated;
- exact tdjson source/version/hash is recorded before authorization;
- persisted transport/collector errors cannot expose known secret fields;
- pending update queue has an explicit resource bound;
- Dependabot alerts are enabled or an equivalent approved vulnerability-monitoring control exists;
- DEV regression remains green;
- CodeQL remains green;
- security owner has verified secret-scanning status before live credentials are entered.

After those checks, the next authorized activity is **POC-TD-01 local session bootstrap only**, followed by a security review of produced local state before public-channel acquisition.
