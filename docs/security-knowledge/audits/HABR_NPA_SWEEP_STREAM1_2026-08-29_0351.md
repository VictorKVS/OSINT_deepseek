# Habr NPA sweep — Stream 1 — 2026-08-29 03:51 MSK

## Delta

- NEW_TARGET_FULL_TEXT: +2 (`149-ФЗ/27.07.2006`, `ПП РФ №211/21.03.2012`)
- FRESHER_FULL_TEXT_SIBLING: +1 (`152-ФЗ/27.07.2006`, snapshot through 08.08.2024)
- EXACT_DUPLICATE_SET: +1 (`149-ФЗ` TXT x2, same blob SHA)
- PRIMARY_OFFICIAL_LIFECYCLE_BLOCKER: +1 (`ПП РФ №211`)
- OLD_BLOCKER_CLOSED: `GITHUB_FULL_TEXT_149-FZ`

## 1. Федеральный закон от 27.07.2006 №149-ФЗ

Target: «Об информации, информационных технологиях и о защите информации».

GitHub:
- repo: `VictorKVS/gpt-agent`
- commit: `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8`
- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/Федеральный закон от 27 июля 2006 г N 149 ФЗ Об информации информационных технол/Федеральный закон от 27 июля 2006 г N 149 ФЗ Об информации информационных технол.txt`
- size: `578431` bytes
- type: `TXT/blob`
- blob SHA: `c87237ea64a326cabb76f8fbc9791bb65c30a36d`

Body checks:
- exact date/number/title present;
- adoption/approval dates present;
- body reaches Articles 17 and 18;
- terminal signature block present: President, Moscow/Kremlin, 27.07.2006, №149-ФЗ;
- GARANT export footer dated 21.11.2024;
- amendments list in the file reaches 09.11.2024.

Classification: `FULL_TEXT / RUSSIAN / GARANT_CONSOLIDATED_EXPORT / NON_OFFICIAL_GITHUB_COPY / REVISION_THROUGH_09.11.2024 / STALE_CONFIRMED`.

Duplicate:
- sibling path ending `...информационных технол (1).txt`
- same size `578431` and same blob SHA `c87237...`
- classification: `EXACT_DUPLICATE_X2`.

Format sibling candidate:
- PDF, size `474862`, blob `cdf38ac57e2a6b4a1ff7e56fec0ab240f938fc0f`; body not independently verified in this pass.

Official/currentness check:
- Kremlin legal bank confirms exact identity of 149-ФЗ;
- official publication portal records later direct amendments to 149-ФЗ: 568-ФЗ and 569-ФЗ of 29.12.2025;
- therefore the GitHub snapshot through 09.11.2024 is not current.

Result: old blocker `GITHUB_FULL_TEXT_149-FZ` CLOSED; `GITHUB_CURRENT_CONSOLIDATED_149-FZ` remains OPEN.

## 2. Постановление Правительства РФ от 21.03.2012 №211

Target: «Об утверждении перечня мер, направленных на обеспечение выполнения обязанностей, предусмотренных Федеральным законом “О персональных данных” ... операторами, являющимися государственными или муниципальными органами».

GitHub:
- repo: `VictorKVS/gpt-agent`
- commit: `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8`
- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/ПП Р Ф 2103 2012 г  N  211 Об утверждении перечня мер/Постановление Правительства РФ от 21 марта 2012 г. N 211 Об утверждении перечня мер .txt`
- size: `16085` bytes
- type: `TXT/blob`
- blob SHA: `e35cb53ce9a8995306eb99206b0759c8c19b6d79`

Body checks:
- exact type/date/number/title present;
- dispositive part and signature `Председатель Правительства РФ В. Путин` present;
- attached approved `Перечень мер` is included through its final point 2;
- amendments stated in export: 20.07.2013, 06.09.2014, 15.04.2019.

Classification: `FULL_TEXT / RUSSIAN / GARANT_CONSOLIDATED_EXPORT / NON_OFFICIAL_GITHUB_COPY / DECLARED_REVISION_THROUGH_15.04.2019 / CURRENT_CANDIDATE_NOT_PRIMARY_VERIFIED`.

Format sibling candidate:
- PDF, size `94885`, blob `61214187c156b729ae6bf69b51ce72870ebb3cbf`; body not independently verified in this pass.

Official/currentness check:
- official-publication newspaper `Российская газета` confirms original PP №211 identity and publication on 29.03.2012;
- the 15.04.2019 №454 amendment is independently identifiable and matches the revision chain, but a primary Government/pravo lifecycle card was not reliably resolved in this pass.

Blocker: `PRIMARY_OFFICIAL_LIFECYCLE_PP211_FETCH_BLOCKER`. Do not label GitHub copy `OFFICIAL` or `VERIFIED_CURRENT` until primary lifecycle resolution succeeds.

## 3. Федеральный закон от 27.07.2006 №152-ФЗ — fresher GitHub sibling

GitHub:
- repo: `VictorKVS/gpt-agent`
- commit: `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8`
- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/Персональные данные ФЗ 152/Федеральный закон от 27 июля 2006 г N 152 ФЗ О персональных данных с изменениями.txt`
- size: `243457` bytes
- type: `TXT/blob`
- blob SHA: `4fe5ea95dc698364acfcffcd57c99659fea18ca3`

Body checks:
- exact identity present;
- amendments list reaches 08.08.2024;
- body reaches Articles 23.1, 24 and 25;
- terminal Moscow/Kremlin/date/№152-ФЗ block present;
- minor text-extraction defect: signature rendered `В. Пути` rather than `В. Путин`; this does not break legal identity because all other body identifiers and terminal structure agree.

Classification: `FULL_TEXT / RUSSIAN / GARANT_CONSOLIDATED_EXPORT / NON_OFFICIAL_GITHUB_COPY / REVISION_THROUGH_08.08.2024 / STALE_CONFIRMED / MINOR_TEXT_EXTRACTION_DEFECT`.

Format sibling candidate:
- PDF, size `332302`, blob `1f7d14f661d587a5ef17191aaef73c014e5d82ad`; body not independently verified in this pass.

Official/currentness check:
- Kremlin legal bank confirms 152-ФЗ identity and a revision chain later than the GitHub snapshot (at least 28.02.2025 №23-ФЗ);
- Federal Law 26.07.2026 №265-ФЗ directly amends Article 12 of 152-ФЗ; official publication identifier resolved through a current legal review as `0001202607260024`, but fetching the publication.pravo.gov.ru card timed out in this pass.

Result: this supersedes the previously found 2020 GitHub snapshot as a fresher candidate, but does not close `GITHUB_CURRENT_CONSOLIDATED_RU_152-FZ`.

## Gates added/confirmed

1. `SAME_BLOB_SHA + SAME_SIZE = EXACT_DUPLICATE`, even when filenames differ.
2. `FULL_TEXT_SNAPSHOT != CURRENT_TEXT` — currentness is a separate official-lifecycle check.
3. `END_OF_BODY_CHECK` is mandatory before promoting a candidate from header match to `FULL_TEXT`.
4. `PRIMARY_LIFECYCLE_UNRESOLVED => NO VERIFIED_CURRENT LABEL`.
5. Minor export/OCR defects are recorded separately and do not automatically invalidate identity if the full legal identity tuple and terminal structure agree.
