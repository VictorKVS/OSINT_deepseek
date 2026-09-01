# Task 1 — Automated deep-dive pass 004

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly stated in a registry/official/public record.
- `SOURCE_CLAIM` — statement by a source that has not yet been independently reproduced from the underlying primary record.
- `INFERENCE` — analytical conclusion from established facts.
- `HYPOTHESIS` — proposition requiring evidence.

## Evidence grades
- `A` — primary/official record.
- `B` — strong secondary / registry aggregator / documented corporate page.
- `C` — analytical lead or incomplete attribution.
- `D` — weak/unverified lead; not usable in conclusions.

---

## J1-A004-01 — New historical address-cluster node: ООО «ХимТехИнвест» / HimTechInvest

### FACT
A further company was resolved at the same address used by TECHNOSPETSTRADING, TECHNOSPETSTRADINGEXPORT and AS Garantstroy:

- name: ООО «ХимТехИнвест»;
- UNP: `192648636`;
- EGR registration: `2016-05-13`;
- address: Belarus, Minsk, Naklonnaya 28;
- primary activity: wholesale of machinery/equipment for agriculture and forestry, code `46610`.

Source:
- Kartoteka.by registry card (states EGR registration and address): https://kartoteka.by/unp-192648636
- B2BHint TST address-cluster view: https://b2bhint.com/en/company/by/ooo-tehnospectrejding--193256472

Evidence grade: `B` for the accessible aggregator rendering of EGR data. Primary EGR page should still be archived when technically retrievable.

### Analytical value
The chronological address cluster now contains at least:

1. AS Garantstroy — registered 2014; later moved to Naklonnaya 28.
2. HimTechInvest — registered 2016; Naklonnaya 28.
3. TECHNOSPETSTRADING — registered 2019; Naklonnaya 28.
4. TECHNOSPETSTRADINGEXPORT — registered 2022; Naklonnaya 28.

AS Garantstroy, HimTechInvest and TECHNOSPETSTRADING also have an agricultural-machinery wholesale activity overlap in public registry-derived data.

### INFERENCE
The repeated address + sector overlap is a useful continuity indicator and justifies a historical corporate/personnel cross-check.

Evidence grade for continuity inference: `C`.

### What this does NOT prove
- common ownership;
- shared management;
- shared bank accounts;
- common contracts or inventory;
- that Naklonnaya 28 is a single-tenant facility;
- participation of HimTechInvest in fertilizer export or sanctions circumvention.

### Next pivot
- founders/directors of HimTechInvest by year;
- historical EGR changes and address start date;
- landlord/property owner of Naklonnaya 28;
- shared phones/e-mails/domains/bank accounts/POAs with AS Garantstroy/TST;
- court/procurement records with the same counterparties.

---

## J1-A004-02 — 2020 PPE-production overlap at Naklonnaya 28

### SOURCE_CLAIM
Public business-directory profiles show both HimTechInvest and TECHNOSPETSTRADING presenting PPE-related production at the same physical/legal address around 2020:

- HimTechInvest Flagma profile: Naklonnaya 28; activity stated as production of respiratory-protection equipment and wholesale; representative listed as Alexey Petrovich Stasevich; profile registration 2020-09-17.
- TECHNOSPETSTRADING Flagma profile: legal and actual address Naklonnaya 28; activity stated as production of disposable medical masks; profile registration 2020-12-14.

Sources:
- https://flagma.by/1827415/
- https://flagma.by/1878197/

Evidence grade: `B/C`. The pages demonstrate how the companies publicly described themselves, but they do not independently prove actual production, production capacity, ownership of machinery, or common operations.

### INFERENCE
The shared address plus contemporaneous PPE-related self-description is a stronger operational pivot than address coincidence alone and merits checking whether the companies used common premises/equipment/personnel during 2020.

Evidence grade: `C`.

### Red Team
Do not convert this into a shared-enterprise edge without a lease, equipment record, common employee, phone/e-mail/domain overlap, invoice or other primary evidence.

### Search result
No reliable direct overlap was found in this pass between TST and HimTechInvest on the publicly visible HimTechInvest phone/e-mail/person name.

Status: `NO-HIT` for direct personnel/contact attribution.

---

## J1-A004-03 — AS Garantstroy current liquidation status; stale-source conflict

### FACT / strong current registry-derived indication
Kartoteka.by currently displays for ООО «АС Гарантстрой», UNP `192237039`:

