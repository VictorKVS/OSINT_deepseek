# Task 1 — Automated deep-dive pass 006

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / TST PL / related fertilizer export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly stated in a primary/official/public record.
- `SOURCE_CLAIM` — statement/data exposed by a secondary or registry-derived source, not yet reproduced from the underlying primary record.
- `INFERENCE` — analytical conclusion from established facts.
- `HYPOTHESIS` — proposition requiring evidence.

## Evidence grades
- `A` — primary/official record.
- `B` — strong secondary / registry-derived / document-based source.
- `C` — analytical lead or incomplete attribution.
- `D` — weak/unverified lead; not usable in conclusions.

---

## J1-A006-01 — PKP CARGO restriction-list version diff: TST network absent 02.12.2024, present by 15.12.2025

### FACT / A
PKP CARGO publishes appendices to customer restriction `Nr 352-24` / `Nr 326-25`, both introduced under telegram `COPP-7803/719/22`.

Official 2024 appendix, state as of `02.12.2024`:
- `Załącznik do ograniczenia Nr 352-24`, change 25;
- list ends at item 88;
- exact-name search and visual inspection show no `TECHNOSPETSTRADING`, `TECHNOSPETSTRADINGEXPORT`, `WORLD CHEM TRADING`, `GrandGranit`, or `TST PL`.

Source:
https://www.pkpcargo.com/wp-content/uploads/2024/12/zal.doograniczenia35224zm.25.pdf

Official 2025 appendix, state as of `15.12.2025`:
- `Załącznik do ograniczenia Nr 326-25`, change 40;
- item 90 — TECHNOSPETSTRADINGEXPORT LLC, Naklonnaya 28, Minsk;
- item 91 — TECHNOSPETSTRADING LLC, Naklonnaya 28, Minsk;
- item 92 — WORLD CHEM TRADING CO. L.L.C., Dubai;
- item 94 — MetaTradingProm LLC;
- item 100 — GrandGranit LLC;
- item 105 — TST PL Sp. z o.o., Biała Podlaska.

Source:
https://www.pkpcargo.com/wp-content/uploads/2023/11/zal.doograniczenia32625zm.40.pdf

Evidence grade: `A` for presence/absence in the dated official PKP CARGO appendices.

### INFERENCE / C
The rail-carrier restriction/customer-list exposure of the TST network emerged between the checked 02.12.2024 and 15.12.2025 versions. The configuration is consistent with the subsequent Polish sanctions timeline, but the exact first-addition dates of items 90–105 have not yet been reconstructed.

### What this does NOT prove
- that PKP CARGO transported any specific TST/GrandGranit shipment;
- that any particular wagon was stopped or refused;
- that every listed entity was included for the same legal reason;
- the full legal/operational effect of restriction `326-25` without the main restriction text / telegram;
- the exact date each TST-network entity first appeared.

### Next pivot
1. Recover intermediate versions of `326-25` and perform a version diff to establish first-addition dates for items 90, 91, 92, 100 and 105.
2. Recover the main text of restriction `326-25` and telegram `COPP-7803/719/22`.
3. Overlay first-addition dates with sanctions decisions and route changes.
4. Search PKP/rail documentation for wagon-specific restrictions, CIM/SMGS or consignment references.

---

## J1-A006-02 — TST PL 2024 financial profile quantifies a high-turnover, very thin operating structure

### SOURCE_CLAIM / B+
BizRaport reproduces figures from the 2024 financial statement filed for KRS `0001041620` (TST PL). Independent registry pages confirm that 2023 and 2024 financial statements are deposited in the KRS financial-document repository.

Key 2024 figures exposed by BizRaport:
- revenue: `24,823,915.55 PLN` versus `1,584,077.88 PLN` in 2023;
- net loss: `63,338.50 PLN`;
- operating costs: `24,887,253.72 PLN`;
- depreciation: `0 PLN`;
- materials and energy: `11,090.94 PLN`;
- external services: `623,598.56 PLN`;
- wages: `285,790.96 PLN`;
- social benefits: `65,006.14 PLN`;
- other operating costs: `23,901,767.12 PLN`;
- assets: `7,484,775.86 PLN`;
- liabilities: `7,584,227.82 PLN`;
- current liabilities: `7,263,327 PLN`;
- cash: approximately `1,000 PLN` in the service's liquidity presentation;
- receivables/other current assets: approximately `7.1m PLN`;
- inventory: approximately `425k PLN`;
- employment: `1` person in 2024.

