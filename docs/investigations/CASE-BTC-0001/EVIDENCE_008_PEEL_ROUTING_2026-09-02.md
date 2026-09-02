# CASE-BTC-0001 — Evidence 008 — downstream peel-like routing

Date: 2026-09-02  
Subject: `1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75`

## Purpose

Verify whether downstream wallets after closure of `[00421c7e25]` are one-off recipients or remain behaviorally/transactionally connected to the earlier wallet network.

## Confirmed facts

1. `[bfeb6e4da3]` had a direct bidirectional relationship with the original cluster `[00421c7e25]` on 2016-04-02:
   - `[00421c7e25] -> [bfeb6e4da3]`: `0.002 BTC`;
   - `[bfeb6e4da3] -> [00421c7e25]`: `0.0002 BTC`.

2. After the original cluster was closed, the main downstream branch later reached `[2dff4efd27]`.

3. On 2016-06-07 19:05:28 `[2dff4efd27]` routed:
   - `0.163818 BTC -> [62508e39cd]`;
   - `0.00175 BTC -> [bfeb6e4da3]`;
   - fee `0.0000605 BTC`.

4. On 2016-06-07 23:36:33 `[62508e39cd]` routed:
   - `0.162018 BTC -> [201a6b1c7d]`;
   - `0.00174 BTC -> [bfeb6e4da3]`;
   - fee `0.00006 BTC`.

5. On 2016-06-09 18:55:57 `[201a6b1c7d]` routed:
   - `0.126958 BTC -> [24d939ef1e]`;
   - `0.035 BTC -> [0127bfd429]`;
   - fee `0.00006 BTC`.

6. The other branch after convergence in `[130e06a98b]`, wallet `[0be397ba68]`, later sent `0.0152353 BTC` to SatoshiDice.com-original in tx `d88a4406724be48808e98756a58645619d7b1c6011dc7855b7634a51137e5ce9` on 2016-06-26.

## Interpretation

**HYPOTHESIS — HIGH CONFIDENCE:** repeated remote-hop interaction with the earlier counterparty `[bfeb6e4da3]`, combined with the other branch returning to SatoshiDice, materially strengthens the model of a related user-controlled gambling-wallet network.

The `2dff -> 62508 -> 201a` sequence has **peel-like routing characteristics**: the dominant balance is repeatedly moved forward while smaller side outputs are separated. This description is behavioral only; it does not by itself prove a common legal owner.

## Provenance / contamination control

Late activity of `[2dff4efd27]` after it received new unrelated deposits is **not** treated as continuation of the original coin path. The trace is constrained by temporal continuity and the appearance of new independent inputs.

A 2017 transfer from `[2dff4efd27]` to a very large unlabeled cluster (`98,811` addresses / `508,270` transactions in WalletExplorer) is therefore not attributed to the original 2016 funds.

## Evidence artifacts

- run `33594846725`, artifact `9833024603`, SHA-256 `17cf041bcae7b00de6c219f30a189a667ae776a9056dbca2206db110a5774fe6`;
- run `33594924344`, artifact `9833048400`, SHA-256 `2682c394721794725e1aaa842df2f4a2575337705fcc80534e6076d24f397b06`;
- run `33595000838`, artifact `9833073386`, SHA-256 `cb8c6fb7adeda851598dc780538a12a8ea5397fa50591bd03e81bcabd34598cb`.

## Improvement

**Priority P0:** tracer must track temporal continuity and provenance, not only address/wallet history.

Acceptance rule:
- each hop stores timestamp, transferred amount and percentage of tracked flow;
- new unrelated inputs are recorded as contamination/mixing events;
- confidence in downstream attribution is automatically reduced after mixing;
- late wallet activity is never back-propagated to earlier funds without explicit coin-flow evidence.

## Stop condition

At the current depth the activity type is already supported by repeated SatoshiDice behavior and a recurrent connected-wallet pattern. Continue deeper only when a path reaches a reliably labeled service, produces a new off-chain identifier, or is required by a specific investigative question. Otherwise deeper traversal adds anonymous clusters without proportionate attribution value.
