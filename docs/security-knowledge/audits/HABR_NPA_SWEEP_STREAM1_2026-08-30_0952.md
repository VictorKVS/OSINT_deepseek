# Habr NPA sweep — поток 1 — 2026-08-30 09:52 MSK

## Delta this pass

- `GITHUB_FULL_TEXT +1` — 149-ФЗ.
- `GITHUB_FULL_TEXT_REFRESH_CONFIRMED +1` — 152-ФЗ: ранее известная GitHub-копия проверена на новом commit/ref и теперь содержит редакционную помету до 26.07.2026 №265-ФЗ.
- `GITHUB_FULL_TEXT_BLOCKER +2` — 27-ФЗ/1996 и 125-ФЗ/2004.
- `BODY_IDENTITY_CONFIRMED +2` — 149-ФЗ и 152-ФЗ.
- `CURRENT_EDITION_CORROBORATED +4`.
- `POST_HABR_SNAPSHOT_AMENDMENT +2` — 149-ФЗ (210-ФЗ/2026) и 152-ФЗ (265-ФЗ/2026).
- `HABR_STALE_TITLE_CONFLICT +1` — 27-ФЗ/1996.
- `KNOWN_FUTURE_EFFECTIVE_CHANGE +2` — 149-ФЗ с 01.09.2026; 27-ФЗ имеет раздельные даты вступления изменений 29-ФЗ/2026.
- exact-дубли полного нормативного тела: `+0`.
- новые body-identity конфликты GitHub-кандидатов: `+0`.

## 1. Федеральный закон от 27.07.2006 №149-ФЗ

**Название:** «Об информации, информационных технологиях и о защите информации».

### GitHub

- repo: `Grantik/odin-vault`
- commit/ref: `c4ece018394cb8d19633b733a8320caf6f3173e5`
- path: `sync/canon/law/fz_149_informacia_20060727_kremlin.txt`
- blob SHA: `2e4ea7b69a66fd9d8fc0df3d1a338bc4c0d29bc3`
- size: `535670` bytes
- type: `TXT/file`
- companion HTML: `sync/canon/law/fz_149_informacia_20060727_kremlin.html`, blob `5c40bcbe8ee7e772f23a3c20351644463de1e0b1`, `544908` bytes.

Проверка тела: в начале файла совпадают номер `149-ФЗ`, дата `27.07.2006`, название и даты принятия/одобрения. В конце присутствуют ст.18, подпись Президента, `Москва, Кремль`, дата и номер. Это полный нормативный текст, а не упоминание или конспект.

В `MANIFEST.md` repo указывает машинное происхождение текста с `kremlin.ru/acts/bank/24157/print` и SHA-256 `a0fc87d09095e49aaf1153ae1aefc31e976af3366f49cd2315ac301a8dedb512`. Это provenance, но **не делает GitHub-копию официальной публикацией**.

### Актуальность / официальный слой

GitHub-шапка заканчивает перечень редакций Федеральным законом от 26.06.2026 №210-ФЗ. Актуальные правовые источники также показывают редакцию 149-ФЗ от 26.06.2026; номер официального опубликования 210-ФЗ — `0001202606260070`.

При этом уже опубликован 29.12.2025 №568-ФЗ, который изменяет 149-ФЗ и вступает в силу **01.09.2026**. Официальная карточка: https://publication.pravo.gov.ru/Document/View/0001202512290056 . Поэтому на 30.08.2026 GitHub-копия проходит current-effective gate, но имеет известную границу устаревания `2026-09-01`.

Статус: `GITHUB_FULL_TEXT_CONFIRMED / BODY_IDENTITY_CONFIRMED / NON_OFFICIAL_GITHUB_COPY_WITH_PRIMARY_SOURCE_PROVENANCE / CURRENT_EFFECTIVE_TEXT_CORROBORATED_AS_OF_2026-08-30 / KNOWN_FUTURE_CHANGE_2026-09-01`.

## 2. Федеральный закон от 27.07.2006 №152-ФЗ

**Название:** «О персональных данных».

### GitHub — refresh ранее известной находки

- repo: `Grantik/odin-vault`
- commit/ref: `c4ece018394cb8d19633b733a8320caf6f3173e5`
- path: `sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt`
- blob SHA: `0d3f7c3d0618464af74753ad5a92e59568eb9211`
- size: `238166` bytes
- type: `TXT/file`
- companion HTML: blob `7823ea155ff602b1ff624dcec507f62893852551`, `243414` bytes.

Внутренние реквизиты совпадают; хвост содержит ст.25, подпись Президента, `Москва, Кремль`, дату и №152-ФЗ. Это полный текст. В шапке теперь присутствует редакционная помета `от 26.07.2026 №265-ФЗ`.

