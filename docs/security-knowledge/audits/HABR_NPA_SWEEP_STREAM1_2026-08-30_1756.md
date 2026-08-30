# Habr NPA sweep — поток 1 — 2026-08-30 17:56 MSK

Scope: продолжение системного прохода по Habr 432466 и пользовательскому списку НПА. В этом проходе закрыты новые позиции: 123-ФЗ/2020, ПП РФ №857/2015, приказы Роскомнадзора №84 и №85/2015, приказ Минтранса №162/2024, приказ Минздрава №139н/2025.

## Сводка

- GITHUB_FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +6
- DUPLICATE_REFERENCE_ARTIFACT: +2 файла одного уже известного тела 152-ФЗ
- HABR_STALE_TITLE_CONFLICT: +1 (123-ФЗ)
- CURRENT_EDITION_CORROBORATED: +2 (123-ФЗ, ПП №857)
- EXPLICIT_VALIDITY_WINDOW_CONFIRMED: +2 (Минтранс №162, Минздрав №139н)
- PRIMARY/AGENCY_HOSTED_FULLTEXT_OR_PUBLICATION_POINTER: +3
- Новых конфликтов идентичности целевого GitHub-body: 0
- Новых exact-дублей полного нормативного тела: 0

## 1. Федеральный закон от 24.04.2020 №123-ФЗ

Target identity: Федеральный закон от 24.04.2020 №123-ФЗ о специальном регулировании для ИИ в Москве; действующее на дату прохода название дополнено блоком об особенностях обработки ПДн при формировании региональных составов данных и предоставлении доступа к ним.

### GitHub
Exact code search по `"123-ФЗ" + "24.04.2020"` дал 2 результата, `incomplete_results=false`, оба в уже известном корпусе 152-ФЗ:

1. repo: `Grantik/odin-vault`
   - commit/ref: `890e95b3413ab562d56bd524d70de99f5e2b620c`
   - path: `sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.txt`
   - blob: `0d3f7c3d0618464af74753ad5a92e59568eb9211`
   - size: 238166 bytes (тот же blob, размер ранее измерен)
   - type: TXT/file
   - classification: `DUPLICATE_REFERENCE_ARTIFACT / REFERENCE_ONLY / WRONG_PRIMARY_BODY / REJECT`
   - body identity check: файл внутри начинается `Федеральный закон от 27.07.2006 г. № 152-ФЗ` / `О персональных данных`; 123-ФЗ встречается в перечне изменяющих законов, но не является телом файла.

2. repo: `Grantik/odin-vault`
   - commit/ref: `890e95b3413ab562d56bd524d70de99f5e2b620c`
   - path: `sync/canon/law/fz_152_personalnye_dannye_20060727_kremlin.html`
   - blob: `7823ea155ff602b1ff624dcec507f62893852551`
   - size: 243414 bytes (ранее измеренный размер того же blob)
   - type: HTML/file
   - classification: `DERIVED_DUPLICATE_REFERENCE / WRONG_PRIMARY_BODY / REJECT`

Target full body not found -> `GITHUB_FULL_TEXT_BLOCKER`.

### Актуальность / официальный слой
Current consolidated sources show edition `08.08.2024`. Federal Law №233-ФЗ from 08.08.2024 changes both 152-ФЗ and 123-ФЗ; its publication pointer is `0001202408080031`. The provisions changing the title/body of 123-ФЗ take effect 01.09.2025. Habr version dated 28.05.2026 still shows the old title without the regional-data clause -> `HABR_STALE_TITLE_CONFLICT`.

Important lifecycle gate: the original experimental legal regime was set for five years from 01.07.2020, but the act itself must not be marked wholly expired solely because that experiment period ended; later amendments effective from 01.09.2025 continue to regulate regional data compositions. Classification: `EXPERIMENT_PERIOD_ENDED != ACT_EXPIRED`.

Sources:
- Habr: https://habr.com/ru/articles/432466/
- Current 123-ФЗ title/edition: https://www.consultant.ru/law/podborki/fz_ob_iskusstvennom_intellekte/
- 233-ФЗ publication pointer: https://publication.pravo.gov.ru/document/0001202408080031

## 2. Постановление Правительства РФ от 19.08.2015 №857

Target identity: `Об автоматизированной информационной системе "Реестр нарушителей прав субъектов персональных данных"` + утвержденные Правила + критерии определения оператора реестра.

### GitHub
Exact code search по номеру/date/title: `total_count=0`, `incomplete_results=false`.

- repo: null
- commit: null
- path: null
- size: null
- type: null
- status: `GITHUB_FULL_TEXT_BLOCKER`

### Актуальность
Current consolidated text is edition `13.11.2019`; the changing act is PP RF №1443 dated 13.11.2019, which adds a paragraph to item 9 of the Rules. The edition starts 26.11.2019 after official publication of №1443 on 18.11.2019. No later amendment was found in the final freshness check.

Completeness gate: `FULL_TEXT = постановление + Правила + Критерии`; a copy containing only the dispositive part is `PARTIAL_TEXT`.

