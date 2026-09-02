# Task 1 automated deep-dive — pass 007

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / TST PL / related fertilizer export network
Status: ACTIVE

## Evidence scale
- A — primary/official source
- B — strong secondary/document-based source
- C — analytical inference / unresolved lead
- D — weak/unverified lead

## J1-A007-001 — Official-source cross-reference error for TST PL

Type: FACT + CONFLICT
Evidence: A

Primary sources:
- TST PL decision dated 2025-10-09: https://www.slaskie.kas.gov.pl/documents/3559133/10975999/Decyzja_TST_PL_Sp_z_oo.pdf
- WORLD CHEM delisting refusal dated 2025-12-22: https://www.gov.pl/attachment/8444bcb4-a2e6-462e-8496-eee08e91d44e
- GrandGranit decision dated 2025-08-06: https://www.lubelskie.kas.gov.pl/c/document_library/get_file?groupId=3554183&uuid=c2091a78-7077-4b85-98e8-a19cd0be7972

FACT:
- The original TST PL decision is `DPP-WTPZ.0272.113.2025.BS(2)` dated 2025-10-09, based on KAS request 2025-09-25 `DZP9.K410.69.2025.Z220.1`.
- The later WORLD CHEM decision incorrectly states that TST PL was sanctioned under `DPP-WTPZ.0272.106.2025.BS(3)` after request `DZP9.K410.62.2025.Z220.1` dated 2025-07-31.
- Those `.106 / .62` identifiers belong to GrandGranit.

Interpretation:
This is a cross-reference/copy error inside an official later decision. It does not invalidate the TST PL sanctions decision, but it demonstrates that even official summary passages require source-to-source validation.

What this does NOT prove:
- no conclusion about merits of the TST PL case changes from this clerical/reference conflict;
- it does not imply falsification of the underlying evidence.

Control rule:
For decision number, application number and initiation date, use the subject-specific original decision as the chronology anchor.

Next pivot:
- check whether other later MSWiA decisions reproduce the same erroneous TST PL identifiers;
- build an official decision cross-reference table and flag inconsistent identifiers automatically.

## J1-A007-002 — Exact KAS initiation chronology

Type: FACT
Evidence: A

Source: WORLD CHEM delisting refusal + subject-specific TST PL decision.

Results:
- TECHNOSPETSTRADING: KAS request 2024-11-29, `DZP9.K410.65.2024.Z079.1`; MSWiA decision 2024-12-17, `DPP-WTPZ.0272.103.2024(2)`.
- TECHNOSPETSTRADINGEXPORT: KAS request 2024-12-06, `DZP9.K410.68.2024.Z079.1`; decision 2024-12-17, `DPP-WTPZ.0272.104.2024(4)`.
- GrandGranit: KAS request 2025-07-31, `DZP9.K410.62.2025.Z220.1`; decision 2025-08-06, `DPP-WTPZ.0272.106.2025.BS(3)`.
- TST PL: KAS request 2025-09-25, `DZP9.K410.69.2025.Z220.1`; decision 2025-10-09, `DPP-WTPZ.0272.113.2025.BS(2)`.

INFERENCE / C:
The sequence is useful as an enforcement/discovery timeline: TST → TSTExport → GrandGranit → TST PL.

What this does NOT prove:
These request dates are not the dates on which the underlying conduct began, nor necessarily the first dates on which KAS knew about it.

Next pivot:
Overlay KAS request dates with first known customs declarations, contracts, invoices, wagon movements and route changes.

## J1-A007-003 — WORLD CHEM delisting attempt and network-continuity position

Type: FACT + SOURCE_CLAIM
Evidence: A as an official administrative record/position

Primary source:
- https://www.gov.pl/attachment/8444bcb4-a2e6-462e-8496-eee08e91d44e

FACT:
- WORLD CHEM TRADING CO. L.L.C. filed an application for removal from the Polish sanctions list on 2025-11-12.
- MSWiA refused removal on 2025-12-22.

