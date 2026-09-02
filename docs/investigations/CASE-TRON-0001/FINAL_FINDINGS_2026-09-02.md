# CASE-TRON-0001 — Final findings — 2026-09-02

**Subject:** `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF`  
**Status:** `CLOSED_AT_OPEN_SOURCE_ATTRIBUTION_LEVEL / BRAND_IDENTITY_UNRESOLVED`

## Primary evidence

Official USDT contract: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`.

Complete TRONGrid pagination was captured in GitHub Actions run `33643733770`:

- artifact: `9851943581`;
- artifact SHA-256: `30de03059123cd5a7ed023cc84932395804aefa7f3011f78412c8153d0e38d4e`;
- 48 raw response pages + manifest + normalized analysis.

## Critical normalization finding

The endpoint returned `9,474` official-USDT TRC-20 events:

- `9,473` events with `type=Transfer`;
- `1` event with `type=Approval`.

Approval tx `90fe0a0d487b61f87ec791ef99004a27a677723c8fae55300abb91f70c1073ee` contains value equal to maximum `uint256` (`2^256 - 1`). It is an allowance, not a money transfer. Summing it as USDT would create a false outgoing volume of about `1.1579e71 USDT`.

**P0 rule:** financial flow calculations MUST filter event type. `Transfer` may enter token-flow accounting; `Approval`/allowance events must be stored separately.

## Verified official-USDT Transfer statistics

Observation window: `2026-06-11 10:44:45 UTC` through `2026-06-21 22:18:33 UTC` (~10.48 days).

- Transfer events: `9,473`;
- incoming transfers: `9,033`;
- outgoing transfers: `440`;
- unique incoming senders: `8,863`;
- unique outgoing recipients: `4`;
- incoming volume: `77,702,995.808781 USDT`;
- outgoing volume: `77,702,995.000000 USDT`;
- transfer-flow difference: `+0.808781 USDT`;
- largest incoming: `754,980 USDT`;
- largest outgoing: `940,000 USDT`;
- median incoming: `1,386 USDT`;
- mean incoming: ~`8,602 USDT`;
- one-time incoming senders: `8,735 / 8,863` (~`98.56%`).

## Confirmed reference transfers

### 600,000 USDT

- txid: `7092e095be109ec6de8cdb856d0a030b1b87cfe2cbfa8917a5da2c62e81c58a4`;
- from: `TBBc6QRDkyP4wYmWjBcoGYrGra2jRY9c14`;
- to: target;
- amount: `600,000 USDT`;
- time: `2026-06-13 15:23:57 UTC`.

This promotes the previous secondary-monitoring lead to `FACT`.

### 820 USDT

- txid: `36c2996f0e40b9531b687eb818885f6d612d3fbc4f50e12aa94f374028160131`;
- from: `TJDnKdo9kaM6yVPEwb93Y2ER6gZLR37MFb`;
- to: target;
- amount: `820 USDT`;
- time: `2026-06-15 04:46:51 UTC`.

Time between the 600k and this 820 event: `37h 22m 54s`.

Four additional incoming transfers of exactly `820 USDT` from different senders exist in the complete transfer set; therefore `820` is not a unique attribution key.

## Sweep pattern

Main outgoing recipient: `TXjjw736ii8mkei7ubXSRjfyyc2hxibXSA`.

- transfers to it: `433 / 440` outgoing transfers;
- amount: `77,537,340 USDT`;
- share of outgoing volume: `99.7868%`;
- median sweep amount: `145,000 USDT`;
- mean sweep amount: ~`179,070 USDT`;
- median interval: ~`17.7 minutes`;
- mean interval: ~`34.9 minutes`.

Other outgoing recipients:

- `TSgV3q2EzdWTcTQ8SgScTwQJVeSbHoceXK`: `165,000 USDT`;
- `TKgFnt86i9uMHFP9bRY4371LdDU5n2kWwt`: `500 USDT`;
- `TPwezUWpEGmFBENNWJHwXHRG1D2NCEEt5s`: `155 USDT` across 4 transfers; TRONSCAN publicly labels this contract `Bridgers: Cross-chain Bridge`.

## Attribution logic

1. Thousands of incoming transfers from almost nine thousand unique senders are inconsistent with a normal personal wallet profile.
2. Incoming and outgoing volumes nearly match: the address functions as a pass-through/collection node, not an accumulator.
3. `99.7868%` of outgoing value is swept to one address with regular cadence measured in tens of minutes.
4. The graph compresses `8,863` incoming senders into `4` outgoing recipients — a strong centralized collection/settlement signature.
5. The activity window is short and extremely intensive, consistent with operational wallet rotation.
6. No reliable public brand label was found for the target or the main sweep recipient, so a specific company/platform name is not asserted.

## Probability by assignment category

- web platform / payment or crypto service operating a collection/sweep wallet: **60%**;
- organization / merchant / OTC / settlement operator with automated infrastructure: **38%**;
- ordinary individual self-custody wallet: **2%**.

Combined institutional/service probability: ~**98%**.

Confidence is `HIGH` for institutional/service vs ordinary personal wallet, and `MEDIUM` for platform vs other organization because a reliable public brand identity is still absent.

## Unresolved

`NOT_CONFIRMED`: specific company/brand, legal entity, individual beneficiary, KYC identity, purpose of every incoming payment, customer economic ownership, fiat endpoint.

## Method improvements

- `P0`: normalize timestamps to UTC while preserving source-local timezone.
- `P0`: enforce TRC-20 event-type filtering (`Transfer != Approval`).
- `P0`: save raw responses, URL, timestamp and SHA-256.
- `P1`: calculate sender singleton ratio, in/out degree, flow concentration, sweep cadence and address lifecycle automatically.
- `P1`: classify graph roles (`source / collector / sweep / treasury / service endpoint`) with confidence and evidence provenance.