- EGR status: `Находится в процессе ликвидации`;
- MNS status: `В процессе ликвидации`;
- date shown: `06.09.2024`;
- address: Minsk, Naklonnaya 28, non-residential premises;
- activity: code 46610.

Source:
- https://kartoteka.by/unp-192237039

Evidence grade: `B+` pending archival retrieval from the Belarus EGR itself (direct EGR page timed out in this pass).

### CONFLICT
B2BHint currently renders AS Garantstroy as active/not in liquidation, but the same page notes its company data were last updated four years ago. This conflicts with the more recent Kartoteka status dated 06.09.2024.

Source:
- https://b2bhint.com/en/company/by/ooo-as-garantstroj--192237039

Resolution rule: prefer the newer registry-derived status provisionally; obtain the current official EGR extract before upgrading to grade A.

### Analytical value
The liquidation date precedes the December 2024 Polish sanctions against TST/TSTExport, but chronology alone does not establish causation or asset/business transfer.

### What this does NOT prove
- why liquidation began;
- whether assets/personnel/contracts moved to TST or another entity;
- any relationship between liquidation and sanctions;
- insolvency or criminal proceedings.

### Next pivot
- current official EGR extract;
- liquidation notice and liquidator identity;
- asset/creditor notices;
- last directors/founders;
- transactions or transfers around 2024.

---

## J1-A004-04 — PKP CARGO operational-restriction list: TST / TSTExport / WORLD CHEM / GrandGranit

### FACT
An official PKP CARGO appendix titled `Załącznik do ograniczenia Nr 326-25 (wprowadzone tg COPP-7803/719/22)`, status date `07.10.2025`, lists in its `Nazwa Klienta` table:

- position 90 — TECHNOSPETSTRADINGEXPORT LLC, Minsk, Naklonnaya 28;
- position 91 — TECHNOSPETSTRADING LLC, Minsk, Naklonnaya 28;
- position 92 — WORLD CHEM TRADING CO. L.L.C., Dubai;
- position 93 — ROSTUMEL HOLDING LIMITED, Cyprus;
- position 94 — MetaTradingProm LLC, Minsk;
- position 100 — GrandGranit LLC, Minsk.

Primary source:
- PKP CARGO PDF: https://www.pkpcargo.com/wp-content/uploads/2023/11/zal.doograniczenia32625zm.36.pdf

Evidence grade: `A` for presence of the named entities in PKP CARGO's official restriction appendix.

### Analytical value
This creates a new railway-compliance pivot. Several entities already relevant to the fertilizer investigation are independently present in the same PKP CARGO operational restriction appendix.

### Critical limitation / Red Team
The main operative text of restriction No. 326-25 was not recovered in this pass. Therefore do **not** describe the appendix as proof that PKP CARGO imposed a complete carriage ban, froze cargo, or refused a specific shipment. The document only establishes that the entities were listed as clients under that restriction at the stated date.

Co-listing also does not by itself create a commercial or control relationship between TST, Rostumel, MetaTradingProm and GrandGranit.

### Next pivot
- recover the operative text of restriction No. 326-25 and telegram COPP-7803/719/22;
- reconstruct change history across earlier appendices (398-23, 352-24, 326-25) to identify first-addition dates for TST/TSTExport/WORLD CHEM/GrandGranit;
- determine whether the restriction corresponds to sanctions screening, payment/compliance controls, carriage refusal or another operational measure;
- compare first-addition dates with Polish sanctions dates and known railway route changes.

---

## J1-A004-05 — Hungary / Latvia contract identities

Repeated exact-date/name searches did not disclose reliable public identities for:

- the Latvian entity in the 10.01.2025 contract described by Polish authorities;
- the Hungarian entity in the 21.02.2025 contract;
- the external payer under the Hungarian supply arrangement.

Status: `NO-HIT`.

No candidate company has been promoted into the graph without a contract, VAT/EORI, invoice, customs declaration or other identifying primary evidence.

---

## Updated priority queue

1. Current official EGR extract + liquidation file for AS Garantstroy.
2. HimTechInvest founders/directors/history and physical occupancy of Naklonnaya 28.
3. Main text of PKP CARGO restriction 326-25 / telegram COPP-7803/719/22.
4. First-addition date of TST/TSTExport/WORLD CHEM/GrandGranit to PKP restriction appendices.
5. Latvian contract party (10.01.2025), Hungarian company (21.02.2025), external payer.
6. CMR/CIM/SMGS/wagon numbers and cargo fingerprints linking physical shipments across Belarus–Latvia–Hungary/Poland/EU.
