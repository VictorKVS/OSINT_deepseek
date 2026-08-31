# Habr NPA sweep — Stream 1 — 2026-08-31 04:54 MSK

Scope: Habr 432466, section `Идентификация и аутентификация`, positions 44–50, plus the first two in-scope items of `Служба информационной безопасности организации`.

## Deduplicated Habr targets

Positions 44–47 are already represented in the lifecycle graph and are not counted as new target findings unless new GitHub/full-text/current-status evidence appears:

- Минцифры №445 от 05.05.2023 — already captured as replacement for №494/2021.
- Минцифры №446 от 05.05.2023 — already captured as replacement for №902/2021.
- Минцифры №453 от 12.05.2023 — already captured as replacement for №930/2021; later amended by №553/2025.
- Минцифры №1024 от 29.11.2023 — already captured as replacement for №685/2021 and as an amendment source for №453.

`DUPLICATE_TARGET_ENTRY +4`.

## New targets

### Bank of Russia Methodological Recommendations №4-МР, 14.02.2019

GitHub search:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Exact number/date search and title-fragment search returned zero indexed GitHub code results. No mention/abstract was promoted to body status.

Identity / provenance:
- Bank of Russia official Vestnik publication records confirm №4-МР dated 14.02.2019 and the Habr title; published in `Вестник Банка России №12 (2064)` on 20.02.2019.
- Classification is `RECOMMENDATION_MATERIAL`, not automatically an NPA.

Current applicability:
- Bank of Russia issued later biometric-security guidance №18-МР dated 08.10.2024 and №19-МР dated 09.10.2024 for the post-572-ФЗ architecture.
- No formal cancellation of №4-МР was confirmed in this pass.
- State: `LEGACY_RECOMMENDATION_SCOPE_OVERLAP_2019_vs_18MR_19MR_2024 / CURRENT_APPLICABILITY_BLOCKER`.

### Минцифры России №773, 16.09.2024

GitHub search:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Exact title/date and official-publication-ID search returned zero indexed GitHub code results.

Identity / publication:
- date: 16.09.2024
- Minjust registration: №79838, 21.10.2024
- official publication pointer: `0001202410220021`, 22.10.2024
- entry into force: 02.11.2024
- direct official portal content fetch was unavailable in this pass, so status is `PRIMARY_PUBLICATION_POINTER_CONFIRMED`, not `PRIMARY_DIRECT_FETCH_VERIFIED`.

Lifecycle:
- full accessible text states that paragraph 2 recognizes Минцифры order №1308 dated 06.12.2021 as invalid.
- new edge: `773 -> REPEALS -> 1308`, effective 02.11.2024.
- current status is corroborated by current legal copies, but no primary consolidated current-status page was resolved: `CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER`.

### Минцифры России №392, 28.04.2026

GitHub search:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Exact title/date search returned zero indexed GitHub code results.

Identity / provenance:
- official Minцифры page dated 29.04.2026 confirms order №392 dated 28.04.2026 and the approved list.
- accessible full text confirms the number/date/title and the list body.

Lifecycle / scope:
- paragraph 2 invalidates only `абзац четвертый пункта 1` of Минцифры order №55 dated 04.02.2021.
- this is a partial normative/list-component repeal, not repeal of all of №55.
- new edge: `392 -> PARTIALLY_REPEALS -> Order 55/2021, paragraph 4 of point 1`.

Formal-status blocker:
- no Minjust registration or stable publication.pravo.gov.ru record was confirmed in this pass.
- classify as `OFFICIAL_MINISTRY_HOSTED_DEPARTMENTAL_LIST_ORDER / GENERAL_BINDING_NPA_STATUS_UNRESOLVED` rather than automatically treating the hosted copy as a generally binding registered NPA.

### Presidential Decree №250, 01.05.2022

GitHub search:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Exact-title search returned zero indexed GitHub code results.

Identity / official publication:
- decree: 01.05.2022 №250, `О дополнительных мерах по обеспечению информационной безопасности Российской Федерации`.
- official publication ID: `0001202205010023`, 01.05.2022.

Current edition:
- Presidential Decree №500 dated 13.06.2024 directly amends №250.
- official publication ID for №500: `0001202406130032`, 13.06.2024.
- current edition dated 13.06.2024 is corroborated by consolidated legal sources; primary current consolidated status was not separately resolved in this pass.
- state: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_LATEST_AMENDMENT_CONFIRMED / CURRENT_EDITION_2024-06-13_CORROBORATED / PRIMARY_CURRENT_STATUS_BLOCKER`.

### Government Resolution №1272, 15.07.2022

GitHub search:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

Exact title/date search returned zero indexed GitHub code results.

Identity / official publication:
- PP RF 15.07.2022 №1272, exact Habr title confirmed.
- official publication ID: `0001202207190035`, 19.07.2022.
- official publication PDF: 19 pages.

Completeness gate:
`FULL_TEXT` requires the resolution plus both approved standard regulations (`типовое положение о заместителе руководителя` and `типовое положение о структурном подразделении`). A shorter file containing only the operative resolution or one regulation is `PARTIAL_TEXT`.

No later amendment/repeal was confirmed in this pass, but absence of a hit is not treated as primary current-status proof: `PRIMARY_CURRENT_STATUS_BLOCKER`.

## New counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `DUPLICATE_TARGET_ENTRY +4`
- `NEW_REPEAL_EDGE +1` (`773 -> 1308`)
- `NEW_PARTIAL_REPEAL_EDGE +1` (`392 -> №55/2021, абз.4 п.1`)
- `OFFICIAL_CBR_RECOMMENDATION_PUBLICATION_CONFIRMED +1`
- `PRIMARY_PUBLICATION_POINTER_CONFIRMED +1` (`№773`)
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` (`Указ №250`, `ПП №1272`)
- `PRIMARY_LATEST_AMENDMENT_CONFIRMED +1` (`Указ №250 <- №500/2024`)
- `OFFICIAL_MINISTRY_HOSTED_DEPARTMENTAL_LIST_ORDER +1`
- `CURRENT_APPLICABILITY_BLOCKER +1` (`4-МР`)

## New regression / acceptance gates

1. `RECOMMENDATION_MATERIAL != NPA`.
2. `LATER_GUIDANCE_SCOPE_OVERLAP != FORMAL_REPEAL`.
3. `PARTIAL_REPEAL_OF_PRIOR_COMPONENT != WHOLE_PREDECESSOR_REPEALED`.
4. `OFFICIAL_MINISTRY_HOSTED_DEPARTMENTAL_LIST != AUTOMATICALLY_REGISTERED_GENERAL_BINDING_NPA`.
5. `PRIMARY_INITIAL_PUBLICATION + AMENDMENT != PRIMARY_CURRENT_STATUS`.
6. `FULL_TEXT_FOR_MULTI-APPROVAL_ACT_REQUIRES_ALL_APPROVED_COMPONENTS`.