SOURCE_CLAIM:
- The decision quotes the Head of KAS opinion dated 2025-12-08, ref `DZP9.410.64.2024.Z079.6`.
- KAS stated that even if WORLD CHEM ceased the challenged activity in Poland, Armen Harutyunyan continued activity in the disputed fertilizer trade/production sphere through related structures, which triggered further KAS actions.

What this does NOT prove:
- this is an administrative position, not a criminal judgment;
- the public decision does not expose the full tax/customs-secret annex;
- each later transaction still requires its own primary evidence.

Next pivot:
- look for litigation concerning the refusal to delist WORLD CHEM;
- identify public portions of the KAS annex/evidence chain;
- connect enforcement dates to GrandGranit and TST PL transaction chronology.

## J1-A007-004 — PKP CARGO narrows TST PL first-appearance window

Type: FACT + INFERENCE
Evidence: A for document states; C for inferred ordering relative to sanctions

Primary sources:
- PKP CARGO restriction annex `zm.36`, state 2025-10-07: https://www.pkpcargo.com/wp-content/uploads/2023/11/zal.doograniczenia32625zm.36.pdf
- PKP CARGO restriction annex `zm.40`, state 2025-12-15: https://www.pkpcargo.com/wp-content/uploads/2023/11/zal.doograniczenia32625zm.40.pdf

FACT:
- As of 2025-10-07, the list already contained TSTExport (90), TST (91), WORLD CHEM (92), MetaTradingProm (94), and GrandGranit (100).
- TST PL did not appear in `zm.36`.
- By 2025-12-15, TST PL appears as position 105.
- The `zm.40` header says that revision added positions 110–111, so TST PL must have appeared in an earlier intermediate revision, most likely `zm.37–39`.

INFERENCE / C:
The first-appearance window for TST PL is narrowed to after the 2025-10-07 state and before the 2025-12-15 state. Because the TST PL sanctions decision is dated 2025-10-09, exact ordering cannot yet be claimed: an intermediate revision could theoretically have been issued on 2025-10-08.

RED TEAM:
The PKP PDF is a flat `Lp. / Nazwa Klienta / REGON / Uwagi` table. Search-engine extraction can concatenate adjacent rows. The neighboring entries after TST PL (Erpbel, FIRN EU, OOO Firma Innowacyjna Mark, Firn M, AVALON, FGUP) are independent list entries and MUST NOT be converted into graph edges to TST PL.

What this does NOT prove:
- reason for the PKP inclusion;
- refusal to carry a particular wagon;
- relation to a specific fertilizer shipment.

Next pivot:
1. recover `zm.37`, `zm.38`, `zm.39`;
2. identify their state dates and which positions each revision added;
3. retrieve the main text of restriction 326-25 / telegram `COPP-7803/719/22`;
4. compare exact position-105 date with the 2025-10-09 sanctions decision and TST PL rail/customs records.

## J1-A007-005 — Hungarian/Latvian identities and French Astramar contact

Type: NO-HIT

Search scope:
- exact contract dates 2025-01-10 and 2025-02-21;
- TST PL / TECHNOSPETSTRADING + Hungarian supplier + external payer;
- Latvia contract party / procedure 42;
- Astramar + French intermediary/contact.

Result:
No new reliable public name was recovered in this pass.

Control:
Do not insert plausible Hungarian, Latvian or French companies into the graph without a contract, declaration, invoice, registry-linked document or another reliable source.

## Google Docs updates

Updated:
- Appendix 6 — added official-source cross-reference error, exact KAS initiation chronology, WORLD CHEM delisting/continuity section.
- Appendix 7 — added narrowed PKP first-appearance window for TST PL and a PDF-row-concatenation Red Team warning.

## Priority pivots for next pass
1. PKP `zm.37–39` and exact TST PL position-105 insertion date.
2. Main PKP restriction 326-25 / `COPP-7803/719/22` legal/operational meaning.
3. Repeated TST PL reference error across official MSWiA decisions.
4. Public court records on WORLD CHEM delisting refusal.
5. Hungarian contract party, Latvian contract party, external payer.
6. Astramar French contact and final consignee.
7. Cargo fingerprints: certificates, exact mass, wagon numbers, CN, CMR/CIM/SMGS, customs declaration, payment side.