Sources:
- https://www.bizraport.pl/krs/0001041620/tst-pl-spolka-z-ograniczona-odpowiedzialnoscia
- https://www.imsig.pl/krs/0001041620
- EMIS independently reports 2024 net sales growth of `1466.4%` and total-asset growth of `956.42%`.

Evidence grade: `B+` until the original RDF/e-KRS 2024 statement is archived directly.

### INFERENCE / C
The combination of ~24.8m PLN turnover, one employee, zero depreciation, very small cash balance, high receivables/liabilities and a net loss is consistent with a low-asset wholesale/trading/intermediary operating model rather than a capital-intensive producer. This is analytically consistent with TST PL's registered chemical-wholesale activity and the KAS description of its role in fertilizer imports.

### What this does NOT prove
- that TST PL was a sham company;
- sanctions evasion by itself;
- beneficial ownership beyond already documented official sources;
- identities of customers, suppliers or external payer from the financial statement summary;
- movement of specific cargoes.

### Next pivot
1. Archive the original 2024 RDF/e-KRS financial statement and notes.
2. Inspect notes for related-party receivables/payables, advances, currency positions and supplier/customer concentration.
3. Compare turnover and receivable/payable balances to known 2024 TST-origin fertilizer flows.

---

## J1-A006-03 — Two publicly listed TST PL bank accounts provide payment-document pivots

### SOURCE_CLAIM / B
Puls Biznesu Monitor Firm lists two accounts for TST PL, NIP `1133099179`:
- `PL75 1020 1185 0000 4902 0361 2314`
- `PL80 1020 1185 0000 4702 0361 2322`

Source:
https://monitorfirm.pb.pl/firma/tst-pl/

The Polish Ministry of Finance VAT White List exposes an official API capable of validating NIP↔bank-account assignment, but this pass did not retrieve a dated result for these two account numbers.

API documentation:
https://wl-api.mf.gov.pl/

Evidence grade: `B` pending direct Ministry of Finance White List validation.

### Analytical value
These account numbers are strong document-matching pivots for invoices, contracts, payment orders, court exhibits and leaked/commercial documents already in the open-source corpus. A match can connect a payment document to TST PL without relying only on company-name spelling.

### What this does NOT prove
- who sent or received any specific payment;
- the bank counterparty on any transaction;
- whether the accounts were active on a particular historic date;
- a connection to the unnamed external payer in the 2025 Hungarian contract.

### Next pivot
1. Validate both accounts through the official VAT White List for relevant historical dates.
2. Search exact IBANs in public invoices, judgments, procurement/court attachments and leaked-source publications.
3. Compare with bank details in any recovered TST PL / Latvian / Hungarian contract or invoice.

---

## J1-A006-04 — Hungarian company / Latvian contract party / external payer / French contact

Repeated exact-date and route searches did not disclose a reliable public identity for:
- the Latvian counterparty in the `2025-01-10` contract;
- the Hungarian counterparty in the `2025-02-21` contract;
- the external payer allowed by those arrangements;
- the French contact who asked Astramar director Viesturs Andersons to assist the shipment.

Status: `NO-HIT`.

No speculative candidate has been inserted into the graph.

---

## Updated priority queue

1. PKP CARGO version diff to date first appearance of TST/TSTExport/WORLD CHEM/GrandGranit/TST PL and obtain the underlying restriction text.
2. Original 2024 TST PL RDF/e-KRS statement and explanatory notes; related-party receivables/payables.
3. Official VAT White List verification of the two TST PL accounts; exact-IBAN document search.
4. Latvian contract party (2025-01-10), Hungarian company (2025-02-21), external payer and French Astramar contact.
5. CMR/CIM/SMGS, wagon numbers, batch/quality certificates and cargo fingerprints linking individual TST/TSTExport/GrandGranit shipments.
