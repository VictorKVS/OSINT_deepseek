# Habr NPA sweep — Stream 1 — 2026-08-30 04:56 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 5
- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- DUPLICATE_REFERENCE_ARTIFACT / DUPLICATE_REFERENCE_HIT: +2 target hits
- GITHUB_FULL_TEXT_BLOCKER: +5
- PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED: +3 (Government pages for 4088-r, 1105-r, 1315-r)
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +2 (Decree 490; FZ 123)
- PRIMARY_AMENDMENT_RELATION_CONFIRMED: +2 (Decree 124 -> Decree 490; FZ 233 -> FZ 123)
- PRIMARY_CURRENT_CONSOLIDATED_BODY_CONFIRMED: +1 (1315-r, edition marker 2963-r/2024)
- INTERNAL_CROSS_REFERENCE_SUPERSEDED: +1 (4088-r -> repealed 2471-r)
- HABR_STALE_TITLE_CONFLICT: +1 (123-FZ)
- TEMPORAL_LIFECYCLE_CLARIFICATION: +1 (123-FZ experiment term vs residual PD/data provisions)
- exact full-body duplicates: +0
- new GitHub body-level identity conflicts: +0

## Findings

### 1. Указ Президента РФ от 10.10.2019 № 490
Target: `О развитии искусственного интеллекта в Российской Федерации` + complete National AI Strategy through 2030.

GitHub:
- exact Code Search for number/date/AI wording returned one hit only:
  - repo: `Grantik/odin-vault`
  - commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
  - path: `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`
  - blob: `067866c9fe3b098c0432205ca554945298e53bd8`
  - size: `METADATA_UNRESOLVED`
  - type: `TXT/file`
- body inspection proves this file is the `Концепция государственной информационной системы «Российский транспорт»`, Moscow 2024, not Decree №490 or the National AI Strategy.
- the same artifact was already rejected in the previous sweep for Decrees №203 and №400; therefore this is not a new candidate but a `DUPLICATE_REFERENCE_ARTIFACT / WRONG_PRIMARY_BODY / REJECT`.
- target status after rejection: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary official publication confirms date, number and title; publication number `0001201910110003`, publication date 2019-10-11.
- primary Kremlin body of Decree №124 dated 2024-02-15 explicitly amends both Decree №490 and the National Strategy approved by it.
- current legal databases checked in this pass show the consolidated edition dated 2024-02-15; no later amendment was identified in this pass.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_AMENDMENT_RELATION_CONFIRMED_2024-02-15 / CURRENT_EDITION_CORROBORATED_2024-02-15 / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: `FULL_TEXT = signing decree + complete National Strategy in the relevant edition`.

### 2. Распоряжение Правительства РФ от 22.12.2022 № 4088-р
Target: `Концепция формирования и развития культуры информационной безопасности граждан Российской Федерации`.

GitHub:
- exact Code Search for `4088-р` returned `total_count=0`, `incomplete_results=false`.
- exact number + characteristic title wording also returned zero.
- repo/commit/path/size/type: `null`.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary Government page reproduces the signing order and full approved Concept, including the approval header `УТВЕРЖДЕНА ... от 22 декабря 2022 г. № 4088-р`.
- status: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

New cross-reference conflict:
- the official text of the 4088-r Concept still expressly refers to the children's information-security Concept approved by Government Order №2471-r dated 2015-12-02.
- the primary Government text of Order №1105-r dated 2023-04-28 expressly repeals №2471-r in paragraph 4 and approves the replacement children's Concept.
- classification: `INTERNAL_CROSS_REFERENCE_SUPERSEDED_AFTER_2023-04-28`.
- this does **not** by itself repeal or invalidate 4088-r; it is a stale internal normative reference that should be modeled as a relation-level freshness defect, not an act-level repeal.

### 3. Распоряжение Правительства РФ от 28.04.2023 № 1105-р
Target: `Концепция информационной безопасности детей в Российской Федерации`.

GitHub:
- exact Code Search for `1105-р` returned `total_count=0`, `incomplete_results=false`.
- number + title search also returned zero.
- repo/commit/path/size/type: `null`.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary Government page reproduces the signing order and complete approved Concept.
- paragraph 4 explicitly repeals Government Order №2471-r dated 2015-12-02.
- the Government page does not display an amendment marker for 1105-r in the text resolved in this pass; no claim of immutable/current consolidation is inferred merely from that absence.
- status: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / REPEALS_2471-R_PRIMARY_CONFIRMED / CURRENT_AMENDMENT_STATUS_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.

### 4. Распоряжение Правительства РФ от 20.05.2023 № 1315-р
Target: `Концепция технологического развития на период до 2030 года`.

