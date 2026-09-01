# Habr NPA Sweep — Stream 1 — 2026-09-01 07:51 MSK

## Scope
Continuation of the systematic pass over Habr 432466 and the user NPA list.
Current boundary: СМЭВ / ГосТех.

Targets in this pass:
1. Приказ Минкомсвязи России от 23.06.2015 №210.
2. Указ Президента РФ от 31.03.2023 №231.
3. Распоряжение Правительства РФ от 21.10.2022 №3102-р.
4. Постановление Правительства РФ от 30.11.2022 №2194.
5. Постановление Правительства РФ от 16.12.2022 №2338.

Rule retained: a GitHub copy is never treated as an official source automatically. GitHub is used only as a corpus/candidate source; identity, lifecycle and official status are verified separately.

## GitHub body search

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| Минкомсвязи №210/2015 | `ale88andr/obs-vault` | `7c3b5dfa92bde4382d3148b9b16131080718c281` | `InfoSec/Законодотельство ИБ/Список НПА, в которых требуется использование СКЗИ.md` | `UNRESOLVED_CONNECTOR_METADATA` | Markdown | `MENTION_ONLY / STUDY_NOTES_WITH_CLAUSE_EXCERPTS / REJECTED_AS_NORMATIVE_BODY` |
| Указ №231/2023 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| Распоряжение №3102-р/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ПП №2194/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ПП №2338/2022 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

### GitHub identity findings

The `ale88andr/obs-vault` file contains the exact target number/date/title for Минкомсвязи №210 and short extracts/notes about the СМЭВ requirements, but it is a study/reference list, not the normative body. Therefore it is not promoted to candidate/full text.

Gate: `TARGET_MENTION_WITH_EXCERPTS != TARGET_NORMATIVE_BODY`.

No GitHub full-body duplicate and no GitHub body identity conflict were confirmed in this pass.

## Official/current-status verification

### Минкомсвязи №210/2015
Identity and MinJust registration are corroborated: 23.06.2015, №210, registration 25.08.2015 №38668; the original version was officially published 27.08.2015. Secondary legal cards show edition 22.02.2017, but a current primary consolidated body was not resolved in this pass.

Status: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

Completeness gate: `FULL_TEXT = ORDER + ENTIRE TECHNICAL REQUIREMENTS`.

### Указ Президента №231/2023
A new lifecycle layer is confirmed: Указ Президента РФ от 12.06.2026 №416 explicitly provides that Указ №231 от 31.03.2023 becomes invalid **from 01.09.2027**.

Official publication pointer for №416 is corroborated as `0001202606120001`, publication date 12.06.2026; direct primary-card fetch was not stable in this pass.

Classification:
- `ENACTED_FUTURE_REPEAL_2027-09-01`
- `CURRENT_NOT_YET_REPEALED_ON_2026-09-01`
- `PRIMARY_PUBLICATION_POINTER_CORROBORATED`
- `PRIMARY_DIRECT_FETCH_BLOCKER`

Gate: `ENACTED_FUTURE_REPEAL != CURRENT_REPEAL`.

### Распоряжение №3102-р/2022
Current edition advanced: Распоряжение Правительства РФ от 08.09.2025 №2474-р amends №3102-р. Current legal cards show edition as of 08.09.2025.

Classification: `CURRENT_EDITION_ADVANCED_2025-09-08`.

Blocker: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_POINTER_BLOCKER`.

Completeness gate: `FULL_TEXT = ORDER + ENTIRE APPROVED GOSTECH CONCEPT`.

### ПП №2194/2022
Formal repeal confirmed. ПП РФ от 08.09.2025 №1388 explicitly recognizes ПП №2194 от 30.11.2022 as invalid. Available legal metadata places entry into force of №1388 on 18.09.2025. Official publication pointer is corroborated as `0001202509100014`, publication 10.09.2025; direct primary-card fetch remains blocked.

Habr still lists №2194 in the active ГосТех section after the formal repeal.

Classification:
- `HABR_REPEALED_ACT_CONFLICT`
- `FORMAL_REPEAL_CONFIRMED_PP_1388_2025`
- `REPEAL_EFFECTIVE_2025-09-18`
- `PRIMARY_DIRECT_FETCH_BLOCKER`

Gate: `REFERENCE_LIST_ENTRY_AFTER_FORMAL_REPEAL != CURRENT_ACT`.

### ПП №2338/2022
The same ПП №1388/2025 that repeals №2194 also amends the Положение о ГосТех approved by №2338. Government platform search results expose №2338 as edition 08.09.2025.

Classification:
- `CURRENT_EDITION_ADVANCED_2025-09-08`
- `LATEST_AMENDMENT_PP_1388_2025`

Completeness gate: `FULL_TEXT = PP_2338 + ENTIRE GOSTECH REGULATION + CURRENT 2025 AMENDMENTS`.

A future GitHub copy of the original 2022 wording must be classified `OLD_EDITION`, not `FULL_TEXT_CURRENT`.

## New counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `HABR_REPEALED_ACT_CONFLICT +1`
- `FORMAL_REPEAL_CONFIRMED +1`
- `CURRENT_EDITION_ADVANCED_2025 +2`
- `ENACTED_FUTURE_REPEAL +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Continue from Habr subsection `Обеспечение защиты информации в ГИС`, beginning with ПП РФ №372 от 26.03.2025, then the federal/general NPA priority within that section.