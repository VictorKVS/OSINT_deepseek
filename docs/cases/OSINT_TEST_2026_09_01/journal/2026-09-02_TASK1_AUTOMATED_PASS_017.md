# Task 1 automated deep-dive — pass 017

Date of access: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Start-of-pass anti-duplication check

Reviewed the latest journal first: `2026-09-02_TASK1_AUTOMATED_PASS_016.md`.
PASS_016 had already covered Astramar's 2025/2026 VID/financial profile, the Krasts Invests June 2026 ownership/control/address reset, the stale LAFF co-ownership statement, the 03.08.2026 bailiff-document pivot and the unresolved French/Hungarian/payment/shipment targets. Those closed queries were not repeated without cause.

Evidence labels:
- `FACT` — directly visible fact in an official/public record or stable entity identifier.
- `SOURCE_CLAIM` — a source reports a fact whose underlying primary record is not independently archived in this pass.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — unverified working proposition.
- `A/B/C/D` — official/primary → strong documentary secondary → analytical/discovery → weak/unverified.

---

## J17-001 — KRASTS INVESTS: name of the new shareholder/board member resolved from registry-derived data

Entity: SIA `KRASTS INVESTS`
Registration no.: `52103017931`
Relevant event dates: `2026-06-16`, `2026-06-29`
Access date: `2026-09-02`

Sources:
- B2BHint officer record: https://b2bhint.com/lv/officer/10613364
- Firmas.lv current company record: https://www.firmas.lv/lv/uznemumi/krasts-invests/52103017931

### SOURCE_CLAIM / B
B2BHint, which attributes its Latvian officer data to the Commercial Law / Enterprise Register source layer, identifies `Jansons Jānis` as:
- `KRASTS INVESTS` board member, appointed `2026-06-29`;
- `KRASTS INVESTS` member/shareholder, appointed `2026-06-16`.

Firmas independently corroborates the exact corporate state and dates while redacting the person's name in free output:
- exactly one natural-person shareholder;
- `100%`, `1,000` shares x `88 EUR`, total `88,000 EUR`;
- effective `2026-06-16`, registered UR `2026-06-29`;
- exactly one current board member with individual representation from `2026-06-29`;
- one natural-person UBO from `2026-06-29`, control type `as member`.

The role/date cross-check materially increases confidence that the B2BHint name refers to the natural person hidden in the free Firmas table. The name itself remains B, not A, until the 16.06.2026 shareholder register or a direct UR extract is read.

### What this does NOT prove
- motive/consideration for the June 2026 ownership transfer;
- any role of Jānis Jansons in the January 2025 TECHNOSPETSTRADING→Astramar shipment;
- any fertilizer, customs, payment or sanctions activity by him;
- identity of the seller of the shares immediately before 16.06.2026.

### Next pivots
1. Retrieve the shareholder register dated `16.06.2026` and compare to `23.08.2024`.
2. Extract seller/buyer names, unique identifiers and percentage transition.
3. Compare the new controller against the exact post-29.06.2026 address/contact and the 03.08.2026 bailiff document.

---

## J17-002 — RED TEAM: same displayed name appears under two different B2BHint person IDs; wider role graphs must not be merged

Source:
- https://b2bhint.com/lv/officer/10613364
- https://b2bhint.com/lv/officer/102290192

### CONFLICT / IDENTITY-RESOLUTION WARNING / C
B2BHint has two separate person-record IDs with the same displayed name `Jansons Jānis`:
- officer ID `10613364` carries the visible KRASTS INVESTS board/member rows;
- officer ID `102290192` carries the visible KRASTS INVESTS UBO row from `2026-06-29`.

Because these are distinct aggregator person objects, it is unsafe to merge their many other listed companies/roles simply on the shared name. This is especially important because `Jānis Jansons` is not a unique identifier.

### Allowed use
The exact `KRASTS INVESTS` role/date rows can be used as a registry-derived lead because they independently align with the company-level Firmas dates/state. Other-company roles from either person page are excluded from the case graph unless resolved by a unique personal identifier or a primary company record.

### What this does NOT prove
- that the two B2BHint person objects are necessarily different natural persons;
- that they are necessarily the same natural person;
- any connection between unrelated companies listed on those profile pages and the TST network.

### Next pivot
Use the KRASTS INVESTS shareholder register / official UR extract, not the aggregator-wide person graph, to resolve identity.

---

## J17-003 — New address-level 1-hop: IK PŪRE at the exact new KRASTS INVESTS legal address

