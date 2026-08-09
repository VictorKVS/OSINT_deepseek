# Stage 06 — Telegram Experiment Audit

**Scope:** `telegram_bridge/` and `father_osint/transports/teleproto.py`  
**Status:** reviewed for M2 repository rationalization

## 1. Why this exists

The current FATHER OSINT DEV baseline already has a transport-neutral `TelegramCollector` contract. The repository also contains one concrete live-transport experiment: a Python subprocess adapter (`TeleprotoTransport`) calling a Node.js bridge using the `teleproto` package.

That implementation was created before the current transport-selection gate was complete.

## 2. Current implementation

```text
ResearchTask
   ↓
TelegramCollector
   ↓
TeleprotoTransport (Python)
   ↓ subprocess
telegram_bridge/teleproto_search.mjs
   ↓
Node.js + teleproto
   ↓
Telegram MTProto
```

The bridge requires environment secrets (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_STRING_SESSION`) and a channel list, then returns JSON messages to Python.

## 3. Findings

### F-01 — This is a transport experiment, not an approved architecture decision

The existence of code does not prove production fit. No benchmark/ADR has yet approved `teleproto` against the current candidate set (for example TDLib or another maintained MTProto approach).

### F-02 — The current DEV product does not depend on it

The current CI baseline, fixture collectors, Telegram collector contract, Analyst/Socrates DEV loop and canonical runners execute without Node.js, Telegram credentials or the bridge.

### F-03 — It introduces a second runtime prematurely

Keeping the experiment in the active product tree creates implicit maintenance obligations for:
- Node.js runtime;
- npm dependency lifecycle;
- subprocess behavior;
- Telegram session secrets;
- live-network error handling;
- rate/flood handling;
- transport-specific security review.

None of these are required to prove current DEV contracts.

### F-04 — The useful asset is the boundary, not this implementation

`TelegramCollector` depends on a small `TelegramTransport` protocol. This is the correct architecture because a later donor/benchmark cycle can plug in the selected transport without changing OSINT material semantics.

## 4. Decision

**REMOVE THE CONCRETE TELEPROTO EXPERIMENT FROM THE ACTIVE REPOSITORY.**

Keep:
- `TelegramCollector` contract;
- transport-neutral tests;
- donor/technology research documents;
- requirement that future live Telegram transport must pass SOURCE_VERIFIED → TECHNICALLY_VERIFIED → BENCHMARKED → APPROVED.

Remove:
- `father_osint/transports/teleproto.py`;
- `telegram_bridge/teleproto_search.mjs`;
- `telegram_bridge/package.json`;
- bridge README;
- export of `TeleprotoTransport` from `father_osint/transports/__init__.py`.

The `father_osint/transports/` package may remain as an explicit future boundary, but without an approved concrete implementation.

## 5. WHY remove instead of keep/defer in place

A deferred implementation inside the active tree still biases future engineers toward it and makes the repository appear to support a production transport it has never accepted. Git history already preserves the PoC if it needs to be inspected later.

This follows the FATHER rule:

```text
requirement
  ↓
donor review
  ↓
ADR / benchmark
  ↓
approved transport
  ↓
implementation
```

not:

```text
existing PoC
  ↓
therefore architecture
```

## 6. Verification gate

After removal:
1. clean GitHub Actions checkout;
2. import check;
3. full pytest;
4. `run_dev_osint.py`;
5. `run_dev_pipeline.py`.

If all pass, the current DEV product is proven independent from this experimental transport.
