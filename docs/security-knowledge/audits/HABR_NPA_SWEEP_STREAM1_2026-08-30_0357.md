# Habr NPA sweep — Stream 1 — 2026-08-30 03:57 MSK

Source snapshot: Habr article 432466, version dated 2026-05-28, plus the user-maintained NPA queue.

## Delta for this pass

- targets processed: 7
- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- REJECTED_REFERENCE_ONLY: +3 target hits (2 unique GitHub artifacts)
- DUPLICATE_REFERENCE_ARTIFACT: +1
- GITHUB_FULL_TEXT_BLOCKER: +7
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +4
- PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED: +2
- PRIMARY_IDENTITY_CROSS_REFERENCE_CONFIRMED: +1
- OFFICIAL_PUBLICATION_POINTER_CORROBORATED: +2
- LATEST_AMENDMENT_CORROBORATED: +2
- exact full-body duplicates: +0
- new body-level identity conflicts: +0

## Findings

### 1. Постановление Правительства РФ от 21.03.2012 № 211
Target: перечень мер для государственных и муниципальных операторов ПДн.

GitHub:
- exact target search: no reproducible act body.
- rejected hit:
  - repo: `Grantik/odin-vault`
  - commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
  - path: `sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt`
  - blob: `bad57fdb9d2f27f9d120964eb2c8011ee0cf58f4`
  - size: `METADATA_UNRESOLVED`
  - type: `TXT/file`
  - body identity: Минэкономразвития России, приказ от 18.02.2022 № 67 `О государственной информационной системе "Экономика"`; this is not PP №211.
  - classification: `REFERENCE_ONLY / WRONG_PRIMARY_BODY / NOT_ACT_BODY / REJECT`.
- target classification after rejection: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official publication source `Российская газета` reproduces the signing act and attached list, signed 2012-03-21 and published 2012-03-29.
- PP №454 of 2019-04-15 directly amends subparagraph `а` of point 1 of the list approved by PP №211; the amendment relation and exact body are independently corroborated.
- current consolidated body was not obtained directly from `publication.pravo.gov.ru` in this pass.
- status: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED_INITIAL / LATEST_AMENDMENT_CORROBORATED_2019-04-15 / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: `FULL_TEXT = постановление + полный утвержденный перечень мер`.

### 2. Указ Президента РФ от 05.12.2016 № 646
Target: Доктрина информационной безопасности Российской Федерации.

GitHub:
- exact and broad searches returned no reproducible target body.
- repo/commit/path/size/type: null.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary official publication index confirms exact date, number and title.
- publication number: `0001201612060002`.
- publication date: 2016-12-06.
- direct current consolidated body was not resolved in this pass.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: signing decree + full attached Doctrine.

### 3. Указ Президента РФ от 09.05.2017 № 203
Target: Стратегия развития информационного общества в Российской Федерации на 2017–2030 годы.

GitHub:
- exact target search: no body.
- broad search returned:
  - repo: `Grantik/odin-vault`
  - commit: `c4028e14dcadc511b566826ce2ee8e1fccbf83d0`
  - path: `sync/canon/package/samples/koncepciya_gis_rt_teo.txt`
  - blob: `067866c9fe3b098c0432205ca554945298e53bd8`
  - size: `METADATA_UNRESOLVED`
  - type: `TXT/file`
  - actual body: `Концепция государственной информационной системы «Российский транспорт»`, Москва 2024.
  - it states only that the Concept was developed in accordance with the Strategy approved by Decree №203.
  - classification: `REFERENCE_ONLY / WRONG_PRIMARY_BODY / NOT_ACT_BODY / REJECT`.
