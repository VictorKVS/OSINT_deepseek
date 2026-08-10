# TDLib PoC — local bootstrap

This directory is an isolated PoC. It does **not** approve TDLib for production and must not change the frozen FATHER domain contracts.

## Local prerequisites

- Python 3.12
- a locally built/installed TDLib `tdjson` shared library from the approved upstream/version
- Telegram `api_id` and `api_hash` created for the local operator
- a non-empty local TDLib database-encryption key
- an existing Telegram account authorized for the PoC

Do not commit credentials, encryption keys, native binaries or TDLib session/database files.

## Required local environment

Set locally only:

```bash
export TDJSON_LIBRARY=/absolute/path/to/libtdjson.so
export TDJSON_SHA256='<sha256-of-the-exact-approved-binary>'
export TELEGRAM_API_ID=123456
export TELEGRAM_API_HASH='...'
export FATHER_TDLIB_DB_KEY='...'
export FATHER_TDLIB_RUNTIME="$HOME/.father-osint/tdlib"
```

The harness refuses to load `tdjson` unless the exact file exists and its SHA-256 equals `TDJSON_SHA256`. Do not obtain the expected hash from the same untrusted location as an unknown binary; record the approved TDLib source/version and compute/verify the built artifact as part of the PoC evidence.

`TELEGRAM_PHONE_NUMBER` is optional. If omitted, the harness asks locally using hidden input. Authentication code, email code and 2FA password are requested interactively when TDLib asks for them and are not printed.

`FATHER_TDLIB_DB_KEY` must be non-empty and stable for the local database. For the PoC it is supplied outside Git. A production implementation will use an OS/application secret store rather than repository configuration.

The repository-default `.runtime/` path is ignored by Git, but an external runtime directory is still preferred.

## Bootstrap

From repository root:

```bash
python -m poc.tdlib.run_local
```

Expected result:

```text
Verified tdjson SHA-256: ...
TDLib authorization ready. Local PoC session initialized.
```

This proves only POC-TD-01 (session bootstrap). It does not prove history collection, checkpoint/restart, source isolation, rate handling or production readiness.

## Current API contract

The PoC follows current TDLib initialization semantics: `database_encryption_key` is passed in `setTdlibParameters`. The harness supports current phone/email/code/password authorization states and deliberately refuses automatic new-account registration.

## Next PoC increment

After bootstrap succeeds locally, run the bounded public-channel harness to implement/measure POC-TD-02 through POC-TD-09. Exact public source handles belong in the run report, not in the architecture contract.

## Security rules

- never paste `api_hash`, DB key, login code, email code, password or session database into issues/chat/logs;
- runtime/session directories stay outside Git;
- verify native-library provenance before any Telegram credential is used;
- use a dedicated PoC runtime directory with restrictive local permissions where practical;
- if credentials are suspected exposed, revoke/rotate them before continuing;
- live Telegram authorization is intentionally not executed in shared GitHub Actions;
- GitHub secret-scanning/push-protection state must be manually verified before the first live credential run because the current integration cannot read that repository setting.
