# Habr NPA sweep — Stream 1 — 2026-08-31 17:03 MSK

Scope: Habr 432466 block `Судебные тяжбы, компьютерная криминалистика`.

Targets: 144-ФЗ/1995; УПК РФ 174-ФЗ/2001; АПК РФ 95-ФЗ/2002; ГПК РФ 138-ФЗ/2002; КАС РФ 21-ФЗ/2015; СТО ФСБ КК 1-2018 `Компьютерная экспертиза. Термины и определения`.

## GitHub evidence

### 144-ФЗ
- repo: `El-Kh01/foiv-website`
- commit: `8d56ebf7a3564f53b1df99e2b33d833a3704617a`
- path: `foivs/fsb.html`
- size: `50144` bytes
- type: `HTML`
- blob: `4647fd48641690e29f186c2505133587b5a3a881`
- internal identity: exact bibliographic line `Федеральный закон "Об оперативно-розыскной деятельности" от 12.08.1995 N 144-ФЗ`.
- classification: `MENTION_ONLY / REFERENCE_PAGE / REJECTED_AS_NORMATIVE_BODY`.

### УПК РФ / 174-ФЗ
- repo: `ShaerWare/AI_Secretary_System`
- commit: `f77413909317db65c18fa577f8adea3965e4510c`
- path: `wiki-pages/ru-upk-rf/document__cons_doc_LAW_34481.md`
- size: `98889` bytes
- type: `Markdown`
- internal identity: exact title/date/number in header; edition `08.03.2026`, changes effective through `26.04.2026`.
- corpus is split across sibling `document__cons_doc_LAW_34481*.md` files.
- classification: `RELIABLE_SEGMENTED_FULL_TEXT_CANDIDATE / MULTIPART_CONSOLIDATED_CORPUS / SINGLE_FILE_NOT_FULL_TEXT / NONOFFICIAL_GITHUB_COPY`.
- current comparison: working consolidated edition is `26.07.2026`, latest confirmed amendment effective `06.08.2026`.
- status: `GITHUB_EDITION_STALE`.

### АПК РФ / 95-ФЗ
- repo: `SergSi/EXPERT`
- commit: `7b6cc83b69d251a1ff53c4d6dc15c5b854e8961e`
- path: `NORMATIVE/АПК РФ.txt`
- size: `884326` bytes
- type: `TXT`
- blob: `8e8ebefacd527cc0f42b9215b630dbf2db50b808`
- body check: reaches Article 332 and terminal signature.
- terminal identity: `Арбитражный процессуальный кодекс Российской Федерации`, `24 июля 2002 года`, `N 95-ФЗ` all present.
- terminal source marker: `01.05.2026 / Система ГАРАНТ / 206/206`.
- classification: `RELIABLE_FULL_BODY_CANDIDATE / NUMBER_DATE_TITLE_TERMINAL_VERIFIED / SOURCE_SNAPSHOT_2026-05-01 / NONOFFICIAL_GITHUB_COPY`.
- do not infer current status from snapshot alone; currentness is checked separately.

### ГПК РФ / 138-ФЗ
- repo: `SergSi/EXPERT`
- commit: `7b6cc83b69d251a1ff53c4d6dc15c5b854e8961e`
- path: `NORMATIVE/ГПК РФ.txt`
- size: `1349252` bytes
- type: `TXT`
- blob: `9d2a5028dd975849a0189612d9e6c982a7da4d30`
- blocker: metadata is present, but connector body fetch did not yield usable text for internal number/date/title verification.
- classification: `LARGE_GITHUB_CANDIDATE / FETCH_OR_ENCODING_IDENTITY_BLOCKER / NOT_PROMOTED_TO_RELIABLE_FULL_TEXT`.

