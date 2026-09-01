# Task 1 automated deep-dive — pass 003

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Result codes / evidence grades
- `FACT` — directly supported fact
- `SOURCE_CLAIM` — source asserts the fact; underlying record not independently archived
- `INFERENCE` — analytical conclusion from established facts
- `HYPOTHESIS` — unverified working version
- `A` — primary/official evidence
- `B` — strong secondary/document-based evidence
- `C` — analytical lead
- `D` — weak/unverified lead
- `CONFLICT` — material source disagreement requiring resolution

## J3-001 — Polish administrative-court challenges were dismissed

Primary sources:
- MSWiA/KAS decision on Armen Harutyunyan: https://www.pomorskie.kas.gov.pl/documents/3555563/52925751/Decyzja%2BArmen%2BSeryozhaevich
- MSWiA decision refusing WORLD CHEM delisting, 22.12.2025: https://www.gov.pl/attachment/8444bcb4-a2e6-462e-8496-eee08e91d44e

FACT:
- WORLD CHEM TRADING challenged the 17.12.2024 Polish sanctions decision. WSA Warszawa dismissed the complaint on 05.08.2025, case `V SA/Wa 604/25`.
- TECHNOSPETSTRADING LLC challenged its 17.12.2024 decision. WSA Warszawa dismissed the complaint on 13.08.2025, case `V SA/Wa 597/25`.
- TECHNOSPETSTRADINGEXPORT LLC challenged its 17.12.2024 decision. WSA Warszawa dismissed the complaint on 13.08.2025, case `V SA/Wa 598/25`.
- The 22.12.2025 WORLD CHEM decision expressly calls the WORLD CHEM judgment `prawomocnym` (final/binding in the sense used by the Polish decision).

Evidence grade: `A`.

What this proves:
- the three companies used judicial review and the WSA did not annul the challenged Polish administrative sanctions decisions at that stage.

What this does NOT prove:
- a criminal conviction;
- criminal guilt of any person;
- that every factual allegation in the administrative reasoning was independently adjudicated as a criminal fact.

Next pivots:
1. Retrieve full WSA judgments `V SA/Wa 597/25`, `598/25`, `604/25` from the administrative-court database.
2. Check whether cassation complaints were filed to NSA in the TST/TSTExport cases and their status.
3. Extract which evidentiary findings the courts explicitly accepted, rejected or left outside review.

## J3-002 — WORLD CHEM: 38 customs declarations and stable exporter identifiers

Primary source:
- MSWiA decision DPP-WTPZ.0272.34.2025(45), 22.12.2025: https://www.gov.pl/attachment/8444bcb4-a2e6-462e-8496-eee08e91d44e

FACT:
- WORLD CHEM TRADING CO. L.L.C. business number: `2823197`.
- License number: `1115715`.
- BLS / Federal Reservation Number: `11965260`.
- In 2021–2024 WORLD CHEM appeared in `38` customs declarations as consignor/exporter from Belarus to Poland.
- Goods identified by the decision:
  - urea 46N, CN `3102 10 10 00`;
  - urea/ammonium nitrate mixture in aqueous or ammoniacal solution, CN `3102 80 00 00`.
- The Polish authority states WORLD CHEM was an intermediary rather than the industrial producer and linked the physical production to GRODNO AZOT.
- WORLD CHEM requested removal from the Polish sanctions list on 12.11.2025; MSWiA refused the request on 22.12.2025.

Evidence grade: `A`.

Analytical value:
The 38-declaration figure gives a concrete customs-record target set. Exact declaration numbers, dates, importers, customs offices, wagon/transport references and invoices can potentially reconstruct the older export graph and compare it with later TST/TSTExport flows.

What this does NOT prove:
- that all 38 declarations involved the same buyer, route or intermediary;
- that every declaration is connected to TECHNOSPETSTRADING;
- that WORLD CHEM physically handled or repacked the goods.

Next pivots:
1. Recover the 38 declaration identifiers and dates.
2. Resolve Polish importers/consignees and customs offices.
3. Match declarations to rail CMR/CIM/wagon identifiers and invoices.
4. Compare recurring payer/bank/forwarder identities with TST/TST PL.

## J3-003 — TST / TSTExport formation and exporter-role chronology

