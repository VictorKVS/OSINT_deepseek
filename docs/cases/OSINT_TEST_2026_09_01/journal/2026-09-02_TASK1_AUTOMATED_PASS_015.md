# Task 1 automated deep-dive — pass 015

Date of access: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Start-of-pass anti-duplication check

Reviewed the latest journal first: `2026-09-02_TASK1_AUTOMATED_PASS_014.md`.
PASS_014 had already covered the fresh Apeks serviss `nodrošinājums`, tax-debt jump, VID-decision lead, court case `A420010026 / A/26/289`, current procuration state and the next VID/UR/court pivots. Those queries were not repeated without cause.

Evidence labels used below:
- `FACT` — direct fact from a registry/public document or stable unique identifier.
- `SOURCE_CLAIM` — source reports an event/role whose underlying primary record is not independently archived in this pass.
- `INFERENCE` — analytical conclusion from established facts.
- `HYPOTHESIS` — unverified working proposition.
- `A` — primary/official evidence.
- `B` — strong secondary/document-based evidence.
- `C` — analytical/discovery lead.
- `D` — weak/unverified.

---

## J15-001 — New named Latvian consignee in the comparative Grodno Azot / MetaTradingProm route: CONCORDE Group

Event/publication date: 2025-06-22.
Access date: 2026-09-02.
Source:
- LSM / LTV `De facto`: https://www.lsm.lv/raksts/zinas/latvija/22.06.2025-de-facto-peta-sankciju-apiesanas-shemas-baltkrievu-karbamids-plust-eiropa-caur-latviju.a604247/

### SOURCE_CLAIM / B
LSM states that, in March 2025, MetaTradingProm sold urea to an Estonian company, while another Belarusian company, `Belamiks`, was shown as the consignor; the Latvian consignee was named as `Concorde group`. LSM reports that Concorde Group told the programme it did not see risks in importing the urea into Latvia.

The same article separately traces a Grodno Azot-linked cargo through exact weight / wagon-number continuity and later reloading, and names Cargo Bridge in the Latvian leg. That comparative cargo-tracing methodology was already journaled in PASS_003; the **Concorde Group consignee identity itself had not previously been elevated into the journal as a resolved node**.

### Critical scope / what this does NOT prove
- This is **not proven to be a TECHNOSPETSTRADING shipment**.
- No edge `TECHNOSPETSTRADING ↔ CONCORDE Group` is created from this article.
- It does not establish the final buyer, MRN, wagon numbers, warehouse used, payment route or beneficial origin of the specific cargo.
- `Belamiks` being listed as consignor does not itself establish that Belamiks produced the urea.

### Next pivots
1. Resolve the exact legal entity behind LSM's `Concorde group` by registration/VAT identifiers.
2. Search its railway code, customs/broker footprint, operational warehouse address, bank/payment identifiers and cargo documents.
3. Search MetaTradingProm/Belamiks/Concorde exact-name combinations with CMR/SMGS/MRN, invoice, certificate, wagon and batch terms.

---

## J15-002 — CONCORDE Group corporate identity resolved to a concrete Latvian transport company

Sources:
- ZL.lv registry-derived profile: https://www.zl.lv/en/company/concorde-group-sia/
- Firmas.lv: https://www.firmas.lv/lv/uznemumi/concorde-group/40103935545
- B2BHint registry-derived profile: https://b2bhint.com/en/company/lv/concorde-group--40103935545

### FACT / B+
A Latvian company matching the exact published name and logistics profile is:
- registered name: SIA `CONCORDE Group`;
- registration no.: `40103935545`;
- VAT: `LV40103935545`;
- incorporation: `2015-10-05`;
- legal address: `Hāpsalas iela 6-69, Rīga, LV-1005`;
- public category/NACE: rail freight transport (`49.20`) / transport support.

Evidence is graded B+ because the accessible pages reproduce Latvian registry/VID data, but this pass did not retrieve a signed/full official UR extract directly.

### SOURCE_CLAIM / B
Registry-derived B2BHint identifies:
- `Iļja Lavrovs` — board member since 2015, right of individual representation;
- `Svetlana Lavrova` — shareholder/member and beneficial owner since 2022.

### What this does NOT prove
- that this exact legal entity is the LSM consignee beyond the strong name+jurisdiction+rail-logistics match; LSM did not publish the registration number;
- that either named person signed the March 2025 cargo documents;
- that the company had any direct contract with TECHNOSPETSTRADING.

### Next pivots
- direct Latvian UR extract and historical member/board filings;
- signatures on CMR/SMGS/customs documents;
- exact railway code and customs/EORI identifiers.

---

## J15-003 — High-value operational/payment fingerprint: railway code, port warehouse, weighing/labeling and public IBANs

Source document:
- Transport and Telecommunication Institute (TSI) hosted PDF: https://tsi.lv/wp-content/uploads/2025/12/prakses-piedavajums.pdf
- Search-indexed document text accessed 2026-09-02. The PDF itself returned HTTP 403 to direct fetch during this pass, so visual page-level verification is `BLOCKED`; exact document publication date is not printed in the indexed text (URL path indicates `/2025/12/`).

### SOURCE_CLAIM / B
The company-authored recruitment/training document states that SIA CONCORDE Group provides:
- road transport including Baltic ports Riga/Klaipėda/Tallinn;
- transit declaration and customs-document preparation;
- international sea transport;
- railway transport Latvia → CIS;
- **its own railway code**, said to enable direct RŽD/LDZ tariffs for wagon/container transport;
- warehouse work in the Riga port area;
- cargo inspection, storage, loading/unloading, packing, **weighing and labeling**, palletising and load securing.

