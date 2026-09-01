# CASE-BTC-0001 — Search Journal

**Subject:** Bitcoin address `1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75`  
**Task:** collect and structure public data/statistics; isolate attribution-relevant facts; estimate whether the controller is more likely an organization/platform or an individual.  
**Current disposition:** `IN_PROGRESS`  
**Public journal:** redacted public-source record; no private keys, seed material or restricted data.

## Five-stream status

| Stream | Scope | Status | Current result |
|---|---|---:|---|
| 1 | Primary on-chain statistics and chronology | `BLOCKED/PENDING` | Address syntax is validated; complete node-backed address summary and transaction inventory have not yet been archived. |
| 2 | Counterparties, clustering and graph | `PENDING` | Cannot be completed reliably before primary transaction inventory. |
| 3 | Off-chain attribution | `NO_HIT/PARTIAL` | Exact-string public web and GitHub searches returned no reliable identity or service label. |
| 4 | Abuse, sanctions and risk | `PARTIAL` | No reliable exact-address abuse/sanctions attribution found in completed searches; broader counterparty screening awaits graph extraction. |
| 5 | Red Team and source control | `PASS` for current scope | Invalid inference from address format/volume alone is expressly rejected. |

## Validated technical facts

| Fact | Result | Grade |
|---|---:|---:|
| Base58Check checksum | `PASS` | A (deterministic validation) |
| Network/version byte | `0x00` | A |
| Address family | Bitcoin mainnet legacy `P2PKH` | A |
| Payload hash160 | `7ff2913a5fe25f64330b2080b7501ecc44a0c3e1` | A |
| Checksum | `9b4ab1e0` | A |

The address format does **not** identify a wallet application, exchange, person, country, device, ownership model or lawful/unlawful purpose.

## Search log

| Entry | Result | Query / action | Source or tool | Result summary | Next pivot |
|---|---:|---|---|---|---|
| BTC-0001 | `PASS` | Decode and validate Base58Check | deterministic local validation | Valid Bitcoin mainnet P2PKH address; technical fields recorded above. | Preserve validation fixture. |
| BTC-0002 | `NO_HIT` | Exact query: `"1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75"` | public web search | No indexed result linking the address to a named person, company, service or event. | Repeat across archives, forums, code, paste-like and legal sources. |
| BTC-0003 | `NO_HIT` | Exact query with terms `Bitcoin`, `balance`, `transaction`, `wallet` | public web search | No reliable indexed address-specific page or attribution hit returned. | Obtain explorer data directly. |
| BTC-0004 | `NO_HIT` | Exact address search in GitHub code | GitHub search | No relevant public code/document match. | Re-run after searching hashes/txids discovered on-chain. |
| BTC-0005 | `BLOCKED` | `IMPORTDATA` from Blockchain.info address endpoints | Google Sheets working file | External data fetch requires manual user authorization; `#REF!` is not evidence. | Do not cite sheet; collect through an approved API/worker or browser export. |
| BTC-0006 | `BLOCKED` | Direct API collection from Blockstream/Mempool/Blockchain.info in current runtime | current web/runtime boundary | Exact endpoint output was not acquired as a preservable primary capture. | Use local worker, authenticated connector, browser export or node-backed API. |
| BTC-0007 | `REJECTED` | Hypothesis: legacy `1...` address implies an old private user | Red Team | Address type only reflects script/address encoding; services may also use P2PKH. | Do not score entity type from prefix alone. |
| BTC-0008 | `REJECTED` | Hypothesis: no search hit means unused or anonymous owner | Red Team | Search-index absence does not establish transaction inactivity or deliberate concealment. | Resolve on-chain history first. |

## Required primary collection fields

The next accepted collection must record, from at least two independent node-backed sources:

```text
confirmed balance
mempool delta
confirmed transaction count
mempool transaction count
total funded outputs
total spent outputs
lifetime received and sent
current UTXO set
first activity block/time
last activity block/time
all txids or reproducible pagination cursor
collection timestamp UTC
source URL/API version
raw capture hash and restricted storage location
```

## Attribution-relevant features to calculate after collection

- one-time receipt/spend versus repeated use;
- fan-in and fan-out;
- regularity and time-of-day pattern;
- amount quantization/round-number behavior;
- consolidation and sweeping behavior;
- change-address structure;
- recurring counterparties;
- common-input ownership candidates, with CoinJoin/payjoin false-positive controls;
- exposure to publicly labeled exchanges, payment processors, mining pools, gambling services, mixers, ransomware/extortion or donation pages;
- exact address reuse in invoices, websites, forums, source code, court records, leak reports and archived pages.

## Current entity-type assessment

`NOT SCORED`.

Any numerical probability would presently be presentation without evidence because transaction history and counterparties have not been collected. The final score must cite the features that move probability toward:

- custodial platform/deposit address;
- merchant/payment address;
- organization treasury;
- individual self-custody;
- automated service or collection address.

## Current conclusion

The only defensible findings are that the address is technically valid and presently lacks a reliable indexed public attribution in the searches completed. On-chain statistics, behavioral classification and controller probability remain open tasks.
