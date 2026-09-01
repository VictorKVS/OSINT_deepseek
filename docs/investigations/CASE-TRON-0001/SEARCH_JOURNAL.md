# CASE-TRON-0001 — Search Journal

**Subject:** TRON address `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF`  
**Task:** collect and structure public data/statistics; isolate attribution-relevant facts; estimate whether the controller is more likely an organization/platform or an individual.  
**Current disposition:** `IN_PROGRESS`  
**Public journal:** redacted public-source record.

## Five-stream status

| Stream | Scope | Status | Current result |
|---|---|---:|---|
| 1 | Primary on-chain statistics and chronology | `PARTIAL` | Address validated; one incoming USDT transaction confirmed in TRONSCAN; complete account history remains pending. |
| 2 | Counterparties, clustering and graph | `PARTIAL` | Two incoming counterparties are leads; only one transfer is primary-source confirmed. |
| 3 | Off-chain attribution | `NO_HIT/PARTIAL` | No reliable owner/platform label found in completed exact-string searches. |
| 4 | Abuse, sanctions and risk | `PARTIAL` | No exact-address official sanctions/abuse label established; counterparty exposure cannot be completed without full graph. |
| 5 | Red Team and source control | `REVIEW/PASS` | A prior decoding error was detected and corrected; service-vs-person attribution remains unscored. |

## Validated technical facts

| Fact | Result | Grade |
|---|---:|---:|
| Base58Check checksum | `PASS` | A (deterministic validation) |
| TRON mainnet prefix | `0x41` | A |
| Decoded payload | `41d9c925989c89b8ddcb6f68e2f76c3534c0439a4a` | A |
| Checksum | `c76d5cd4` | A |

### Red Team correction

A prior working note used the incorrect payload `41da383c182b70b7d6c91487a4e5fb44d415fbec56`. That value does not decode from the supplied Base58Check address and must not appear in the final report. The corrected payload is recorded above.

## Primary confirmed transaction

| Field | Value |
|---|---|
| Result | `PASS` |
| Asset | USDT TRC-20 |
| Amount | `820 USDT` |
| From | `TJDnKdo9kaM6yVPEwb93Y2ER6gZLR37MFb` |
| To | `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF` |
| Txid | `36c2996f0e40b9531b687eb818885f6d612d3fbc4f50e12aa94f374028160131` |
| Block | `83609827` |
| Time | `2026-06-15 04:46:51 UTC` |
| Contract | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` (USDT) |
| Source | `https://tronscan.org/transaction/36c2996f0e40b9531b687eb818885f6d612d3fbc4f50e12aa94f374028160131/overview` |
| Evidence grade | A for the explorer-displayed transaction record |

The transaction proves only that the address received this token transfer. It does not identify the beneficial owner, purpose, underlying contract or off-chain payer/payee.

## Secondary large-transfer lead

| Field | Value |
|---|---|
| Result | `PARTIAL/REVIEW` |
| Reported asset | USDT |
| Reported amount | `600,000 USDT` |
| Reported from | `TBBc6QRDkyP4wYmWjBcoGYrGra2jRY9c14` |
| Reported to | `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF` |
| Reported time | `2026-06-14 00:23:57` in the source display |
| Source | `https://www.coingrab.net/tx2/?cur=&pp=89&ww=2022-02-07` |
| Evidence grade | C/B discovery lead |

This item must not be promoted to a confirmed fact until its txid is resolved and checked in TRONSCAN/TronGrid or another primary node-backed source. The page is a broad transaction monitor, not an authoritative account dossier.

## Search log

| Entry | Result | Query / action | Source or tool | Result summary | Next pivot |
|---|---:|---|---|---|---|
| TRON-0001 | `PASS` | Decode and validate Base58Check | deterministic local validation | Valid TRON mainnet address; corrected payload recorded. | Add validation fixture and regression test. |
| TRON-0002 | `PASS` | Verify txid `36c299...0131` | TRONSCAN | Successful 820 USDT incoming transfer confirmed. | Expand sender history and destination subsequent movement. |
| TRON-0003 | `PARTIAL` | Exact-address public web search | public search | One confirmed transaction page and one secondary large-transfer mention found; no owner label. | Obtain account overview and full history. |
| TRON-0004 | `PARTIAL/REVIEW` | Review reported 600,000 USDT transfer | Coingrab monitoring page | Source reports transfer to target address, but txid absent from current evidence package. | Resolve txid by time/from/to/amount. |
| TRON-0005 | `NO_HIT` | Search exact address for named owner, exchange, merchant or platform | public web/GitHub | No reliable attribution hit found in completed searches. | Search deposit pages, forums, Telegram, court documents, scam reports and archived sites. |
| TRON-0006 | `REJECTED` | Hypothesis: one 600,000 USDT receipt proves institutional ownership | Red Team | A high-value transaction may involve an individual, OTC settlement, exchange deposit, escrow, pass-through address or internal transfer. | Require recurring operational pattern and labels. |
| TRON-0007 | `REJECTED` | Hypothesis: an address receiving USDT controls the private key beneficially | Red Team | A platform-generated deposit address may be technically controlled by a custodian but economically associated with a customer. | Separate key controller, account holder and beneficial recipient. |
| TRON-0008 | `REVIEW` | Compare previously recorded hex payload with deterministic decode | Red Team | Prior payload was wrong and has been superseded. | Correct all Google Docs and future exports. |

## Mandatory next collection

The next accepted on-chain export must include:

```text
account creation/activation time
TRX balance and resource state
all TRC-20 holdings
complete TRX transaction history
complete TRC-20 transfer history
contract calls and approvals
incoming/outgoing totals by token
first and last activity
unique counterparties
recurring counterparties
sweep/consolidation events
transaction fees/resources
public labels/tags
collection timestamp UTC
API/explorer version
raw capture hash and restricted storage location
```

## Attribution-relevant analysis plan

- Determine whether incoming funds are rapidly swept to a recurring destination.
- Test whether deposit sizes are heterogeneous customer-like payments or bilateral settlements.
- Identify whether the address interacts with known exchange hot wallets, payment processors, OTC desks, gambling services, mixers, sanctions-listed entities or scam clusters.
- Search all exact counterparties, txids and time/amount pairs off-chain.
- Check whether the address is published on a website, invoice, Telegram channel, forum, donation page, bot, merchant page, court filing or law-enforcement notice.
- Separate technical key custody from economic/beneficial control.

## Current entity-type assessment

`NOT SCORED` for final reporting.

A provisional percentage would be premature because only one transaction is primary-source confirmed and the complete outgoing pattern is unknown. The final assessment should separately score:

1. custodial platform/deposit address;
2. business/merchant/OTC settlement address;
3. organization treasury;
4. individual self-custody;
5. automated collection or pass-through address.

## Current conclusion

The address is valid and has at least one confirmed incoming USDT transfer. A second, much larger incoming transfer is a material but unverified lead. No reliable public owner label is established. Full transaction history, outgoing behavior, counterparties and service labels are required before any defensible controller probability can be assigned.
