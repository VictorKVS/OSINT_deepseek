# 06. Автоматический backlog развития

## P0 — M3A Source Packs

1. `RU_COMPANY_CORE`
   - ФНС ЕГРЮЛ/ЕГРИП capture/download;
   - ГИР БО;
   - Федресурс;
   - арбитражные дела;
   - ЕИС закупок;
   - source cards, hashes, parser fixtures.
2. `GLOBAL_SANCTIONS_CORE`
   - UN XML;
   - OFAC downloadable lists;
   - UK CSV/XML;
   - EU dataset;
   - exact/fuzzy candidate separation and identifier review.
3. `PUBLIC_IDENTITY_CORE`
   - Sherlock/Maigret adapters;
   - profile existence validator;
   - account candidate merge without person attribution.
4. `PASSIVE_DOMAIN_CORE`
   - DNS/RDAP/certificate transparency/archive;
   - no active scan or brute force.

## P0 — M3B Windows↔Kali Bus

- typed envelope schema;
- file spool with atomic rename;
- idempotency and sequence checks;
- per-job directories;
- HMAC/Ed25519 signature policy;
- worker allowlist;
- result manifests and dead-letter queue;
- integration test with synthetic adapters.

## P1 — M3C Factory UI

- queue of requests;
- four profile cards;
- stage/wave visualization;
- checkboxes: Planned / Adapter / Smoke / Evidence / Normalized / Reviewed;
- coverage and blocking gaps;
- case deep links;
- analyst and decision-maker modes.

## P1 — M3D Monitoring

- schedule by risk tier;
- event-driven reruns;
- source list version watcher;
- change comparison with prior run;
- alert deduplication;
- reviewer assignment and SLA.

## P1 — Quality calibration

- labelled namesake fixtures;
- sanctions false-positive cases;
- company historical-name cases;
- profile account-attribution traps;
- duplicate/repost source families;
- precision, recall, rejection and rework statistics.

## P2 — Country Packs

Prioritize countries arising from real cases. Each pack must include:

```text
national company register
national insolvency and gazette
courts/regulators
securities filings
VAT/tax validation where lawful
procurement/debarment
language/transliteration rules
source terms and access constraints
```

No country is marked connected until a real smoke test, capture, parser test and source-governance review pass.
