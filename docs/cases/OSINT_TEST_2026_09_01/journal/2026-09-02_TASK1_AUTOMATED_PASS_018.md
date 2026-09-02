# Task 1 automated deep-dive — pass 018

Date of access: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE — high-value gap closure for deliverable

## Start-of-pass anti-duplication check

Reviewed the latest journal first: `2026-09-02_TASK1_AUTOMATED_PASS_017.md`. PASS_017 had already covered KRASTS INVESTS/Jānis Jansons identity-resolution and the unresolved Hungarian/external-payer/French/shipment gaps. This pass did not repeat those closed searches without cause and concentrated on official decisions and primary documentary material capable of changing the deliverable conclusions.

Evidence labels:
- `FACT` — directly visible fact in an official/public record or stable primary document.
- `SOURCE_CLAIM` — source reports an operational fact whose underlying source record is not itself public/read in this pass.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — unverified working proposition.
- `A/B/C/D` — official/primary → strong documentary secondary → analytical/discovery → weak/unverified.

---

## J18-001 — Official TST PL decision partially closes the “external payer” gap

Primary source:
- MSWiA decision `DPP-WTPZ.0272.113.2025.BS(2)`, dated `2025-10-09`, concerning TST PL Sp. z o.o.
- Official gov.pl copy: https://www.gov.pl/attachment/24038b12-876c-4991-8b93-5d7ea1e716ea
- Official KAS mirror: https://www.mazowieckie.kas.gov.pl/c/document_library/get_file?groupId=3554560&uuid=a2bed4e5-8b26-4799-9114-21e59065f66c
Event dates described by the decision: `2025-01-10`, `2025-02-21`, and activity from February 2025.
Access date: `2026-09-02`.

### SOURCE_CLAIM / A — documentary payer role
The ministerial decision, relying on KAS findings, states that:
- from February 2025 the main TST PL supplier was an unnamed Hungarian company trading fertilizer under CN 3102;
- the fertilizer was of Belarusian origin, customs-cleared in Latvia, with Hungary declared as the country of destination/movement;
- the Hungarian entity had a urea contract with TECHNOSPETSTRADING containing a clause permitting payment by an external payer;
- on `2025-01-10` a new contract was concluded with an unnamed Latvian entity in which **TST PL was designated as payer although it was not a party to the contract**, with the goods then moving to the Hungarian company;
- on `2025-02-21` TECHNOSPETSTRADING concluded a direct contract with the Hungarian entity, again containing an external-payer clause.

This materially closes the *role* portion of the “external payer” gap: TST PL is explicitly identified by the official decision as the payer designated in the 10.01.2025 Latvian contract.

### What this confirms
- TST PL’s documentary payer role in the unnamed Latvian contract dated `2025-01-10`, according to the official KAS/MSWiA finding;
- a two-stage contractual chronology: Latvian contract on 10.01.2025 and direct TECHNOSPETSTRADING→Hungarian contract on 21.02.2025;
- the unnamed Hungarian entity became the main TST PL supplier from February 2025;
- Belarusian origin / Latvian customs clearance / declared movement to Hungary as officially recorded findings.

### What this does NOT prove
- that a bank transfer was actually executed by TST PL;
- payment order/reference, bank, IBAN/SWIFT used by TST PL, amount, value date or currency;
- name/VAT/EORI of the Latvian counterparty;
- name/VAT/EORI of the Hungarian company;
- shipment-level MRN, CMR/CIM/SMGS, vehicle/wagon number, lot or certificate.

### Next pivots
1. Obtain the contract/invoice/payment-order exhibits behind the KAS finding, especially the 10.01.2025 Latvian contract and 21.02.2025 Hungarian contract.
2. Search for historical Polish VAT White List bank-account records for TST PL around 10.01–21.02.2025 and compare with any payment-order copy.
3. Resolve the Latvian and Hungarian legal entities only from contract/VAT/EORI/MRN identifiers, not name similarity.

