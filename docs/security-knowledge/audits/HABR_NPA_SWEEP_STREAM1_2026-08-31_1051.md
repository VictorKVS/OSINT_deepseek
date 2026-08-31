# Habr NPA sweep — Stream 1 — 2026-08-31 10:51 MSK

## Scope
Continuation of Habr 432466, subsection `Техническое регулирование. Аттестация объектов информатизации`:

1. `Положение по аттестации объектов информатизации по требованиям безопасности информации` (Гостехкомиссия, 25.11.1994).
2. Приказ Гостехкомиссии России 05.01.1996 No. 3 — типовые положения системы сертификации/аттестации.
3. Приказ ФСТЭК России 29.04.2021 No. 77 — порядок организации и проведения работ по аттестации объектов информатизации.
4. Информационное сообщение ФСТЭК России 02.09.2021 No. 240/24/4303.
5. Материал Минцифры России `Типовое техническое задание на выполнение работ по оценке уровня защищенности информационной инфраструктуры` (исходно распространен 03.06.2022).
6. Информационное сообщение ФСТЭК России 11.04.2022 No. 240/24/1950.
7. Приказ ФСТЭК России 27.07.2023 No. 147 — аттестация работников органов по сертификации/испытательных лабораторий.

Habr reference: https://habr.com/ru/articles/432466/

## GitHub normative-body search

Exact number/date/title searches were performed for all seven targets. Searches were also run for FSTEK message numbers `240/24/4303`, `240/24/1950` and official publication identifier `0001202108100027` for Order 77. No full normative body and no reliable body candidate was found.

| target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| Gostekhkomissiya Regulation 25.11.1994 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Gostekhkomissiya Order 3/1996 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK Order 77/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK message 240/24/4303 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| MinDigital typical technical assignment | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK message 240/24/1950 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEK Order 147/2023 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No new GitHub full-body duplicate and no GitHub body identity conflict was found. No mention/summary hit was promoted to normative body.

## New confirmed findings, conflicts and blockers

### Gostekhkomissiya Regulation of 25.11.1994

The document identity is corroborated by accessible full legal copies. No primary official current-status card or formal repeal act was resolved in this pass.

There is a material status conflict in secondary sources: consolidated legal databases continue to expose the Regulation as active, while sector/legal commentary argues that parts of the old certification/attestation architecture lost practical effect after the old 1995 certification system ceased in 2018. This interpretation is not sufficient evidence of formal repeal.

Order 77/2021 is narrower in scope (information with restricted access that is not a state secret), while the 1994 Regulation covers a broader historical attestation framework. Therefore replacement of the entire 1994 act by Order 77 must not be inferred.

Classification: `STATUS_CONFLICT_NONPRIMARY / FORMAL_REPEAL_NOT_CONFIRMED / PRIMARY_CURRENT_STATUS_BLOCKER`.

Gate: `DEPENDENCY_ON_REPEALED_OR_REBUILT_FOUNDATIONAL_REGIME != AUTOMATIC_FORMAL_REPEAL_OF_DERIVATIVE_ACT`.

### Gostekhkomissiya Order No. 3 of 05.01.1996

Accessible archival/legal sources confirm that Order 3 approved several typical regulations within the old certification/attestation system. No primary repeal clause for Order 3 itself was found.

The 2018 FSTEK transition material directly concerns termination of the 1995 certification regulation, not a formal repeal of Order 3. Secondary commentary inferring that the 1996 typical regulations also ceased with the old system remains interpretive evidence only.

Classification: `DERIVATIVE_STATUS_CONFLICT / FORMAL_REPEAL_NOT_CONFIRMED / PRIMARY_CURRENT_STATUS_BLOCKER`.

Gate: `PARENT_SYSTEM_TERMINATED != FORMAL_REPEAL_OF_EVERY_DERIVATIVE_DOCUMENT`.

### FSTEK Order No. 77 of 29.04.2021

