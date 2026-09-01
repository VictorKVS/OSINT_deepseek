# Habr NPA sweep — Stream 1 — 2026-09-01 06:56 MSK

Scope: Habr 432466, section «Государственные и муниципальные информационные системы», positions 48–55.

## GitHub body search

Classification rule: a GitHub copy is never treated as an official source. `FULL_TEXT` requires internal identity (number/date/title) plus complete operative body/attachments; status/currentness is checked separately against official/publication sources.

| Target | GitHub result | repo | commit | path | size | type | classification |
|---|---|---|---|---|---:|---|---|
| Минцифры 06.12.2021 №1308 | no reliable body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Минцифры 07.12.2021 №1312 | no reliable body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| ЦИК 08.06.2022 №86/715-8 | no reliable body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Минэкономразвития 15.11.2022 №624 | no reliable body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Минцифры №611 / ФСО №96, 12.07.2024 | no reliable body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Минцифры 31.07.2024 №677 | no reliable body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Письмо Минцифры 17.09.2024 №П25-305029 | no reliable GitHub body/candidate | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER / NON_NPA_REFERENCE |
| Минцифры 02.12.2025 №1106 | one exact mention only | pikov-vitaliy/pikov-expert-lectures | 3743195404811ac9c3468c948bc4e78c67b56561 | new-courses/index.html | UNRESOLVED_CONNECTOR_METADATA | HTML | MENTION_ONLY / EDUCATIONAL_TIMELINE / REJECTED_AS_NORMATIVE_BODY |

GitHub exact searches used number/date/title/distinctive phrases. No full-body duplicate and no body identity conflict found in this batch.

## New confirmed status/currentness findings

### 48. Минцифры №1308 от 06.12.2021
- Habr still lists №1308 as an ordinary item.
- The act is no longer current: Минцифры №773 от 16.09.2024, registered 21.10.2024 №79838, expressly repeals №1308; effective 02.11.2024.
- Initial №1308 identity/publication was previously verified; exact primary publication pointer for repealing №773 remains unresolved in this run, although official-publication date 22.10.2024 is corroborated by Rossiyskaya Gazeta and the registered text contains the repeal clause.
- Class: `HABR_REPEALED_ACT_CONFLICT`; successor: `ORDER_773_2024`.
- Source: https://rg.ru/documents/2024/10/23/mincifry-prikaz773-site-dok.html
- Registered text: https://minjust.consultant.ru/documents/53357

### 49. Минцифры №1312 от 07.12.2021
- Initial publication identity: registered 18.02.2022 №67348; official publication number `0001202202180016`.
- Current consolidated body must include BOTH later amendments: №523 от 07.06.2023 (registration №74183; point 4) and №979 от 13.11.2023 (registration №76392; point 5; effective 25.12.2023).
- A GitHub copy of the pristine 2021/2022 text is therefore `OLD_EDITION`, not current full text.
- Current secondary card: edition 13.11.2023; direct primary consolidated current-status card remains a blocker.
- Sources: https://base.garant.ru/403547538/ ; https://normativ.kontur.ru/document/1/462335-prikaz-mintsifry-rf-ot-07-12-2021-n-1312

### 50. ЦИК №86/715-8 от 08.06.2022
- Current working edition advanced to 24.06.2026.
- Amendments now include ЦИК №205/1583-8 от 23.07.2025 and №10/99-9 от 24.06.2026.
- №10/99-9 expressly amends the Requirements (including new p.1.12 and changes to p.2.1, 4.2, 4.6, 5.4, 6.2, 7.9) and orders official publication in the CEC Vestnik.
- Class: `CURRENT_EDITION_ADVANCED_2026`; old 2022 or 2025 copies are `OLD_EDITION`.
- Direct primary current consolidated CEC page was not resolved in this run; current edition is corroborated by the amendment text and current legal-system consolidation.
- Sources: https://www.consultant.ru/document/cons_doc_LAW_419319/92d969e26a4326c5d02fa79b8f9cf4994ee5633b/ ; https://pravo.ppt.ru/postanovlenie/tsik/n-10-99-9-342111

