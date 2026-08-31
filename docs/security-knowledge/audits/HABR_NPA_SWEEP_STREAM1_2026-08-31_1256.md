# Habr NPA sweep — Stream 1 — 2026-08-31 12:56 MSK

## Scope

Continued the systematic pass over Habr article 432466, section **«Лицензирование деятельности в области информационной безопасности»**, positions 8–14:

1. Постановление Правительства РФ от 16.04.2012 № 314.
2. Перечень нормативных правовых актов / методических документов / национальных стандартов for licensing under PP RF №79.
3. Перечень контрольно-измерительного и испытательного оборудования / средств контроля эффективности защиты for licensing under PP RF №79.
4. Информационное сообщение ФСТЭК России от 26.03.2015 № 240/13/1139.
5. Приказ ФСБ России от 31.01.2022 № 35.
6. Приказ ФСТЭК России от 28.12.2021 № 206.
7. Приказ ФСТЭК России от 28.12.2021 № 207.

Method: GitHub body discovery is separated from legal status verification. A GitHub copy is never treated as official merely because it is hosted on GitHub.

## GitHub body search

Exact searches were run by number/date/title and distinctive title fragments. No normative body or reliable body candidate was found for any of the seven targets.

| Target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| PP RF №314/2012 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEC PP79 normative/methodical list | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEC PP79 equipment list | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEC message №240/13/1139 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSB order №35/2022 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEC order №206/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| FSTEC order №207/2021 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

Counters for GitHub discovery in this batch:

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +7`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## New confirmed findings

### PP RF №314 of 16.04.2012

Identity is stable: the act approves the Regulation on licensing activity involving detection of electronic devices intended for covert acquisition of information.

Current consolidated legal sources reproduce edition **03.02.2023** and show amendments by PP RF №2198/2020, №2518/2021 and №159/2023. No later repeal/amendment was confirmed in this pass.

Evidence level:

- `CURRENT_STATUS_CORROBORATED_NONPRIMARY`
- `PRIMARY_CURRENT_STATUS_BLOCKER`

Completeness rule for a future GitHub candidate:

`FULL_TEXT = resolution body + complete current appended Regulation`.

A file containing only the operative clauses of the resolution is `PARTIAL_TEXT`.

### FSTEC list of NPA/methodical documents/national standards for PP RF №79

A same-scope **10.12.2024** edition is referenced by the 2026 mandatory-requirements materials and by FSTEC information material №240/13/6597 dated 26.12.2024. The FSTEC legacy attachment link used from Habr resolves through an old `/component/attachments/download/...` URL and did not provide enough evidence that Habr points to the current edition.

Official FSTEC current-page pointer discovered:

`https://fstec.ru/dokumenty/vse-dokumenty/perechni/perechen-normativnykh-pravovykh-aktov-metodicheskikh-dokumentov-i-natsionalnykh-standartov-ot-10-dekabrya-2024-g`

Direct fetch of that FSTEC page timed out in this pass.

Classification:

- `CURRENT_VERSION_2024_CORROBORATED`
- `HABR_UNVERSIONED_OR_STALE_LINK_BLOCKER`
- `PRIMARY_DIRECT_FETCH_BLOCKER`

The list may reference documents carrying restricted markings. Restricted underlying materials are not sought merely to satisfy completeness of the public index.

### FSTEC PP RF №79 equipment list — major 2026 update

A new edition of the equipment / protection-effectiveness-control list was approved **10.08.2026**. Multiple legal/industry sources point to the FSTEC publication and to FSTEC information message №240/13/5521 of 11.08.2026.

Official FSTEC pointers discovered:

- `https://fstec.ru/dokumenty/vse-dokumenty/perechni/perechen-kontrolno-izmeritelnogo-i-ispytatelnogo-oborudovaniya-sredstv-kontrolya-effektivnosti-zashchity-informatsii-ot-10-avgusta-2026-g`
- `https://fstec.ru/dokumenty/vse-dokumenty/informatsionnye-i-analiticheskie-materialy/informatsionnoe-soobshchenie-fstek-rossii-ot-11-avgusta-2026-g-n-240-13-5521`

Transition dates found:

- for **licence applicants**: new lists apply from **01.12.2026**;
- for **existing licensees**: equipment must be brought into compliance by **01.03.2027**.

The previous widely cited PP79 equipment list is dated **19.04.2017**. Habr's FSTEC link resolves to a legacy attachment URL (`/component/attachments/download/354`), not to the newly dated 2026 page.

Classification as of 2026-08-31:

- `APPROVED_NEW_VERSION_WITH_STAGED_APPLICABILITY`
- `HABR_STALE_OR_UNVERSIONED_ATTACHMENT_CONFLICT`
- `FORMAL_SUPERSESSION_CLAUSE_PRIMARY_FETCH_BLOCKER`

