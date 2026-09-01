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

### J-004 — Ownership/control clarified by official Polish decision
- Primary source: Polish KAS/MSWiA decision materials.
- Result:
  - Armen S. Harutyunyan identified as controlling TECHNOSPETSTRADING LLC;
  - Ruzanna Khachatryan identified as formal owner of 24% of TECHNOSPETSTRADING LLC and as granting Armen representation authority on 2024-06-06;
  - TECHNOSPETSTRADINGEXPORT LLC identified as a wholly owned subsidiary of TECHNOSPETSTRADING LLC;
  - Armen identified as indirect owner of TECHNOSPETSTRADINGEXPORT LLC;
  - BELTECHNIKA.LT UAB identified as 90% owner of TST PL; Armen is sole owner/director of BELTECHNIKA.LT UAB;
  - Uluana Atrashkevich owns 10% of TST PL and is president of its management board.
- Status: `FOUND-A`.
- Correction: earlier wording that Export ownership was not established is superseded.
- Family note: no reliable public source found in this pass proving that Ruzanna Khachatryan is a spouse/relative of Armen Harutyunyan. Do not infer kinship from Armenian nationality or community membership.

### J-005 — Quantified TST PL import dependence
- Primary source: official Polish decision.
- Result: TST PL imported `3,360,078 kg` of urea in 2023–2025; until the end of 2024 TECHNOSPETSTRADING LLC was the exclusive supplier according to the decision.
- Status: `FOUND-A`.
- Analytical value: establishes a measurable, concentrated supplier relationship rather than a generic corporate association.

### J-006 — 2025 route change: Belarus → Latvia → Hungary / Poland
- Primary source: Polish KAS/MSWiA decision.
- Result:
  - after December 2024 sanctions, TECHNOSPETSTRADING LLC continued exports from Belarus;
  - exports were no longer sent directly to Polish counterparties, but via companies from other EU states or to companies in other EU states;
  - from February 2025 TST PL's main supplier became a Hungarian entity;
  - Belarus-origin fertilizer was customs-cleared in Latvia, with Hungary declared as destination/movement country;
  - the Hungarian company had a urea supply contract with TECHNOSPETSTRADING LLC;
  - contract contained a clause allowing an external payer.
- Status: `FOUND-A` for the official position.
- Key pivot: identify Hungarian entity, Latvian importer/customs declarant, external payer, and final Polish/EU buyer.

### J-007 — Dubai route and named buyer
- Sources: BIC/LRT/OCCRP investigative materials.
- Result:
  - Technospetstrading planned supply of `30,000 tonnes` of carbamide to UAE worth about `EUR 15m`;
  - named buyer: `DP World Commodities and Logistics FZE`;
  - route involved Lithuanian logistics/terminal infrastructure; BKT/Klaipėda appears in the shipment chain;
  - earlier documents traced loading at Auls station next to Grodno Azot.
- Status: `FOUND-B` (document-based investigative source; primary cargo docs not yet archived in case store).
- Pitfall: UAE destination can be commercial/re-export; it must not be treated as evidence of concealment by itself.

### J-008 — Trade route after Poland tightened control: Latvia becomes key corridor
- Sources: OCCRP/BIC + official Polish decision.
- Result:
  - investigative materials describe renewed Belarus fertilizer flows into Latvia in 2025;
  - one Technospetstrading invoice showed shipment to Hungary via Latvia;
  - OCCRP/BIC report at least 278 railcars crossing to Latvia in the cited period across broader fertilizer flows;
  - route structure overlaps with official KAS finding about Latvia customs clearance and Hungarian supplier role.
- Status: `FOUND-A/B` depending on sub-fact.
- Analytical value: independent source families converge on Latvia as a post-sanctions transit pivot.

### J-009 — Business economics / internal margin claim
- Source: BIC investigation based on documents/accounts supplied by sources.
- Result claimed by BIC:
  - Technospetstrading intermediary share: about 19–31% of Grodno Azot selling price;
  - related foreign companies reselling to EU buyers allegedly added another 17–30%;
  - estimated private intermediary benefit around USD 140/ton in cited examples;
  - BIC estimated private intermediary services could have cost Grodno Azot more than USD 35m in 2024, while Grodno Azot received USD 59m from EU exports.
- Status: `FOUND-B/C` — strong investigative claim, requires underlying invoices/accounts for A-grade use.
- Important: do not present these figures as audited financial statements.

### J-010 — Armen Harutyunyan ↔ Sergei Teterin political-business bridge
- Sources:
  - BIC: Armen described as former business partner of Sergei Teterin;
  - EUR-Lex: Sergei Teterin is an EU-listed Belarusian businessman in Lukashenka's inner circle.