### 51. Минэкономразвития №624 от 15.11.2022
- Identity confirmed: registration 29.11.2022 №71202; official publication 29.11.2022; Habr title matches.
- Full text completeness = order + approved Requirements.
- No repeal/amendment confirmed in this batch; absence of a found repeal is not promoted to proof of current status.
- Class: `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.
- Agency copy: https://rospatent.gov.ru/ru/documents/prikaz-minekonomrazvitiya-624-15112022

### 52. Минцифры №611 / ФСО №96 от 12.07.2024
- Registration 19.08.2024 №79192; published on the official legal-information portal 20.08.2024; effective 31.08.2024.
- A staged layer activates exactly 01.09.2026: formats 2.7.1 (apps 1–2) apply only until 01.09.2026; transition to formats 3.0 (apps 4–5) begins 01.09.2026.
- `FULL_TEXT` completeness requires the Requirements and all appendices, including both old and new format sets plus refusal-reason appendix.
- Class: `STAGED_EFFECTIVE_LAYER_ACTIVATED_2026-09-01`.
- Source: https://rg.ru/documents/2024/08/22/prikaz611-96-site-dok.html

### 53. Минцифры №677 от 31.07.2024
- Identity/registration confirmed: Минюст №79322.
- Secondary current sources show effect from 10.09.2024; no repeal/amendment confirmed in this batch.
- Exact primary official-publication pointer and direct primary consolidated current-status card were not resolved.
- Class: `PRIMARY_PUBLICATION_POINTER_BLOCKER` + `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`.

### 54. Письмо Минцифры №П25-305029 от 17.09.2024
- This is a ministry letter with recommendations, not a registered normative legal act.
- Habr correctly labels it «Письмо», but it must be stored in a separate `NON_NPA_REFERENCE / RECOMMENDATION` layer and not mixed with NPA validity logic.
- A complete 4-page secondary copy exists with the letter and three recommendation blocks, but no GitHub copy and no direct official Ministry original were confirmed in this run.
- Class: `NON_NPA_MATERIAL`; blocker: `PRIMARY_MINISTRY_ORIGINAL_BLOCKER`.
- Secondary full copy: https://bft.ru/newspictures/15_%20%D0%BA%20%D0%BF.1.11_%D0%9F%D0%B8%D1%81%D1%8C%D0%BC%D0%BE%20%20%D0%9C%D0%B8%D0%BD%D1%86%D0%B8%D1%84%D1%80%D1%8B%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8%20%D0%BE%D1%82%2017_09_2024%20N%20%D0%9F25-305029_%D0%A0%D0%B5%D0%BA%D0%BE%D0%BC%D0%B5%D0%BD%20%D0%B3%D0%BE%D1%81%D1%81%D0%BB%D1%83%D0%B6%D0%B0%D1%89%D0%B8%D0%BC_%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%20%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF-%D1%82%D1%8C.pdf

### 55. Минцифры №1106 от 02.12.2025
- Registration confirmed: 19.05.2026 №86515; effective 31.05.2026.
- GitHub hit is only an educational HTML timeline that repeats the date/number/short description. It contains no operative clauses or Requirements; rejected as normative body.
- Full text completeness = order + approved Requirements.
- Habr links to a Ministry page, but direct Ministry fetch/current primary publication pointer remain unresolved in this run.
- Class: `GITHUB_MENTION_ONLY_REJECTED`; `PRIMARY_MINISTRY_DIRECT_FETCH_BLOCKER` / `PRIMARY_PUBLICATION_POINTER_BLOCKER`.
- Ministry URL as linked by Habr: https://digital.gov.ru/documents/prikaz-minczifry-rossii-%E2%84%96-1106-ob-utverzhdenii-trebovanij-k-obespecheniyu-informaczionnoj-bezopasnosti-v-ramkah-predostavleniya-oblachnyh-uslug-posredstvom-gosudarstvennoj-edinoj-oblachnoj-pla

## New counters

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +8`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `HABR_REPEALED_ACT_CONFLICT +1`
- `CURRENT_EDITION_ADVANCED_2026 +1`
- `STAGED_EFFECTIVE_LAYER_ACTIVATED_2026-09-01 +1`
- `NON_NPA_REFERENCE_CLASSIFIED +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## Gates added/confirmed

- `REFERENCE_OR_TIMELINE_MENTION != TARGET_NPA_BODY`
- `REGISTERED_BASE_TEXT + LATER_AMENDMENTS = CURRENT_BODY`
- `STAGED_FORMAT_TRANSITION_DATE != ACT_EXPIRY`
- `LETTER_IN_LEGISLATION_REFERENCE_LIST != NORMATIVE_LEGAL_ACT`
- `GITHUB_COPY_OFFICIAL_STATUS = NEVER_AUTOMATIC`

Next boundary: Habr subsection «Государственные и муниципальные информационные системы. СМЭВ» — Минкомсвязи №210/2015, then «ГосТех» (Указ №231/2023, распоряжение №3102-р/2022, ПП №2194/2022, №2338/2022), while continuing user-priority federal/PDn/information acts.