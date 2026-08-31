# Habr NPA sweep — Stream 1 — 2026-08-31 17:03 MSK

Scope: continue Habr 432466 systematic sweep, current block `Судебные тяжбы, компьютерная криминалистика`.

Targets checked:
1. Federal Law 12.08.1995 N 144-FZ `Об оперативно-розыскной деятельности`.
2. Criminal Procedure Code RF, Federal Law 18.12.2001 N 174-FZ.
3. Arbitration Procedure Code RF, Federal Law 24.07.2002 N 95-FZ.
4. Civil Procedure Code RF, Federal Law 14.11.2002 N 138-FZ.
5. Code of Administrative Court Procedure RF, Federal Law 08.03.2015 N 21-FZ.
6. STO.FSB.KK 1-2018 `Компьютерная экспертиза. Термины и определения`.

## New GitHub evidence

### 144-FZ
- repo: `El-Kh01/foiv-website`
- commit: `8d56ebf7a3564f53b1df99e2b33d833a3704617a`
- path: `foivs/fsb.html`
- size: `50144` bytes
- type: `HTML`
- blob: `4647fd48641690e29f186c2505133587b5a3a881`
- in-document identity: page explicitly lists `Федеральный закон "Об оперативно-розыскной деятельности" от 12.08.1995 N 144-ФЗ`.
- classification: `MENTION_ONLY / REFERENCE_PAGE / REJECTED_AS_NORMATIVE_BODY`.
- reason: FSB reference webpage; it does not contain the full statutory body.

### UPK RF / 174-FZ
- repo: `ShaerWare/AI_Secretary_System`
- commit: `f77413909317db65c18fa577f8adea3965e4510c`
- path: `wiki-pages/ru-upk-rf/document__cons_doc_LAW_34481.md`
- size: `98889` bytes
- type: `Markdown`
- in-document identity: exact header says `Уголовно-процессуальный кодекс Российской Федерации от 18.12.2001 N 174-ФЗ (ред. от 08.03.2026) ...`.
- corpus structure: document is split across sibling `document__cons_doc_LAW_34481*.md` files.
- classification: `RELIABLE_SEGMENTED_FULL_TEXT_CANDIDATE / MULTIPART_CONSOLIDATED_CORPUS / SINGLE_FILE_NOT_FULL_TEXT / NONOFFICIAL_GITHUB_COPY`.
- freshness: GitHub snapshot is `red. 08.03.2026`; current working consolidated edition is later (`26.07.2026`, amendments effective from `06.08.2026`).
- status: `GITHUB_EDITION_STALE`.

### APK RF / 95-FZ
- repo: `SergSi/EXPERT`
- commit: `7b6cc83b69d251a1ff53c4d6dc15c5b854e8961e`
- path: `NORMATIVE/АПК РФ.txt`
- size: `887142` bytes
- type: `TXT`
- blob: `54f741ed854c5eb9018685a5c247fe8b6a19deb7`
- body check: file proceeds through Article 332 and terminates with `Президент Российской Федерации В.Путин / Москва, Кремль / 24 июля 2002 года / N 95-ФЗ`.
- identity check: number/date terminal verified; literal full title was not exposed in fetched portions.
- classification: `RELIABLE_FULL_BODY_CANDIDATE / NUMBER_DATE_TERMINAL_VERIFIED / TITLE_LITERAL_CHECK_BLOCKER / NONOFFICIAL_GITHUB_COPY`.
- edition date inside fetched portions not reliably resolved; do not classify as current automatically.

### GPK RF / 138-FZ
- repo: `SergSi/EXPERT`
- commit: `7b6cc83b69d251a1ff53c4d6dc15c5b854e8961e`
- path: `NORMATIVE/ГПК РФ.txt`
- size: `1345993` bytes
- type: `TXT`
- blob: `9d2a5028dd975849a0189612d9e6c982a7da4d30`
- blocker: connector could enumerate metadata, but full/partial body fetch repeatedly returned no usable text because of large-file/encoding behavior.
- classification: `LARGE_GITHUB_CANDIDATE / FETCH_OR_ENCODING_IDENTITY_BLOCKER / NOT_PROMOTED_TO_RELIABLE_FULL_TEXT`.