### КАС РФ / 21-ФЗ
- repo: `SergSi/EXPERT`
- commit: `7b6cc83b69d251a1ff53c4d6dc15c5b854e8961e`
- path: `NORMATIVE/КАС РФ.txt`
- size: `921551` bytes
- type: `TXT`
- blob: `a1fe7002102d2d0bb00be05ed341038d5528f4a9`
- body check: reaches Article 365 and terminal signature.
- terminal identity: `Кодекс административного судопроизводства Российской Федерации`, `8 марта 2015 г.`, `N 21-ФЗ` all present.
- terminal source marker: `01.05.2026 / Система ГАРАНТ / 147/147`.
- classification: `RELIABLE_FULL_BODY_CANDIDATE / NUMBER_DATE_TITLE_TERMINAL_VERIFIED / SOURCE_SNAPSHOT_2026-05-01 / NONOFFICIAL_GITHUB_COPY`.

### СТО ФСБ КК 1-2018
- exact GitHub searches by identifier/title: no usable candidate.
- normalized GitHub fields: `repo=null / commit=null / path=null / size=null / type=null`.
- official FSB web index corroborates identifier/title and posting date 13.12.2018.
- classification outside GitHub: `PRIMARY_OFFICIAL_FSB_HOSTING_CONFIRMED / STANDARD_OR_METHODOLOGICAL_DOCUMENT`.
- no Minjust/official legal-publication status established; `PRIMARY_NPA_STATUS_BLOCKER`.

## Current/official status layer — independent of GitHub

- `144-ФЗ`: consolidated sources show red. `01.04.2025`; 41-ФЗ/2025 official publication is corroborated as `0001202504010010`. Direct primary current consolidated card unresolved: `PRIMARY_CURRENT_STATUS_BLOCKER`.
- `УПК РФ`: 251-ФЗ/2026 changes Articles 31 and 151; effective `06.08.2026`; current working red. `26.07.2026`. GitHub red. `08.03.2026` is stale. Primary publication card for 251-ФЗ unresolved in this pass.
- `АПК РФ`: current working red. `15.12.2025`, changes effective `01.01.2026`; 485-ФЗ/2025 changes АПК РФ, official publication number corroborated as `0001202512150050`.
- `ГПК РФ`: current effective layer on `31.08.2026` is red. `04.07.2026`; 223-ФЗ/2026 amended Article 29, effective `15.07.2026`, publication number corroborated as `0001202607040011`. 333-ФЗ/2026 creates a further enacted change effective `01.09.2026`: `CURRENT_EFFECTIVE_BODY_2026-08-31 + ENACTED_FUTURE_CHANGE_2026-09-01`.
- `КАС РФ`: current working red. `09.04.2026`; 79-ФЗ/2026 changes КАС РФ and is effective `10.05.2026`; official publication ID `0001202604090006`.
- `СТО ФСБ КК 1-2018`: official FSB hosting does not automatically establish registered NPA status.

## New counters
- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +3`
- `GITHUB_MENTION_ONLY_REJECTED +1`
- `LARGE_GITHUB_IDENTITY_BLOCKER +1`
- `GITHUB_FULL_TEXT_BLOCKER +6`
- `GITHUB_EDITION_STALE +1`
- `ENACTED_FUTURE_CHANGE +1`
- `PRIMARY_OFFICIAL_STANDARD_HOSTING_CONFIRMED +1`
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`

## New gates
- `SEGMENTED_CORPUS != SINGLE_FILE_FULL_TEXT`
- `NUMBER_DATE_TITLE_IDENTITY_VERIFIED != CURRENTNESS_VERIFIED`
- `LARGE_FILE_PRESENT != BODY_VERIFIED`
- `GITHUB_FULL_BODY_SHAPE != OFFICIAL_SOURCE`
- `PREPARED_TOMORROW_CONSOLIDATION != CURRENT_EFFECTIVE_BODY_TODAY`
- `OFFICIAL_REGULATOR_HOSTING != REGISTERED_NPA_STATUS`

## Next priority boundary
Continue Habr with higher-priority federal law / Government / Roskomnadzor material: 98-ФЗ `О коммерческой тайне`, 395-1 `О банках и банковской деятельности`, 224-ФЗ on insider information, then `Защита связи`: 176-ФЗ, 126-ФЗ, PP RF 538/2005, 532/2009 and current Roskomnadzor acts.
