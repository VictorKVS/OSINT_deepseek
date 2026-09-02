# CASE-BTC-0001 — Evidence 009 — SatoshiDice flow accounting correction

Date: 2026-09-02  
Subject: `1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75`  
Priority: `P0`

## Why this correction exists

A Red Team accounting pass found that WalletExplorer's wallet-level `sent` delta can exceed the amount actually sent to a named service when the same transaction has another external output. Therefore wallet-level deltas must not be used as service stake totals without raw-transaction reconciliation.

This evidence supersedes any wording that treats `0.69013308 BTC` as SatoshiDice bets or `-0.31903891 BTC` as gambling P&L.

## Verified direct SatoshiDice flow

For WalletExplorer cluster `00421c7e25459ed4` / `[00421c7e25]`:

- `21` WalletExplorer rows labeled sent to `SatoshiDice.com-original`;
- raw Blockstream transactions contain exactly `21` direct outputs to `1dice...` betting addresses;
- direct betting outputs total **`0.506111 BTC`**;
- `21` WalletExplorer rows labeled received from `SatoshiDice.com-original`;
- in all `21` received transactions, every external input resolves to `SatoshiDice.com-original`; mixed/unresolved external sources = `0`;
- verified wallet inflow in those service-only received transactions = **`0.37109417 BTC`**;
- direct service-flow difference = **`-0.13501683 BTC` before network fees**.

### Direct betting outputs by address

| Address | Direct BTC |
|---|---:|
| `1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp` | 0.385112 |
| `1dice97ECuByXAvqXpaYzSaQuPVvrtmz6` | 0.023999 |
| `1dice9wVtrKZTBbAZqz1XiTmboYyvpD3t` | 0.011000 |
| `1dice9wcMu5hLF4g81u8nioL5mmSHTApw` | 0.025000 |
| `1dicec9k7KpmQaA8Uc8aCCxfWnwEWzpXE` | 0.061000 |
| **Total** | **0.506111** |

## Exceptional mixed-destination transaction

Txid: `1d832a9aca1382c4f618f4e922796ab69c0c764e22c9bedd019340cdafe294f3`  
Time: `2016-05-14 17:10:53 UTC`

Input from the investigated wallet cluster:
- `0.22408304 BTC` from `1LJ3aPB1ru68xuqVbY8XzHK89HN7Z7j1Zz`.

Outputs:
- **`0.02000000 BTC`** -> SatoshiDice `1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp`;
- **`0.20402208 BTC`** -> `1A1GUw9yWbBBVSCcAEux7vV4Ft3KxN7NzL`;
- fee `0.00006096 BTC`.

WalletExplorer therefore reports wallet net outflow `0.20402208 BTC` for the row, but only `0.02 BTC` is the direct SatoshiDice bet.

## Resolution of the non-service output

Address `1A1GUw9yWbBBVSCcAEux7vV4Ft3KxN7NzL` belongs to one-address WalletExplorer cluster `[3169931e38]`, has `2` transactions, received and spent exactly `0.20402208 BTC`, final balance `0`.

At `2016-05-14 23:47:28 UTC`, approximately 6 h 36 min after the mixed transaction, that address spent its full balance:

- `0.18128188 BTC` -> `1FyWxydjfT8tiCrH46rnXmpGJ5JuKWVt8u`, which is one of the original 29 addresses in `[00421c7e25]`;
- `0.02267947 BTC` -> `1ER3D2PtFFghHssmzn7qSugkKbkzvEWtND`;
- fee `0.00006073 BTC`.

This proves that the `0.20402208 BTC` co-output cannot be counted as a SatoshiDice stake and that most of it returned to the investigated cluster.

## Automation / bot status

The wallet used five different SatoshiDice betting addresses with different historical odds. One pair of bets shares the same WalletExplorer block timestamp. However WalletExplorer timestamps are block times, not exact transaction creation/broadcast times.

**Status: `BOT USAGE — NOT CONFIRMED`.**

Timing evidence alone is insufficient to distinguish manual use from scripted betting.

## Mandatory methodology changes

1. Store `wallet_delta`, `direct_service_flow`, and `other_flow` separately for every service-labeled transaction.
2. If direct service flow and wallet delta differ, emit `MIXED_DESTINATION` or `MIXED_SOURCE` instead of silently assigning the full wallet delta to the service.
3. If a source contains a target service label but the parser extracts zero rows, the pipeline must fail (`P0_PARSE_GATE`) rather than return a successful empty result.
4. Service P&L must be derived only after raw input/output reconciliation.
5. Block timestamps may support sequencing but must not be presented as proof of automation.

## Evidence artifacts

- corrected service-flow run `33619718757`, artifact `9842406798`, SHA-256 `b4c458b9fad8762392ab6d2c8e00ee1c7f5934d1e4cf0550a106b7f9ee08ce6`;
- exceptional-output resolver run `33619536473`, artifact `9842324682`, SHA-256 `fbd690384ceda1248c497e74618a9eeb772d1d171177b93da6ff28a71c17829a`;
- earlier parser-audit artifact `9842249126`, SHA-256 `84df19aab4adadbbee64619cf14c14c1f6175fc375af57d6be05fcbee66318a9`.

## Correct conclusion

**FACT:** direct SatoshiDice betting outputs total `0.506111 BTC`; verified service-only inflows total `0.37109417 BTC`; gross direct service-flow difference is `-0.13501683 BTC` before network fees.

**FACT:** the larger `0.69013308 BTC` wallet-level outflow across SatoshiDice-labeled transactions includes unrelated/co-routed funds and is not the stake total.

**NOT CONFIRMED:** bot use, real-world controller identity, and whether all connected unlabeled clusters share one legal owner.