---

## J18-002 — Official Armen decision confirms TECHNOSPETSTRADING-linked import into Latvia under customs procedure 42

Primary source:
- MSWiA decision `DPP-WTPZ.0272.112.2025.BS(2)`, dated `2025-10-09`, concerning Armen Seryozhaevich Harutyunyan.
- Official gov.pl copy: https://www.gov.pl/attachment/97d03558-f9ce-491e-ba7c-85ceffb8d86e
Access date: `2026-09-02`.

### SOURCE_CLAIM / A
The official decision states, based on KAS findings, that import into Latvia of goods of Belarusian origin was carried out through TECHNOSPETSTRADING using **customs procedure 42** — import from a third country into one EU Member State followed by movement to another EU Member State. The same section describes the Hungarian supplier/TST PL chain and the external-payer clause.

### What this confirms
- an official administrative finding connecting TECHNOSPETSTRADING, Belarus-origin goods, import into Latvia and procedure 42;
- Latvia was not merely mentioned as a transit geography: a concrete customs procedure is identified.

### What this does NOT prove
- MRN/declaration number;
- Latvian declarant/representative/EORI;
- customs office/post;
- exact consignee per declaration;
- vehicle/wagon/CMR/SMGS identifiers;
- that every TST-linked Latvia shipment used procedure 42.

### Next pivot
Recover one shipment-level MRN or customs annex entry; from it pivot to declarant, EORI, customs representative, VAT movement and transport documents.

---

## J18-003 — Important official-document conflict: TST PL decision ID is .113, not .106

Primary sources:
1. TST PL decision itself: `DPP-WTPZ.0272.113.2025.BS(2)`, `2025-10-09`.
2. Armen decision `DPP-WTPZ.0272.112.2025.BS(2)` independently cites TST PL as `.113.2025.BS(2)`.
3. WORLD CHEM deletion-refusal decision `DPP-WTPZ.0272.34.2025(45)`, `2025-12-22`, official copy: https://www.gov.pl/attachment/8444bcb4-a2e6-462e-8496-eee08e91d44e

### CONFLICT / A
The later WORLD CHEM refusal decision contains a cross-reference identifying the TST PL decision as `DPP-WTPZ.0272.106.2025.BS(3)`. That identifier is inconsistent with the TST PL decision itself and with the Armen decision. The same WORLD CHEM decision and the TST PL decision identify `.106.2025.BS(3)` as the **GrandGranit** decision of `2025-08-06`.

### Corrected conclusion for the deliverable
- TST PL: **`DPP-WTPZ.0272.113.2025.BS(2)`**, 09.10.2025.
- GrandGranit: **`DPP-WTPZ.0272.106.2025.BS(3)`**, 06.08.2025.
- The WORLD CHEM decision’s `.106` reference to TST PL should be treated as an apparent clerical/cross-reference error unless another primary record establishes otherwise.

### What this does NOT prove
- why the error occurred;
- any substantive defect in the underlying TST PL or GrandGranit findings.

---

## J18-004 — WORLD CHEM deletion refusal adds customs-volume and litigation evidence

Primary source:
- MSWiA decision `DPP-WTPZ.0272.34.2025(45)`, dated `2025-12-22`, refusing WORLD CHEM TRADING CO. L.L.C.’s request of `2025-11-12` for removal from the Polish sanctions list.
- Official copy: https://www.gov.pl/attachment/8444bcb4-a2e6-462e-8496-eee08e91d44e
Access date: `2026-09-02`.

Entity identifiers stated in the decision:
- WORLD CHEM TRADING CO. L.L.C.
- Dubai commercial registry no. `2823197`
- licence `1115715`
- BLS Federal Reservation Number `11965260`
- address: Office 02, Aber King Khalfan Muhammad Khalfan Al Hamli – Al Thanyah 1, Dubai.

