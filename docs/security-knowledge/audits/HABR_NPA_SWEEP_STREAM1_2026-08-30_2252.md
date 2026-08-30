# Habr NPA sweep — Stream 1 — 2026-08-30 22:52 MSK

Scope: Habr 432466, `Идентификация и аутентификация`, positions 12–16. Processed: PP RF No. 1799 (20.10.2021), No. 1815 (23.10.2021), No. 1066 (15.06.2022), No. 1067 (15.06.2022), No. 1089 (16.06.2022).

## Counters

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +5
- NEW_GITHUB_DUPLICATE: +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT: +0
- HABR_REPEALED_ACT_CONFLICT: +3
- HABR_STALE_TITLE_AND_SCOPE_CONFLICT: +2
- PRIMARY_GOVERNMENT_CURRENT_FULLTEXT_CONFIRMED: +1
- PRIMARY_REPEAL_PUBLICATION_CONFIRMED: +1
- OFFICIAL_REPEAL_PUBLICATION_POINTER_CORROBORATED: +2
- CURRENT_EDITION_CORROBORATED: +2
- EXPLICIT_VALIDITY_WINDOW_OVERRIDDEN_BY_EARLY_REPEAL: +1
- QUEUE_DATE_METADATA_CORRECTION: +1

## GitHub search result

Exact date/number and title-oriented GitHub code searches returned no indexed target-body files or reliable candidates for all five documents. Therefore for each target:

`repo=null; commit=null; path=null; size=null; type=null; classification=GITHUB_FULL_TEXT_BLOCKER`.

No GitHub copy was treated as an official source. No mention, implementation, summary, corpus registry, or reference artifact was promoted to a full-text candidate.

## Confirmed findings

### PP RF 20.10.2021 No. 1799

- GitHub: no full text/candidate; all file metadata fields null.
- Habr 28.05.2026 still lists No. 1799 as item 12.
- PP RF 22.05.2023 No. 810 expressly recognizes No. 1799 as invalid and establishes the replacement accreditation rules.
- No. 810 entered into force on 01.06.2023; therefore No. 1799 is not a current requirement after that date.
- Official publication pointer for No. 810 is corroborated as `0001202305220032`, 22.05.2023; direct publication portal card timed out in this pass, so the record is not promoted to `PRIMARY_DIRECT_FETCH_VERIFIED`.
- Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_EFFECTIVE_2023-06-01 / OFFICIAL_REPEAL_PUBLICATION_POINTER_CORROBORATED`.

Sources:
- Habr: https://habr.com/ru/articles/432466/
- PP 810 text/status: https://normativ.kontur.ru/document/1/449053-postanovlenie-pravitelstva-rf-ot-22-05-2023-n-810
- Official publication pointer target: https://publication.pravo.gov.ru/document/0001202305220032

### PP RF 23.10.2021 No. 1815

- GitHub: no full text/candidate; all file metadata fields null.
- Correct date is `23.10.2021`. The previous queue line accidentally carried `22.10.2021`; corrected here as `QUEUE_DATE_METADATA_CORRECTION`.
- Original act established the biometric collection/processing cases from 01.03.2022 and originally carried a regulatory horizon through 01.03.2028.
- PP RF 23.03.2024 No. 367 includes No. 1815 in the list of acts recognized as invalid. No. 367 took effect on official publication, 26.03.2024.
- Therefore the originally stated future validity horizon did not preserve No. 1815 after an explicit repeal.
- Official publication pointer for No. 367 is corroborated as `0001202403260025`, 26.03.2024; direct card timed out in this pass.
- Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_EFFECTIVE_2024-03-26 / EXPLICIT_VALIDITY_WINDOW_OVERRIDDEN_BY_EARLY_REPEAL`.

Sources:
- Habr: https://habr.com/ru/articles/432466/
- PP 367 text/status: https://normativ.kontur.ru/document/1/468063-postanovlenie-pravitelstva-rf-ot-23-03-2024-n-367
- Official publication pointer target: https://publication.pravo.gov.ru/document/0001202403260025

### PP RF 15.06.2022 No. 1066