Sources:
- Current text: https://www.consultant.ru/document/cons_doc_LAW_184743/
- Amendment №1443: https://www.zakonrf.info/postanovlenie-pravitelstvo-rf-1443-13112019/

## 3. Приказ Роскомнадзора от 22.07.2015 №84

Target identity: `Об утверждении Порядка взаимодействия оператора реестра нарушителей прав субъектов персональных данных с провайдером хостинга и Порядка получения доступа к информации, содержащейся в реестре ..., оператором связи`.

### GitHub
Exact code search: `total_count=0`, `incomplete_results=false`.

- repo/commit/path/size/type: null
- status: `GITHUB_FULL_TEXT_BLOCKER`

### Тело / актуальность
Full reproduced text confirms exact number/date/title and contains two independent appendices: (1) interaction procedure with hosting provider; (2) access procedure for telecom operator. Current legal mirrors continue to expose the document as an актуальная версия; no later amendment/repeal was found in this pass.

Completeness gate: `FULL_TEXT = приказ + приложение 1 + приложение 2`.

Primary initial publication card remains unresolved in this pass; do not upgrade a legal mirror to official-publication status.

## 4. Приказ Роскомнадзора от 22.07.2015 №85

Target identity: `Об утверждении формы заявления субъекта персональных данных о принятии мер по ограничению доступа к информации, обрабатываемой с нарушением законодательства Российской Федерации в области персональных данных`.

### GitHub
Exact code search: `total_count=0`, `incomplete_results=false`.

- repo/commit/path/size/type: null
- status: `GITHUB_FULL_TEXT_BLOCKER`

### Тело / актуальность
Reproduced current text confirms exact date/number/title; registered in MinJustice 17.08.2015 №38544; effective from 01.09.2015. No later amendment/repeal found in this pass.

Completeness gate: `FULL_TEXT = приказ + полная утвержденная форма заявления`.

Primary official publication card unresolved; current legal-system copies are corroboration only.

## 5. Приказ Минтранса России от 02.05.2024 №162

Target identity: `Об утверждении порядка формирования и ведения автоматизированных централизованных баз персональных данных о пассажирах и персонале (экипаже) транспортных средств, а также срока хранения и порядка предоставления содержащихся в них данных`; MinJustice reg. №78358 от 30.05.2024.

### GitHub
Exact code search: `total_count=0`, `incomplete_results=false`.

- repo/commit/path/size/type: null
- status: `GITHUB_FULL_TEXT_BLOCKER`

### Official/agency-hosted body and lifecycle
A complete 17-page PDF is hosted on the official Rostranadzor domain and confirms the order, full Procedure, repeal of earlier Mintrans orders №243/2012, №228/2013 and №242/2014, entry into force 01.09.2024 and validity until 01.09.2030.

Classification: `OFFICIAL_AGENCY_HOSTED_FULLTEXT_CONFIRMED`, but this hosted copy is not automatically the official-publication event record.

Source: https://rostransnadzor.gov.ru/storage/documents/%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7%20%D0%9C%D0%B8%D0%BD%D1%82%D1%80%D0%B0%D0%BD%D1%81%D0%B0%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8%20%D0%BE%D1%82%2002.05.2024%20N%20162.pdf

## 6. Приказ Минздрава России от 20.03.2025 №139н

Target identity: `Об утверждении Порядка обезличивания сведений о лицах, которым оказывается медицинская помощь, а также о лицах, в отношении которых проводятся медицинские экспертизы, медицинские осмотры и медицинские освидетельствования`; MinJustice reg. №81828 от 14.04.2025.

### GitHub
Exact code search: `total_count=0`, `incomplete_results=false`.

- repo/commit/path/size/type: null
- status: `GITHUB_FULL_TEXT_BLOCKER`

### Official/publication layer
Publication pointer resolved: `0001202504140009`; document entered into force 01.09.2025 and is explicitly valid until 01.09.2031. It replaces Minzdrav order №341н/2018. Full body consists of the order plus the complete approved Procedure.

Classification: `OFFICIAL_PUBLICATION_POINTER_CORROBORATED / EXPLICIT_VALIDITY_WINDOW_CONFIRMED / GITHUB_FULL_TEXT_BLOCKER`.

Source: https://publication.pravo.gov.ru/document/0001202504140009

## New regression gates

1. `EXPERIMENT_PERIOD_ENDED != ACT_EXPIRED` — termination of a time-limited experiment does not by itself terminate the whole federal law if later operative provisions continue.
2. `HABR_TITLE_FRESHNESS` — title changes effective before the Habr snapshot date are genuine stale-reference conflicts, not post-snapshot drift.
3. `OFFICIAL_AGENCY_HOSTED_COPY != OFFICIAL_PUBLICATION_EVENT` — an agency-hosted complete PDF is strong provenance, but official publication remains a separate field/event.
4. `REGISTERED_FORM_DOCUMENT_FULL_TEXT_REQUIRES_FORM` — for form-approving orders the approved form is part of the full normative body.

## Queue next

Continue with remaining unprocessed PDn/general-information positions after item 48 and adjacent Roskomnadzor/general acts; keep priority on exact GitHub body discovery, primary-source lifecycle, and stale Habr references.