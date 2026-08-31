# Habr NPA sweep — Stream 1 — 2026-08-31 08:52 MSK

## Scope
Continuation of the systematic review of Habr 432466 (`Техническое регулирование`), targets:

1. Federal Law 27.12.2002 No. 184-FZ — `О техническом регулировании`.
2. Federal Law 26.06.2008 No. 102-FZ — `Об обеспечении единства измерений`.
3. Federal Law 29.06.2015 No. 162-FZ — `О стандартизации в Российской Федерации`.
4. Government Resolution 30.12.2016 No. 1567 — defence/security standardization.
5. Ministry of Digital Development Order 22.09.2020 No. 486 — software/database classifier.

Habr reference: https://habr.com/ru/articles/432466/

## GitHub normative-body search

Exact number/date/title searches and broader title-fragment searches were performed for all five targets. No full normative body and no reliable normative-body candidate was found.

| target | repo | commit | path | size | type | classification |
|---|---|---|---|---:|---|---|
| 184-FZ/2002 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| 102-FZ/2008 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| 162-FZ/2015 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP 1567/2016 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| Order 486/2020 | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

### Rejected GitHub hit — 184-FZ

A search hit was found in a public repository, but inspection proves it is a website reference page rather than the law body:

- repo: `AxHulk/osp-kavkaz-ing`
- commit: `b902d3e57875c53d2c284e3e257fefc7f8d5e9e9`
- path: `src/pages/Accreditation.tsx`
- blob SHA: `019eb2fb8c4e15d46859ff2a43c58517b56bfbd8`
- size: `174314` bytes
- type: `TSX / React source page`
- classification: `MENTION_ONLY / REFERENCE_PAGE / REJECTED_AS_NORMATIVE_BODY`

The file is an accreditation website page for an organization and only cites legal acts among its reference materials. It is neither a full text nor a reliable full-text candidate. Target-level `repo/commit/path/size/type` therefore remain null.

No new GitHub full-body duplicate and no body identity conflict was found in this batch.

## New confirmed lifecycle/current-edition evidence

### Federal Law No. 184-FZ of 27.12.2002

Habr identity is correct, but the temporal state requires provision-level handling.

As of **2026-08-31**, Federal Law No. 126-FZ of 02.05.2026 has been enacted but has **not yet entered into force**. It enters into force on **2026-09-01** and repeals point 15 of article 46 of 184-FZ. The official-publication pointer previously resolved for No. 126-FZ is `0001202605020011`; the law is also officially published in `Российская газета` and its effective date is explicit in article 5.

Federal Law No. 331-FZ of 04.08.2026 directly amends 184-FZ in article 3, but its relevant main layer enters into force only on **2027-03-01**. Corroborated official-publication pointer: `0001202608040074`, published 04.08.2026.

Therefore the corpus must keep separately:

- `CURRENT_EFFECTIVE_BODY_2026-08-31`;
- `ENACTED_FUTURE_CHANGE_2026-09-01` (126-FZ);
- `ENACTED_FUTURE_CHANGE_2027-03-01` (331-FZ).

A consolidated copy that already incorporates those future amendments must not silently be treated as the currently effective body.

Status/gate: `PREPARED_OR_FUTURE_CONSOLIDATED_EDITION != CURRENT_EFFECTIVE_BODY`.

### Federal Law No. 102-FZ of 26.06.2008

Current consolidated legal systems identify edition **08.08.2024**, with amendments/additions whose staged commencement is completed through **01.01.2026**.

Primary publication of Federal Law No. 18-FZ of 14.02.2024, which directly amends 102-FZ, is confirmed on the official legal-publication portal:

- publication No. `0001202402140015`;
- publication date `14.02.2024`.

The later Federal Law No. 232-FZ of 08.08.2024 also directly changes 102-FZ (including article 3.1). Its official publication metadata are corroborated as:

- publication No. `0001202408080042`;
- publication date `08.08.2024`.

As of 2026-08-31 no later amendment to the target body was confirmed in this pass. This is not upgraded to a primary consolidated-current-text claim because the official publication portal proves promulgation of amending acts, not a continuously consolidated target text.

Status: `CURRENT_CONSOLIDATED_EDITION_2024-08-08_CORROBORATED / PRIMARY_AMENDMENT_PUBLICATIONS_CONFIRMED`.

### Federal Law No. 162-FZ of 29.06.2015

Primary identity is directly confirmed:

- official publication No. `0001201506300047`;
- publication date `30.06.2015`;
- title exactly `О стандартизации в Российской Федерации`.