Initial official publication is corroborated by the official publication identifier `0001202108100027`; Ministry of Justice registration No. 64589. Direct retrieval of that primary publication page timed out in this pass, so identity is treated as `OFFICIAL_PUBLICATION_POINTER_CORROBORATED`, not as a successful direct fetch.

A new primary lifecycle event is confirmed: FSTEK Order No. 60 of 27.02.2026 directly amends Order 77. Official publication: `0001202606250029`, 25.06.2026; Ministry of Justice registration No. 87202 of 24.06.2026. Order 60 enters into force on 01.09.2026.

Therefore as of 31.08.2026 the corpus must store two states:

- `CURRENT_EFFECTIVE_BODY_2026-08-31` — Order 77 before Order 60 takes effect;
- `ENACTED_FUTURE_CHANGE_2026-09-01_BY_ORDER_60_2026`.

Order 60 changes, among other things, periodic control/attestation reporting and vulnerability/security-testing related provisions. A full-text copy of Order 77 that does not incorporate Order 60 becomes stale from 01.09.2026.

Classification: `PRIMARY_FUTURE_AMENDMENT_PUBLICATION_CONFIRMED / ENACTED_FUTURE_CHANGE_2026-09-01`.

Gate: `CURRENT_FULL_TEXT_TODAY_CAN_BECOME_STALE_NEXT_DAY_BY_ALREADY_PUBLISHED_AMENDMENT`.

### FSTEK information message No. 240/24/4303 of 02.09.2021

Identity and official hosting are confirmed on the FSTEK website. The message explains the entry into force/application of Order 77.

This is an official informational material, not a registered normative legal act. It must not be put into the NPA body layer merely because it is hosted on the regulator's official site.

Classification: `PRIMARY_OFFICIAL_INFORMATIONAL_HOSTING_CONFIRMED / NON_NPA_OFFICIAL_MATERIAL / REFERENCES_BASE_ORDER_77`.

Gate: `OFFICIAL_REGULATOR_HOSTING != NORMATIVE_LEGAL_NATURE`.

### MinDigital typical technical assignment for assessment of information-infrastructure protection

The Ministry's official site currently hosts the document with the matching title and exposes it as a DOCX resource (search index reports approximately 52 KB), together with a standardized report form. Direct page retrieval timed out in this pass.

The original 03.06.2022 dissemination date is corroborated by contemporaneous external coverage, but current Ministry CMS/search timestamps reflect later site publication/migration and must not be treated as the original legal/document date.

This is a template/methodical material, not an NPA.

Classification: `PRIMARY_HOSTING_CONFIRMED / ORIGINAL_DATE_CORROBORATED_NONPRIMARY / NON_NPA_OFFICIAL_MATERIAL / DIRECT_PAGE_FETCH_BLOCKER`.

Gates: `MINISTRY_HOSTED_TEMPLATE != NPA`; `CMS_PAGE_DATE != ORIGINAL_DOCUMENT_DATE`; `CURRENT_HOSTING != CURRENT_NORMATIVE_FORCE`.

### FSTEK information message No. 240/24/1950 of 11.04.2022

Identity and official FSTEK hosting are confirmed. The message concerns implementation/submission of attestation materials under Order 77, including points 27 and 32.

It is official informational guidance, not an NPA. Since Order 60/2026 changes Order 77 from 01.09.2026, including provisions relevant to periodic control/reporting, this 2022 guidance requires compatibility revalidation from that date. No formal repeal of the information message was found.

Classification: `PRIMARY_OFFICIAL_INFORMATIONAL_HOSTING_CONFIRMED / NON_NPA_OFFICIAL_MATERIAL / FUTURE_GUIDANCE_COMPATIBILITY_BLOCKER_2026-09-01`.

Gate: `BASE_NPA_AMENDED != AUTOMATIC_FORMAL_REPEAL_OF_INFORMATION_MESSAGE`, but the message cannot be assumed substantively current after the amendment without revalidation.

### FSTEK Order No. 147 of 27.07.2023

