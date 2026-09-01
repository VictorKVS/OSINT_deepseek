# Habr NPA sweep — Stream 1 — 2026-09-01 12:51 MSK

Scope: Habr 432466, section `Критическая информационная инфраструктура (КИИ)`, positions 15–20.

Targets:
1. ФСБ России от 23.12.2025 № 539
2. ФСБ России от 25.12.2025 № 546
3. ФСБ России от 25.12.2025 № 547
4. ФСБ России от 25.12.2025 № 548
5. ФСБ России от 26.12.2025 № 553
6. ФСБ России от 26.12.2025 № 554

## GitHub body sweep

Exact searches were run by authority + date + number and by distinctive title fragments. No target normative body or reliable body candidate was confirmed on indexed GitHub code in this pass.

| act | repo | commit | path | size | type | class |
|---|---|---|---|---:|---|---|
| ФСБ №539/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ФСБ №546/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ФСБ №547/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ФСБ №548/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ФСБ №553/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |
| ФСБ №554/2025 | null | null | null | null | null | `GITHUB_FULL_TEXT_BLOCKER` |

A broad phrase hit for the title fragment of №539 resolved only to an older 2018 №368 reference in `IKarasev/Study`; it is not the 2025 target and is rejected as `OLD_PREDECESSOR_MENTION`, not a candidate.

Counters: `GITHUB_FULL_TEXT +0`, `RELIABLE_GITHUB_CANDIDATE +0`, `NEW_GITHUB_FULL_BODY_DUPLICATE +0`, `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Primary publication identity

Official publication index (`publication.pravo.gov.ru`) confirms all six identities and registrations:

| act | registration | publication id | publication date | official PDF index |
|---|---:|---|---|---|
| ФСБ №539 от 23.12.2025 | 84782 (25.12.2025) | `0001202512260014` | 26.12.2025 | 136 KB / 4 pp |
| ФСБ №546 от 25.12.2025 | 84870 (30.12.2025) | `0001202512300066` | 30.12.2025 | 415 KB / 8 pp |
| ФСБ №547 от 25.12.2025 | 84871 (30.12.2025) | `0001202512300064` | 30.12.2025 | 667 KB / 12 pp |
| ФСБ №548 от 25.12.2025 | 84872 (30.12.2025) | `0001202512300058` | 30.12.2025 | 405 KB / 8 pp |
| ФСБ №553 от 26.12.2025 | 84873 (30.12.2025) | `0001202512300059` | 30.12.2025 | 663 KB / 12 pp |
| ФСБ №554 от 26.12.2025 | 84874 (30.12.2025) | `0001202512300063` | 30.12.2025 | 846 KB / 17 pp |

Direct official document-card fetch is intermittently timing out for several IDs. Therefore store `OFFICIAL_PUBLICATION_POINTER_CONFIRMED` separately from `PRIMARY_DIRECT_FETCH_OK`. Do not treat a secondary full-text mirror as the official source.

## Lifecycle / conflicts

### №539 + №546: one predecessor split into two successor acts

Old ФСБ №368/2018 approved two procedures in one act: (a) exchange of incident information and (b) receipt by CII subjects of information about attack means/methods and prevention/detection methods.

New №539 starts 30.01.2026 and separately regulates the second function. New №546 starts 30.01.2026 and regulates the exchange function; clause 2 of №546 formally repeals №368 from the same date.

Classification:
- `SPLIT_SUCCESSOR_PAIR = FSB_539_2025 + FSB_546_2025`
- `FORMAL_REPEAL_CONFIRMED = FSB_368_2018 by FSB_546_2025`
- `CROSS_ACT_REPEAL_DEPENDENCY`: №539 does not itself contain the repeal clause for the shared predecessor.
- `SUCCESSOR_SCOPE_EXPANDED`: №546 expressly covers computer attacks and computer incidents.

Habr still lists old №368 in the separate `ГосСОПКА` section while also listing №539/№546 here. This is `HABR_INTERNAL_LIFECYCLE_CONFLICT` and `HABR_REPEALED_ACT_CONFLICT`.

### №547: replacement of №282/2019 and its amendment

№547 starts 30.01.2026. Clause 2 expressly repeals:
- ФСБ №282 от 19.06.2019;
- ФСБ №348 от 07.07.2022 (amending №282).

The successor scope is broader than the old title: it covers computer attacks and computer incidents and also the information resources of organs/organizations subject to part 4 article 9 of 187-FZ.

Classification:
- `FORMAL_REPEAL_CONFIRMED = FSB_282_2019 + FSB_348_2022`
- `SUCCESSOR_SCOPE_EXPANDED`
- `HABR_INTERNAL_LIFECYCLE_CONFLICT`: Habr still lists №282 in the `ГосСОПКА` section.

### №548: new continuous-interaction regime, no repeal clause found

№548 starts 30.01.2026 and establishes continuous interaction with ГосСОПКА via NКЦКИ for CII subjects owning significant CII objects and for the expanded category of organs/organizations under part 4 article 9 of 187-FZ.

The operative part contains approval + effective-date clauses; no clause formally repealing an earlier FSB order was found. Do not infer a predecessor repeal by analogy.

Classification:
- `NEW_REGULATORY_LAYER_2026`
- `NO_FORMAL_PREDECESSOR_REPEAL_CLAUSE_FOUND`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER` remains because the official publication portal is not a consolidated-status service and no later primary repealing/amending act was found in this pass.

