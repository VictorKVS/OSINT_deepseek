# Transports

**Status:** EXPERIMENTAL / FROZEN FOR DEV ACCEPTANCE.

Transport adapters implement external protocol/library mechanics under collectors. They are deliberately excluded from the minimum DEV acceptance path.

```text
Collector contract
    ↓
Transport adapter
    ↓
External protocol/library
```

Current candidate:
- `teleproto.py` — experimental Telegram transport bridge adapter.

No transport is APPROVED for production merely because code exists. Transport selection later requires donor review, PoC, benchmark, security review and ADR.