Initial publication is directly confirmed on the official portal: publication No. `0001202311230015`, publication date 23.11.2023; Ministry of Justice registration No. 76065.

Accessible full legal text confirms entry into force on 01.09.2024 and includes the approved procedure plus application/certificate appendices. No later amendment was confirmed in this pass; current status is corroborated outside the primary publication portal, so the corpus keeps `PRIMARY_CURRENT_STATUS_BLOCKER` rather than inferring current force solely from absence of repeal.

Completeness: `FULL_TEXT = order shell + complete approved Procedure + Appendix 1 application + Appendix 2 certificate`; omission of an appendix is `PARTIAL_TEXT`.

Classification: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_STATUS_CORROBORATED_NONPRIMARY / PRIMARY_CURRENT_STATUS_BLOCKER`.

## New counts

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +1` (FSTEK 147)
- `OFFICIAL_PUBLICATION_POINTER_CORROBORATED +1` (FSTEK 77 initial publication)
- `PRIMARY_FUTURE_AMENDMENT_PUBLICATION_CONFIRMED +1` (FSTEK 60 -> Order 77)
- `ENACTED_FUTURE_CHANGE +1` (01.09.2026)
- `PRIMARY_OFFICIAL_INFORMATIONAL_HOSTING_CONFIRMED +3` (4303, 1950, MinDigital template hosting)
- `NON_NPA_OFFICIAL_MATERIAL +3`
- `STATUS_OR_DERIVATIVE_STATUS_CONFLICT_NONPRIMARY +2` (1994 Regulation; Order 3/1996)
- `FORMAL_REPEAL_NOT_CONFIRMED +2`
- `PRIMARY_CURRENT_STATUS_BLOCKER +3` (1994; Order 3/1996; Order 147)
- `FUTURE_GUIDANCE_COMPATIBILITY_BLOCKER +1` (240/24/1950 from 01.09.2026)
- `DIRECT_PAGE_FETCH_BLOCKER +1` (MinDigital template page)
- `HABR_REPEALED_ACT_CONFLICT +0`
- `DUPLICATE_TARGET_ENTRY +0`

## New corpus gates

1. `OFFICIAL_REGULATOR_HOSTING != NORMATIVE_LEGAL_NATURE`.
2. `MINISTRY_HOSTED_TEMPLATE != NPA`.
3. `CMS_PAGE_DATE != ORIGINAL_DOCUMENT_DATE`.
4. `CURRENT_HOSTING != CURRENT_NORMATIVE_FORCE`.
5. `DEPENDENCY_ON_REPEALED_OR_REBUILT_FOUNDATIONAL_REGIME != AUTOMATIC_FORMAL_REPEAL_OF_DERIVATIVE_ACT`.
6. `PARENT_SYSTEM_TERMINATED != FORMAL_REPEAL_OF_EVERY_DERIVATIVE_DOCUMENT`.
7. `CURRENT_FULL_TEXT_TODAY_CAN_BECOME_STALE_NEXT_DAY_BY_ALREADY_PUBLISHED_AMENDMENT`.
8. `BASE_NPA_AMENDED != AUTOMATIC_FORMAL_REPEAL_OF_INFORMATION_MESSAGE`.
9. `FULLTEXT_FSTEK_ORDER_WITH_APPROVED_PROCEDURE = ORDER_SHELL + PROCEDURE + ALL_CURRENT_APPENDICES`.

## Next queue

Continue with Habr subsection `Лицензирование деятельности в области информационной безопасности`:

1. Federal Law 04.05.2011 No. 99-FZ `О лицензировании отдельных видов деятельности`.
2. Government Resolution 31.07.1996 No. 770.
3. Government Resolution 21.11.2011 No. 957.
4. Government Resolution 03.02.2012 No. 79.
5. Government Resolution 03.03.2012 No. 171.
6. Government Resolution 12.04.2012 No. 287.
7. Government Resolution 16.04.2012 No. 313.