Current consolidated legal systems identify edition **04.08.2026**.

Federal Law No. 330-FZ of 04.08.2026 directly amends 162-FZ; the official publication number is corroborated as `0001202608040075`. The official `Российская газета` text confirms the law, signing date 04.08.2026 and its effective-date structure. The target amendment effective on signature/publication is already part of the 2026-08-31 current layer.

Status: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_EDITION_2026-08-04_CORROBORATED / LATEST_AMENDMENT_330-FZ_CONFIRMED`.

### Government Resolution No. 1567 of 30.12.2016

Current consolidated edition is **12.03.2024**, with changes made by Government Resolution No. 295 of 12.03.2024. Corroborated official publication pointer for No. 295: `0001202403150011`, publication date 15.03.2024. The current consolidated text explicitly lists No. 295 among the amending acts.

Completeness has a special restriction: No. 1567 approves **two Regulations**, and the first Regulation contains section **XII `Для служебного пользования`**. The sweep must not seek, reconstruct, ingest, or expose restricted content merely to satisfy a full-text metric.

Accordingly any open GitHub/public copy can at most be classified:

`PUBLIC_BODY_EXCLUDING_RESTRICTED_SECTION`

and cannot be promoted to `FULL_NORMATIVE_BODY` while a non-public DСП section is part of the legally approved structure.

New blocker/gate: `PUBLIC_OPEN_SECTIONS_COMPLETE != FULL_NORMATIVE_BODY_WHEN_RESTRICTED_SECTION_EXISTS` and `DO_NOT_SEEK_RESTRICTED_CONTENT_TO_SATISFY_COMPLETENESS`.

### Ministry of Digital Development Order No. 486 of 22.09.2020

Primary identity is directly confirmed on the official legal-publication portal:

- publication No. `0001202010290057`;
- publication date `29.10.2020`;
- Ministry of Justice registration No. `60646` dated 29.10.2020;
- exact title `Об утверждении классификатора программ для электронных вычислительных машин и баз данных`.

Latest confirmed amendment is Ministry of Digital Development Order No. 1041 of 04.12.2023:

- registered by Ministry of Justice 11.03.2024 No. `77464`;
- official publication No. `0001202403110026` dated 11.03.2024;
- entered into force **22.03.2024**;
- directly amends the classifier approved by Order No. 486.

Current consolidated edition is therefore `04.12.2023`, effective with No. 1041 from 22.03.2024.

Completeness gate: `FULL_TEXT` requires the order shell **plus the entire classifier**, not merely the information-security class referenced in Habr or one classifier section. A one-class extract is `PARTIAL_TEXT`.

## New counts

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +5`
- `MENTION_ONLY_REJECTED +1` (184-FZ website reference page)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `ENACTED_FUTURE_CHANGE +2` (184-FZ: 01.09.2026 and 01.03.2027)
- `RESTRICTED_SECTION_COMPLETENESS_BLOCKER +1` (PP 1567)
- `PRIMARY_INITIAL_PUBLICATION_CONFIRMED +2` (162-FZ, Order 486)
- `PRIMARY_AMENDMENT_PUBLICATION_CONFIRMED +3` (102-FZ via 18-FZ/232-FZ; PP 1567 via PP 295; Order 486 via Order 1041)
- `HABR_NEW_TITLE_OR_REPEAL_CONFLICT +0`

## New corpus gates

1. `PREPARED_OR_FUTURE_CONSOLIDATED_EDITION != CURRENT_EFFECTIVE_BODY`.
2. `PRIMARY_PUBLICATION_OF_AMENDING_ACT != PRIMARY_CONSOLIDATED_CURRENT_TEXT`.
3. `PUBLIC_OPEN_SECTIONS_COMPLETE != FULL_NORMATIVE_BODY_WHEN_RESTRICTED_SECTION_EXISTS`.
4. `DO_NOT_SEEK_RESTRICTED_CONTENT_TO_SATISFY_COMPLETENESS`.
5. `CLASSIFIER_FULLTEXT = ORDER_SHELL + ALL_CLASSIFIER_SECTIONS`.
6. `SINGLE_REFERENCED_CLASSIFIER_CATEGORY = PARTIAL_TEXT`.
7. `GITHUB_REFERENCE_PAGE_WITH_NPA_CITATION = MENTION_ONLY`, even if repo/path/commit/size are fully known.

## Next queue

Continue after `Техническое регулирование` into `Техническое регулирование. Сертификация средств защиты информации`, re-counting already closed targets only when a new GitHub body, new primary lifecycle evidence, amendment/repeal, or current-edition change appears.
