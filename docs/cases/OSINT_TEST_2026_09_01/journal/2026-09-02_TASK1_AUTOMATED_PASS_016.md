# Task 1 automated deep-dive — pass 016

Date of access: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Start-of-pass anti-duplication check

Reviewed the latest journal first: `2026-09-02_TASK1_AUTOMATED_PASS_015.md`.
PASS_015 had already resolved SIA CONCORDE Group in the comparative MetaTradingProm/Belamiks route, its registry identifiers, public bank/payment fingerprint, Riga operational-address lead and a no-link warning for TECHNOSPETSTRADING. Those queries were not repeated without cause.

Evidence labels:
- `FACT` — fact directly visible in a public/registry-derived record or stable identifier.
- `SOURCE_CLAIM` — source reports a fact whose underlying primary record was not independently archived in this pass.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — unverified working proposition.
- `A/B/C/D` — primary/official → strong documentary secondary → analytical/discovery → weak/unverified.

---

## J16-001 — ASTRAMAR LIEPĀJA: current corporate/VID status and a dated taxpayer-rating change

Entity: SIA `ASTRAMAR LIEPĀJA K.A.`
Registration no.: `42103016440`
VAT: `LV42103016440`
Event dates: 2025-09-04 and 2026-05-13
Access date: 2026-09-02

Sources:
- Firmas.lv, reproducing Latvian SRS/VID data: https://www.firmas.lv/en/companies/astramar-liepaja-k-a/42103016440
- Latvian-language mirror: https://www.firmas.lv/lv/uznemumi/astramar-liepaja-k-a/42103016440

### SOURCE_CLAIM / B+
The registry/VID-derived profile shows taxpayer rating history:
- `2025-09-04`: rating `A` — good compliance / no significant tax-violation risks indicated by the rating;
- `2026-05-13`: rating `B` — compliance needs improvement, with the source description referring to timely declarations and declaration/payment of taxes.

The company remains shown as registered/active, with no liquidation, insolvency or general suspension entry in the same profile.

### What this does NOT prove
- no direct tax offence is established by a B rating;
- the rating change is not evidence that the 10.01.2025 TECHNOSPETSTRADING contract caused a tax issue;
- no MRN, invoice, payment order or shipment is linked to the rating change.

### Next pivots
1. Direct VID rating/decision record if publicly retrievable.
2. 2025 annual-report management note and related-party/payables disclosures.
3. Check whether any VID decision, court matter or securing measure can be tied to a specific transaction before creating causal edges.

---

## J16-002 — ASTRAMAR 2025 financial profile independently cross-checked

Sources:
- Okredo registry-derived profile: https://okredo.com/en-lv/company/sia-astramar-liepaja-k-a-42103016440
- EMIS company profile, updated 2026-07-24: https://www.emis.com/php/company-profile/LV/Astramar_Liepaja_KA_SIA_en_9997687.html
- Firmas.lv current profile above.

### SOURCE_CLAIM / B+
Okredo reproduces the following 2025 financial figures for Astramar:
- turnover: `632,128 EUR`;
- profit before tax: `-13,155 EUR`;
- net result: `-13,486 EUR`;
- equity: `-105,239 EUR`;
- liabilities / amounts payable: `343,834 EUR`;
- non-current assets: `79,430 EUR`;
- current assets: `159,165 EUR`.

EMIS independently reports 2025 net-sales growth of `80.43%`, total-assets growth of `57.17%`, and improvement in net profit/loss; Firmas flags current loss/negative equity. Firmas also shows that the 2025 annual report was received in 2026.

### INFERENCE / C
The company materially increased turnover in 2025 while remaining loss-making with negative equity. This is useful context for assessing counterparties and payment flows, but does not itself indicate illegality or sanctions circumvention.

### What this does NOT prove
- no conclusion about the profitability of the specific TST→Astramar 22 t shipment;
- no identity of the payer, final customer or Hungarian downstream party;
- no evidence of false accounting or insolvency.

---

## J16-003 — RED TEAM correction: Astramar `nodrošinājums` must NOT be described as a new 2025/2026 restriction

Sources:
- Firmas current profile: `Has security means / Ir nodrošinājumi`.
- Okredo current profile: latest indexed event for securing measures is `2022-04-14 — Change in securing measures`.