Primary sources:
- TECHNOSPETSTRADING decision DPP-WTPZ.0272.103.2024(2), 17.12.2024: https://www.gov.pl/attachment/b1700454-a36a-4c0c-8c3c-10faed93c99b
- TECHNOSPETSTRADINGEXPORT decision DPP-WTPZ.0272.104.2024(4), 17.12.2024: https://www.gov.pl/attachment/a1f7f6d6-abed-4a51-a0f1-02ef2371d2a5

FACT:
- TECHNOSPETSTRADING began activity in May 2019.
- The official decision says the company website described trade as its principal activity through September 2020 and expansion into fertilizer `production` from 2022.
- From 2022 TECHNOSPETSTRADING appeared as Belarus→Poland consignor/exporter of CN `3102 10 10 00` and `3102 80 00 00`.
- The same decision records the Polish authority's position that TECHNOSPETSTRADING was an intermediary in the UAN product rather than the industrial producer and purchased Grodno Azot products directly or indirectly.
- TECHNOSPETSTRADINGEXPORT began activity on `28.09.2022` and in 2022 appeared as Belarus→Poland consignor/exporter of the same two CN categories.
- GRODNO AZOT had been subject to EU restrictive measures from `02.12.2021` according to the decisions.

Evidence grade: `A` for the dates and official findings.

INFERENCE (`C`):
The timeline is operationally significant: the two TST entities' fertilizer-export role becomes visible after the December 2021 sanctions on GRODNO AZOT, with TSTExport incorporated in September 2022 and appearing as exporter in the same year. Temporal succession is a strong investigation pivot but is not, by itself, proof of intent or sanctions circumvention.

Red-team note:
The TECHNOSPETSTRADINGEXPORT decision heading gives registration number `193648909`; one quoted line in the reasoning appears to contain a shortened/typo form `19368909`. Use `193648909` as the validated official registration number.

Next pivots:
1. Earliest individual TST/TSTExport customs declarations in 2022.
2. First buyer/consignee and first customs broker after 02.12.2021.
3. Compare pricing, wagon ownership, certificates and producer fields before/after the exporter change.

## J3-004 — Official KAS/MSWiA position on post-sanctions replacement entities

Primary source:
- MSWiA/KAS decision on Armen Harutyunyan: https://www.pomorskie.kas.gov.pl/documents/3555563/52925751/Decyzja%2BArmen%2BSeryozhaevich
- Supporting official TST PL decision: https://www.gov.pl/attachment/24038b12-876c-4991-8b93-5d7ea1e716ea

SOURCE_CLAIM / official administrative finding:
- The Polish authority states that after the December 2024 measures, TECHNOSPETSTRADING continued exporting Belarus-origin goods but no longer directly to Polish counterparties; flows moved through companies in other EU states / to other EU states.
- The official Armen decision attributes to Armen Harutyunyan organization of new entities carrying on similar activity after the original companies were sanctioned, and discusses GrandGranit as a replacement/continuation node.
- From February 2025 TST PL's main supplier became a Hungarian entity that had a direct urea contract with TECHNOSPETSTRADING; Belarus-origin goods were customs-cleared in Latvia with Hungary as declared movement/destination; the agreement allowed an external payer.

Evidence grade: `A` for the existence and wording of the official administrative position.

Important legal limitation:
Treat this as KAS/MSWiA's administrative finding, not as a criminal conviction. The fact that sanctions decisions survived WSA review strengthens their administrative evidentiary status but does not convert them into criminal judgments.

Next pivots:
1. Identify the Hungarian entity and Latvian contractual entity by VAT/EORI, invoice, declaration or contract copy.
2. Identify the external payer and banking route.
3. Obtain the complete GrandGranit ownership/directorship source records.

## J3-005 — CONFLICT: which TST entity did Nikita Ter-Minasov direct?

Sources:
- Official Polish decision on Armen Harutyunyan / WORLD CHEM later decision: official text says GrandGranit's owner was a person previously a director in `TECHNOSPETSTRADING LLC`.
- BIC / InvestigateBel document-based reporting identifies Nikita Ter-Minasov as head/acting director of `TECHNOSPETSTRADINGEXPORT LLC` in 2023–2024 and as GrandGranit owner.

Status: `CONFLICT`.
Evidence grade:
- official Polish statement: `A` as a statement of the authority;
- BIC identity/directorship claim: `B` pending archival of the underlying Belarus corporate/employment record.

