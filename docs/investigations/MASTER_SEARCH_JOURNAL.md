# Master OSINT Search Journal

**Repository:** `VictorKVS/OSINT_deepseek`  
**Journal date:** 2026-09-01  
**Change class:** documentation / provenance / no change to frozen DEV v1 implementation  
**Public status:** redacted public-source journal

## Consolidated case status

| Case | Subject | Stream 1: primary data | Stream 2: graph | Stream 3: attribution | Stream 4: risk | Stream 5: Red Team | Overall |
|---|---|---:|---:|---:|---:|---:|---:|
| `CASE-BY-0001` | Companies at Minsk, Naklonnaya St., 28 | `PASS` | `PASS/PARTIAL` | `PARTIAL` | `PASS` | `PASS` | `CLOSED` at preliminary management-decision scope |
| `CASE-BTC-0001` | BTC `1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75` | `BLOCKED/PENDING` | `PENDING` | `NO_HIT/PARTIAL` | `PARTIAL` | `PASS` for current caveats | `IN_PROGRESS` |
| `CASE-TRON-0001` | TRON `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF` | `PARTIAL` | `PARTIAL` | `NO_HIT/PARTIAL` | `PARTIAL` | `REVIEW` | `IN_PROGRESS` |

## Five parallel workstreams

1. **Primary/on-chain collection** — balances, transfers, transaction chronology, token activity, counterparties and raw identifiers.
2. **Graph and clustering** — first-hop and controlled multi-hop relations, recurring counterparties, consolidation/sweep patterns and service clusters.
3. **Off-chain attribution** — exact-string searches, public labels, websites, forums, social networks, public court/registry records and address reuse.
4. **Risk and abuse review** — public sanctions, scam/abuse reports, ransomware/extortion/hack references and exposure to labeled services.
5. **Red Team and source control** — false-positive search, entity-resolution challenges, source reliability, limitations and report wording.

## Current verified results

### CASE-BY-0001

- `PASS` — two key interrelated legal entities were resolved at the supplied address, with separate registration identifiers.
- `PASS` — the primary observable function of the export entity is wholesale/export trade in chemical products.
- `PASS` — direct Polish national sanctions exposure is documented by Polish official sources.
- `PASS` — the official package separates Polish national measures from EU-wide listing and separates administrative findings from criminal guilt.
- `NO_HIT` — no substantiated public-source finding of terrorism, extremism, narcotics trafficking or unlawful arms trafficking was identified in the checked corpus.
- `CLOSED` — case closed at the approved preliminary management-decision scope; reopen only for a concrete transaction, new source or formal tasking.

### CASE-BTC-0001

- `PASS` — the address passes Base58Check validation.
- `PASS` — version byte `0x00`; address class: Bitcoin mainnet legacy P2PKH.
- `PASS` — hash160: `7ff2913a5fe25f64330b2080b7501ecc44a0c3e1`.
- `NO_HIT` — exact-string public web and GitHub searches did not return a reliable owner label or off-chain identity.
- `BLOCKED` — current primary on-chain statistics have not yet been archived from two independent explorers; Google Sheets external import requires manual authorization and is not evidence.
- `PENDING` — balance, confirmed/unconfirmed transaction count, lifetime received/sent totals, UTXO set, first/last activity, counterparty graph and clustering.

### CASE-TRON-0001

- `PASS` — the address passes Base58Check validation for TRON mainnet.
- `PASS` — decoded payload: `41d9c925989c89b8ddcb6f68e2f76c3534c0439a4a`.
- `PASS` — confirmed TRC-20 USDT transfer of `820 USDT` from `TJDnKdo9kaM6yVPEwb93Y2ER6gZLR37MFb`; txid `36c2996f0e40b9531b687eb818885f6d612d3fbc4f50e12aa94f374028160131`; block `83609827`; timestamp `2026-06-15 04:46:51 UTC`; source: TRONSCAN transaction page.
- `PARTIAL` — secondary monitoring source reports a `600,000 USDT` incoming transfer from `TBBc6QRDkyP4wYmWjBcoGYrGra2jRY9c14` on 2026-06-14; txid and primary explorer confirmation remain pending.
- `NO_HIT` — no reliable public owner/service label was found in exact-string searches completed to date.
- `REVIEW` — prior working documents contained an incorrect decoded hex payload; the corrected value above must replace it everywhere before final delivery.
- `PENDING` — full TRX/TRC-20 history, token holdings, outgoing movement, counterparties, timing/amount clusters, contract interactions, labels and entity-type probability.

## Priority queue

| Priority | Case | Action | Result target |
|---:|---|---|---|
| 1 | `CASE-TRON-0001` | Obtain full primary account and TRC-20 history from TRONSCAN/TronGrid or independent node-backed source | Complete transaction inventory and correct all statistics |
| 2 | `CASE-TRON-0001` | Resolve txid for the reported `600,000 USDT` transfer | Promote or reject secondary lead |
| 3 | `CASE-BTC-0001` | Obtain address summary and transaction list from at least two independent node-backed explorers | Balance, counts, totals, chronology and UTXOs |
| 4 | Both wallets | Build first-hop counterparties and identify recurring service labels | Attribution-relevant graph |
| 5 | Both wallets | Exact-string and contextual off-chain search for wallet reuse | Owner/platform/person evidence |
| 6 | Both wallets | Red Team review of service-vs-person attribution | Defensible probability assessment |

## Production rule

No wallet is attributed to a person, company, exchange, merchant, OTC desk or other platform solely because of transaction volume or one labeled counterparty. Attribution requires a documented bridge such as a public label, signed statement, deposit-page publication, court filing, service disclosure, repeated operational pattern plus corroboration, or another independently verifiable identifier.

## Next journal update

The next commit must record actual primary on-chain values, explorer URL(s), collection timestamp, raw capture hash/location, any labels observed, and the disposition of each attribution hypothesis.
