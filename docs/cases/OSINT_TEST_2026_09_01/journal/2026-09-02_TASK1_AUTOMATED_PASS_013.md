# Task 1 — Automated deep-dive pass 013

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / linked fertilizer-export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly observable in a primary/official/registry document or an exact-match check.
- `SOURCE_CLAIM` — claim made by an identified source and not independently adjudicated here.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — testable working theory.

Grades: `A` primary/official; `B` strong document-based secondary/registry mirror; `C` analytical lead; `D` weak/unverified.

## J1-A013-01 — Apeks serviss: exact controller/signatory identified
Type: FACT / registry-derived
Grade: B+

Current Latvian registry mirrors identify SIA `Apeks serviss`, reg. `41503055853`, VAT `LV41503055853`, Spaļu iela 1P, Daugavpils. The same open-data record identifies `Aņisjko Vjačeslavs` as:
- board member since 10.06.2011 with the right to represent the company individually;
- 100% shareholder since 07.10.2021;
- beneficial owner since 15.07.2019.

Sources:
- https://vissviena.lv/uznemums/41503055853/sabiedriba-ar-ierobezotu-atbildibu-apeks-serviss/
- https://b2bhint.com/en/company/lv/apeks-serviss--41503055853
- https://www.firmas.lv/lv/uznemumi/apeks-serviss/41503055853

### Analytical value
This turns the Apeks branch from an organization-only node into a signature/authority pivot. Any lawfully published CMR, SMGS/CIM, customs declaration, warehouse receipt, POA or contract can now be checked against a specific individual with sole representation authority.

### What this does NOT prove
- that Aņisjko personally signed or knew of a specific TECHNOSPETSTRADING shipment;
- that he had any relationship to Armen Harutyunyan outside Apeks transactions;
- any unlawful conduct.

### Next pivots
1. Search exact name/transliterations in TST/Apeks contracts, CMR/SMGS/MRN, warehouse records and court attachments.
2. Obtain registry historical officer/procuration documents dated 26.06.2025 and 07.04.2026.

## J1-A013-02 — Material corporate changes immediately after the June-2025 public exposure
Type: SOURCE_CLAIM + TEMPORAL CORRELATION
Grade: B for events; C for any causal interpretation

Okredo records for Apeks serviss:
- `01.07.2025` — change in officers;
- `01.07.2025` — change in procurations;
- `01.07.2025` — another unidentified corporate change;
- `09.04.2026` — change in procurations.

Firmas.lv exposes the underlying non-public-part filing metadata: two applications and a company/organization decision are dated `26.06.2025` and registered `01.07.2025`; another application is dated `07.04.2026` and added `09.04.2026`.

Sources:
- https://okredo.com/en-lv/company/sabiedriba-ar-ierobezotu-atbildibu-apeks-serviss-41503055853
- https://www.firmas.lv/lv/uznemumi/apeks-serviss/41503055853

LTV/LSM's report naming Apeks as a carrier of fertilizer from the same Belarusian company in the TECHNOSPETSTRADING context was published on `22.06.2025`:
- https://www.lsm.lv/raksts/zinas/latvija/22.06.2025-de-facto-peta-sankciju-apiesanas-shemas-baltkrievu-karbamids-plust-eiropa-caur-latviju.a604247/

### INFERENCE / C — temporal correlation only
The corporate documents were dated four days after the LSM publication. This timing is investigative-relevant but **does not prove** that the filings were a response to the publication, sanctions scrutiny or any fertilizer transaction. The names and scope of the procuration changes are not visible in the open metadata.

### Next pivots
1. Lawfully obtain the UR EDOC filings dated 26.06.2025 and 07.04.2026.
2. Extract procurist identity, rights, term, cancellation/appointment and signatures.
3. Search those names in customs/logistics documents before and after the change dates.

## J1-A013-03 — New Apeks serviss administrative court case against Latvian SRS/VID
Type: SOURCE_CLAIM
Grade: B

Okredo's public legal-proceedings section reports an open administrative case:
- opened/date shown: `22.04.2026`;
- case: `A420010026`, secondary identifier `A/26/289`;
- applicant: SIA `Apeks serviss`;
- respondent: `Valsts ieņēmumu dienests` (State Revenue Service / VID);
- court: `Administratīvā apgabaltiesa`;
- status: `Open`;
- one hearing shown.

Source:
- https://okredo.com/en-lv/company/sabiedriba-ar-ierobezotu-atbildibu-apeks-serviss-41503055853

Current Firmas/Lursoft-derived data separately show substantial VID-administered tax debt in mid-2026, but the public case card does not state its subject.

### What this does NOT prove
- that the case concerns TECHNOSPETSTRADING, urea, sanctions, customs procedure 42 or fertilizer imports;
- that it concerns the tax debt;
- that VID alleged wrongdoing.

### Next pivots
1. Search Latvian court portal for acceptance order, subject matter, hearing schedule and later judgment.
2. Search exact case number `A420010026` and `A/26/289` in official decisions/publications.
3. Only connect the case to the fertilizer investigation if the procedural document itself provides that bridge.

## J1-A013-04 — Historical customs-warehouse authorization gives exact Apeks infrastructure identifiers
Type: FACT / document-derived historical infrastructure
Grade: B+

A published `Latvijas muitas noliktavu saraksts uz 01.11.2016` contains row 89 for `APEKS SERVISS SIA`:
- VAT/entity identifier: `LV 41503055853`;
- customs-warehouse authorization: `LV-98-A-0280`;
- legal/warehouse address: Spaļu iela 1P, Daugavpils;
- customs codes: `0810`, `0816`;
- contact at the time: `Nikita Katjušins`, tel. `29901130`, `apeks.serviss@gmail.com`.