### №553: formal replacement of №281/2019

№553 entered into force 10.01.2026. Clause 2 expressly repeals ФСБ №281 от 19.06.2019. Full-text completeness for any GitHub candidate requires both approved attachments: Appendix №1 (Порядок) and Appendix №2 (Технические условия).

Classification:
- `FORMAL_REPEAL_CONFIRMED = FSB_281_2019`
- `HABR_INTERNAL_LIFECYCLE_CONFLICT`: Habr still lists №281 in `ГосСОПКА`.
- `FULL_TEXT_REQUIRES_ALL_TWO_APPROVED_APPENDICES`

### №554: formal replacement of №196/2019

№554 entered into force 10.01.2026. Clause 2 expressly repeals ФСБ №196 от 06.05.2019. A full body must include the order and the complete Requirements appendix.

Classification:
- `FORMAL_REPEAL_CONFIRMED = FSB_196_2019`
- `HABR_INTERNAL_LIFECYCLE_CONFLICT`: Habr still lists №196 in `ГосСОПКА`.
- `FULL_TEXT_REQUIRES_REQUIREMENTS_APPENDIX`

## New gates

- `ONE_PREDECESSOR_CAN_SPLIT_INTO_MULTIPLE_SUCCESSORS`
- `REPEAL_CLAUSE_CAN_RESIDE_IN_SIBLING_SUCCESSOR`
- `SUCCESSOR_SCOPE_EXPANSION_REQUIRES_SEMANTIC_DIFF, NOT NUMBER_ONLY_MAPPING`
- `NO_REPEAL_CLAUSE != REPEAL`
- `OFFICIAL_PUBLICATION_POINTER_CONFIRMED != PRIMARY_DIRECT_FETCH_OK`
- `GITHUB_COPY != OFFICIAL_SOURCE`

## New counters

- `FORMAL_REPEAL_CONFIRMED +4 predecessor acts` (№368, №282, №281, №196; plus amending №348 as a fifth repealed instrument)
- `HABR_REPEALED_ACT_CONFLICT +4` (№368, №282, №281, №196 remain listed elsewhere in Habr)
- `HABR_INTERNAL_LIFECYCLE_CONFLICT +4`
- `SPLIT_SUCCESSOR_PAIR +1`
- `SUCCESSOR_SCOPE_EXPANDED +2` (№546, №547)
- `NEW_REGULATORY_LAYER_2026 +1` (№548)
- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Next boundary

Continue KII positions 21–28: ФСТЭК №31/2014, №227/2017, №229/2017, №235/2017, №236/2017, №239/2017, №135/2019 and №75/2020. Check current editions especially after the 2025–2026 reform of 187-FZ/categorization; do not infer that older ФСТЭК orders are obsolete unless a primary act says so.

Primary references:
- Habr section: https://habr.com/ru/articles/432466/
- Official publication portal: https://publication.pravo.gov.ru/
- №539: https://publication.pravo.gov.ru/document/0001202512260014
- №546: https://publication.pravo.gov.ru/document/0001202512300066
- №547: https://publication.pravo.gov.ru/document/0001202512300064
- №548: https://publication.pravo.gov.ru/document/0001202512300058
- №553: https://publication.pravo.gov.ru/document/0001202512300059
- №554: https://publication.pravo.gov.ru/document/0001202512300063
