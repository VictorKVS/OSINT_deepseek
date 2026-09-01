# Task 1 automated deep-dive — pass 002

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / fertilizer export network
Status: ACTIVE

## Result codes / evidence grades
- FACT — directly supported fact
- SOURCE_CLAIM — source asserts the fact, provenance not independently archived
- INFERENCE — analytical conclusion from established facts
- HYPOTHESIS — unverified working version
- A — primary/official evidence
- B — strong secondary or document-based evidence
- C — analytical lead
- D — weak/unverified lead

## J2-001 — Target loan agreement materially clarifies Teterin ↔ Harutyunyan link

Sources:
- BIC investigation: https://investigatebel.org/en/investigations/grodno-azot-sankcii-es-shema
- Contract page 1: https://investigatebel.org/storage/page_blocks/June2025/363.jpg
- Contract page 2: https://investigatebel.org/storage/page_blocks/June2025/373.jpg

FACT / SOURCE_CLAIM:
- Document title: `ДОГОВОР ЦЕЛЕВОГО ЗАЙМА № 27/03/17`, Minsk, 27.03.2017.
- Lender: ООО «БелПакСнаб», UNP 192394911.
- Lender represented by Sergei Semenovich Teterin as director of the managing organization.
- Borrower: ООО «АС Гарантстрой», UNP 192237039, represented by D.V. Grigorkevich.
- Principal: equivalent of USD 1,771,386 at 1% annual interest.
- Clause 1.5 states the purpose as reimbursement of damage under criminal case No. `15128000373` for Armen Sergeevich Harutyunyan.
- Repayment deadline stated as 30.09.2017.

Evidence grade: B+.
Reason: primary-looking signed/stamped contract copy is publicly archived by BIC, but no official court/bank-authenticated copy has yet been recovered.

RED TEAM correction:
BIC prose says Teterin provided Harutyunyan a USD 1.7m loan. The published contract is legally more specific and different: BelPakSnab, represented by Teterin, lends to AS Garantstroy; Harutyunyan is not the borrower. The loan purpose is payment of damage tied to Harutyunyan's criminal case.

What this does NOT prove:
- that Teterin personally funded Harutyunyan;
- that the full amount was actually transferred;
- who ultimately received the damage payment;
- final judgment, legal qualification, sentence or exact role of all persons in case 15128000373.

Next pivots:
1. Full judgment/order in criminal case 15128000373.
2. Bank transfer/payment evidence.
3. Corporate ownership/management of BelPakSnab and AS Garantstroy in 2017.
4. Why AS Garantstroy was selected as borrower for payment linked to Harutyunyan.

## J2-002 — AS Garantstroy is a historical bridge to Naklonnaya 28

Sources:
- https://b2bhint.com/en/company/by/ooo-as-garantstroj--192237039
- https://b2bhint.com/en/company/by/ooo-tehnospectrejding--193256472
- https://egr.gov.by/egrmobile/information?pan=192237039
- loan agreement pages above.

FACT:
- AS Garantstroy UNP 192237039 is registered/recorded at `Republic of Belarus, Minsk, Naklonnaya 28` in registry-derived public data.
- TECHNOSPETSTRADING LLC and TECHNOSPETSTRADINGEXPORT LLC use the same address.
- AS Garantstroy's primary activity is wholesale of agricultural machinery, equipment and supplies (4661), same primary profile shown for TECHNOSPETSTRADING.
- In the 27.03.2017 loan contract, AS Garantstroy's address was `Minsk, Zhilunovicha 2B`.
- Registry-derived history shows a location-change notification on 06.02.2019.
- TECHNOSPETSTRADING was incorporated on 20.05.2019 at Naklonnaya 28.

Evidence grade:
- A/B for registration/address/activity timeline.
- C for continuity/control inference.

INFERENCE:
The sequence `2017 loan tied to Harutyunyan → AS Garantstroy changes address in Feb 2019 → TECHNOSPETSTRADING incorporated at same address in May 2019` creates a materially stronger historical bridge than a mere modern shared address.

What this does NOT prove:
- common beneficial owner;
- common management;
- that AS Garantstroy was part of the same fertilizer scheme;
- that AS Garantstroy was the vehicle used in the criminal conduct referenced by the cropped case excerpt.

Next pivots:
1. AS Garantstroy founders/directors by year.
2. Full registry change packet 2017–2020.
3. Owner/landlord and tenant history of Naklonnaya 28.
4. Shared staff, phones, emails, powers of attorney and banks with TST.
5. D.V. Grigorkevich links to Armen Harutyunyan / Sergei Teterin.

## J2-003 — Criminal-case excerpt remains incomplete

Source:
- https://investigatebel.org/storage/page_blocks/June2025/354.jpg

SOURCE_CLAIM:
A cropped document fragment says a participant in an organized group led by A.S. Harutyunyan assisted an alleged criminal scheme involving sale in the Russian Federation of Belarus-produced agricultural machinery/equipment and extraction of budget income through deception without signs of theft.

Evidence grade: B/C.
Limitation: no header, date, court, case number or full context visible in the crop. It cannot independently establish Harutyunyan's conviction, sentence or exact charge.

Next pivot: recover the complete document and tie it explicitly to case 15128000373.

## J2-004 — Latvia customs enforcement materially narrows the physical corridor

Primary/strong source:
- LSM / De facto, 24.08.2025: https://www.lsm.lv/raksts/zinas/ekonomika/24.08.2025-baltkrievu-karbamids-latvija-muitas-policija-lietas-neierosina-par-spiti-sankciju-apiesanas-pazimem.a611523/

