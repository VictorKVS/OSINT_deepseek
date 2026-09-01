# OSINT Test Search Journal — 2026-09-01

> Status: ACTIVE / append-only by convention
> Scope: three test tasks — company by address, Bitcoin address, TRON address
> Rule: every search action must record query/source/result/evidence grade/next pivot. No silent deletion of failed searches.

## Result codes
- `FOUND-A` — primary/official evidence found
- `FOUND-B` — strong secondary/aggregated evidence found
- `FOUND-C` — analytical lead / hypothesis
- `NO-HIT` — no relevant indexed result
- `BLOCKED` — source inaccessible / technical restriction
- `CONFLICT` — sources disagree / identity unresolved

## Task 1 — Company at Minsk, Naklonnaya 28

### J-001 — Address resolution
- Input: `Республика Беларусь, г. Минск, ул. Наклонная, д. 28`
- Result: two key related legal entities resolved in checked sources:
  - TECHNOSPETSTRADING LLC / ООО «Техноспецтрейдинг», reg. no. `193256472`
  - TECHNOSPETSTRADINGEXPORT LLC / ООО «ТехноспецтрейдингЭкспорт», UNP `193648909`
- Status: `FOUND-A/B`
- Pitfall: address is not a unique entity identifier.
- Next: treat Export as primary object when UNP 193648909 is supplied; keep 193256472 as related entity.

### J-002 — Business model / sanctions / persons
- Sources: corporate site, KAS/MSWiA Poland, BRC, provided technical conditions.
- Result: confirmed trading/export role; production role claimed by company but full independent production cycle not established.
- Status: `FOUND-A/B + CONFLICT`
- Key risk: direct Polish national sanctions exposure; EU applicability requires separate legal analysis.
- Special threat check: no confirmed terrorism/extremism/drug-trafficking/illegal-arms links found in checked corpus.

### J-003 — Red Team corrections
- Removed unsupported formulations: “straw company”, “criminal scheme”, “EU-wide listing” where not independently established.
- Kept KAS statements attributable to KAS.
- Status: `FOUND-A` for corrections to methodology.

## Task 2 — Bitcoin address

### Object
`1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75`

### J-101 — Address syntax validation
- Method: Base58Check validation / address structure.
- Result: valid Bitcoin mainnet legacy P2PKH address.
- Version byte: `0x00`
- Hash160: `7ff2913a5fe25f64330b2080b7501ecc44a0c3e1`
- Status: `FOUND-A` (cryptographic format only).
- What this does NOT prove: owner, activity, balance, risk, service attribution.

### J-102 — Exact-match web search
- Queries:
  - exact address
  - exact address + bitcoin
  - exact address + blockchair
  - exact address + blockchain.com
- Result: no reliable indexed attribution or public profile found in search results.
- Status: `NO-HIT`
- Interpretation: low off-chain discoverability is not evidence of private-person ownership.

### J-103 — GitHub exact-match search
- Result: no indexed repository hit for the exact Bitcoin address.
- Status: `NO-HIT`

### J-104 — Technical extraction attempt through Google Sheets IMPORTDATA
- Targets: blockchain.info address balance / received / sent / rawaddr endpoints.
- Result: Google Sheets returned `#REF!` requiring desktop approval for external URL access.
- Status: `BLOCKED`
- Important: no balance/transaction statistics inferred from this failure.
- Next: obtain primary address history from an explorer/API/node outside the blocked Sheets import path.

## Task 3 — TRON address

### Object
`TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF`

### J-201 — Address syntax validation
- Result: valid TRON mainnet Base58Check address.
- Prefix: `0x41`
- Hex: `41da383c182b70b7d6c91487a4e5fb44d415fbec56`
- Status: `FOUND-A` (format only).

### J-202 — Confirmed 820 USDT receipt
- Primary source: TRONSCAN transaction page.
- txid: `36c2996f0e40b9531b687eb818885f6d612d3fbc4f50e12aa94f374028160131`
- Block: `83609827`
- Time: `2026-06-15 04:46:51 UTC`
- From: `TJDnKdo9kaM6yVPEwb93Y2ER6gZLR37MFb`
- To: `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF`
- Token: USDT TRC-20 (`TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`)
- Amount: `820 USDT`
- Result: successful / confirmed.
- Status: `FOUND-A`

### J-203 — 600,000 USDT large-transfer lead
- Secondary source: Coingrab transaction monitor index.
- Time shown: `2026-06-14 00:23:57`
- From: `TBBc6QRDkyP4wYmWjBcoGYrGra2jRY9c14`
- To: `TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF`
- Amount shown: `600,000 USDT` (approx. USD value displayed by source).
- Status: `FOUND-B/C`
- Limitation: txid not yet recovered and transaction not yet independently verified on TRONSCAN.
- Next: locate exact txid and verify event log on primary explorer.

### J-204 — Sender exact-match searches
- Addresses searched:
  - `TBBc6QRDkyP4wYmWjBcoGYrGra2jRY9c14`
  - `TJDnKdo9kaM6yVPEwb93Y2ER6gZLR37MFb`
- Result: no reliable named-entity attribution surfaced in indexed web search during this pass.
- Status: `NO-HIT`
- Next: inspect sender account histories, recurring counterparties, exchange tags, funding source, and post-receipt sweep behavior.

## Five workstreams — current status

### Stream 1 — On-chain statistics
- BTC: `BLOCKED/PENDING` primary extraction.
- TRON: one primary transaction confirmed; one large-transfer lead pending txid verification.

### Stream 2 — Counterparties / graph
- BTC: pending on-chain dataset.
- TRON: two direct incoming counterparties identified; entity attribution pending.

### Stream 3 — Off-chain attribution
- BTC: no exact indexed attribution found.
- TRON: no direct owner label found; sender labels unresolved.

### Stream 4 — Risk / sanctions / abuse
- BTC: pending reliable transaction graph.
- TRON: no owner-level adverse attribution established yet; transaction size alone is not adverse evidence.

### Stream 5 — Red Team / source control
- Active. Key warning: address ≠ person; exchange deposit address may be technically controlled by a platform but economically associated with a customer.

## Required next pivots
1. Recover complete BTC address history from at least two independent primary on-chain sources.
2. Recover TRON account overview and full TRC-20 history.
3. Find txid for the 600,000 USDT transfer and confirm on TRONSCAN.
4. Trace first-hop and second-hop counterparties for TRON, prioritizing recurring/sweeping addresses.
5. Search any recovered counterparties for public service tags, sanctions, scams, court/police notices, exchange references, merchant/OTC traces, and unusual cross-chain links.
6. Record every hit/no-hit/conflict in this journal before drafting final attribution probabilities.