Source PDF:
- https://www.lauto.lv/wp-content/uploads/2016/03/Latvijas-muitas-noliktavu-saraksts-uz-01.11.2016.pdf

The PDF was visually checked at the row containing Apeks.

### What this does NOT prove
- that authorization `LV-98-A-0280`, the customs codes or Nikita Katjušins remained current in 2025–2026;
- that a TST shipment used that authorization.

### Next pivots
1. Find the 2025/2026 Latvian customs-warehouse register and version-diff authorization `LV-98-A-0280`.
2. Search exact authorization/codes in MRN, transit and customs documents.
3. Search Nikita Katjušins only as a historical operational contact, not as a current officer without corroboration.

## J1-A013-05 — Apeks explicitly advertises the exact document/logistics functions sought in this case
Type: SOURCE_CLAIM / self-declared capability
Grade: B

Current Apeks business listing describes services including:
- customs warehouse and customs brokerage;
- declarations and document processing;
- TIR carnet;
- CMR;
- `SMGS consignment note`;
- INTRASTAT;
- railway access roads / railway supply;
- import/export/transit;
- listed service corridors including Belarus and Hungary.

Source:
- https://www.zl.lv/en/company/apeks-serviss-sia/

LSM separately reported in June 2025 that Apeks transported fertilizer from the same Belarusian supplier discussed in the TECHNOSPETSTRADING part of the investigation.

### INFERENCE / C
Spaļu iela 1P is therefore a high-priority **documentary pivot** for recovery of TST shipment records: CMR/SMGS/MRN/warehouse receipts are operationally plausible at this node. Capability alone is not evidence that a particular TST shipment used each service or Hungary corridor.

## J1-A013-06 — TPC/LOGITRA expansion at the same physical node: named Daugavpils operational contact and origin-certificate function
Type: FACT for corporate self-description + prior independent operational corroboration
Grade: A for TPC's current self-published service/contact data; B for historical TPC↔Apeks operational relationship

TPC's current site identifies:
- `Warehouse in Daugavpils (Latvia), railway loading works` at `Spalu iela 1p, Daugpilis`;
- contact for that warehouse: `Giedrius Lubas`, `+370 687 71 344`, `tpc@tpc.eu`;
- a separate origin-certificate function/contact: `Vaidutė Slišajevienė`, `sert@tpc.eu`.

Source:
- https://tir-service.lt/lt/

Independent Lithuanian civil-case reporting in case `e2-629-936/2025` describes an unrelated 2018 shipment whose CMR routed goods from Klaipėda to SIA Apeks Serviss in Daugavpils via UAB Tranzito paslaugų centras; it therefore supports that TPC↔Apeks is a real operational logistics relationship, not merely a shared-address coincidence.

Source:
- https://www.temidy.lt/byla/992f2e3b-582f-4306-9bf6-689b841e4e80

### What this does NOT prove
- TPC handled TECHNOSPETSTRADING fertilizer;
- TPC issued or changed a certificate of origin for TST cargo;
- Giedrius Lubas or Vaidutė Slišajevienė had any role in the disputed shipments.

### Next pivots
1. Search TST/Apeks documents for `tpc@tpc.eu`, `sert@tpc.eu`, Giedrius Lubas, TPC code `300154147` and VAT `LT100001992119`.
2. Search for certificate issuer/contact metadata and customs declarations referencing the Daugavpils warehouse.

## J1-A013-07 — Second customs operator historically at the same physical warehouse: TKS SIA (do not make a TST edge yet)
Type: FACT / infrastructure-neighbor lead
Grade: B+

The same 01.11.2016 customs-warehouse list shows `TKS SIA`, reg/VAT `LV41503039505`, authorization `LV-98-A-0320`, with the warehouse address `Spaļu iela 1P, Daugavpils` and the same customs codes `0810/0816`. Current 2026 registry-mirror data show TKS remains active with NACE 5210 storage/warehousing, legal address Višķu iela 21M.

Sources:
- https://www.lauto.lv/wp-content/uploads/2016/03/Latvijas-muitas-noliktavu-saraksts-uz-01.11.2016.pdf
- https://saraksts.lv/41503039505

### Red Team boundary
Do **not** create `TKS ↔ TECHNOSPETSTRADING` or `TKS ↔ Apeks corporate control` edges from physical co-location alone. The value is as an infrastructure-neighbor pivot. A second basis is required: CMR/SMGS/MRN, contract, shared contact, customs filing, ownership/person, payment or actual cargo record.

## Priority pivots from this pass
1. Obtain/identify the Apeks procurist changes of 26.06.2025 and 07.04.2026.
2. Recover court documents for `A420010026 / A/26/289` and determine the actual subject.
3. Version-diff current Latvian customs authorization for Apeks against historical `LV-98-A-0280`.
4. Search `Aņisjko Vjačeslavs`, `Nikita Katjušins`, `Giedrius Lubas`, `apeks.serviss@gmail.com`, `tpc@tpc.eu`, `sert@tpc.eu`, `0810/0816`, `LV-98-A-0280` in CMR/SMGS/MRN/invoices/warehouse records.
5. Preserve TKS only as a candidate infrastructure neighbor until an independent operational edge appears.

No new reliable shipment-level MRN, wagon number, Hungarian company identity, French requester identity or external payer was identified in this pass. No private-relative or ethnicity/nationality-based links were added.