SOURCE_CLAIM / near-primary reporting:
- Latvian Customs conducted enhanced checks in July 2025 on Belarus-origin urea and saw signs of possible sanctions circumvention.
- Tax and Customs Police issued four decisions refusing to open criminal proceedings; Customs together with the Financial Intelligence Unit appealed; prosecution was reviewing the decisions.
- Cargoes imported by four Latvian companies were under customs supervision.
- 6.1k tonnes were stored in free zones/customs warehouses in Riga and Liepaja, intended for Estonia, Poland and Germany.
- One named company was `RIN Cargo`.
- Latvijas dzelzceļš reported 32k tonnes of Belarusian urea moved in 2025; Latvian Customs statistics showed 35k tonnes imported from Belarus in the first seven months.
- Eurostat data cited by LSM indicated 65% of all Belarusian urea imported into the EU in June 2025 went via Latvia.
- Last Belarus urea shipment released 29.06.2025; last urea-solution shipment 10.07.2025; flow stopped in August.

Evidence grade: B+ pending archival of VID/LDz/Eurostat primary records.

Critical limitation:
These figures describe the broader Belarusian urea corridor, not TECHNOSPETSTRADING alone. No direct edge should be created from the entire 6.1k/35k-tonne flow to TST.

Next pivots:
1. Identify all four Latvian importers.
2. Customs declaration IDs and EORI/VAT numbers.
3. Which warehouse/free zone held which cargo.
4. Final consignees in Estonia, Poland and Germany.
5. Wagon numbers / CIM / storage records.

## J2-005 — RIN Cargo is a real customs/rail/storage node

Sources:
- LSM article above.
- https://www.ringroup.lv/
- https://www.1188.lv/en/catalog/customs-warehouse-4060/rin-cargo-821524
- https://www.firmas.lv/lv/uznemumi/rin-cargo/40103392557

FACT / SOURCE_CLAIM:
- SIA RIN Cargo, reg. no. `40103392557`.
- Legal address: Ilzenes iela 2, Riga, LV-1005.
- Primary activity: warehousing/storage (NACE 52.10).
- Public directory lists a customs-warehouse branch at Rankas iela 4A, Riga.
- RiN Group publicly offers customs warehouse, European warehouse, excise warehouse, customs broker and railway service.
- LSM names RIN Cargo as one of companies whose imported urea was under customs supervision.

Evidence grade: A/B for company/infrastructure; B for inspected-cargo association.

What this does NOT prove:
- that RIN Cargo's inspected urea was supplied by TECHNOSPETSTRADING;
- that the specific cargo was stored at Rankas iela 4A.

Next pivot: declaration/warehouse IDs and cargo-level documents.

## J2-006 — Astramar/Piemare gives a concrete Liepaja physical-handling pivot

Source:
- https://www.astramarliepaja.lv/

FACT:
Astramar Liepaja's public site states that stevedoring company LSEZ `PIEMARE` AS operates at Liepaja port berths 64, 65, 73, 74, 75 and 76, with >20,000 m² open storage, 2,000 m² closed warehouses, portal cranes, forklifts and wheel loaders, and experience with bulk cargo.

Context already established:
LSM reported Astramar Liepaja had a urea contract with TECHNOSPETSTRADING in early 2025 and that director Viesturs Andersons said the request came from an acquaintance in France.

Evidence grade: A/B for physical capability; C for use by the specific TST cargo.

INFERENCE:
Piemare/these berths are now high-value physical pivots for locating the exact TST shipment because the infrastructure is technically suitable for rail/port bulk handling.

What this does NOT prove:
- that TST cargo used Piemare;
- that any of berths 64/65/73–76 handled the shipment.

Next pivots:
1. Vessel-call records.
2. Berth logs and cargo manifests.
3. Wagon-to-berth transshipment records.
4. Stevedoring contract / invoice.
5. Vessel name, destination port, final buyer and French intermediary/contact.

## J2-007 — Exact searches for criminal case and corporate identities

Queries:
- `"15128000373" Арутюнян`
- `"15128000373" Беларусь уголовное дело`
- `"192394911" "БелПакСнаб"`
- `"192237039" "АС Гарантстрой"`
- `"БелПакСнаб" Тетерин`
- `"АС Гарантстрой" Григоркевич`

Results:
- no reliable indexed full judgment or official criminal-case document for No. 15128000373 found in this pass — `NO-HIT`;
- company identities/UNPs independently resolve in public Belarus registry-derived services;
- AS Garantstroy is reported as in liquidation in official EGR-indexed result; this is current-status context, not directly material to 2017/2019 control.

## Documents updated
- Google Docs Appendix 6: added loan-contract red-team correction and AS Garantstroy historical-address bridge.
- Google Docs Appendix 7: added Latvia customs-enforcement corridor, RIN Cargo node, and Astramar/Piemare physical-handling pivot.

## Highest-priority next pivots
1. Full criminal case No. 15128000373 judgment/order.
2. AS Garantstroy ownership/management timeline and D.V. Grigorkevich.
3. Naklonnaya 28 property/tenant history.
4. All four Latvian importers under July 2025 customs checks.
5. RIN Cargo cargo-specific declaration/warehouse records.
6. Astramar/Piemare vessel/berth/wagon records and French contact.
7. Hungarian TST PL supplier + external payer.
8. CMR/CIM, wagon numbers, certificates of origin/quality and batch IDs linking Grodno → Latvia → EU.