What cannot be concluded yet:
- whether the official Polish document used TECHNOSPETSTRADING LLC as shorthand, contains an entity-level mistake, or relies on a different management episode;
- whether Ter-Minasov held roles in both entities at different times.

Next pivots:
1. Belarus EGR historical director extracts for both UNP `193256472` and `193648909` covering 2022–2025.
2. Payroll/employment records referenced by BIC.
3. Powers of attorney and signatures on contracts/invoices.

## J3-006 — Comparative wagon-level route through Latvia: MetaTradingProm → Cargo Bridge

Strong secondary source:
- LSM / De facto, 22.06.2025: https://www.lsm.lv/raksts/zinas/latvija/22.06.2025-de-facto-peta-sankciju-apiesanas-shemas-baltkrievu-karbamids-plust-eiropa-caur-latviju.a604247/
- Cargo Bridge public site: https://cargobridge.org/

SOURCE_CLAIM:
LSM traced a separate Grodno Azot-linked urea shipment at wagon level:
- `30.10.2024`: Grodno Azot quality-tested urea in three wagons.
- The same day `MetraTradingProm` prepared shipment documents with the same weight and same wagon numbers and sold to a Polish company at EUR 307/t.
- Polish customs refused entry.
- `10.03.2025`: the cargo was sold to an Estonian company at EUR 405/t.
- In Poland it was reloaded into other wagons and returned to Belarus.
- It was then sent Belarus → Latvia → Liepāja → Lithuania.
- LSM names Latvian forwarder `Cargo Bridge` as sender/forwarder in the Latvian leg.

Cargo Bridge FACT:
- AS CARGO BRIDGE, reg. no. `40203314328`, VAT `LV40203314328`.
- The company publicly offers bulk-cargo forwarding by land/rail/sea, accompanying-document preparation, intermodal transport, stevedoring, customs-document preparation and storage.

Evidence grade: `B` for the tracked shipment; `A/B` for Cargo Bridge's self-published identity/services.

Critical limitation:
This is **not a TECHNOSPETSTRADING shipment**. No TST graph edge should be created from this shipment without separate evidence.

Analytical value:
It demonstrates a proven method for the broader Grodno Azot export network: matching `quality certificate / exact weight / wagon numbers` can survive changes of seller and later detect reloading into new wagons. This is the most practical template for tracing TST cargo through Latvia.

Next pivots:
1. Recover the three original wagon numbers from the underlying documents/images.
2. Identify the Polish buyer and Estonian buyer.
3. Identify reloaded wagon numbers, Liepāja terminal/berth and Lithuanian consignee.
4. Apply the same wagon/weight/certificate matching method to TST, TSTExport and GrandGranit consignments.

## J3-007 — Hungarian identity and remaining Latvian importers still unresolved

Queries repeated with exact contract dates and roles:
- `21.02.2025 TECHNOSPETSTRADING Hungary urea external payer`
- `10.01.2025 TECHNOSPETSTRADING Latvia contract TST PL payer`
- Polish/Hungarian/Latvian variants of the above.
- searches for the other three Latvian companies whose cargoes were under July 2025 customs review.

Result:
- no reliable indexed name for the Hungarian supplier found in this pass — `NO-HIT`;
- no reliable identification of the other three Latvian importers beyond RIN Cargo — `NO-HIT`.

Rule:
Do not infer company names from industry fit or temporal proximity. Require contract/declaration/VAT/EORI or a source explicitly naming the party.

## Documents updated in this pass
- Google Docs Appendix 6: official WSA case outcomes, WORLD CHEM customs-declaration count/identifiers, TST/TSTExport chronology, and Ter-Minasov entity conflict.
- Google Docs Appendix 7: comparative wagon-level Latvia tracing method and Cargo Bridge logistics node, clearly segregated from the TST graph.

## Highest-priority next pivots
1. Full WSA judgments V SA/Wa 597/25, 598/25, 604/25 and any NSA cassation follow-up.
2. The 38 WORLD CHEM customs declaration identifiers.
3. First 2022 TST/TSTExport declarations and counterparties.
4. Historical director extracts resolving Ter-Minasov TST vs TSTExport conflict.
5. Hungarian entity + Latvian contractual entity + external payer.
6. Remaining three Latvian importers under July 2025 review.
7. Original and reloaded wagon numbers in the MetaTradingProm/Cargo Bridge example.
8. TST-specific CMR/CIM, wagon numbers, certificates, batches and customs declarations.