- GitHub: no full text/candidate; all file metadata fields null.
- Habr 28.05.2026 still shows the original long-form title based on the former `единая информационная система персональных данных...` terminology.
- Current consolidated title is `О размещении физическими лицами своих биометрических персональных данных в единой биометрической системе с использованием мобильного приложения единой биометрической системы`.
- Current edition is corroborated as 19.09.2025; it includes amendments No. 851/2023, No. 367/2024, No. 1183/2025 and No. 1443/2025.
- The primary Government page for PP No. 1183/2025 explicitly amends No. 1066 and adds point 7: the resolution acts until 01.03.2028, except the regional-segment Rules, which act until 01.01.2027.
- Current full text requires both approved Rule sets; a file containing only the federal EBS mobile-app Rules is `PARTIAL_TEXT`.
- Classification: `HABR_STALE_TITLE_AND_SCOPE_CONFLICT / CURRENT_EDITION_CORROBORATED_2025-09-19 / PRIMARY_LATEST_AMENDMENT_RELATION_CONFIRMED`.

Sources:
- Habr: https://habr.com/ru/articles/432466/
- Primary Government PP 1183/2025: https://government.ru/docs/all/160478/
- Current consolidated copy used only for current-body corroboration: https://normativ.kontur.ru/document?documentId=501910&moduleId=1

### PP RF 15.06.2022 No. 1067

- GitHub: no full text/candidate; all file metadata fields null.
- Primary initial publication is directly confirmed: `0001202206170005`, 17.06.2022; the original title uses the former long-form EBS wording.
- The current Government-hosted text now carries the title `О случаях и сроках использования биометрических персональных данных, размещенных физическими лицами в единой биометрической системе с использованием мобильного приложения единой биометрической системы`.
- The Government page lists amendments No. 383/2023, No. 893/2023, No. 15/2025, No. 1183/2025 and No. 1443/2025; current edition is 19.09.2025.
- PP No. 893/2023 directly rewrote the title and core body. The current act entered into force 01.03.2023 and acts until 01.03.2029.
- Habr 28.05.2026 still carries the pre-893 title.
- Classification: `PRIMARY_GOVERNMENT_CURRENT_FULLTEXT_CONFIRMED / CURRENT_EDITION_2025-09-19 / HABR_STALE_TITLE_AND_SCOPE_CONFLICT`.

Primary sources:
- Initial publication: https://publication.pravo.gov.ru/Document/View/0001202206170005
- Current Government text: https://government.ru/docs/all/141579/
- PP 893/2023 amendment: https://government.ru/docs/all/147802/

### PP RF 16.06.2022 No. 1089

- GitHub: no full text/candidate; all file metadata fields null.
- Habr 28.05.2026 still lists No. 1089 as item 16.
- PP RF 31.05.2023 No. 883 explicitly approves the new Regulation on the unified biometric system, including its regional segments, and expressly recognizes No. 1089 as invalid.
- Primary official publication for No. 883 is directly confirmed: `0001202306010068`, 01.06.2023.
- No. 883 entered into force on official publication; therefore No. 1089 ceased to be the current EBS regulation from 01.06.2023.
- Habr later lists No. 883 itself as item 27 while retaining No. 1089 at item 16, creating an internal lifecycle contradiction inside the same 28.05.2026 checklist.
- Classification: `HABR_REPEALED_ACT_CONFLICT / REPEALED_EFFECTIVE_2023-06-01 / PRIMARY_REPEAL_PUBLICATION_CONFIRMED`.

Primary source:
- https://publication.pravo.gov.ru/document/0001202306010068

## New regression gates

1. `EXPLICIT_VALID_UNTIL != IMMUNITY_FROM_EARLY_REPEAL` — a declared future validity horizon is subordinate to a later explicit repeal; No. 1815 is the regression fixture.
2. `HABR_CAN_CONTAIN_REPEALED_ACT_AND_ITS_REPLACEMENT_SIMULTANEOUSLY` — lifecycle resolution must not trust list position or article freshness; No. 1799/810 and No. 1089/883 are fixtures.
3. `LEGACY_EBS_LONG_TITLE != CURRENT_SCOPE` — title and approved attachments must be resolved through the 572-FZ-era amendment chain for No. 1066/1067.
4. `MULTI_RULE_FULLTEXT_REQUIRES_ALL_APPROVED_RULE_SETS` — No. 1066 is incomplete without both federal-EBS and regional-segment Rules.
5. `NUMBER_ONLY_IDENTITY_KEY_IS_UNSAFE` — later acts can reuse the same numeric identifier in another year; canonical identity remains authority + type + date + number + internal title/body identity.

## Next queue

Continue the same Habr section from item 17: PP RF No. 2326 (16.12.2022), No. 2511 (29.12.2022), No. 405 (17.03.2023), No. 451 (24.03.2023), No. 478 (27.03.2023), deduplicating any already processed act and resolving 572-FZ-era title/lifecycle changes before accepting a current requirement.