GitHub:
- exact Code Search for `1315-р` returned `total_count=0`, `incomplete_results=false`.
- number + characteristic-title search also returned zero.
- repo/commit/path/size/type: `null`.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary Government page reproduces the signing order and approved Concept.
- critically, the same primary Government page displays an explicit edition marker: `(В редакции Распоряжения Правительства Российской Федерации от 21.10.2024 № 2963-р)`.
- current legal databases checked in this pass also show the edition dated 2024-10-21.
- status: `PRIMARY_CURRENT_CONSOLIDATED_BODY_CONFIRMED / AMENDMENT_MARKER_2963-R_2024-10-21 / GITHUB_FULL_TEXT_BLOCKER`.
- any GitHub candidate lacking the 2963-r/2024 edition marker or equivalent amended clauses must be edition-checked before promotion to `CURRENT`.

### 5. Федеральный закон от 24.04.2020 № 123-ФЗ
Target: Moscow AI experiment law, now also governing regional anonymized-data-set processing provisions.

GitHub:
- exact Code Search for `123-ФЗ + 24.04.2020 + искусственного интеллекта` returned one hit only:
  - repo: `Grantik/odin-vault`
  - commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
  - path: `sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt`
  - blob returned by current code-search result: `0d3f7c3d0618464af74753ad5a92e59568eb9211`
  - size: previously inspected corpus artifact; not re-promoted in this pass
  - type: `TXT/file`
- this is the already-known full copy of 152-FZ; 123-FZ appears only as an amendment/cross-reference inside it.
- classification: `DUPLICATE_REFERENCE_HIT / NOT_TARGET_BODY / REJECT`.
- target remains `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary official publication confirms the original 123-FZ: publication number `0001202004240030`, published 2020-04-24, official PDF listed as 1027 KB / 19 pages.
- primary official publication of Federal Law №233-FZ dated 2024-08-08 is `0001202408080031`; its Article 2 directly amends 123-FZ, including the **title**, and adds Articles 6.1 and 6.2 on regional anonymized personal-data sets.
- Article 3(2) of 233-FZ makes Article 2 effective from 2025-09-01.
- current legal text therefore uses the longer title containing `об особенностях обработки персональных данных при формировании региональных составов данных и предоставления доступа к региональным составам данных`.

Conflict with Habr snapshot:
- Habr version dated 2026-05-28 still lists the **pre-2025 title** of 123-FZ, omitting the regional-data wording added by 233-FZ and effective from 2025-09-01.
- classification: `HABR_STALE_TITLE_CONFLICT`.

Lifecycle clarification:
- Article 1 of the 2020 law established the Moscow experimental legal regime for five years beginning 2020-07-01; that experimental period therefore expired in 2025.
- however, 233-FZ subsequently added Articles 6.1 and 6.2 effective 2025-09-01, so the statute cannot be modeled simply as `EXPIRED` as a whole.
- classification: `EXPERIMENTAL_REGIME_TERM_ENDED / RESIDUAL_PD_DATA_PROVISIONS_ACTIVE / WHOLE_ACT_NOT_SIMPLY_EXPIRED`.

## New corpus gates

1. `REFERENCE_FRESHNESS != ACT_FRESHNESS`: an otherwise current act may contain an internal citation to a later-repealed act; store freshness on the relation edge as well as on the act.
2. `HABR_TITLE == SNAPSHOT_TITLE`, not necessarily `CURRENT_LEGAL_TITLE`: title amendments must be edition-aware and checked independently.
3. `TEMPORARY_REGIME_ENDED != WHOLE_FEDERAL_LAW_EXPIRED`: a temporary experiment can end while later-added permanent/residual provisions of the same law remain relevant.
4. A primary Government page carrying an explicit `(В редакции ... )` marker is stronger current-edition evidence than a secondary database revision date; preserve the primary marker separately.
5. Repeated semantic GitHub hits to the same technical/reference file are counted as `DUPLICATE_REFERENCE_ARTIFACT`, not as new candidate discoveries.

## Source pointers used in this pass

Habr:
- https://habr.com/ru/articles/432466/

Primary/official:
- Decree №490 original publication: https://publication.pravo.gov.ru/document/view/0001201910110003
- Decree №490 Kremlin bank: https://www.kremlin.ru/acts/bank/44731
- Decree №124 amendment body: https://www.kremlin.ru/acts/bank/50326/print
- Government Order №4088-r: https://government.ru/docs/all/145092/
- Government Order №1105-r: https://government.ru/docs/all/147360/
- Government Order №1315-r: https://government.ru/docs/all/147621/
- FZ №123 original publication list entry: https://publication.pravo.gov.ru/documents/block/president?index=253
- FZ №233 amendment publication: https://publication.pravo.gov.ru/document/0001202408080031

GitHub rejected/duplicate artifacts:
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/package/samples/koncepciya_gis_rt_teo.txt
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt

Note: GitHub copies are never promoted to official legal sources. Fullness, body identity, title identity, edition/currentness, internal-reference freshness, official publication, amendment relation and effective dates remain separate evidence dimensions.
