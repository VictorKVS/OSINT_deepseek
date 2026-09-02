# Task 1 automated deep-dive — PASS 008

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / TST PL / related fertilizer export network
Status: ACTIVE

## Evidence classes
- `FACT` — directly supported by primary/official record.
- `SOURCE_CLAIM` — attributable claim from a secondary/aggregated source.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — search proposition requiring evidence.

## Grades
- `A` — primary/official evidence.
- `B` — strong secondary/registry-derived/document-based evidence.
- `C` — analytical lead/inference.
- `D` — weak/unverified lead.

## P8-001 — KAS explicitly ties TECHNOSPETSTRADING to Latvia import under customs procedure 42
Type: FACT
Grade: A
Primary source:
- MSWiA decision concerning Armen Harutyunyan:
  https://www.gov.pl/attachment/0d356759-00e1-440d-8e9e-b7569d824cf7

Result:
- The official decision states that, according to KAS findings, imports into Latvia of goods whose country of origin was Belarus were realized through TECHNOSPETSTRADING LLC.
- The same passage states that this was conducted under customs procedure 42.
- The document repeats that from February 2025 the main supplier of TST PL became a Hungarian entity; Belarus-origin fertilizer was customs-cleared in Latvia, Hungary was declared as destination/movement country, and the Hungarian company had a urea supply contract with TECHNOSPETSTRADING LLC containing an external-payer clause.

What this does NOT prove:
- identity of the Latvian importer/declarant;
- identity of the Hungarian company;
- external payer;
- MRN/EORI/VAT of a specific declaration;
- wagon number, final buyer, or physical relabeling/repacking.

Next pivot:
- MRN / procedure 42 records for CN 310210 and CN 31028000, Belarus→Latvia, Jan–Jul 2025;
- EORI/VAT of importer/declarant;
- link MRN to CIM/SMGS, invoices, the 2025-01-10 Latvian contract and 2025-02-21 Hungarian contract.

## P8-002 — GrandGranit rail dispatch from Grodno with TST PL as recipient confirmed again in Armen decision
Type: FACT
Grade: A
Primary source:
- https://www.gov.pl/attachment/0d356759-00e1-440d-8e9e-b7569d824cf7

Result:
- Official decision states GrandGranit began large-scale fertilizer imports into Poland in June 2025.
- Goods were sent by rail from Grodno.
- TST PL was the Polish recipient.
- KAS/MSWiA characterizes GrandGranit as intermediary and Grodno Azot as actual producer in the described flow.

What this does NOT prove:
- exact wagon numbers or CIM/SMGS;
- exact batch/quality certificate;
- physical repacking or relabeling;
- criminal conviction of any person. The circumvention characterization is an administrative authority position.

Next pivot:
- first GrandGranit→TST PL rail consignment in June 2025;
- CIM/SMGS, wagon numbers, Grodno Azot batch/quality certificate, Polish customs declaration.

## P8-003 — BELTECHNIKA.LT corporate change timeline from Lithuanian Register Centre
Type: FACT
Grade: A
Primary sources:
- Registrų centras bulletin 2019-06-07:
  https://www.registrucentras.lt/jar/infleid/download.do?oid=163355
- Registrų centras bulletin 2022-07-15:
  https://www.registrucentras.lt/jar/infleid/download.do?oid=235065
- Registrų centras bulletin / 2023 financial filing registered 2024-06-14:
  https://www.registrucentras.lt/jar/infleid/download.do?oid=284469

Result:
- 2019-06-07: official Lithuanian bulletin records changes to manager and shareholder of UAB Beltechnika.lt, code 302727122.
- The bulletin does not name the incoming manager/shareholder in the indexed text; do not backfill Armen into this historical event without source documents.
- 2022-07-15: official bulletin records capital increase, change in share count and share-capital amount; documents include a sole-shareholder decision dated 2022-07-13.
- 2024-06-14: official bulletin confirms filing of 2023 very-small-company financial statements.

Cross-source current control:
- Polish MSWiA/KAS decision identifies Armen Harutyunyan as sole owner/director of BELTECHNIKA.LT and BELTECHNIKA.LT as 90% owner of TST PL.

What this does NOT prove:
- that Armen was the incoming manager/shareholder specifically on 2019-06-07;
- amount/source of 2022 capital increase without underlying decision;
- any sanctions-evasion purpose.

Next pivot:
- retrieve underlying 2019 JAR documents and 2022 sole-shareholder decision/statutes;
- identify capital source and ownership chronology.

## P8-004 — BELTECHNIKA.LT operational footprint thinned by end-2024
Type: SOURCE_CLAIM + INFERENCE
Grade: B+ for data; C for inference
Sources:
- Rekvizitai legal-entity history (registry/VMI-derived):
  https://rekvizitai.vz.lt/en/company/beltechnika_lt/legal-entity/
- Rekvizitai employees (Sodra-derived):
  https://rekvizitai.vz.lt/en/company/beltechnika_lt/number-of-employees/
- Okredo corroboration:
  https://okredo.com/en-lt/company/uab-beltechnika-lt-302727122

Result:
- VAT code LT100007190215 is shown as active 2020-07-15 through 2024-06-14 and currently inactive.
- Sodra-derived employee history: 3 insured persons on 2022-07-08; 2 on 2023-03-22; 1 on 2023-10-01; 0 on 2024-12-24.
- 2023 revenue shown as EUR 217,105 and net loss EUR 64,328.

INFERENCE / C:
- By end-2024 BELTECHNIKA.LT had a very small publicly observable operating footprint while remaining a key ownership/control bridge to TST PL. This is consistent with a predominantly holding/control role at that stage.

What this does NOT prove:
- shell-company status;
- inactivity;
- tax violation;
- sanctions evasion;
- absence of lawful outsourced operations or contractors.

Next pivot:
- direct VMI VAT-history evidence;
- 2022–2024 financial notes and related-party balances;
- intercompany financing BELTECHNIKA.LT↔TST PL;
- bank accounts and public payment records.

## P8-005 — Search for Hungarian/Latvian names and external payer
Queries included exact contract dates, TECHNOSPETSTRADING, Latvia, Hungary, procedure 42, external payer, urea.
Result:
- No reliable indexed source disclosed the Hungarian legal entity, Latvian contract party, or external payer.
- OCCRP still confirms only a shipment/invoice to Hungary via Latvia without naming the missing legal entity in indexed text.
Status: NO-HIT.
Rule: do not insert candidate companies based only on country, commodity, or timing.

## P8-006 — French Astramar contact
Result:
- No new reliable open-source identification in this pass.
Status: NO-HIT.
Rule: retain as unresolved person/company lead; no graph edge to speculative French traders.

## Google Docs updates
- Appendix 6 updated with BELTECHNIKA.LT ownership/control and operational-footprint timeline, including explicit Red Team limits.
- Appendix 7 updated with primary-source strengthening of TECHNOSPETSTRADING→Latvia→procedure 42 and GrandGranit rail-from-Grodno/TST PL recipient chain.

## Priority pivots after PASS 008
1. MRN/EORI/VAT records for Latvia procedure 42 and CN 310210/31028000.
2. Underlying Lithuanian JAR documents for BELTECHNIKA.LT manager/shareholder change 2019-06-07.
3. 2022 sole-shareholder decision and capital-increase documents for BELTECHNIKA.LT.
4. Direct VMI VAT-history evidence and related-party financial disclosures.
5. Hungarian entity from 2025-02-21 contract.
6. Latvian entity from 2025-01-10 contract.
7. External payer.
8. French Astramar contact.
9. First GrandGranit→TST PL June-2025 CIM/SMGS + wagon/batch fingerprint.
