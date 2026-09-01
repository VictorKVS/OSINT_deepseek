# Habr NPA sweep — Stream 1 — 2026-09-01 03:52 MSK

Scope: systematic pass over Habr 432466 and the user NPA list. Batch: GIS/MIS section, targets PP RF 1498/2022, 1152/2022, 335/2024, 929/2024, 900/2024, Order 4154-r/2024, PP 981/2025.

Method gates preserved:
- GitHub copy is never official by default.
- FULL_TEXT requires the normative body plus all approved rules/regulations/appendices needed to reproduce the signed package or the current consolidated body, as applicable.
- Identity requires at least type + authority + number + date + title/body match.
- Currentness and official status are verified separately from GitHub identity.
- NO_REPEAL_FOUND != PRIMARY_CURRENT_STATUS_CONFIRMED.

## Batch results

| Target | GitHub full/candidate | GitHub metadata | Official/currentness result | Classification |
|---|---|---|---|---|
| PP RF 26.08.2022 No.1498 | none | repo=null; commit=null; path=null; size=null; type=null | Initial official publication 0001202208290024, 29.08.2022. PP RF 28.04.2023 No.670 expressly repeals No.1498; No.670 entered into force 01.06.2023 and is valid until 01.06.2029. | GITHUB_FULL_TEXT_BLOCKER; HABR_REPEALED_ACT_CONFLICT; HABR_INTERNAL_LIFECYCLE_CONFLICT |
| PP RF 28.06.2022 No.1152 | none | repo=null; commit=null; path=null; size=null; type=null | Initial publication 0001202206290022. Working edition advanced by PP RF 30.09.2023 No.1619 (official publication 0001202310060019). No later repeal confirmed in this pass. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER |
| PP RF 20.03.2024 No.335 | none | repo=null; commit=null; path=null; size=null; type=null | Initial publication 0001202403200024. Working edition 08.10.2025 after PP RF No.1561 (official publication 0001202510100019). FULL_TEXT requires the resolution plus both approved rule packages. | GITHUB_FULL_TEXT_BLOCKER; CURRENT_EDITION_2025-10-08_CORROBORATED |
| PP RF 10.07.2024 No.929 | none | repo=null; commit=null; path=null; size=null; type=null | Initial publication 0001202407110024. Working edition 30.10.2025 after PP RF No.1694. Primary amendment publication resolved in this pass: 0001202510310037, published 31.10.2025. | GITHUB_FULL_TEXT_BLOCKER; CURRENT_EDITION_2025-10-30_CORROBORATED |
| PP RF 01.07.2024 No.900 | none | repo=null; commit=null; path=null; size=null; type=null | DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED, but GitHub body search repeated. Initial publication 0001202407010028. PP RF 04.07.2026 No.845, official publication 0001202607060008, takes effect 01.09.2026 and changes No.900; therefore the effective body changes today. | GITHUB_FULL_TEXT_BLOCKER; DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED; CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 |
| Order RF Gov 30.12.2024 No.4154-r | none | repo=null; commit=null; path=null; size=null; type=null | Official Government page contains the order and the attached Concept. Official publication pointer 0001202501090003, published 09.01.2025. FULL_TEXT requires the order plus the entire Concept. | GITHUB_FULL_TEXT_BLOCKER; PRIMARY_ORIGINAL_BODY_CONFIRMED |
| PP RF 30.06.2025 No.981 | none | repo=null; commit=null; path=null; size=null; type=null | Initial publication 0001202507020021. Current working edition 27.04.2026 after PP RF No.473; official publication 0001202604270057. No.473 changes the date in point 4 from 01.01.2027 to 01.01.2028. | GITHUB_FULL_TEXT_BLOCKER; CURRENT_EDITION_2026-04-27_CORROBORATED |

## New confirmed conflicts / lifecycle events

1. **PP 1498/2022 is stale in the Habr GIS/MIS list.** PP 670/2023 expressly recognizes PP 1498 as repealed. The same Habr article also contains PP 670 as a later entry in the biometric section, so the article simultaneously contains the obsolete act and its repealing successor. New gate: `ARTICLE_CAN_CONTAIN_BOTH_REPEALED_ACT_AND_REPEALING_SUCCESSOR`.

2. **PP 900/2024 changed effective body on 2026-09-01.** PP 845/2026 enters into force on 01.09.2026 and amends PP 900. A copy that was current on 2026-08-31 can be stale on 2026-09-01 even if its file hash and identity are otherwise correct.

3. **PP 929/2024 latest amendment primary pointer closed.** PP 1694/2025 official publication is `0001202510310037`, publication date 31.10.2025. Previous pointer blocker removed.

4. **PP 981/2025 staged-date update confirmed.** PP 473/2026, official publication `0001202604270057`, replaces `1 January 2027` with `1 January 2028` in point 4 of PP 981.

## GitHub search outcome

Exact and broad GitHub code searches were repeated for all seven targets using number/date/title and characteristic phrases. No file passed even the candidate threshold. No mention-only file worth retaining was found in this batch.

Counters:
- GITHUB_FULL_TEXT +0
- RELIABLE_GITHUB_CANDIDATE +0
- GITHUB_FULL_TEXT_BLOCKER +7
- GITHUB_MENTION_ONLY_REJECTED +0
- NEW_GITHUB_FULL_BODY_DUPLICATE +0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT +0
- DUPLICATE_TARGET_ALREADY_STATUS_REVIEWED +1
- HABR_REPEALED_ACT_CONFLICT +1
- HABR_INTERNAL_LIFECYCLE_CONFLICT +1
- CURRENT_EFFECTIVE_BODY_CHANGED_2026-09-01 +1
- PRIMARY_LATEST_AMENDMENT_POINTER_BLOCKER_CLOSED +1

## Primary evidence pointers

- PP 1498/2022: https://publication.pravo.gov.ru/Document/View/0001202208290024
- PP 670/2023: https://publication.pravo.gov.ru/document/0001202305030014
- PP 1152/2022: https://publication.pravo.gov.ru/document/0001202206290022
- PP 1619/2023: https://publication.pravo.gov.ru/document/0001202310060019
- PP 335/2024: https://publication.pravo.gov.ru/document/0001202403200024
- PP 1561/2025: https://publication.pravo.gov.ru/document/0001202510100019
- PP 929/2024: https://publication.pravo.gov.ru/document/0001202407110024
- PP 1694/2025: https://publication.pravo.gov.ru/document/0001202510310037
- PP 900/2024: https://publication.pravo.gov.ru/document/0001202407010028
- PP 845/2026: https://publication.pravo.gov.ru/document/0001202607060008
- Order 4154-r/2024 official Government page: https://government.ru/docs/all/157328/
- Order 4154-r official publication: https://publication.pravo.gov.ru/document/0001202501090003
- PP 981/2025: https://publication.pravo.gov.ru/document/0001202507020021
- PP 473/2026: https://publication.pravo.gov.ru/document/0001202604270057

Next boundary: continue immediately after PP 981/2025 in Habr GIS/MIS, while preserving priority for federal laws, Presidential/Government acts, Roskomnadzor and general PDn/information regulation.
