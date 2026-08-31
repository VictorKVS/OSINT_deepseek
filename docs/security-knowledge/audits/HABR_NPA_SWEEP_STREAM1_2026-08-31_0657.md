# Habr NPA sweep — Stream 1 — 2026-08-31 06:57 MSK

Scope: continuation of Habr 432466 (version 28.05.2026): `Системообразующие документы`, positions 10–11, then `Государственные регуляторы` through Roskomnadzor: PP RF №1722/2020, PP RF №336/2022, Presidential Decree №1085/2004, FSTEC Order №167/2005, Federal Law №40-FZ/1995, Presidential Decree №960/2003, PP RF №418/2008, PP RF №228/2009.

Habr reference: https://habr.com/ru/articles/432466/

## GitHub body search

No accepted full normative body or reliable full-body candidate was found for any of the eight targets in this pass. Exact number/date searches and, where applicable, distinctive title/publication-ID searches returned `total_count=0, incomplete_results=false`.

Accepted-body metadata for all eight targets:
- repo: null
- commit: null
- path: null
- size: null
- type: null
- classification: `GITHUB_FULL_TEXT_BLOCKER`

No mention/summary/reference hit was promoted to `FULL_TEXT`. No new full-body GitHub duplicates and no target-body identity conflicts were confirmed.

## 1. Government Resolution 22.10.2020 №1722

Identity:
- Habr number/date/title match.
- Initial official publication pointer: `0001202010230032`, published 23.10.2020.

Currentness:
- current consolidated text is edition 26.01.2026, effective from 04.02.2026.
- PP RF 26.01.2026 №42 changes №1722: the lists are now formed in FGIS `Реестр обязательных требований` from acts present in that register; inclusion of acts absent from the register is prohibited; paragraph 7(1) of the Rules is repealed.
- publication pointer for №42: `0001202601270032`, publication 27.01.2026.

Completeness gate:
- `FULL_TEXT` requires the Resolution plus the complete Rules in the 26.01.2026 edition.
- a faithful 2020/2021 reproduction is `FULL_TEXT_OLD_EDITION`, not current body.

State:
`OFFICIAL_INITIAL_PUBLICATION_POINTER_CORROBORATED / LATEST_AMENDMENT_42_2026_CORROBORATED / CURRENT_EDITION_2026-01-26_EFFECTIVE_2026-02-04 / GITHUB_FULL_TEXT_BLOCKER`.

## 2. Government Resolution 10.03.2022 №336

Identity:
- Habr number/date/title match.
- initial official publication pointer: `0001202203100013`, publication 10.03.2022.

Currentness / temporal state:
- current legal sources show edition 27.08.2026.
- PP RF 27.08.2026 №1086 directly changes №336 and entered into force on official publication; publication pointer corroborated as `0001202608270016`.
- №1086 extends the special assessment regime in paragraph 11(9) for alcohol retail to 01.09.2027 and changes other time-limited elements.
- an already enacted provision from PP RF 28.12.2024 №1955 becomes effective on 01.09.2026: additional electronic act / registry mechanics in paragraph 11(12). Therefore on 31.08.2026 the corpus must preserve `CURRENT_EFFECTIVE_BODY_2026-08-31` separately from `ENACTED_FUTURE_CHANGE_2026-09-01`.

Restricted-public-body issue:
- Appendix №5, introduced by PP RF 11.09.2024 №1234, is marked `Для служебного пользования` in public legal references.
- do not search for or ingest non-public appendix content. A public copy that faithfully reproduces the public body and marks Appendix №5 as restricted can be classified `PUBLIC_BODY_EXCLUDING_RESTRICTED_APPENDIX`, but not `FULL_NORMATIVE_BODY`.

