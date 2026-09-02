# CASE-TRON-0001 — Search Journal

**Subject:** TRON address `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF`  
**Task:** collect and structure public data/statistics; isolate attribution-relevant facts; estimate whether the controller is more likely an organization/platform or an individual.  
**Current disposition:** `CLOSED_AT_OPEN_SOURCE_ATTRIBUTION_LEVEL / BRAND_IDENTITY_UNRESOLVED`  
**Public journal:** redacted public-source record.

## Closure status

| Stream | Scope | Status | Final result |
|---|---|---:|---|
| 1 | Primary on-chain statistics and chronology | `PASS` | Complete official-USDT TRONGrid pagination captured: 48 pages, 9,474 events; 9,473 Transfer + 1 Approval. |
| 2 | Counterparties, clustering and graph | `PASS` | 9,033 incoming transfers from 8,863 senders; 440 outgoing to 4 recipients; main sweep endpoint receives 99.7868% of outgoing value. |
| 3 | Off-chain attribution | `PASS FOR INFRASTRUCTURE TYPE / NO_HIT FOR BRAND` | Strong collection/sweep service pattern; no reliable public brand/legal-entity label found for target or main sweep address. |
| 4 | Abuse, sanctions and risk | `PUBLIC OPEN-SOURCE REVIEW COMPLETE` | No final public adverse brand/identity attribution established; identity/KYC remains outside open-source scope. |
| 5 | Red Team and source control | `PASS` | Incorrect address decode corrected; spam/fake-token risk isolated; Approval max-uint256 excluded from money-flow accounting. |

## Deterministic address validation

| Fact | Result | Grade |
|---|---:|---:|
| Base58Check checksum | `PASS` | A |
| TRON mainnet prefix | `0x41` | A |
| Decoded payload | `41d9c925989c89b8ddcb6f68e2f76c3534c0439a4a` | A |
| Checksum | `c76d5cd4` | A |

A prior working payload was incorrect and is superseded.

## Official USDT evidence set

Official Tether TRC-20 contract: `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`.

Complete pagination was captured in GitHub Actions run `33643733770`:

- artifact `9851943581`;
- artifact SHA-256 `30de03059123cd5a7ed023cc84932395804aefa7f3011f78412c8153d0e38d4e`;
- 48 raw response pages + manifest + normalized analysis.

### P0 normalization correction

The endpoint returned `9,474` events for the official USDT contract:

- `9,473` with `type=Transfer`;
- `1` with `type=Approval`.

Approval tx `90fe0a0d487b61f87ec791ef99004a27a677723c8fae55300abb91f70c1073ee` carries maximum `uint256` allowance and is **not** a money transfer. It must be excluded from USDT volume. This closes the earlier false-zero/false-huge-volume normalization risk.

## Verified official-USDT Transfer statistics

Observation window: `2026-06-11 10:44:45 UTC` through `2026-06-21 22:18:33 UTC` (~10.48 days).

- Transfer events: `9,473`;
- incoming: `9,033`;
- outgoing: `440`;
- unique incoming senders: `8,863`;
- unique outgoing recipients: `4`;
- incoming volume: `77,702,995.808781 USDT`;
- outgoing volume: `77,702,995.000000 USDT`;
- flow difference: `+0.808781 USDT`;
- largest incoming: `754,980 USDT`;
- largest outgoing: `940,000 USDT`;
- median incoming: `1,386 USDT`;
- mean incoming: ~`8,602 USDT`;
- one-time incoming senders: `8,735 / 8,863` (~`98.56%`).

## Reference transfers promoted to FACT

### 600,000 USDT

- txid `7092e095be109ec6de8cdb856d0a030b1b87cfe2cbfa8917a5da2c62e81c58a4`;
- from `TBBc6QRDkyP4wYmWjBcoGYrGra2jRY9c14`;
- to target;
- amount `600,000 USDT`;
- time `2026-06-13 15:23:57 UTC`.

The earlier CoinGrab lead is now independently confirmed by primary TRONGrid data.

### 820 USDT

- txid `36c2996f0e40b9531b687eb818885f6d612d3fbc4f50e12aa94f374028160131`;
- from `TJDnKdo9kaM6yVPEwb93Y2ER6gZLR37MFb`;
- to target;
- amount `820 USDT`;
- time `2026-06-15 04:46:51 UTC`.

Four additional incoming transfers of exactly `820 USDT` from different senders exist, so the amount `820` is not a unique attribution key.

## Main sweep behavior

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

## Final attribution logic

1. Nearly nine thousand unique incoming senders in 10.48 days are inconsistent with an ordinary personal self-custody profile.
2. Incoming and outgoing USDT volumes nearly match; the address is a pass-through/collection node rather than an accumulator.
3. `99.7868%` of outgoing value is regularly swept to one next-hop address.
4. Graph compression is extreme: `8,863` incoming senders to `4` outgoing recipients.
5. The short, intense lifecycle is consistent with operational wallet rotation.
6. No reliable public brand label was found for target or main sweep recipient, so no specific company/platform is asserted.

Assignment-category estimate:

- web platform/payment/crypto service operating a collection/sweep wallet: **60%**;
- organization/merchant/OTC/settlement operator with automated infrastructure: **38%**;
- ordinary individual self-custody wallet: **2%**.

Combined institutional/service probability: ~**98%**.

Confidence: `HIGH` for institutional/service vs ordinary personal wallet; `MEDIUM` for platform vs other organization.

## Not confirmed / requires non-open-source authority

`NOT_CONFIRMED`:

- specific company/brand;
- legal entity;
- individual beneficiary;
- KYC identity;
- purpose of every incoming payment;
- customer economic ownership;
- final fiat endpoint.

## Closure artifacts

- `FINAL_FINDINGS_2026-09-02.md`
- Google Docs main analytical report and investigation journal
- GitHub Actions run `33643733770`, artifact `9851943581`

## Closure decision

The requested open-source task is complete. The target is assessed with high confidence as an automated centralized collection/sweep address. Specific brand/legal identity remains unresolved and is not guessed.
