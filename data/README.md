# Data

This directory currently contains **development fixtures only**. Test data is not intelligence evidence and is not Knowledge Base content.

## Current DEV chain

```text
test scenario
    ↓
prepared fixture
    ↓
FixtureCollector
    ↓
Material
    ↓
MaterialStore
    ↓
MaterialPackage
    ↓
asserted test result
```

`data/dev/` is deterministic input for development and acceptance testing. Its purpose is reproducibility without live Telegram/API/network dependencies.

## Critical invariant

> **Fixture data proves software behavior, not world truth.**

Some fixture records intentionally look realistic and may contain real-looking locators, technology names and dates. They must never be promoted to verified intelligence simply because the text resembles a real source.

Future fixture growth should use an explicit fixture convention/schema (for example scenario ID and synthetic/fixture marker) after the corresponding test requirement is approved.

## What must not be stored here

Do not place production/raw downloaded OSINT evidence into `data/dev/`.

Production evidence storage is a separate future architecture problem and must cover source observations, immutable/raw payloads, hashes, acquisition time, provenance, retention, quarantine, access control and legal/privacy requirements.

See `docs/06_verification/08_CONFIG_DATA_AUDIT.md` for the current boundary decision.