`MANIFEST.md` фиксирует машинную копию с `kremlin.ru/acts/bank/24154/print`; GitHub при этом остается неофициальным носителем.

### Актуальность

Актуальные правовые источники показывают 152-ФЗ в редакции 26.07.2026. №265-ФЗ изменил ст.12; publication pointer: `0001202607260024`. Прямую карточку первичного портала в этом проходе не удалось устойчиво получить, поэтому не повышаем до `PRIMARY_DIRECT_CARD_VERIFIED`.

Статус: `GITHUB_FULL_TEXT_REFRESH_CONFIRMED / BODY_IDENTITY_CONFIRMED / CURRENT_EDITION_CORROBORATED_2026-07-26 / OFFICIAL_PUBLICATION_POINTER_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED_THIS_PASS`.

## 3. Федеральный закон от 01.04.1996 №27-ФЗ

### GitHub

Exact/broad Code Search по номеру, дате и `персонифицированному` дал `0`, `incomplete_results=false`.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`

Статус: `GITHUB_FULL_TEXT_BLOCKER`.

### Конфликт Habr и текущего названия

Habr 432466 (версия 28.05.2026) продолжает приводить название: «Об индивидуальном (персонифицированном) учете **в системе обязательного пенсионного страхования**».

Федеральный закон от 14.07.2022 №237-ФЗ изменил название на: «Об индивидуальном (персонифицированном) учете **в системах обязательного пенсионного страхования и обязательного социального страхования**». Новое название действует с 01.01.2023; актуальную формулировку использует официальный СФР в 2026 году.

Следовательно: `HABR_STALE_TITLE_CONFLICT` — это не post-snapshot изменение, а устаревшее название уже к дате снимка Habr.

Последняя установленная редакция — от 20.02.2026 №29-ФЗ. У №29-ФЗ раздельные даты вступления положений в силу: 01.07.2026, 01.09.2026 и 01.04.2027. Поэтому current-state должен храниться на уровне конкретных норм, а не одной датой документа.

Статус: `CURRENT_EDITION_CORROBORATED_2026-02-20 / SPLIT_EFFECTIVE_DATES / HABR_STALE_TITLE_CONFLICT / GITHUB_FULL_TEXT_BLOCKER`.

## 4. Федеральный закон от 22.10.2004 №125-ФЗ

**Название:** «Об архивном деле в Российской Федерации».

### GitHub

Exact и broad Code Search по номеру/дате/названию дали `0`, `incomplete_results=false`.

- repo: `null`
- commit: `null`
- path: `null`
- size: `null`
- type: `null`

Статус: `GITHUB_FULL_TEXT_BLOCKER`.

### Актуальность / официальный слой

Официальный портал напрямую подтверждает Федеральный закон от 13.12.2024 №469-ФЗ «О внесении изменений в статью 24 Федерального закона "Об архивном деле в Российской Федерации"», номер опубликования `0001202412130022`, дата публикации 13.12.2024: https://publication.pravo.gov.ru/document/0001202412130022 .

Актуальные правовые источники показывают 125-ФЗ в редакции 13.12.2024. Нового более позднего amendment marker в этом проходе не найдено.

Статус: `PRIMARY_LATEST_AMENDMENT_PUBLICATION_CONFIRMED / CURRENT_EDITION_CORROBORATED_2024-12-13 / GITHUB_FULL_TEXT_BLOCKER`.

## New gates

1. `PRIMARY_SOURCE_PROVENANCE_IN_REPO ≠ OFFICIAL_COPY_STATUS` — даже если GitHub MANIFEST доказывает машинное получение с Kremlin/Pravo, GitHub-blob не становится официальной публикацией.
2. `CURRENT_EFFECTIVE_TEXT ≠ ENACTED_FUTURE_TEXT` — у НПА может быть корректная действующая сегодня копия и одновременно известная дата, после которой она станет stale.
3. `TITLE_FRESHNESS` хранится отдельно от body identity и amendment freshness; №27-ФЗ показывает, что корректный номер/дата не спасают устаревшее название.
4. Для изменений с несколькими датами вступления — `EFFECTIVE_DATE` хранить на уровне provision/amendment, а не только акта.

## Sources checked

- Habr 432466: https://habr.com/ru/articles/432466/
- official publication 568-ФЗ: https://publication.pravo.gov.ru/Document/View/0001202512290056
- official publication 469-ФЗ: https://publication.pravo.gov.ru/document/0001202412130022
- SFR current title for 27-ФЗ: https://sfr.gov.ru/order/individual_records/~12272
- RG 29-ФЗ/2026: https://rg.ru/documents/2026/02/26/fz29-dok.html
- RG 237-ФЗ/2022: https://rg.ru/documents/2022/07/19/dokument-zakon-akti.html
