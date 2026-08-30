# Habr NPA sweep — Stream 1 — 2026-08-30 19:51 MSK

Scope: Habr 432466, section `Персональные данные. Особые случаи обработки ПДн`, items 12–18. Item 14 (125-ФЗ) was already processed and was not repeated. This pass covers 177-ФЗ, 79-ФЗ, 402-ФЗ, 230-ФЗ, 168-ФЗ and PP RF №1723/2021.

## GitHub search gate

Exact/title searches were run through GitHub code search for each target. No indexed full-text target body and no reliable body candidate were returned.

| Target | GitHub query | repo | commit | path | size | type | result |
|---|---|---|---|---|---:|---|---|
| 177-ФЗ 23.12.2003 | `177-ФЗ 23.12.2003 страховании вкладов физических лиц банках Российской Федерации` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| 79-ФЗ 27.07.2004 | `79-ФЗ 27.07.2004 государственной гражданской службе Российской Федерации` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| 402-ФЗ 06.12.2011 | `402-ФЗ 06.12.2011 О бухгалтерском учете` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| 230-ФЗ 03.07.2016 | `230-ФЗ 03.07.2016 защите прав законных интересов физических лиц возврат просроченной задолженности` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| 168-ФЗ 08.06.2020 | `168-ФЗ 08.06.2020 единый федеральный информационный регистр населении` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |
| PP RF №1723 09.10.2021 | `1723 09.10.2021 единый федеральный информационный регистр населении персональных данных` | null | null | null | null | null | GITHUB_FULL_TEXT_BLOCKER |

No new GitHub duplicate/reference-only artifact was found in this batch. No target-body identity conflict was found because no candidate body reached the identity gate.

## New confirmed findings

### 177-ФЗ of 23.12.2003

Habr 432466 still gives the historical title `О страховании вкладов физических лиц в банках Российской Федерации`. Current consolidated sources use `О страховании вкладов в банках Российской Федерации`. Federal Law №347-ФЗ of 31.07.2025 itself identifies the target as `Федеральный закон от 23 декабря 2003 года №177-ФЗ "О страховании вкладов в банках Российской Федерации"`.

Primary official publication list: Federal Law №347-ФЗ, publication number `0001202507310113`, published 31.07.2025, PDF 334 KB / 7 pages. The amendment entered into force 30.10.2025. Current consolidated edition of 177-ФЗ: 31.07.2025; later provisions are shown as effective through 14.12.2025.

Classification: `HABR_STALE_TITLE_CONFLICT`, `CURRENT_EDITION_CORROBORATED_2025-07-31`, `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`, `GITHUB_FULL_TEXT_BLOCKER`.

Primary/strong sources:
- https://publication.pravo.gov.ru/ (official list entry №347-ФЗ / `0001202507310113`)
- https://government.ru/docs/all/160275/
- https://www.consultant.ru/document/cons_doc_LAW_45769/

### 79-ФЗ of 27.07.2004

Current consolidated edition is 08.03.2026. Federal Law №52-ФЗ of 08.03.2026 directly amends part 5 of article 15 of 79-ФЗ, introducing mandatory state fingerprint and genomic registration in cases established by federal laws. It entered into force 07.06.2026.

Primary official publication: `0001202603080008`, published 08.03.2026, PDF 486 KB / 10 pages.

Classification: `CURRENT_EDITION_CORROBORATED_2026-03-08`, `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`, `GITHUB_FULL_TEXT_BLOCKER`.

Primary/strong sources:
- https://publication.pravo.gov.ru/document/0001202603080008
- https://www.consultant.ru/document/cons_doc_LAW_528314/
- https://www.consultant.ru/document/cons_doc_LAW_48601/

### 402-ФЗ of 06.12.2011

Current effective consolidated edition is 15.12.2025. Federal Law №471-ФЗ of 15.12.2025 directly changes 402-ФЗ, including articles 16 and 18. Official publication list confirms `0001202512150036`, 15.12.2025, PDF 1002 KB / 20 pages.

A separate enacted future state exists: Federal Law №263-ФЗ of 23.07.2025 changes article 21 of 402-ФЗ and starts on 01.01.2027. Official publication: `0001202507230068`, 23.07.2025, PDF 135 KB / 3 pages.

Classification: `CURRENT_EDITION_CORROBORATED_2025-12-15`, `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`, `ENACTED_FUTURE_CHANGE_2027-01-01`, `GITHUB_FULL_TEXT_BLOCKER`.

Primary/strong sources:
- https://publication.pravo.gov.ru/ (official list entry №471-ФЗ / `0001202512150036`)
- https://publication.pravo.gov.ru/ (official list entry №263-ФЗ / `0001202507230068`)
- https://www.ipbr.org/about/news/2025/12/29/minfin/

### 230-ФЗ of 03.07.2016

Current consolidated edition is 31.07.2025. Article 61 of Federal Law №304-ФЗ directly changes 230-ФЗ. №304-ФЗ generally entered into force 01.03.2026; official publication list confirms №304-ФЗ as `0001202507310080`, published 31.07.2025, PDF 18770 KB / 382 pages.