Entity: `IK PŪRE`
Registration no.: `42102040479`
LEI: `9845004PB7D777LF4D02`
Address: `"Rotas", Dzērvenieki, Cīravas pag., Dienvidkurzemes nov., LV-3453`
Access date: `2026-09-02`

Sources:
- Bloomberg LEI: https://lei.bloomberg.com/leis/view/9845004PB7D777LF4D02
- Firmas address index: https://www.firmas.lv/en/addresses/dienvidkurzemes-nov-ciravas-pag-dzervenieki/100145291
- Latvijas Avīze / LETA-derived reporting: https://www.la.lv/mus-slauc-ka-govis
- Liepajniekiem.lv: https://www.liepajniekiem.lv/zinas/novados/piensaimnieki-mus-slauc-ka-govis-liepaja-un-grobina-zemnieki-protestos-dalis-pienu-par-brivu/

### FACT / B for the legal entity/address
Bloomberg LEI identifies IK PŪRE as reg. `42102040479`, individual merchant, entity status active in the underlying entity data, with both legal and headquarters address exactly `"Rotas", Dzērvenieki ... LV-3453`; validation authority is the Register of Enterprises of the Republic of Latvia. The LEI itself later lapsed, which is not the same as entity liquidation.

Firmas independently indexes PŪRE at `"Rotas", Dzērvenieki`.

### SOURCE_CLAIM / B for proprietor name
Independent Latvian reporting in 2023 describes the Cīravas dairy individual merchant `Pūre` owner as `Jānis Jansons`.

### HYPOTHESIS / C — strong identity-resolution lead, NOT a merged person
KRASTS INVESTS moved to the exact `"Rotas"` address on `2026-06-29`; B2BHint identifies its new shareholder/board member as `Jansons Jānis`; independently, IK PŪRE at that exact address is publicly described as owned by `Jānis Jansons`.

The combined exact full-name + exact-address overlap is a strong lead that these roles may belong to the same natural person. It is **not entered as a confirmed person-identity edge** because no unique natural-person identifier or primary shareholder document was recovered in this pass.

### What this does NOT prove
- that IK PŪRE participates in fertilizer trade, customs, storage, transport, payments or TST operations;
- that the current KRASTS INVESTS controller and the IK PŪRE proprietor are definitively the same person;
- that Jānis Jansons owns the `Rotas` real estate;
- why KRASTS INVESTS moved there;
- any link between the move and the 03.08.2026 bailiff document.

### Next pivots
1. KRASTS INVESTS shareholder register `16.06.2026` — unique person identifier.
2. IK PŪRE official proprietor extract — compare unique identifier only lawfully.
3. Zemesgrāmata/cadastre for `Rotas` — owner and legal basis for KRASTS INVESTS using the address.
4. Post-29.06.2026 KRASTS INVESTS phone/e-mail/contact records; compare only exact identifiers.
5. Bailiff document `03.08.2026` — determine whether it names the same person/address and what the legal object is.

---

## Negative / blocked results

- `NO-HIT`: unknown Hungarian legal entity described in the 2025 TST PL route remains unresolved.
- `NO-HIT`: external payer remains unresolved.
- `NO-HIT`: French Astramar requester/contact remains unresolved.
- `NO-HIT`: no shipment-level MRN, CMR/CIM/SMGS, wagon/truck registration, filled batch/certificate number or payment-order reference recovered in this pass.
- `NO-HIT`: exact public phone search did not produce an independently verified KRASTS INVESTS↔IK PŪRE operational-contact match.
- `BLOCKED`: natural-person unique identifier is not exposed in free registry-derived output; therefore the Jānis Jansons identity merge remains prohibited pending the primary shareholder/proprietor documents.

## Documents updated

- Google Docs Appendix 6 `Приложение 6 — Углублённый анализ корпоративной сети, логистики и связанных лиц`: appended a section on the newly resolved KRASTS INVESTS shareholder/board name, the two-profile B2BHint identity warning, and the exact-address IK PŪRE lead with a strict no-merge caveat.

## Priority next pivots

1. KRASTS INVESTS shareholder registers `23.08.2024` vs `16.06.2026` — exact seller/buyer/percentages/unique identifiers.
2. KRASTS INVESTS bailiff document dated `03.08.2026` — enforcement authority, case/reference, creditor, amount/object.
3. Zemesgrāmata/cadastre for `"Rotas", Dzērvenieki` — owner and right of use.
4. Continue unresolved high-value TST targets: Hungarian entity, external payer, French Astramar contact, payment order, MRN/CMR/CIM/SMGS, wagons/trucks, batch/certificates.
5. Do not pivot through other `Jansons Jānis` companies until a unique identifier resolves the person.