- Result: a non-ethnic, business-based bridge from Armen into a politically exposed Belarusian network.
- Status: `FOUND-A/B` — Teterin status A from EU source; prior partnership B from BIC pending primary corporate record.
- Next: identify exact joint company/project and dates of partnership.

### J-011 — GrandGranit / Fert-Corporation continuation network
- Source: BIC and Polish KAS.
- Result:
  - GrandGranit owner Nikita Ter-Minasov is described as former head/acting director of TECHNOSPETSTRADINGEXPORT LLC in 2023–2024;
  - Fert-Corporation owner/manager Yuri Minich is described as a Technospetstrading driver and 2023 TECHNOSPETSTRADINGEXPORT payroll recipient;
  - on 2025-05-12 Ter-Minasov granted Minich power of attorney to represent GrandGranit;
  - KAS independently states GrandGranit owner was a person linked to TECHNOSPETSTRADING LLC / EXPORT and sanctioned GrandGranit in August 2025.
- Status: `FOUND-A/B`.
- Key graph implication: replacement exporters are not random market entrants; they are linked by prior management/employment/representation edges.

### J-012 — Shared travel pattern
- Source: BIC investigative materials.
- Result: Nikita Ter-Minasov, Yuri Minich, Dmitriy Goshko and Uluana Atrashkevich reportedly bought tickets for the same Belavia Minsk→Dubai flight on 2024-01-05.
- Status: `FOUND-B/C` until underlying booking records are independently archived/verified.
- Interpretation: potentially coordinated business travel; not proof of unlawful activity.

### J-013 — Global Fertilizer / logistics personnel bridge
- Sources: BIC/LRT.
- Result:
  - Global Fertilizer Company owned railcars used in the carbamide route;
  - founder/owner identified by investigators as Diana Ibragimova;
  - investigators said operational contact was Iryna Fadzeyava, formerly of Belneftekhim.
- Status: `FOUND-B`.
- Next: resolve corporate registry, railcar ownership dates, contracts, and Fadzeyava's exact role.

### J-014 — Key methodological rule for family/ethnic links
- Rule: ethnicity, nationality, diaspora membership, shared surname, or cultural community are not evidence of criminality, control, trust relationship, or kinship.
- Family/relative links may be recorded only when supported by public records, direct statements, public corporate documents, sanctions/PEP records, or other reliable evidence.
- Private relatives who have no material public/corporate role are excluded from the report.
- Status: `FOUND-A` methodological control.

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

### J-105 — Repeated indexed web search for explorer exposure
- Queries: exact address + `btc`, `blockchain.com`, `blockchair`.
- Result: no reliable explorer account/transaction page for the exact address surfaced through indexed search in this pass.
- Status: `NO-HIT`
- Interpretation: search-engine visibility is insufficient for on-chain statistics; direct explorer/API retrieval remains mandatory.

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

### J-205 — Large-transfer monitor context
- Secondary source: Coingrab monitor page indexed around the same time window.
- Result: target address appears amid a high-volume stream of large TRON USDT transfers, including multiple 500k–20m USDT movements between unrelated addresses and some addresses tagged by the monitor as Binance/OKX.
- Status: `FOUND-B/C`
- Interpretation: this page is a whale/large-transfer feed, not an attribution database. Presence in the feed does NOT imply relationship with Binance/OKX or with other transfers shown nearby.
- Pitfall: temporal adjacency on an aggregator page must not be converted into a graph edge.

### J-206 — Temporal pattern between two known receipts
- Known timestamps:
  - 600,000 USDT lead: `2026-06-14 00:23:57` (secondary source; pending primary confirmation)
  - 820 USDT confirmed: `2026-06-15 04:46:51 UTC`
- Observation: receipts are approximately 28h23m apart and differ by three orders of magnitude.
- Status: `FOUND-C`
- Possible interpretations to test:
  1. a high-value operating/settlement address receiving both large and small payments;
  2. customer-specific deposit address on a platform where unrelated deposit amounts coexist;
  3. OTC/merchant address;
  4. self-custody address with unrelated counterparties.
- Important: no classification is accepted until outbound/sweep behavior and counterparty recurrence are known.

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
6. For Task 1, identify the Hungarian 2025 supplier, Latvian customs/importer node, external payer, downstream EU buyers, and exact prior joint business linking Armen Harutyunyan to Sergei Teterin.
7. For Task 1, resolve GrandGranit/Fert-Corporation people and document the management/employment/travel edges with source grades.
8. Record every hit/no-hit/conflict in this journal before drafting final attribution probabilities or final Task-1 network conclusions.
