# Habr NPA sweep — Stream 1 — 2026-09-01 13:52

## Scope

Habr 432466, KII positions 21–28:

1. ФСТЭК России от 14.03.2014 № 31
2. ФСТЭК России от 06.12.2017 № 227
3. ФСТЭК России от 11.12.2017 № 229
4. ФСТЭК России от 21.12.2017 № 235
5. ФСТЭК России от 22.12.2017 № 236
6. ФСТЭК России от 25.12.2017 № 239
7. Перечень, утв. приказом ФСТЭК России от 16.07.2019 № 135
8. ФСТЭК России от 28.05.2020 № 75

Rules: GitHub copies are treated only as secondary corpus candidates. Identity (number/date/title/body) and legal status/currentness are checked separately. A filename, README, summary, or link is not a normative body.

## New GitHub findings

| Target | Repo | Commit | Path | Size | Type | Classification | Identity result |
|---|---|---|---|---:|---|---|---|
| №31/2014 | `DROZZER/SIB` | `2c3c106a0ebf12c46327196cd9e0877bbb187549` | `SIB/pdfs/№31 2014-03-14 Требования АСУ ТП.pdf` | 307582 B | PDF/blob | `RELIABLE_GITHUB_CANDIDATE` | filename matches number/date/domain; binary internal identity not readable through connector -> blocker |
| №31/2014 companion | `DROZZER/SIB` | `2c3c106a0ebf12c46327196cd9e0877bbb187549` | `SIB/Доки/8. ФСТЭК/Приказ №31 от 14.04.2014.md` | 5844 B | Markdown | `DETAILED_SUMMARY / REJECTED_AS_NORMATIVE_BODY` | path/reference contains wrong date 14.04.2014; actual order is 14.03.2014 |
| №239/2017 | `DROZZER/SIB` | `2c3c106a0ebf12c46327196cd9e0877bbb187549` | `SIB/pdfs/№239 от 25.12.2017 Требования для КИИ.pdf` | 450546 B | PDF/blob | `RELIABLE_GITHUB_CANDIDATE` | companion note identifies a saved edition dated 28.08.2024; binary internal identity not readable through connector -> blocker |
| №239/2017 companion | `DROZZER/SIB` | `2c3c106a0ebf12c46327196cd9e0877bbb187549` | `SIB/Доки/8. ФСТЭК/Приказ №239 от 25.12.2017.md` | 1053 B | Markdown | `SUMMARY / POINTER_TO_BINARY / REJECTED_AS_NORMATIVE_BODY` | summary only, embeds the PDF |
| №227/2017 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | no reliable body candidate found |
| №229/2017 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | mentions only |
| №235/2017 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | educational/website summaries only |
| №236/2017 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | implementation guidance only; no body |
| №135/2019 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | no reliable body candidate found |
| №75/2020 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` | no reliable body candidate found |

Additional rejected references:
- `pikov-vitaliy/pikov-expert-lectures@3743195404811ac9c3468c948bc4e78c67b56561`, `risk/materials.md`, `threats-kii/materials.md`: educational summaries/reference lists, not bodies.
- `leman-os/securisk@b561486e361cd6c0c75511ad1f4a935e8b130f75`, `frontend/src/pages/Requirements.jsx`: implementation guidance referring to №236, not normative text.

## Official/currentness cross-check

### №31/2014
- Identity: ФСТЭК России 14.03.2014 №31; Minjust №32919.
- Current consolidated revision found: 15.03.2021.
- Latest amendment: ФСТЭК №46 of 15.03.2021; official publication `0001202107010126`, published 01.07.2021; Minjust №64063.
- Gate: `FULL_TEXT_CURRENT` requires the order + full Requirements + appendices.
- Blocker: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` (latest amending act publication is primary-confirmed; consolidated current body was not read from a primary official source).

### №227/2017
- Current revision found: 17.07.2025.
- Latest amendment: ФСТЭК №254 of 17.07.2025; Minjust №83245; official publication `0001202508210006`, published 21.08.2025.
- Any GitHub copy predating this revision is `OLD_EDITION`.

### №229/2017
- No reliable later amendment/repeal found in this pass.
- Do not infer current legal status from absence of a repeal hit.
- Blocker: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### №235/2017
- Current revision found: 20.04.2023.
- Latest confirmed amendment: ФСТЭК №69 of 20.04.2023; Minjust №73969; official publication `0001202306230016`, published 23.06.2023.
- April 2026 changes to №235/№239 were found only as a draft/project. No official publication of a signed/registered final order was confirmed in this pass.
- Gate: `DRAFT_PLANNED_EFFECTIVE_DATE != ACTUAL_EFFECTIVE_DATE`.

### №236/2017
- Current revision found: 11.07.2025.
- Latest amendment: ФСТЭК №247 of 11.07.2025; Minjust №83246; official publication `0001202508210016`, published 21.08.2025.
- Changes took effect 01.09.2025.
- Any pre-2025 GitHub form is `OLD_EDITION`.

### №239/2017
- Current revision found: 28.08.2024.
- Latest confirmed amendment: ФСТЭК №159 of 28.08.2024; Minjust №79900; official publication `0001202410250022`, published 25.10.2024.
- The 2026 proposal affecting №235/№239 remains classified as `DRAFT_AMENDMENT_NOT_EFFECTIVE` unless/until a final signed and officially published act is identified.
- Important lifecycle gate: later loss of force of the №159 clause concerning old order №17 does not by itself cancel the separate №159 amendment to №239: `PARTIAL_AMENDING_CLAUSE_REPEAL != BASE_ACT_REPEAL`.

### №135/2019
- Target is a regulator-approved list for control/supervision.
- No primary current-version/repeal record was resolved in this pass.
- Blocker: `PRIMARY_REGULATOR_CURRENT_VERSION_BLOCKER`.

### №75/2020
- Identity: ФСТЭК 28.05.2020 №75; Minjust №59866.
- Official publication pointer confirmed: `0001202009150068`, published 15.09.2020.
- No later amendment/repeal was confirmed in this pass; absence is not proof of currentness.
- Blocker: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

## New gates

- `PDF_FILENAME_MATCH != INTERNAL_IDENTITY_CONFIRMED`
- `COMPANION_METADATA_DATE_CONFLICT != BODY_IDENTITY_CONFLICT`
- `SUMMARY_OR_IMPLEMENTATION_GUIDANCE != NORMATIVE_BODY`
- `DRAFT_PLANNED_EFFECTIVE_DATE != ACTUAL_EFFECTIVE_DATE`
- `PARTIAL_AMENDING_CLAUSE_REPEAL != BASE_ACT_REPEAL`

## Delta counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +2`
- `PDF_INTERNAL_IDENTITY_BLOCKER +2`
- `GITHUB_METADATA_DATE_CONFLICT +1`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `CURRENT_EDITION_ADVANCED_2025 +2` (№227, №236)
- `DRAFT_AMENDMENT_NOT_EFFECTIVE_2026-09-01 +1` (one project affecting №235 and №239)
- `PRIMARY_LATEST_AMENDMENT_POINTER_CONFIRMED +5` (№31, №227, №235, №236, №239)

## Next boundary

Continue KII positions 29 onward: FSTEK information messages and subsequent federal/regulator acts, preserving separate `NPA / regulator guidance / information message` types.