State:
`OFFICIAL_INITIAL_PUBLICATION_POINTER_CORROBORATED / LATEST_AMENDMENT_1086_2026_PUBLICATION_POINTER_CORROBORATED / CURRENT_EDITION_2026-08-27 / ENACTED_FUTURE_CHANGE_2026-09-01 / DSP_APPENDIX_COMPLETENESS_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

New gates:
- `PUBLIC_TEXT_WITH_DSP_APPENDIX != FULL_NORMATIVE_BODY`.
- `DO_NOT_SEEK_RESTRICTED_APPENDIX_TO_SATISFY_COMPLETENESS`.
- `CURRENT_CONSOLIDATED_EDITION_CAN_CONTAIN_NEXT_DAY_EFFECTIVE_CHANGE`.

## 3. Presidential Decree 16.08.2004 №1085 — FSTEC

Identity:
- Habr number/date/title match.

Currentness:
- current consolidated sources show edition 08.11.2023.
- Presidential Decree 08.11.2023 №846 directly amends №1085 and its FSTEC Regulation; official-publication pointer corroborated as `0001202311080017`.

Completeness gate:
- `FULL_TEXT` requires the decree plus the complete FSTEC Regulation; a bare decree without the Regulation is `PARTIAL_TEXT`.

State:
`LATEST_AMENDMENT_846_2023_PUBLICATION_POINTER_CORROBORATED / CURRENT_EDITION_2023-11-08_CORROBORATED / PRIMARY_INITIAL_PUBLICATION_BLOCKER_FOR_2004_SOURCE / GITHUB_FULL_TEXT_BLOCKER`.

## 4. FSTEC Order 12.05.2005 №167 — FSTEC internal Regulation

Identity:
- Habr correctly gives №167, 12.05.2005 and MinJust registration №6682 dated 06.06.2005.

Currentness:
- current consolidated text is edition 24.08.2023.
- FSTEC Order 24.08.2023 №172 directly amends the Regulation approved by №167.
- primary official publication listing confirms №172, MinJust registration №75184, publication ID `0001202309120024`, publication 12.09.2023; effective 23.09.2023.

Search-data hygiene:
- official portal indexing around publication ID `0001202309120024` can surface noisy neighboring FSTEC entries; identity must be checked by number/date/title inside the target record. The correct target is Order №172 of 24.08.2023 amending Regulation №167.

Completeness gate:
- `FULL_TEXT` requires Order №167 plus the current complete Regulation.

State:
`PRIMARY_LATEST_AMENDMENT_172_2023_CONFIRMED / CURRENT_EDITION_2023-08-24 / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `OFFICIAL_PORTAL_SEARCH_SNIPPET_NOISE_REQUIRES_IN_DOCUMENT_IDENTITY_CHECK`.

## 5. Federal Law 03.04.1995 №40-FZ — FSB

Identity:
- Habr number/date/title match.

Currentness:
- current consolidated sources show edition 28.12.2025 and active status.
- Federal Law 23.07.2025 №239-FZ directly changes №40-FZ and contains staged effective dates, including 01.01.2026 and a separate provision effective 01.04.2026.
- Federal Law 28.12.2025 №492-FZ subsequently amended provisions of №239-FZ before/around their effective transition. Official publication pointer for №492-FZ is `0001202512280002`.

