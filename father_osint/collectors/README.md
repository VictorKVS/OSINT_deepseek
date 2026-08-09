# Collectors

Collectors convert source-facing results into the common `Material` contract. They do not analyze truth, select technologies or publish knowledge.

```text
ResearchTask
   ↓
Collector
   ↓
source acquisition
   ↓
Material
   ↓
OSINTAgent / MaterialStore
```

## Current files

- `dev.py` — fixture-based collector for deterministic DEV testing. **CURRENT DEV candidate.**
- `telegram.py` — transport-neutral Telegram mapping contract. **PROTOTYPE; test before approval.**

## Boundary

Collector = source semantics.  
Transport = protocol/library mechanics.

A collector may depend on a transport interface, but Analyst and Socrates must not depend on Telegram/HTTP/Tor-specific details.
