# Task 1 — Automated deep-dive pass 014

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / linked fertilizer-export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly observable in a primary/official/registry document or exact-match check.
- `SOURCE_CLAIM` — claim made by an identified source and not independently adjudicated here.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — testable working theory.

Grades: `A` primary/official; `B` strong document-based secondary/registry mirror; `C` analytical lead; `D` weak/unverified.

## J1-A014-01 — Apeks serviss: current procuration endpoint is now zero active procurations
Type: FACT / registry-mirror
Grade: B+

Fresh Lursoft data for SIA `Apeks serviss`, reg. `41503055853`, state that the Register of Enterprises data were updated on `26.08.2026` and show `Aktuālie dati. Prokūru saraksts (0)` — no currently active procurations. The same record still shows one historical procuration entry and one board member with sole representation rights.

Source:
- https://company.lursoft.lv/apeks-serviss/41503055853

This materially closes one endpoint left open in PASS_013: the corporate filings dated `26.06.2025` / registered `01.07.2025` and the filing dated `07.04.2026` / added `09.04.2026` resulted, by the latest visible registry state, in **no active procurist**.

### What this does NOT prove
- the identity of the former procurist;
- whether the 2025 filing appointed, altered or revoked a procuration;
- whether the 2026 filing revoked the last procuration;
- any link between those filings and TECHNOSPETSTRADING cargo or the June-2025 media publication.

### Next pivots
1. Obtain the lawful UR EDOC filings dated 26.06.2025 and 07.04.2026.
2. Extract former procurist identity, scope of authority and exact appointment/termination dates.
3. Search that identity/signature in CMR/SMGS/MRN, warehouse receipts, customs representation and contracts.

## J1-A014-02 — New fresh registry signal: Apeks serviss now has an active registered restriction/security measure
Type: FACT / SOURCE-CONFLICT
Grade: B+ for current mirror state; C for timing inference

Fresh Lursoft output, with Register of Enterprises data updated `26.08.2026`, now shows `Aktuālie nodrošinājumi: Ir` — an active registered security/restriction measure exists. A fresh Kombo search result independently exposes `Nodrošinājuma līdzeklis (1)` for the same company and says UR data were updated on `26.08.2026`.

Sources:
- https://company.lursoft.lv/apeks-serviss/41503055853
- https://www.kombo.lv/profile/41503055853/apeks-serviss

### CONFLICT / temporal lead
A cached Lursoft snapshot indexed with an earlier state around mid-August 2026 displayed `Aktuālie nodrošinājumi: Nav`, whereas the current 26.08.2026 state displays `Ir`. This strongly suggests a newly registered measure during the intervening period, but the exact registration date, authority, legal basis and scope are not visible in the free page.

### What this does NOT prove
- that VID imposed the measure;
- that it concerns fertilizer, TECHNOSPETSTRADING, customs procedure 42, sanctions or the pending court case;
- that the measure freezes all assets or prevents business activity;
- that the measure was entered specifically between 14 and 26 August without the underlying change-log document.

### Next pivots
1. Obtain the exact UR restriction/security-measure record and event-history entry.
2. Identify imposing authority, document number/date, legal basis, object and scope.
3. Compare with the pending VID litigation `A420010026 / A/26/289` and tax-debt chronology only after document-level matching.

## J1-A014-03 — Apeks tax debt changed discontinuously after December 2025 and remains ~EUR 167k
Type: FACT / registry-and-VID-data mirror
Grade: B+

Firmas.lv reproduces VID-administered tax-debt history for Apeks serviss:
- 15.09.2025 — EUR 355.45;
- 13.10.2025 — EUR 355.44;
- 13.11.2025 — EUR 355.45;
- 08.12.2025 — EUR 355.45;
- 16/18.02.2026 — EUR 184,400.45;
- 09.03.2026 — EUR 172,703.44;
- 07.04.2026 — EUR 170,414.35;
- 07.05.2026 — EUR 170,111.74;
- 08.06.2026 — EUR 163,769.09;
- 07.07.2026 — EUR 165,934.51;
- 06.08.2026 — EUR 167,034.71.

