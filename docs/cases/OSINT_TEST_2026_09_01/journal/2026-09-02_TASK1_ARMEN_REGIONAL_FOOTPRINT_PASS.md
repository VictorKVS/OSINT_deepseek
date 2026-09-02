# TASK1 — Armen Harutyunyan regional footprint pass

Date: 2026-09-02
Object anchor: Armen Seryozhaevich Harutyunyan / Армен Серёжаевич Арутюнян, DOB 1972-10-07, Armenian citizen (identity anchor from Polish sanctions decision; Poland used only for disambiguation).

## Scope
Targeted web sweep for mentions/footprint in Russia, Belarus, Armenia, and Europe outside Poland.

## Russia
- Searches: exact Russian/Latin name, DOB, TECHNOSPETSTRADING, BELTECHNIKA, candidate Russian corporate links.
- Result: multiple exact-name hits exist, but currently resolved as namesakes/conflicts: a Moscow individual entrepreneur is recorded as a Russian citizen; a Moscow engineer/researcher is born 1965; a physician profile also appears under the same name. None is safely attributable to the 1972 Armenian citizen target.
- Status: CONFLICT / NO-HIT for confirmed target footprint in Russia.
- Next pivot: require DOB 1972-10-07, Armenian citizenship, passport/ID bridge, or corporate document linking target to a Russian entity before adding any Russia edge.

## Belarus
- BIC/investigative materials state the target worked in various Belarusian companies from 1997 and owned several from 2011; describe him as former business partner of Sergei Teterin and as actual/controller figure around TECHNOSPETSTRADING.
- Same materials connect TECHNOSPETSTRADING to Grodno Azot fertilizer export flows and later intermediary structures.
- Status: FOUND-B (investigative/document-based); official Polish materials independently confirm control over TECHNOSPETSTRADING/EXPORT but are outside the requested regional source bucket.
- Next pivot: recover Belarus EGR extracts / historical company list for 1997–present and exact joint ventures with Teterin.

## Armenia
- Armenian domestic web search in Armenian/Russian/English did not surface a reliable political/business profile for the exact 1972 target.
- High-value lead from Ukrainian registry aggregators: TOV BELTEKHNIKA INVEST (EDRPOU 43007046, Kyiv) lists founder Armen Harutyunyan / variant patronymic, Armenian citizenship, and an address in Shahumyan village, Ararat Region, Armenia; company activities include agricultural machinery, chemical wholesale, transport and related trade. Naming/sector overlap with Lithuanian BELTECHNIKA.LT is notable.
- Identity is not yet fully proven because no DOB is exposed in the Ukrainian public result.
- Status: FOUND-B/C lead, identity bridge pending.
- Next pivot: obtain Ukrainian historical extract/UBO record and Armenian registry/residency/corporate record matching DOB 1972-10-07.

## Europe outside Poland
### Lithuania
- UAB BELTECHNIKA.LT, company code 302727122, Vilnius, is publicly shown by Lithuanian registry-derived sources with Armen Harutyunyan as director/manager; one foreign individual participates in ownership.
- Company activity: agricultural machinery; 2023 revenue EUR 217,105, net loss EUR 64,328; VAT status ended 2024-06-14; employee count fell to zero by late 2024 according to registry-derived sources.
- Status: FOUND-B/A- registry-derived; strong match to known network entity.

### Ukraine
- TOV BELTEKHNIKA INVEST (43007046) founder Armen Harutyunyan, Armenia, 100%; Kyiv registration; activities include machinery and chemical wholesale plus freight/transport. Strong new 1-hop candidate.
- Status: FOUND-B/C pending DOB bridge.

### Latvia / Hungary / other EU
- No direct, independently indexed personal profile for the exact target found in this pass outside network/company references already known from the fertilizer route.
- Hungary: supplier identity remains unresolved.
- Latvia: logistics/company nodes are visible, but no new direct personal registration/role for Armen found in this pass.
- Status: NO-HIT for new direct personal role.

## Sanctions scope control
- OpenSanctions currently shows the target sourced from the Polish national sanctions list only; no independent EU-wide personal listing was identified in this pass.
- Do not describe the target as EU-sanctioned solely because linked goods/entities intersect EU sanctions.

## Red Team / identity resolution
- Do not merge same-name Russian persons with the target.
- Do not infer Armenian political ties from citizenship/address alone.
- Treat BELTEKHNIKA INVEST (Ukraine) as a high-value lead, not confirmed same-person fact, until DOB/identity bridge is recovered.