Published operational contacts in the document:
- `dk@concorde.lv`
- `info@concorde.lv`
- `+371 25 665 688`

Published banking/payment identifiers:
- Luminor Bank AS — SWIFT `RIKOLV2X` — EUR IBAN `LV39RIKO0002930240781`;
- AS SEB Banka — SWIFT `UNLALV2X` — USD IBAN `LV04UNLA0050023606117`.

### Analytical value / INFERENCE C
These are strong machine-search keys for invoice/payment-order/CMR/SMGS/MRN reconstruction in the **comparative** Latvian fertilizer route. The combination of rail capability + port-area warehousing + customs documentation + public corporate bank identifiers makes CONCORDE Group a useful cargo/payment pivot.

### RED TEAM — no physical relabeling inference
The phrase `weighing, labeling` describes a legitimate generic warehouse service capability. It does **not** prove that any fertilizer cargo was relabeled, repacked, or had its origin altered physically. Physical relabeling remains unconfirmed without shipment-specific warehouse acts/photos/labels/packaging records.

### Next pivots
- exact railway code;
- exact Riga port warehouse/lease/customs status;
- search both IBANs/SWIFTs in public invoices, court appendices and payment orders;
- match `dk@concorde.lv`, `info@concorde.lv`, phones and VAT to cargo records.

---

## J15-004 — Legal address vs operational address creates a second physical Riga pivot

Sources:
- legal address: ZL/Firmas above;
- Cargoson carrier profile: https://www.cargoson.com/integrations/concorde-group

### SOURCE_CLAIM / B-C
Cargoson identifies the same company by reg. no. `40103935545` and VAT `LV40103935545` but gives an operational/contact address `Rāmuļu iela 29, Rīga, LV-1005`, phone `+371 26855726`, website `concorde.lv`.

### INFERENCE / C
This may represent an operational office/warehouse/logistics point distinct from the legal address Hāpsalas iela 6-69. Because the TSI document separately mentions a warehouse in Riga port territory, `Rāmuļu iela 29` is a concrete physical pivot to verify against property/lease/customs-warehouse/port records.

### What this does NOT prove
- that Rāmuļu iela 29 is itself the warehouse mentioned in the TSI document;
- that the March 2025 urea was stored there;
- that the site is a customs warehouse.

### Next pivot
Property/tenant history and warehouse/customs permits for `Rāmuļu iela 29`, then shipment-level gate/weighing records if a legal basis/source becomes publicly available.

---

## J15-005 — 1-hop corporate pivot: North Meridian's Group through common owner

Sources:
- Datreal public-company graph: https://datreal.com/fi/lv/company/40103935545
- North Meridian's Group registry-derived profiles: https://www.firmas.lv/lv/uznemumi/north-meridian-s-group/40103804046 ; https://saraksts.lv/40103804046

### SOURCE_CLAIM / B-C
Public registry-derived relationship data connect Svetlana Lavrova to both:
- SIA `CONCORDE Group`, reg. `40103935545`;
- SIA `North Meridian's Group`, reg. `40103804046`.

North Meridian's Group:
- incorporated 2014-07-03;
- legal address `Tvaika iela 16-57, Rīga, LV-1005`;
- registry-derived main profile: transport support services;
- no VAT number shown in current Firmas/Lursoft mirror;
- current open-data mirror reports 2025 turnover `0 EUR` and 0 employees, and VID taxpayer rating `N` / inactive taxpayer.

### What this does NOT prove
Shared ownership is a valid corporate relationship, but there is no evidence in this pass that North Meridian's Group participated in fertilizer transport, invoicing, customs clearance, warehousing or payment. No cargo edge is created.

### Next pivot
Search historical invoices/contracts/leases and address/phone/e-mail overlap; do not expand further unless a second operational document links North Meridian's Group to the cargo chain.

---

## J15-006 — Negative / blocked results logged

- `BLOCKED`: direct visual retrieval of `https://tsi.lv/wp-content/uploads/2025/12/prakses-piedavajums.pdf` returned HTTP 403; indexed text is available, but the PDF cannot be visually archived/screenshot in this pass.
- `NO-HIT`: no shipment-level MRN, CMR/CIM/SMGS, wagon number, truck registration, quality-certificate number, invoice number or payment-order reference was recovered for the Concorde/MetaTradingProm/Belamiks shipment in this pass.
- `NO-HIT`: this pass did not identify the still-unknown Hungarian TST PL supplier, the external payer in the TST/Hungary arrangement, or the French Astramar contact.
- `NO-LINK`: no TECHNOSPETSTRADING ↔ CONCORDE Group edge is created; the new node belongs to the broader Grodno Azot / MetaTradingProm comparative route until shipment-specific evidence says otherwise.

## Documents updated
- Google Docs Appendix 7: appended a dedicated section on CONCORDE Group as a newly resolved Latvian consignee/logistics/payment pivot in the comparative route, with explicit segregation from the TST graph and the physical-relabeling Red Team caveat.

## Priority next pivots
1. Exact railway code of CONCORDE Group and LDZ/RŽD customer/forwarder references.
2. `Rāmuļu iela 29` property/lease/warehouse/customs status.
3. Search `LV39RIKO0002930240781`, `LV04UNLA0050023606117`, `RIKOLV2X`, `UNLALV2X`, `dk@concorde.lv`, `info@concorde.lv` in invoices/payment orders/court or customs exhibits.
4. MetaTradingProm + Belamiks + Concorde exact cargo fingerprint: certificate date, mass, wagon number, invoice, MRN/SMGS/CMR, buyer/consignee.
5. Continue unresolved primary TST targets: Hungary legal entity, external payer, French Astramar contact, shipment-level MRN/CMR/CIM/SMGS and wagon/truck IDs.