### CORRECTION / CONFLICT / B+
A current Firmas flag confirms that a securing/restrictive registration object exists, but Okredo's event chronology points to a securing-measure change already on `2022-04-14`.

Therefore it would be incorrect to infer from the current flag alone that Astramar acquired a new post-investigation restriction in 2025 or 2026.

### What this does NOT prove
- identity of the authority imposing the measure;
- legal basis, amount, asset affected or whether the current flag is exactly the same object as the 2022 event;
- any link to TECHNOSPETSTRADING, fertilizer cargo or Latvian customs procedure 42.

### Next pivot
Retrieve the underlying UR securing-measure entry and compare its identifier/date with the 2022 event.

---

## J16-004 — New 1-hop node from Astramar: KRASTS INVESTS underwent a major ownership/control/address reset in June–July 2026

Entity: SIA `KRASTS INVESTS`
Registration no.: `52103017931`
Current VAT shown by the freshest Latvian-language registry-derived page: `LV52103017931` from `2026-07-09`
Access date: 2026-09-02

Sources:
- LAFF Astramar profile: https://laff.lv/lv/astramar-liepaja-k-a-sia
- Firmas.lv current Latvian profile: https://www.firmas.lv/lv/uznemumi/krasts-invests/52103017931
- 1188 older registry snapshot: https://www.1188.lv/en/catalog/companies/krasts-invests-52103017931

### SOURCE_CLAIM / B+ — material corporate relationship
LAFF's public profile for Astramar states that `ASTRAMAR LIEPĀJA K.A.` is a co-owner of the holding-company group including `KRASTS INVESTS`. This is a direct published operational/corporate relationship, not an address-only inference.

### FACT / B+ — current registry-derived state
The freshest Latvian-language Firmas page for reg. `52103017931` shows:
- active status;
- one natural-person shareholder holding `100%`, effective `2026-06-16`, registered in UR `2026-06-29`;
- one current natural-person UBO from `2026-06-29` through shareholder control;
- one current board member with individual representation from `2026-06-29`;
- legal address changed from `Bāriņu iela 7, Liepāja` to `"Rotas", Dzērvenieki, Cīravas pag., Dienvidkurzemes nov., LV-3453` on `2026-06-29`;
- a shareholders' register dated `2026-06-16`, added `2026-06-29`;
- a corporate decision dated `2026-06-16` and application dated `2026-06-25`, added `2026-06-29`;
- the freshest Latvian page shows VAT `LV52103017931` from `2026-07-09`.

The older 1188/CrediWeb-Lursoft snapshot crawled before this change still gives `Bāriņu iela 7`, independently corroborating the address transition rather than a simple typo in the current page.

### RED TEAM / cache conflict on VAT
The English-language Firmas cache, crawled earlier, still says VAT was absent/excluded `2019-08-13`, while the fresher Latvian page says `LV52103017931` from `2026-07-09`. Treat the English result as stale until direct VID/VIES verification; do not merge the two states as simultaneous.

### What this does NOT prove
- no reason/motive for the ownership change is established;
- no evidence that the new owner/board/UBO participated in the 2025 TST→Astramar shipment;
- no direct TST↔Krasts Invests cargo/payment edge is created;
- current free output redacts the natural person's name, so no identity is guessed.

---

## J16-005 — Important current-vs-historical conflict: LAFF still says Astramar is a co-owner of Krasts Invests, while current registry-derived ownership is a single natural person at 100%

### CONFLICT / B+
LAFF still describes Astramar as co-owner of `KRASTS INVESTS`. Current registry-derived shareholder data for Krasts Invests, however, show a single natural person holding `100%` from `2026-06-16`, registered `2026-06-29`.

### INFERENCE / C
Assuming the current shareholder table is complete, the LAFF description is now historical/stale after the June 2026 transaction. This materially changes the current Astramar corporate graph: `Astramar ↔ Krasts Invests` should be represented as **historical/previous ownership relationship pending retrieval of the pre/post shareholder registers**, not as an automatically current equity edge.

Independent historical context: official Latvian Gazette public-official declarations from 1999–2001 document a professional/shareholding overlap between Astramar and then-LSEZ Krasts Invests, reinforcing that the relationship was historically real. No private relatives from those declarations are entered into the graph.