### FACT / A — regulatory procedure
- Original sanction decision: `DPP-WTPZ.0272.105.2024(3)`, `2024-12-17`.
- WORLD CHEM requested removal on `2025-11-12`.
- MSWiA refused removal on `2025-12-22` in `DPP-WTPZ.0272.34.2025(45)`.
- The decision names attorney Marek Drężek as WORLD CHEM’s legal representative in the removal proceeding.

### SOURCE_CLAIM / A — customs and producer role
According to KAS findings reproduced in the decision:
- during `2021–2024`, WORLD CHEM appeared in **38 customs declarations** as sender/exporter from Belarus to Poland of urea `CN 3102 10 10 00` and UAN `CN 3102 80 00 00`;
- Grodno Azot was identified as the actual producer for the relevant Belarusian industrial fertilizers, while WORLD CHEM functioned as an intermediary rather than producer.

The underlying customs declarations are protected in the non-public tax/customs-secret material, so the 38-declaration and producer/intermediary findings are A-level official source claims, not independently reconstructed shipment records.

### FACT / A — court outcomes as stated in official decision
- WORLD CHEM: WSA Warszawa judgment `V SA/Wa 604/25`, `2025-08-05`, complaint dismissed; the later decision states the judgment is final (`prawomocny`).
- TECHNOSPETSTRADING LLC: WSA Warszawa judgment `V SA/Wa 597/25`, `2025-08-13`, complaint dismissed.
- TECHNOSPETSTRADINGEXPORT LLC: WSA Warszawa judgment `V SA/Wa 598/25`, `2025-08-13`, complaint dismissed.

### What this does NOT prove
- individual MRNs/declaration numbers, weights, wagons or buyers within the 38 declarations;
- that the TST/TSTExport court judgments were final — finality is explicitly stated here for WORLD CHEM, not necessarily for the other two;
- court reasoning, because separate public judgment texts/motivations were not recovered in this pass.

### Next pivots
1. Retrieve published/full WSA judgments or case metadata for `V SA/Wa 604/25`, `597/25`, `598/25`.
2. Search for customs-record derivatives keyed by exact CN, period, sender identity and border/customs office.
3. Compare WORLD CHEM declaration chronology with TST/TSTExport/GrandGranit route changes.

---

## J18-005 — Astramar identity of the unnamed 10.01.2025 Latvian counterparty remains a strengthened hypothesis only

Primary-document publication:
- BIC investigation: https://investigatebel.org/ru/investigations/grodno-azot-sankcii-es-shema
- Published Specification No.1 image: https://investigatebel.org/storage/page_blocks/June2025/416.jpg
- Published party/banking details page: https://investigatebel.org/storage/page_blocks/June2025/514.jpg

### FACT / B for the published document content
The published specification is dated `2025-01-10`, contract `10.01/25-UR-DAP`, seller TECHNOSPETSTRADING LLC, buyer `ASTRAMAR LIEPĀJA K.A.` SIA, 22 t ±10%, DAP Brīvostas iela 21, Liepāja. The banking/signature page identifies TECHNOSPETSTRADING and Astramar parties and their bank details/signatories.

### HYPOTHESIS / C
The official TST PL decision describes an unnamed Latvian contract dated exactly `2025-01-10`, with TST PL as payer and onward movement to the Hungarian company. The BIC-published Astramar contract has the exact same date. This creates a materially stronger candidate identity:

`unnamed KAS Latvian contract of 10.01.2025` ≟ `TECHNOSPETSTRADING ↔ Astramar contract 10.01/25-UR-DAP`.

It is **not upgraded** because the official decision does not publish the Latvian party name or contract number, and the published Astramar pages do not show TST PL as payer.

### Missing proof needed for upgrade
- KAS exhibit naming Astramar or showing contract no. `10.01/25-UR-DAP`;
- payment order naming TST PL + Astramar/TECHNOSPETSTRADING + matching invoice/contract reference;
- invoice/MRN/CMR linking the same 22 t consignment into the officially described Hungarian chain.

---

## J18-006 — French contact and shipment identifiers remain unresolved