State:
`CURRENT_EDITION_2025-12-28_CORROBORATED / TRANSITIVE_AMENDMENT_CHAIN_40FZ<-239FZ<-492FZ / STAGED_EFFECTIVE_PROVISIONS_RESOLVED / PRIMARY_INITIAL_PUBLICATION_BLOCKER_FOR_1995_SOURCE / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `AMENDING_ACT_AMENDED_BEFORE_TARGET_EFFECTIVE_DATE_REQUIRES_TRANSITIVE_RESOLUTION`.

## 6. Presidential Decree 11.08.2003 №960 — FSB

Identity:
- Habr number/date/title match.

Currentness:
- current consolidated sources show edition 29.12.2025.
- Presidential Decree 29.12.2025 №1002 directly changes the FSB Regulation and structure approved by №960; it entered into force 01.01.2026.
- official-publication pointer: `0001202512290124`, publication 29.12.2025.

Completeness gate:
- `FULL_TEXT` requires decree + FSB Regulation + current structure; omission of the approved structure is `PARTIAL_TEXT`.

State:
`LATEST_AMENDMENT_1002_2025_PUBLICATION_POINTER_CORROBORATED / CURRENT_EDITION_2025-12-29_EFFECTIVE_2026-01-01 / GITHUB_FULL_TEXT_BLOCKER`.

## 7. Government Resolution 02.06.2008 №418 — Ministry of Digital Development

Identity:
- target Resolution title in Habr is correct.
- Habr's regulator section label still says `Министерство цифрового развития, связи и массовых коммуникаций Российской Федерации (Минкомсвязь)`, while the current Regulation expressly gives the official abbreviated name `Минцифры России`. Classification: `HABR_STALE_REGULATOR_SHORT_NAME_CONFLICT`; this is a section-label metadata conflict, not a target NPA identity conflict.

Currentness:
- current consolidated sources show edition 21.04.2026.
- PP RF 21.04.2026 №445 directly changes the Ministry Regulation under №418; edition effective from 30.04.2026.
- publication pointer for №445 is corroborated as `0001202604220020`.
- a newer draft prepared by the Ministry on 07.08.2026 proposes another change to №418, but as of this pass no final enacted publication was confirmed. It remains `DRAFT_NOT_NPA` and must not be merged into the effective body.

Completeness gate:
- `FULL_TEXT` requires Resolution №418 plus complete current Ministry Regulation.

State:
`HABR_STALE_REGULATOR_SHORT_NAME_CONFLICT / CURRENT_EDITION_2026-04-21_EFFECTIVE_2026-04-30 / LATEST_ENACTED_AMENDMENT_445_2026_CORROBORATED / DRAFT_CHANGE_2026-08-07_NOT_NPA / FINALIZATION_BLOCKER / GITHUB_FULL_TEXT_BLOCKER`.

New gates:
- `FRESH_DRAFT_OF_CURRENT_ACT != ENACTED_CURRENT_EDITION`.
- `SECTION_LABEL_CAN_BE_STALE_WHILE_TARGET_ACT_TITLE_IS_CORRECT`.

## 8. Government Resolution 16.03.2009 №228 — Roskomnadzor

Identity:
- Habr number/date/title match and correctly notes the approved Roskomnadzor Regulation.

Currentness:
- current consolidated sources show edition 21.04.2026, effective from 30.04.2026.
- PP RF 21.04.2026 №445 also directly changes the Roskomnadzor Regulation under №228.
- current body retains Roskomnadzor's supervisory functions in the personal-data sphere.
- an old appendix listing subordinate federal unitary enterprises is already repealed; a candidate that preserves that appendix as current must be treated as `OLD_OR_MIXED_EDITION`.

Completeness gate:
- `FULL_TEXT` requires Resolution №228 plus the current Regulation, excluding provisions formally repealed from the current edition.

State:
`CURRENT_EDITION_2026-04-21_EFFECTIVE_2026-04-30 / LATEST_AMENDMENT_445_2026_CORROBORATED / GITHUB_FULL_TEXT_BLOCKER`.

New gate: `REPEALED_APPENDIX_IN_COPY_CAN_REVEAL_OLD_OR_MIXED_EDITION`.

## Delta counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `CURRENT_EDITION_OR_LATEST_AMENDMENT_RESOLVED +8`
- `NEXT_DAY_EFFECTIVE_CHANGE +1` (№336, 01.09.2026)
- `DSP_APPENDIX_COMPLETENESS_BLOCKER +1` (№336)
- `TRANSITIVE_AMENDMENT_CHAIN +1` (№40-FZ)
- `DRAFT_NOT_NPA +1` (draft change to №418 dated 07.08.2026)
- `OFFICIAL_PORTAL_SNIPPET_IDENTITY_NOISE +1` (FSTEC №172 publication listing)
- `HABR_STALE_REGULATOR_SHORT_NAME_CONFLICT +1` (`Минкомсвязь` vs `Минцифры России`)
- `HABR_STALE_OR_REPEALED_TARGET_NPA_CONFLICT +0` for these eight target documents

## Next unchecked regulator queue

- Federal Law 10.07.2002 №86-FZ — Bank of Russia.
- Presidential Decree 16.08.2004 №1082 — Ministry of Defence.
- Presidential Decree 23.07.2013 №631 — General Staff.
- Presidential Decree 13.10.2004 №1313 — Ministry of Justice.
- Presidential Decree 11.07.2004 №865 — Ministry of Foreign Affairs.
- Presidential Decree 14.04.2022 №203 — Interdepartmental Commission of the Security Council on technological sovereignty / CII.
- Presidential Decree 10.11.2018 №648 — Interdepartmental Commission of the Security Council on information security.