### What this does NOT prove
- exact percentage previously held by Astramar immediately before 16.06.2026;
- identity of the buyer/new shareholder from the free registry output;
- consideration/price or motive for the transaction;
- connection to sanctions, fertilizer trade or the January 2025 contract.

### Next pivot
Retrieve and compare the Krasts Invests shareholder registers dated `2024-08-23` and `2026-06-16`; this should establish exact seller(s), buyer and percentage transition.

---

## J16-006 — New enforcement-document pivot at Krasts Invests after the June 2026 ownership change

Source:
- Firmas.lv `KRASTS INVESTS` document metadata.

### SOURCE_CLAIM / B+
The registry-derived page lists a restricted/non-public document category `Tiesu izpildītāju rīkojumi/pieprasījums/pavadraksti` (bailiff order/request/cover letter), document date and added date `2026-08-03`, one page PDF.

This occurs after the shareholder/board/address changes of 2026-06-16/29 and VAT state shown from 2026-07-09.

### What this does NOT prove
- debt, creditor, amount, enforcement case number, affected asset or adverse finding;
- that the bailiff document concerns the ownership transfer;
- any relation to Astramar's TST transaction, sanctions or fertilizer cargo.

### Next pivots
1. Obtain the 03.08.2026 bailiff document lawfully from UR/public enforcement sources if accessible.
2. Extract bailiff name, execution-case/reference number, creditor/debtor capacity, amount and object.
3. Only then test temporal/corporate connection to the June ownership change.

---

## J16-007 — Astramar operational contacts expanded, but French contact remains unresolved

Source:
- Astramar official website: https://www.astramarliepaja.lv/

### FACT / B+ (company-authored current source)
Current company website lists operational contacts:
- Viesturs Andersons — `+371 29215004`;
- Ervīns Beļāns — `+371 29215003`;
- Sandijs Kulainis — `+371 29277119`;
- Raimonds Kalnieks — `+371 29259479`;
- office `+371 63425506`;
- `astramar@astramarliepaja.lv`.

The same site describes Astramar/Piemare capabilities including open/closed/cold storage and bulk/general cargo handling. These are capability facts only.

### What this does NOT prove
- none of the named contacts is proven to be the unnamed French requester/contact mentioned by journalists;
- no contact is proven to have handled contract `10.01/25-UR-DAP`;
- generic bulk-cargo capability does not prove handling or relabeling of the investigated urea.

### Next pivot
Search these exact names/phones/e-mail against the contract images, payment-order descriptions, CMR/MRN, and contemporaneous correspondence only; do not infer French identity from job role.

---

## Negative / blocked results

- `NO-HIT`: no exact French individual/company behind Astramar's reported "personal request from France" was identified.
- `NO-HIT`: the unknown Hungarian TST PL supplier and the external payer remain unresolved.
- `NO-HIT`: no shipment-level MRN, CMR/CIM/SMGS, wagon number, truck registration, batch/certificate number or payment-order reference was recovered in this pass.
- `NO-HIT`: no new official NSA appeal/cassation record was recovered for WSA cases `V SA/Wa 3613/25` or `V SA/Wa 3682/25`.
- `NO-HIT`: exact CONCORDE Group railway customer/code was not recovered.
- `BLOCKED`: the Krasts Invests current natural-person shareholder/UBO/board name is redacted in the free registry-derived output; identity is not guessed.

## Documents updated

- Google Docs Appendix 6: appended a new section on Astramar's 2025/2026 corporate/VID profile, Red Team correction for its securing-measure flag, and the 2026 Krasts Invests ownership/control/address/VAT reset with the historical-vs-current co-ownership conflict and 03.08.2026 bailiff-document pivot.

## Priority next pivots

1. Krasts Invests shareholder registers `2024-08-23` vs `2026-06-16` — exact seller/buyer/percentages.
2. Krasts Invests bailiff document dated `2026-08-03` — authority, case/reference, amount/object.
3. Direct VID/VIES verification of `LV52103017931` and exact reason for reactivation/new VAT state from `2026-07-09`.
4. Astramar 2025 annual-report notes — related parties, payables/receivables, material contracts if disclosed.
5. Continue primary unresolved TST targets: Hungarian legal entity, external payer, French Astramar contact, shipment-level MRN/CMR/CIM/SMGS, wagons/trucks, certificates and payment orders.
