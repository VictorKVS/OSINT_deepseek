# Habr NPA sweep — Stream 1 — 2026-08-31 02:54 MSK

## Scope

Continuation of the systematic sweep of Habr article 432466, section **«Идентификация и аутентификация»**, positions 32–37:

1. Приказ Минкомсвязи России от 25.06.2018 № 323
2. Приказ Минцифры России от 29.03.2021 № 187
3. Приказ Минцифры России от 25.05.2021 № 494
4. Приказ Минцифры России от 07.07.2021 № 685
5. Приказ Минцифры России от 01.09.2021 № 902
6. Приказ Минцифры России от 10.09.2021 № 930

Habr snapshot checked: version 28.05.2026, https://habr.com/ru/articles/432466/ . The snapshot still lists all six legacy orders, and also lists their later replacements №445/2023, №446/2023, №453/2023 and №1024/2023.

## GitHub body search

Exact number/date searches and title-fragment searches were run for all six targets using GitHub code search. No indexed full normative body and no reliable body candidate was returned.

| Target | repo | commit | path | size | type | Classification |
|---|---|---|---|---:|---|---|
| №323/2018 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №187/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №494/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №685/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №902/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| №930/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No mention/summary artifact was promoted to `FULL_TEXT`. No new GitHub full-body duplicate and no target-body identity conflict was found.

## Newly confirmed lifecycle findings

### 1. Приказ №323/2018 → №685/2021 → №1024/2023

**№323/2018 identity/origin.** Russian Gazette document page confirms exact date, number and title; registered 29.06.2018 №51497; official portal publication occurred 06.07.2018; effective 06.07.2018.

Source: https://rg.ru/documents/2018/07/06/minsvyaz-prikaz-323-site-dok.html

**Replacement by №685/2021.** Order №685 contains a repeal clause for №323. The replacement was registered 03.09.2021 №64868 and entered into force 14.09.2021. Primary official publication metadata for №685: publication ID `0001202109030034`.

**Second-generation replacement.** Order Минцифры от 29.11.2023 №1024, registered 12.01.2024 №76840, directly states in clause 3 that Order №685/2021 is repealed. Official publication ID: `0001202401120014`; replacement effective 23.01.2024.

Primary/official document copy inspected: https://cdnstatic.rg.ru/uploads/attachments/2024/01/15/76840_a9d.pdf (p.3 contains repeal clause for №685).

Classification:
- №323: `REPEALED_BY_685_EFFECTIVE_2021-09-14`
- №685: `REPEALED_BY_1024_EFFECTIVE_2024-01-23`
- chain: `CHAINED_GENERATIONAL_REPLACEMENT_323_TO_685_TO_1024`
- Habr: `HABR_MULTIPLE_SUCCESSIVE_GENERATIONS_SIMULTANEOUSLY`

### 2. Приказ №187/2021 → №848/2023

Initial official publication for №187 is corroborated by primary official publication register: registered 06.09.2021 №64900, publication ID `0001202109060048`.

Order Минцифры от 09.10.2023 №848 was registered 16.11.2023 №75991, officially published 17.11.2023 under publication ID `0001202311170004`, and entered into force 28.11.2023. Its official PDF directly states in clause 2 that №187/2021 is repealed.

Official document page: https://rg.ru/documents/2023/11/20/mincifry-prikaz848-site-dok.html
Official PDF: https://cdnstatic.rg.ru/uploads/attachments/2023/11/20/75991_91e.pdf

Classification: `REPEALED_BY_848_EFFECTIVE_2023-11-28 / PRIMARY_REPEAL_CLAUSE_DIRECT_VERIFIED / HABR_REPEALED_ACT_CONFLICT`.

### 3. Приказ №494/2021 → №445/2023

Initial publication metadata: registered 15.09.2021 №65009, official publication ID `0001202109160019`, publication date 16.09.2021.

Replacement Order Минцифры от 05.05.2023 №445: registered 26.05.2023 №73486; official portal publication 26.05.2023; entered into force 06.06.2023 and is stated to operate until 01.06.2029. Available full-text legal copies identify №494 as repealed by №445.

Official/RG document page: https://rg.ru/documents/2023/05/29/mincifry-prikaz445-site-dok.html
Official publication pointer previously resolved: `0001202305260007`.

Classification: `REPEALED_BY_445_EFFECTIVE_2023-06-06 / HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY`.

### 4. Приказ №902/2021 → №446/2023

Initial primary official publication confirmed: registered 03.11.2021 №65692, publication ID `0001202111030007`, publication date 03.11.2021.

Order Минцифры от 05.05.2023 №446 was registered 26.05.2023 №73487, officially published 26.05.2023, entered into force 06.06.2023 and operates until 01.06.2029. The official PDF directly states in clause 2 that №902/2021 is repealed.

