# TDLib PoC — local bootstrap

This directory is an isolated PoC. It does **not** approve TDLib for production and must not change the frozen FATHER domain contracts.

## Local prerequisites

- Python 3.12
- a locally built/installed TDLib `tdjson` shared library
- Telegram `api_id` and `api_hash` created for the local operator
- an account authorized for the PoC

Do not commit credentials or TDLib session/database files.

## Environment

Set locally only:

```bash
export TDJSON_LIBRARY=/absolute/path/to/libtdjson.so
export TELEGRAM_API_ID=123456
export TELEGRAM_API_HASH='...'
export FATHER_TDLIB_RUNTIME="$HOME/.father-osint/tdlib"
```

`TELEGRAM_PHONE_NUMBER` is optional. If omitted, the harness asks locally using hidden input. Authentication code and 2FA password are always requested interactively and are not printed.

## Bootstrap

From repository root:

```bash
python -m poc.tdlib.run_local
```

Expected result:

```text
TDLib authorization ready. Local PoC session initialized.
```

This proves only POC-TD-01 (session bootstrap). It does not prove history collection, checkpoint/restart, source isolation, rate handling or production readiness.

## Next PoC increment

After bootstrap succeeds locally, run the bounded public-channel harness to implement/measure POC-TD-02 through POC-TD-09. Exact public source handles belong in the run report, not in the architecture contract.

## Security rules

- never paste `api_hash`, login code, password or session database into issues/chat/logs;
- runtime/session directories stay outside Git;
- use a dedicated PoC runtime directory with restrictive local permissions where practical;
- if credentials are suspected exposed, revoke/rotate them before continuing;
- live Telegram authorization is intentionally not executed in shared GitHub Actions.