Fresh Lursoft data show EUR `166,698.12` as of `26.08.2026`.

Sources:
- https://www.firmas.lv/lv/uznemumi/apeks-serviss/41503055853
- https://company.lursoft.lv/apeks-serviss/41503055853

### INFERENCE / C
The public series contains a clear discontinuity between December 2025 and February 2026. The administrative case against VID (`A420010026`) was opened on 22.04.2026, after the debt was already visible at roughly EUR 170k. This makes the debt/VID-decision/court sequence a high-priority legal pivot.

### What this does NOT prove
- that the court case challenges this tax debt;
- that the debt arises from customs, VAT, fertilizer imports or TST shipments;
- that Apeks committed a tax violation;
- that the debt is final and uncontested.

### Next pivots
1. Recover the VID decision underlying the debt and/or restriction.
2. Recover the court acceptance order and statement of claim in `A420010026`.
3. Match exact decision number/date/amount before creating any causal edge.

## J1-A014-04 — One VID decision is indexed for Apeks, but its content is not openly exposed
Type: FACT / metadata lead
Grade: B+

The current Lursoft company record lists `VID lēmumu saraksts (1)` — one State Revenue Service (VID) decision associated with Apeks serviss. The details redirect behind authentication and were not available in the open page.

Source:
- https://company.lursoft.lv/apeks-serviss/41503055853

This is a concrete document-recovery target because it may explain the tax debt, the newly visible registered restriction, the pending administrative case, or none of them.

### What this does NOT prove
- subject, date or outcome of the VID decision;
- that it is the decision challenged in `A420010026`;
- any connection to TST or fertilizer cargo.

### Next pivot
Search/obtain the public or lawfully accessible VID decision metadata and match its identifier against the court file and UR restriction record.

## J1-A014-05 — Apeks 2025 annual-report profile deteriorated materially
Type: SOURCE_CLAIM / annual-report mirror
Grade: B+

Okredo and Saraksts reproduce 2025 annual-report figures for Apeks serviss:
- turnover: EUR `1,839,649` vs EUR `2,671,482` in 2024 (about -31%);
- net result: `-122,592` EUR vs `+2,533` EUR in 2024;
- equity: EUR `81,394` vs `228,986` in 2024 (about -64%);
- amounts payable/liabilities: EUR `87,233` vs `43,466` in 2024 (about +101%);
- current assets: EUR `167,453` vs `270,158` in 2024;
- employees: 10 in 2025.

Sources:
- https://okredo.com/en-lv/company/sabiedriba-ar-ierobezotu-atbildibu-apeks-serviss-41503055853
- https://saraksts.lv/41503055853

### INFERENCE / C
The 2025 loss, equity contraction, 2026 tax-debt discontinuity and current restriction form a meaningful financial/regulatory deterioration sequence. It justifies deeper document recovery around VID and the 2025 annual report.

### Red Team boundary
Do not infer insolvency, unlawful activity, sanctions evasion or causation by TST. Current registry mirrors show Apeks remains registered, VAT-active, and without an insolvency/liquidation entry.

## Priority pivots from this pass
1. Exact UR record for the newly visible active `nodrošinājums` / security measure.
2. The single indexed VID decision: number, date, legal basis, amount and operative part.
3. Court file `A420010026 / A/26/289`: acceptance order, claim subject and challenged VID decision.
4. UR EDOC procuration filings 26.06.2025 and 07.04.2026; identify the former procurist.
5. Only after exact document matching, test whether any of the above connects to customs, procedure 42, MRN/CMR/SMGS or TECHNOSPETSTRADING cargo.

No new reliable shipment-level MRN, CMR/CIM/SMGS, wagon number, Hungarian company identity, external payer or French contact was identified in this pass. No private-relative or ethnicity/nationality-based links were added.