Official document page: https://rg.ru/documents/2023/05/29/mincifry-prikaz446-site-dok.html
Official PDF: https://cdnstatic.rg.ru/uploads/attachments/2023/05/29/73487_4ae.pdf

Classification: `REPEALED_BY_446_EFFECTIVE_2023-06-06 / PRIMARY_REPEAL_CLAUSE_DIRECT_VERIFIED / HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY`.

### 5. Приказ №930/2021 → №453/2023; early repeal overrides original validity horizon

Target №930 is a `DUPLICATE_TARGET_ENTRY`: it was already encountered earlier as the replacement of №321/2018. This pass adds a **new lifecycle edge**.

Initial official publication: registered 28.10.2021 №65621, publication ID `0001202110280037`, publication date 28.10.2021. The original act had an explicit horizon to 01.03.2028.

Order Минцифры от 12.05.2023 №453 was registered 30.05.2023 №73620, officially published 31.05.2023 and entered into force 11.06.2023; it replaces №930. The replacement is stated to operate to 01.06.2029, with specified provisions only to 01.01.2027.

Official/RG document page: https://rg.ru/documents/2023/06/02/mincifra-prikaz453-site-dok.html

Current replacement layer: №453 has later amendments. Primary official publication register confirms Order Минцифры от 19.06.2025 №553, registered 17.09.2025 №83555, publication ID `0001202509170002`, amending appendices 1, 2 and 5 to №453.

Classification:
- `REPEALED_BY_453_EFFECTIVE_2023-06-11`
- `EXPLICIT_VALID_UNTIL_OVERRIDDEN_BY_EARLY_REPEAL`
- `CURRENT_REPLACEMENT_HAS_LATER_AMENDMENT_553_2025`
- `HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY`

A secondary source was found with a one-day effective-date discrepancy for №453 (10.06.2023), while the Russian Gazette document page gives 11.06.2023. Canonical corpus date remains the primary/official-publication date: `2023-06-11`. Classification: `SECONDARY_EFFECTIVE_DATE_CONFLICT_PRIMARY_WINS`.

## Habr conflict cluster

All six legacy targets in positions 32–37 are repealed as of the 28.05.2026 Habr snapshot:

- №323 — repealed 14.09.2021;
- №187 — repealed 28.11.2023;
- №494 — repealed 06.06.2023;
- №685 — repealed 23.01.2024;
- №902 — repealed 06.06.2023;
- №930 — repealed 11.06.2023.

Therefore this pass adds `HABR_REPEALED_ACT_CONFLICT +6`. For №494/445, №902/446, №930/453 and №685/1024 the Habr snapshot simultaneously lists the repealed act and its replacement. The №323→№685→№1024 chain demonstrates that the reference can contain **three successive generations at once**.

## Full-text completeness gates

If GitHub candidates appear later, `FULL_TEXT` requires:

- №323: order + both approved conformity forms;
- №187: order + complete Procedure;
- №494 / №902: order + complete approved threat list;
- №685: order + both approved conformity forms;
- №930: order + all approved procedures/requirements and appendices, not only the operative part.

## New/strengthened corpus rules

1. `CHAIN_OF_REPLACEMENTS_MUST_BE_RESOLVED_TO_TERMINAL_EFFECTIVE_ACT`.
2. `HABR_MULTIPLE_SUCCESSIVE_GENERATIONS_SIMULTANEOUSLY` is a regression fixture, not a hypothetical case.
3. `PRIMARY_EFFECTIVE_DATE_OVERRIDES_SECONDARY_EFFECTIVE_DATE` when a secondary consolidation conflicts with official publication metadata.
4. Existing rule reconfirmed by №930: `EXPLICIT_VALID_UNTIL != IMMUNITY_FROM_EARLY_REPEAL`.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `DUPLICATE_TARGET_ENTRY +1` (№930; lifecycle edge is new)
- `HABR_REPEALED_ACT_CONFLICT +6`
- `HABR_REPEALED_ACT_AND_REPLACEMENT_SIMULTANEOUSLY +4`
- `CHAINED_GENERATIONAL_REPLACEMENT +1`
- `PRIMARY_REPEAL_CLAUSE_DIRECT_VERIFIED +3` (№187 via №848; №902 via №446; №685 via №1024)
- `SECONDARY_EFFECTIVE_DATE_CONFLICT_PRIMARY_WINS +1`

## Next queue

Continue Habr identification/authentication block without reprocessing already closed targets:

- №142/2022
- №658/2022
- №334/2023
- №378/2023
- №387/2023
- №432/2023

Then continue with positions 44+ only for new GitHub body evidence or new lifecycle/current-edition evidence; known replacement roles must be deduplicated.
