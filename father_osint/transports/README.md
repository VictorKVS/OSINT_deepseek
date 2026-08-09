# Transports

**Status:** FUTURE INTEGRATION BOUNDARY / NO APPROVED IMPLEMENTATION.

Transport adapters implement external protocol/library mechanics under collectors. The current DEV baseline intentionally has no concrete live transport implementation.

```text
Collector contract
    ↓
Transport adapter selected by ADR/benchmark
    ↓
External protocol/library
```

The earlier `TeleprotoTransport` / Node bridge PoC was removed during Stage 06 after audit because it had never passed the required donor review, benchmark, security review and ADR gate.

The architecture keeps this package boundary so a future approved transport can be added without changing `TelegramCollector` or material/provenance semantics.

## Gate for adding a transport

```text
requirement
  ↓
SOURCE_VERIFIED donor review
  ↓
TECHNICALLY_VERIFIED PoC
  ↓
BENCHMARKED
  ↓
security / operational review
  ↓
ADR APPROVED
  ↓
implementation here
```

No concrete transport is production-approved merely because a library or PoC exists.