- target remains `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- primary official publication index confirms exact identity.
- publication number: `0001201705100002`.
- publication date: 2017-05-10.
- direct current consolidated body was not resolved in this pass.
- status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: signing decree + full Strategy.

### 4. Указ Президента РФ от 02.07.2021 № 400
Target: Стратегия национальной безопасности Российской Федерации.

GitHub:
- exact target search: no body.
- broad search returned the same `Grantik/odin-vault` GИС `Российский транспорт` concept already rejected for Decree №203.
- artifact metadata is identical to section 3; it is another NPA reference inside a technical concept, not the decree body.
- classification: `REFERENCE_ONLY / WRONG_PRIMARY_BODY / NOT_ACT_BODY / REJECT / DUPLICATE_REFERENCE_ARTIFACT`.
- target remains `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official publication portal confirms exact identity: `0001202107030001`, published 2021-07-03.
- the official Kremlin page reproduces the full decree and attached Strategy; body confirms `Москва, Кремль / 2 июля 2021 года / № 400` and point 1 approves the attached Strategy.
- later official presidential acts continue to cite Decree №400 as a legal basis, which corroborates current policy relevance but is not treated as a substitute for a separately verified consolidated version.
- status: `PRIMARY_OFFICIAL_FULLTEXT_CONFIRMED / CURRENT_RELEVANCE_PRIMARY_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.

### 5. Указ Президента РФ от 18.06.2024 № 529
Target: приоритетные направления научно-технологического развития и перечень важнейших наукоемких технологий.

GitHub:
- exact and characteristic-title searches returned no reproducible target body.
- repo/commit/path/size/type: null.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- publication pointer corroborated as `0001202406180018`, published 2024-06-18; direct fetch from the official publication portal timed out in this pass.
- a later official Kremlin act (Decree №896 of 2025-12-08) explicitly cites `Указ ... от 18 июня 2024 г. № 529` with the exact target title, confirming act identity from a primary source.
- official search is collision-prone because Decree number `529` is reused in other years (for example 2022 and 2025 acts with different titles).
- status: `PRIMARY_IDENTITY_CROSS_REFERENCE_CONFIRMED / OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_INITIAL_CARD_TIMEOUT / GITHUB_FULL_TEXT_BLOCKER`.
- identity gate remains `DATE + NUMBER + TITLE`, never number alone.

### 6. Распоряжение Правительства РФ от 03.06.2019 № 1189-р
Target: Концепция создания и функционирования национальной системы управления данными + дорожная карта на 2019–2021 годы.

GitHub:
- exact and characteristic-title searches returned no reproducible target body.
- repo/commit/path/size/type: null.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- official publication pointer corroborated: `0001201906070046`, published 2019-06-07.
- the Government primary page `government.ru/docs/36940/` was identified but direct fetch timed out in this pass.
- current full text/identity is corroborated by legal databases, but primary direct current body is not closed.
- status: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_TIMEOUT / FULLTEXT_SECONDARY_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.
- completeness gate: `FULL_TEXT = распоряжение + полная Концепция + полный план мероприятий (дорожная карта)`.

### 7. Постановление Правительства РФ от 16.03.2009 № 228
Target: Положение о Роскомнадзоре.

GitHub:
- exact search returned no reproducible target body.
- repo/commit/path/size/type: null.
- classification: `GITHUB_FULL_TEXT_BLOCKER`.

Official/current:
- current consolidated legal sources show amendments through `ПП РФ от 21.04.2026 № 445`.
- full body of PP №445 confirms that it amends PP №228 by adding subparagraph 5.1.21 concerning permissions for franking machines and repealing subparagraph 5.5.2.
- PP №445 was officially published 2026-04-22 under publication number `0001202604220020` and entered into force 2026-04-30; this publication metadata is corroborated, while the direct primary publication card was not fetched in this pass.
- status: `LATEST_AMENDMENT_CORROBORATED_2026-04-21 / OFFICIAL_PUBLICATION_POINTER_CORROBORATED_FOR_AMENDMENT / PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED / GITHUB_FULL_TEXT_BLOCKER`.
- any future GitHub candidate dated before the 2026 amendment must not be promoted to `CURRENT` without edition analysis.

## New corpus gates

1. `MULTI_TARGET_REFERENCE_ARTIFACT != NPA_COPY`: one technical document may mention many target acts and appear in several searches; it is still one rejected reference artifact.
2. `FULL_TEXT_FOR_STRATEGY_DECREE = SIGNING_DECREE + COMPLETE_APPROVED_STRATEGY`.
3. `FULL_TEXT_FOR_ORDER_WITH_ROADMAP = SIGNING_ORDER + CONCEPT + COMPLETE_ROADMAP`.
4. Reused act numbers require `DATE + NUMBER + TITLE` identity; Decree №529 is a concrete collision example.
5. Later primary-source citation proves `CURRENT_RELEVANCE`, not automatically `CURRENT_CONSOLIDATED_BODY`.
6. A later amendment body may be fully corroborated while the base act still remains `PRIMARY_CURRENT_CONSOLIDATED_BODY_UNRESOLVED`; keep these evidence dimensions separate.

## Source pointers used in this pass

Primary/official:
- Habr source snapshot: https://habr.com/ru/articles/432466/
- Decree №646 official publication: https://publication.pravo.gov.ru/document/view/0001201612060002
- Decree №203 official publication: https://publication.pravo.gov.ru/document/view/0001201705100002
- Decree №400 official publication: https://publication.pravo.gov.ru/Document/View/0001202107030001
- Decree №400 official Kremlin body: https://www.kremlin.ru/acts/bank/47046/print
- PP №211 official publication in `Российская газета`: https://rg.ru/documents/2012/03/30/dannie-dok.html
- Government Order №1189-р primary page (direct fetch timeout this pass): https://government.ru/docs/36940/

GitHub rejected artifacts:
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/package/samples/minekonom_prikaz_67_gis_ekonomika.txt
- https://github.com/Grantik/odin-vault/blob/c4028e14dcadc511b566826ce2ee8e1fccbf83d0/sync/canon/package/samples/koncepciya_gis_rt_teo.txt

Note: GitHub copies are never promoted to official legal sources. Fullness, body identity, edition/currentness, official publication, amendment relation and effective dates remain separate evidence dimensions.