### KAS RF / 21-FZ
- repo: `SergSi/EXPERT`
- commit: `7b6cc83b69d251a1ff53c4d6dc15c5b854e8961e`
- path: `NORMATIVE/КАС РФ.txt`
- size: `929965` bytes
- type: `TXT`
- fetched terminal confirms last Article 365 and `Президент Российской Федерации / В. Путин / Москва, Кремль / 8 марта 2015 г. / N 21-ФЗ`.
- terminal metadata: `01.05.2026 / Система ГАРАНТ / 147/147`.
- identity: number/date verified; literal full title not exposed in fetched portions.
- classification: `RELIABLE_FULL_BODY_CANDIDATE / NUMBER_DATE_TERMINAL_VERIFIED / SOURCE_SNAPSHOT_2026-05-01 / TITLE_LITERAL_CHECK_BLOCKER / NONOFFICIAL_GITHUB_COPY`.

### STO.FSB.KK 1-2018
- exact GitHub searches for `СТО.ФСБ.КК 1-2018` and title `Компьютерная экспертиза. Термины и определения` returned no usable candidate.
- normalized candidate fields: `repo=null / commit=null / path=null / size=null / type=null`.
- official FSB web index/search corroborates the standard name, identifier and posting date 13.12.2018.
- classification outside GitHub: `PRIMARY_OFFICIAL_FSB_HOSTING_CONFIRMED / STANDARD_OR_METHODOLOGICAL_DOCUMENT`.
- NPA status is not inferred from FSB hosting; no Minjust/official legal-publication status was established in this pass.
- status: `PRIMARY_NPA_STATUS_BLOCKER`.

## Official/current status layer — separate from GitHub

### 144-FZ
Working consolidated sources show edition `01.04.2025`; Federal Law 41-FZ of 01.04.2025 is published as official publication No. `0001202504010010`. Direct primary current consolidated card for 144-FZ was not resolved in this pass.
Status: `CURRENT_EDITION_CORROBORATED_NONPRIMARY_2025-04-01 / PRIMARY_CURRENT_STATUS_BLOCKER`.

### UPK RF
Federal Law 251-FZ of 26.07.2026 changes Articles 31 and 151 of UPK RF; change is effective 06.08.2026. Current consolidated sources show UPK red. `26.07.2026`.
Status: `CURRENT_EDITION_2026-07-26 / LATEST_AMENDMENT_CONFIRMED / PRIMARY_PUBLICATION_CARD_BLOCKER`.
GitHub red. 08.03.2026 is stale.

### APK RF
Current consolidated sources show red. `15.12.2025`, amendments effective `01.01.2026`. Federal Law 485-FZ of 15.12.2025 changes APK RF; official publication number is corroborated as `0001202512150050`.
Status: `CURRENT_EDITION_2025-12-15_EFFECTIVE_2026-01-01`.
GitHub body candidate freshness remains unresolved.

### GPK RF
Current effective consolidated layer on 31.08.2026 is red. `04.07.2026`; Federal Law 223-FZ of 04.07.2026 amended Article 29 and entered into force 15.07.2026; publication number is corroborated as `0001202607040011`.
Federal Law 333-FZ of 04.08.2026 creates a further GPK change effective `01.09.2026`.
Status: `CURRENT_EFFECTIVE_BODY_2026-08-31 + ENACTED_FUTURE_CHANGE_2026-09-01_BY_333_FZ`.
Gate: prepared consolidated edition effective tomorrow must not overwrite today's effective body.

### KAS RF
Current consolidated sources show red. `09.04.2026`. Federal Law 79-FZ of 09.04.2026 changes KAS RF and enters into force one month after official publication, i.e. `10.05.2026`; official publication ID: `0001202604090006`.
Status: `CURRENT_EDITION_2026-04-09 / PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED`.

### STO.FSB.KK 1-2018
Official FSB hosting/identity is corroborated. This is not automatically a registered normative legal act.
Status: `OFFICIAL_REGULATOR_STANDARD_HOSTING_CONFIRMED / NPA_STATUS_NOT_ESTABLISHED`.

## New counters
- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +3` (UPK segmented corpus; APK; KAS)
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
- `TERMINAL_NUMBER_DATE_MATCH_WITHOUT_TITLE_LITERAL != FULL_IDENTITY_VERIFIED`
- `LARGE_FILE_PRESENT != BODY_VERIFIED`
- `GITHUB_FULL_BODY_SHAPE != CURRENT_EDITION`
- `PREPARED_TOMORROW_CONSOLIDATION != CURRENT_EFFECTIVE_BODY_TODAY`
- `OFFICIAL_REGULATOR_HOSTING != REGISTERED_NPA_STATUS`

## Next priority boundary
Continue Habr with federal-law / Government / Roskomnadzor priority rather than low-value departmental material: `98-FZ О коммерческой тайне`, `395-1 О банках и банковской деятельности`, `224-FZ insider information`, then `Защита связи` starting with `176-FZ`, `126-FZ`, PP RF 538/2005, 532/2009 and current Roskomnadzor acts.