Do **not** flatten this to `old list repealed on 10.08.2026`: approval date, applicant effective date and transition deadline for existing licensees are different legal/operational events.

### FSTEC information message №240/13/1139 of 26.03.2015

A full accessible non-GitHub copy was found, including the appendix with typical errors in applications and attached documents.

This is an **information/explanatory material**, not automatically a registered NPA. Its text is tied to licensing procedures and administrative regulations of the period; no formal repeal was found, but current substantive relevance cannot be assumed after subsequent licensing reforms.

Classification:

- `NON_NPA_INFORMATIONAL_MATERIAL`
- `CURRENT_GUIDANCE_RELEVANCE_BLOCKER`

Gate: `INFORMATIONAL_MESSAGE != REGISTERED_NPA`.

### FSB order №35 of 31.01.2022 — latest amendment confirmed by primary official source

The key new lifecycle event is **FSB order №479 of 16.11.2024**, registered by Minjust **03.12.2024 №80446**, official publication number **0001202412040003**, published **04.12.2024**.

Primary official source:

`https://publication.pravo.gov.ru/document/0001202412040003`

Order №479 explicitly amends FSB order №35 and expands/changes its forms. Consolidated copies show that the current body after this amendment contains forms/applications **1–23**, not only the earlier 1–15 set.

Classification:

- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`
- `BASE_ORDER_PLUS_OLD_APPENDICES != CURRENT_FULL_TEXT_AFTER_AMENDMENT`

Completeness rule:

`FULL_TEXT = order №35 in current edition + all current forms/applications 1–23`.

A copy containing only forms 1–15 is `OLD_EDITION_OR_PARTIAL`.

### FSTEC order №206 of 28.12.2021

Primary official publication is confirmed from the official publication register:

- Minjust registration: **28.02.2022 №67507**
- publication number: **0001202202280047**
- publication date: **28.02.2022**
- official PDF size in register: **351 KB / 8 pages**

The 2026 mandatory-requirements list for technical protection of confidential information still cites order №206, corroborating current applicability. No repeal was found.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`
- `CURRENT_APPLICABILITY_CORROBORATED_BY_2026_REQUIREMENTS_LIST`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`

Completeness rule: order + complete evaluation-sheet form. Bare operative text is `PARTIAL_TEXT`.

### FSTEC order №207 of 28.12.2021

Primary official publication is directly confirmed:

- Minjust registration: **28.02.2022 №67506**
- publication number: **0001202202280035**
- publication date: **28.02.2022**
- official PDF size in register: **382 KB / 9 pages**

Primary source:

`https://publication.pravo.gov.ru/document/0001202202280035`

The 2026 mandatory-requirements list for development/production of confidential-information protection tools still cites order №207. No repeal was found.

Classification:

- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED`
- `CURRENT_APPLICABILITY_CORROBORATED_BY_2026_REQUIREMENTS_LIST`
- `PRIMARY_CONSOLIDATED_CURRENT_STATUS_BLOCKER`

Completeness rule: order + complete evaluation-sheet form.

## New gates added

1. `NEW_FSTEC_LIST_APPROVAL != SAME_EFFECTIVE_DATE_FOR_APPLICANTS_AND_EXISTING_LICENSEES`
2. `OFFICIAL_SITE_LEGACY_ATTACHMENT_LINK != CURRENT_VERSION`
3. `INFORMATIONAL_MESSAGE != REGISTERED_NPA`
4. `CURRENT_MANDATORY_REQUIREMENTS_LIST_CORROBORATION != PRIMARY_CONSOLIDATED_STATUS`
5. `BASE_ORDER_PLUS_OLD_APPENDICES != CURRENT_FULL_TEXT_AFTER_AMENDMENT`
6. `APPROVAL_DATE != TRANSITION_COMPLETION_DATE`

## New-event counters

- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` — FSTEC №206, №207.
- `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED +1` — FSB №35 via №479/2024.
- `APPROVED_NEW_FSTEC_LIST_WITH_STAGED_APPLICABILITY +1` — PP79 equipment list 10.08.2026.
- `HABR_STALE_OR_UNVERSIONED_ATTACHMENT_CONFLICT +1` — PP79 equipment list link.
- `HABR_UNVERSIONED_OR_STALE_LINK_BLOCKER +1` — PP79 NPA/methodical list.
- `NON_NPA_INFORMATIONAL_MATERIAL +1` — №240/13/1139.
- `CURRENT_GUIDANCE_RELEVANCE_BLOCKER +1`.
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`.
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`.

## Next queue boundary

Continue licensing section positions 15–22:

- FSTEC order №226/2022;
- FSTEC order №3/2023;
- FSTEC order №4/2023;
- FSB order №142/2023;
- FSTEC orders №163/2025 and №164/2025;
- FSTEC information message №240/13/3384;
- FSTEC material/order referenced by Habr as №483/2025.

Then move to the next Habr section on information security / personal data while also reconciling the user's separate NPA list.
