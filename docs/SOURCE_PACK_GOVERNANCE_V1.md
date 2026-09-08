# Source and country-pack governance

## Core rule

A source family in a plan is not equivalent to a connected adapter. Every source family has independent lifecycle data:

```text
PLANNED → CONTRACT_DEFINED → CONNECTED → SMOKE_TESTED
→ NORMALIZED → MERGE_TESTED → REVIEWED → PRODUCTION_APPROVED
```

## Required source-pack fields

- `source_id` and `source_family`;
- jurisdiction and language;
- official, commercial, media, archive or community class;
- access method;
- authentication requirement;
- terms/licence note;
- lawful-use note;
- request and rate limits;
- parser and adapter version;
- evidence-capture policy;
- expected freshness;
- last health check;
- known blind spots;
- fallback sources;
- access class;
- owner and reviewer;
- retirement/supersession state.

## Update control

Source endpoints, sanctions lists and registry interfaces can change without a code release. Therefore:

- source packs are versioned data;
- health status is measured, not assumed;
- stale packs block production approval;
- replacement sources do not silently rewrite old case provenance;
- every historical case retains the exact source-pack and adapter versions used.

## Legal and privacy controls

Public accessibility is not a universal permission to collect, combine, retain or publish data. Each case still needs purpose, proportionality, minimization, access restrictions, retention and export review.

Sensitive data, home addresses, private contact details and unsupported allegations must not enter public exports merely because a tool discovered them.
