# 2026-08-09 — M2 Telegram transport experiment cleanup

**Stage:** 06 — Verification and Repository Rationalization  
**Trigger / problem:** an unapproved Teleproto/Node Telegram transport PoC remained inside the active repository tree even though the current DEV baseline did not depend on it and no donor benchmark/ADR had approved it.  
**Decision:** remove the concrete PoC while preserving the transport-neutral `TelegramCollector` contract and the future `father_osint/transports/` boundary.  

## WHY

Keeping a deferred concrete transport in the active tree would create three problems:

1. it would visually bias future design toward `teleproto` merely because code already existed;
2. it would imply Node.js/npm/session-secret maintenance obligations that are not part of the current DEV contract;
3. it would invert the FATHER engineering chain from `requirement → review → benchmark → ADR → implementation` into `existing PoC → architecture`.

Git history preserves the experiment for later study, so deletion from the active tree does not destroy engineering history.

## Files/documents affected

Removed:
- `father_osint/transports/teleproto.py`
- `telegram_bridge/teleproto_search.mjs`
- `telegram_bridge/package.json`
- `telegram_bridge/README.md`

Changed:
- `father_osint/transports/__init__.py`
- `father_osint/transports/README.md`
- root `README.md`

Added:
- `docs/06_verification/12_TELEGRAM_EXPERIMENT_AUDIT.md`

## Evidence

Before removal, the current clean DEV baseline already passed without installing Node.js/teleproto or providing Telegram credentials.

After removal, GitHub Actions clean checkout again completed successfully:
- repository checkout: PASS;
- Python setup: PASS;
- DEV dependencies: PASS;
- current verification job: PASS.

The Telegram collector contract remains covered by transport-neutral tests.

## Result

**PASS**

The current product now has:

```text
TelegramCollector contract
        ↓
TelegramTransport protocol
        ↓
NO APPROVED CONCRETE IMPLEMENTATION YET
```

A future live transport must enter through the donor lifecycle and ADR/benchmark gate.

## New risks/open questions

- live Telegram transport still needs current donor verification and benchmark;
- session-secret handling, flood/rate behavior and runtime security are intentionally unresolved until the PROD/live-source requirement is approved.

## Next action

Continue M2 with `services/llm-gateway/`: decide whether it belongs in this repository as a frozen subproject or should be moved out entirely, based on dependency evidence and product boundaries.
