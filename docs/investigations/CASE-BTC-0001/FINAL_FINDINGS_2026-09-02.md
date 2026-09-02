# CASE-BTC-0001 — Final findings — 2026-09-02

**Subject:** `1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75`  
**Status:** `CLOSED_AT_OPEN_SOURCE_ACTIVITY_ATTRIBUTION_LEVEL / IDENTITY_UNRESOLVED`

## Primary address-level evidence

Deterministic validation confirms Bitcoin mainnet legacy P2PKH, version byte `0x00`, hash160 `7ff2913a5fe25f64330b2080b7501ecc44a0c3e1`.

Independent preserved on-chain captures agree on:

- confirmed transactions: `27`;
- funded outputs: `18`;
- spent outputs: `18`;
- lifetime received: `0.09119321 BTC`;
- lifetime sent: `0.09119321 BTC`;
- final confirmed balance: `0 BTC`;
- mempool activity at collection: `0`;
- first activity: `2016-03-30 14:47:37 UTC`;
- last activity of the target address: `2016-05-17 18:32:03 UTC`.

Evidence captures include GitHub Actions artifacts `9832728645` and `9832763404` with SHA-256 values recorded in `WORKLOG_2026-09-02.md`.

## Wallet-cluster evidence

WalletExplorer places the target in unlabeled cluster `00421c7e25459ed4` / `[00421c7e25]`:

- `29` addresses;
- `65` transactions;
- activity window `2016-03-30` through `2016-05-18`;
- external received: `0.90805818 BTC`;
- external sent: `0.90507183 BTC`;
- network fees: `0.00298635 BTC`;
- final balance: `0 BTC`.

**Method boundary:** WalletExplorer clustering is an analytical heuristic. It supports a wallet-level behavioral model but is not legal proof that all addresses have one real-world owner.

## Verified SatoshiDice direct flow

Red Team reconciliation separates wallet delta from direct service flow.

For `[00421c7e25]`:

- `21` outgoing transactions contain exactly `21` direct betting outputs to independently labeled `SatoshiDice.com-original` addresses;
- direct betting outputs total **`0.506111 BTC`**;
- `21` incoming service-only transactions return **`0.37109417 BTC`** from SatoshiDice;
- gross direct service-flow difference: **`-0.13501683 BTC` before network fees**.

The earlier wallet-level amount `0.69013308 BTC` must **not** be treated as total stakes. Transaction `1d832a9aca1382c4f618f4e922796ab69c0c764e22c9bedd019340cdafe294f3` contains only `0.02000000 BTC` direct to SatoshiDice and a separate `0.20402208 BTC` output. Most of that co-output later returned to the investigated cluster. The earlier derived `-0.31903891 BTC` gambling P&L is therefore rejected.

Canonical correction: `EVIDENCE_009_SATOSHIDICE_FLOW_ACCOUNTING_2026-09-02.md`.

## Downstream routing

After the original cluster closed, funds moved through multiple unlabeled clusters. The observed graph includes split/reconvergence and later re-entry into the gambling/service contour:

- final `0.18793875 BTC` moved from `[00421c7e25]` to `[f915b4559c]`;
- that cluster split to `[b57bb19d60]` and `[0e5cad0da4]`;
- both branches later converged into `[130e06a98b]`;
- `[0e5cad0da4]` has earlier interactions involving PrimeDice, SatoshiDice and ChangeTip;
- a later branch `[0be397ba68]` again sent `0.0152353 BTC` to a SatoshiDice betting address.

This supports continued related gambling-network behavior. It does **not** prove one legal owner for all unlabeled clusters, and no fiat cash-out endpoint was established.

## Attribution conclusion

**FACT:** the target address is part of a small unlabeled wallet cluster with repeated, quantified, bidirectional SatoshiDice interaction.

**HIGH-CONFIDENCE HYPOTHESIS:** the observed behavior is most consistent with the **user/client side of a Bitcoin gambling wallet/network**, potentially manually operated or automated. It is not behaving like SatoshiDice's own operational wallet and does not show the mass-customer collection pattern expected from a typical exchange deposit infrastructure.

Assignment-category estimate:

- individual/user self-custody or automated wallet acting for one user: **85%**;
- small organization/operator using its own automation or linked wallets: **10%**;
- web platform/exchange/custodial service as direct controller of the target address: **5%**.

Confidence is `HIGH` for **user-side gambling activity** and `MEDIUM` for individual-vs-small-operator separation. Percentages are an analytical model, not commercial AML scoring.

## Abuse / sanctions check

Exact-address searches in public indexed sources scoped to OFAC, BitcoinAbuse, Chainabuse and BitcoinWhosWho produced `NO_INDEXED_MATCH_FOUND`.

This is **not** equivalent to a clean-address certification and does not cover non-indexed/private intelligence datasets.

## Unresolved / requires external authority or a new off-chain pivot

`NOT_CONFIRMED`:

- real-world controller name;
- legal entity;
- bot usage;
- IP/geography/device ownership;
- KYC identity;
- final fiat cash-out;
- legal common ownership of every connected unlabeled cluster.

A move from activity attribution to identity requires an independent off-chain identifier: publication of a related address/txid, lawful service/KYC data, a court/law-enforcement record, or another independently verifiable identity edge.

## Closure decision

`CASE-BTC-0001` is **closed for the requested open-source task**. Address-level and cluster-level metrics are preserved separately; SatoshiDice accounting has passed Red Team correction; behavioral attribution is evidence-based; identity remains explicitly unresolved rather than guessed.
