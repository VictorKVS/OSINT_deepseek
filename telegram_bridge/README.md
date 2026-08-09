# Telegram Bridge

**Status:** EXPERIMENTAL / DEFERRED FROM CURRENT DEV GATE.

This directory explores a real Telegram transport bridge. It is intentionally isolated from the simplified development proof.

```text
TelegramCollector
      ↓
TelegramTransport contract
      ↓
bridge / external MTProto implementation
      ↓
Telegram
```

The bridge is **not** required to accept OSINT Agent v1 in DEV mode. Real account sessions, API credentials, reconnect/rate-limit strategy, secret storage and operational monitoring belong to the later PROD/BATTLE gate.

Do not expand this directory until transport requirements and comparative PoC criteria are approved.