Source for French lead:
- LSM/LTV `De facto`, published `2025-06-22`: https://www.lsm.lv/raksts/zinas/latvija/22.06.2025-de-facto-peta-sankciju-apiesanas-shemas-baltkrievu-karbamids-plust-eiropa-caur-latviju.a604247/

### SOURCE_CLAIM / B
Astramar representative Viesturs Andersons is quoted as saying that the request came personally “from France, from a person I know” and he agreed to help send the cargo.

### What this does NOT prove
- name or legal identity of the French person/company;
- whether that person was buyer, broker, consignee, payer or merely an introducer;
- any French invoice/payment/shipping role.

### NO-HIT / BLOCKED this pass
- `NO-HIT`: exact Hungarian company identity remains unresolved in the public official text.
- `NO-HIT`: no public payment order recovered; only the official documentary designation of TST PL as payer is established.
- `NO-HIT`: no shipment-level MRN, CMR/CIM/SMGS, wagon or truck number for the 10.01/21.02 route was recovered.
- `NO-HIT`: no filled certificate of origin/quality or lot number tied to that route was recovered.
- `NO-HIT`: no name/company behind the French Astramar request was resolved.
- `NO-HIT`: direct public texts/reasoning of WSA cases `V SA/Wa 604/25`, `597/25`, `598/25` were not independently recovered; outcomes are presently grounded through the MSWiA decisions.
- `BLOCKED`: the public MSWiA/KAS decision states that the detailed annex contains tax/customs-secret information. This likely explains why entity names and shipment identifiers are absent from the public version.
- `BLOCKED`: direct historical Polish VAT White List verification for TST PL bank accounts around January–February 2025 was not completed in this environment; any commercial-aggregator account list remains discovery-level only until verified through the Ministry of Finance service.

---

## Deliverable impact / accepted wording

### Main-text conclusions allowed
1. Official Polish administrative decisions establish that TST PL was designated as payer in a Latvian contract dated 10.01.2025 despite not being a party, with goods then moving to the Hungarian company; this is a **documentary payer role**, not proof of an executed wire.
2. The official Armen decision records a TECHNOSPETSTRADING-linked Belarus→Latvia import chain using customs procedure 42.
3. The public documents do not name the Hungarian entity or publish shipment-level MRN/CMR/SMGS/payment-order identifiers.
4. Correct TST PL sanctions decision identifier is `.113.2025.BS(2)`; `.106.2025.BS(3)` belongs to GrandGranit. A later WORLD CHEM decision contains an apparent cross-reference error on this point.
5. WORLD CHEM’s 2025 removal request was refused; the official decision reproduces KAS findings of 38 Belarus→Poland customs declarations in 2021–2024 and names the WSA cases for WORLD CHEM/TST/TSTExport.

### “Предположительно / требует проверки” only
- The unnamed Latvian contract dated 10.01.2025 may be the published TECHNOSPETSTRADING↔Astramar `10.01/25-UR-DAP` document because the dates coincide exactly, but there is no public primary cross-reference proving identity.
- French requester identity and exact role remain unknown.

## Documents updated
- GitHub journal: this PASS_018.
- Google Docs Appendix 6: regulatory/judicial correction block for WORLD CHEM/TST/TSTExport and TST PL decision-ID conflict.
- Google Docs Appendix 7: route/payer/procedure-42 block, with Astramar identity retained under “Предположительно / требует проверки”.

## Priority next pivots
1. Contract/payment exhibits behind the 10.01.2025 Latvian and 21.02.2025 Hungarian contracts.
2. Exact Hungarian company VAT/EORI/name.
3. MRN/EORI/declarant for the Latvia procedure-42 entry.
4. Payment order and TST PL historical verified bank-account record.
5. Shipment-level invoice/CMR/SMGS/certificate/wagon or truck identifiers.
6. Full WSA judgment texts for `V SA/Wa 604/25`, `597/25`, `598/25`.
