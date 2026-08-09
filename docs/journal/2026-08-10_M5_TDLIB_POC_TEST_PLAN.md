# Development Journal — M5 TDLib PoC Test Plan

**Date:** 2026-08-10  
**Stage:** 07 — M5 Telegram Radar  
**Result:** PASS — PoC test contract defined; product integration still blocked pending evidence.

## Trigger

Telegram Radar requirements and donor refresh produced two PoC candidates: TDLib first, GramJS second. The next risk was starting implementation before defining what a successful transport PoC must prove.

## Decision

Create a transport-neutral TDLib PoC test plan before adapter/product code.

Primary document:

`docs/07_next_requirement/04_TDLIB_POC_TEST_PLAN.md`

## WHY

A connection to Telegram is not sufficient evidence of production fit. The PoC must test the properties FATHER actually depends on:

- stable source/message identity;
- bounded history collection;
- provenance-preserving mapping;
- restart/checkpoint behavior;
- source isolation and timeouts;
- explicit rate-limit/retry behavior;
- session/secrets separation;
- compatibility with frozen DEV v1 contracts.

The same logical cases will later be applied to GramJS so the ADR compares observed behavior rather than project popularity or architectural preference.

## Important constraints

- 5–10 **public** channels only;
- exact source list verified immediately before execution;
- no private material or access-control bypass;
- no credentials/session data in Git or normal logs;
- no new confidence/reliability percentage without a defined denominator;
- no TDLib-specific object may leak above the `TelegramTransport` boundary;
- current 21-test DEV v1 baseline must remain green.

## Evidence required next

1. minimal TDLib adapter design;
2. isolated PoC harness;
3. redacted local configuration/session procedure;
4. execution on selected public test channels;
5. raw measurements and defects;
6. TDLib PoC run report;
7. equivalent GramJS PoC;
8. comparative security review + ADR.

## Next action

Design the **minimal TDLib adapter contract and PoC harness** against the already-existing `TelegramTransport` protocol. Do not modify upper-layer domain contracts unless the test plan proves a missing requirement.
