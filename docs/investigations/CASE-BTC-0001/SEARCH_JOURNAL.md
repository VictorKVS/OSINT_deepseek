# CASE-BTC-0001 — Search Journal

**Subject:** Bitcoin address `1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75`  
**Task:** collect and structure public data/statistics; isolate attribution-relevant facts; estimate whether the controller is more likely an organization/platform or an individual.  
**Current disposition:** `CLOSED_AT_OPEN_SOURCE_ACTIVITY_ATTRIBUTION_LEVEL / IDENTITY_UNRESOLVED`  
**Public journal:** redacted public-source record; no private keys, seed material or restricted data.

## Closure status

| Stream | Scope | Status | Final result |
|---|---|---:|---|
| 1 | Primary on-chain statistics and chronology | `PASS` | 27 confirmed tx; 0.09119321 BTC received and spent; zero final balance; activity 2016-03-30 to 2016-05-17. |
| 2 | Counterparties, clustering and graph | `PASS WITH HEURISTIC CAVEAT` | WalletExplorer cluster `[00421c7e25]`: 29 addresses / 65 tx; downstream split/reconvergence traced; SatoshiDice service path verified. |
| 3 | Off-chain attribution | `PASS FOR ACTIVITY TYPE / NO_HIT FOR IDENTITY` | Repeated user-side SatoshiDice activity is high-confidence; no reliable real-world identity found. |
| 4 | Abuse, sanctions and risk | `PUBLIC_INDEXED_CHECK COMPLETE` | Exact target returned `NO_INDEXED_MATCH_FOUND` in scoped OFAC/BitcoinAbuse/Chainabuse/BitcoinWhosWho searches; not a clean certification. |
| 5 | Red Team and source control | `PASS` | Wallet-delta vs direct-service-flow accounting corrected; bot use and identity not overstated. |

## Validated technical facts

| Fact | Result | Grade |
|---|---:|---:|
| Base58Check checksum | `PASS` | A |
| Network/version byte | `0x00` | A |
| Address family | Bitcoin mainnet legacy `P2PKH` | A |
| Payload hash160 | `7ff2913a5fe25f64330b2080b7501ecc44a0c3e1` | A |
| Confirmed transactions | `27` | A/B independently cross-checked |
| Lifetime received | `0.09119321 BTC` | A/B |
| Lifetime sent | `0.09119321 BTC` | A/B |
| Final balance | `0 BTC` | A/B |

## Wallet-cluster findings

WalletExplorer places the address in unlabeled wallet cluster `00421c7e25459ed4` / `[00421c7e25]`:

- 29 addresses;
- 65 transactions;
- activity `2016-03-30` through `2016-05-18`;
- received externally `0.90805818 BTC`;
- sent externally `0.90507183 BTC`;
- fees `0.00298635 BTC`;
- final balance `0 BTC`.

The cluster is an analytical heuristic and is not legal proof of one owner.

## SatoshiDice evidence and Red Team correction

Verified direct service flow:

- 21 direct betting outputs to independently labeled `SatoshiDice.com-original` addresses: `0.506111 BTC`;
- 21 service-only incoming transactions from SatoshiDice: `0.37109417 BTC`;
- direct service-flow difference: `-0.13501683 BTC` before network fees.

**Rejected metric:** `0.69013308 BTC` wallet-level outflow across SatoshiDice-labeled rows is not the total bet amount. One mixed-destination transaction sent only `0.02000000 BTC` to SatoshiDice and `0.20402208 BTC` elsewhere; most of the latter later returned to the investigated cluster. Therefore the earlier derived `-0.31903891 BTC` gambling P&L is invalid and superseded.

Canonical correction: `EVIDENCE_009_SATOSHIDICE_FLOW_ACCOUNTING_2026-09-02.md`.

## Downstream graph

After the original cluster closed, the final balance moved to `[f915b4559c]`, split into `[b57bb19d60]` and `[0e5cad0da4]`, then reconverged into `[130e06a98b]`. A later branch `[0be397ba68]` again sent funds to SatoshiDice. `[0e5cad0da4]` has earlier history involving PrimeDice, SatoshiDice and ChangeTip.

This supports a continuing related gambling-network motif but does not establish one legal owner or a fiat cash-out endpoint.

## Final activity-type assessment

**FACT:** the address belongs to a small unlabeled wallet cluster with repeated, quantified, bidirectional SatoshiDice interactions.

**HYPOTHESIS — HIGH CONFIDENCE:** the target is on the **user/client side of a Bitcoin gambling wallet/network**, potentially manual or automated.

Assignment-category estimate:

- individual/user self-custody or automated wallet acting for one user: 85%;
- small organization/operator with own automation or linked wallets: 10%;
- web platform/exchange/custodial service as direct controller: 5%.

`NOT_CONFIRMED`: real-world controller, legal entity, bot use, IP/geography/device, KYC identity, final fiat cash-out, legal common ownership of all connected unlabeled clusters.

## Closure artifacts

- `FINAL_FINDINGS_2026-09-02.md`
- `WORKLOG_2026-09-02.md`
- `EVIDENCE_008_PEEL_ROUTING_2026-09-02.md`
- `EVIDENCE_009_SATOSHIDICE_FLOW_ACCOUNTING_2026-09-02.md`

## Closure decision

The requested open-source task is complete. No owner identity is asserted without a new independent off-chain identity edge.