There is already an enacted future change: Federal Law №20-ФЗ of 11.02.2026 changes article 17.1 of 230-ФЗ and enters into force 01.09.2026. The official daily list shows the publication number for №20-ФЗ as `0001202602110015`. A previously recorded `0001202602110016` value belongs to the adjacent entry and is incorrect for №20-ФЗ; corpus metadata must be corrected.

Classification: `CURRENT_EDITION_CORROBORATED_2025-07-31`, `PRIMARY_AMENDING_ACT_PUBLICATION_CONFIRMED`, `ENACTED_FUTURE_CHANGE_2026-09-01`, `PUBLICATION_ID_CORRECTION_20-FZ:0016->0015`, `GITHUB_FULL_TEXT_BLOCKER`.

Primary/strong sources:
- https://publication.pravo.gov.ru/ (official list entry №304-ФЗ / `0001202507310080`)
- https://publication.pravo.gov.ru/documents?date=11.02.2026&periodType=day (official list entry №20-ФЗ / `0001202602110015`)
- https://www.consultant.ru/document/cons_doc_LAW_200497/

### 168-ФЗ of 08.06.2020

Current consolidated edition is 28.11.2025. Federal Law №442-ФЗ of 28.11.2025 directly changes articles 4 and 11 of 168-ФЗ and entered into force 28.05.2026 after the 180-day deferred period.

Primary official publication list: `0001202511280105`, published 28.11.2025, PDF 185 KB / 4 pages.

Classification: `CURRENT_EDITION_CORROBORATED_2025-11-28`, `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`, `EFFECTIVE_FROM_2026-05-28`, `GITHUB_FULL_TEXT_BLOCKER`.

Primary/strong sources:
- https://publication.pravo.gov.ru/ (official list entry №442-ФЗ / `0001202511280105`)
- https://rg.ru/documents/2025/12/08/fz442-dok.html
- https://www.consultant.ru/document/cons_doc_LAW_354474/

### PP RF №1723 of 09.10.2021

Queue metadata correction: the target date is `09.10.2021`, exactly as stated by Habr; a prior planning note had `11.10.2021` and must not be propagated.

Current consolidated edition is 28.05.2026. PP RF №612 of 28.05.2026 directly changes №1723. Clause 3 of №612 ties its entry into force to Federal Law №442-ФЗ; №442-ФЗ entered into force 28.05.2026, therefore the №612 amendments are already part of the current effective body as of 30.08.2026.

The full amendment body and identity are corroborated by current legal-text sources, but a stable direct official publication card/publication number for PP №612 was not resolved in this pass. Therefore do not mark its publication event as primary-verified yet.

Classification: `CURRENT_EDITION_CORROBORATED_2026-05-28`, `LATEST_AMENDMENT_RELATION_CONFIRMED`, `PRIMARY_PUBLICATION_ID_BLOCKER_PP612`, `QUEUE_METADATA_CORRECTION_1723_DATE:11.10->09.10`, `GITHUB_FULL_TEXT_BLOCKER`.

Strong sources:
- https://www.consultant.ru/document/cons_doc_LAW_535299/
- https://www.consultant.ru/document/cons_doc_LAW_535299/92d969e26a4326c5d02fa79b8f9cf4994ee5633b/
- https://www.consultant.ru/document/cons_doc_LAW_354474/

## New corpus gates / corrections

1. `TITLE_IS_TEMPORAL_METADATA`: the act number/date can remain identical while the legal title changes; Habr title must be freshness-checked (177-ФЗ).
2. `OFFICIAL_LIST_ENTRY_OVERRIDES_DERIVED_PUBLICATION_ID`: publication IDs are accepted from the official portal list over mirrors/previous notes; corrected №20-ФЗ to `0001202602110015`.
3. `AMENDMENT_EFFECTIVE_DATE_CAN_BE_DERIVED_BY_CROSS_ACT_REFERENCE`: PP №612 points to the effective date of №442-ФЗ, so the two lifecycle records must be linked rather than storing an ungrounded date.
4. `CURRENT_EFFECTIVE_BODY != ENACTED_FUTURE_BODY`: 230-ФЗ has a current 31.07.2025 edition plus an already enacted change effective 01.09.2026; 402-ФЗ has a future state effective 01.01.2027.
5. `QUEUE_METADATA_MUST_PASS_IDENTITY_GATE`: PP №1723 date corrected to 09.10.2021 before corpus ingestion.

## Counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `NEW_GITHUB_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `HABR_STALE_TITLE_CONFLICT +1`
- `PRIMARY_LATEST/AMENDING_PUBLICATION_CONFIRMED +5`
- `ENACTED_FUTURE_CHANGE +2`
- `PUBLICATION_ID_CORRECTION +1`
- `QUEUE_METADATA_CORRECTION +1`
- `PRIMARY_PUBLICATION_ID_BLOCKER +1` (PP №612)

## Next queue

Continue without repeating closed items. Next relevant federal/general PDn block after Habr special-cases: storage and operator-internal documents, prioritizing Rosarchiv №236/2019, №142/2021, №77/2023, RKN recommendations of 27.07.2017 and RKN order №201/2022; classify methodological/recommendation material separately from NPA.