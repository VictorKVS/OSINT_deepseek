# Habr NPA sweep — Stream 1 — 2026-09-01 22:55 MSK

## Boundary

Продолжен раздел Habr 432466 «Государственная система обнаружения, предупреждения и ликвидации последствий компьютерных атак (ГосСОПКА)», позиции 5–11.

Уникальные новые цели этого прохода:

1. Приказ ФСБ России от 24.07.2018 № 366 «О Национальном координационном центре по компьютерным инцидентам».
2. Приказ ФСБ России от 24.07.2018 № 367 «Об утверждении Перечня информации, представляемой в ГосСОПКА, и Порядка представления информации в ГосСОПКА».
3. Приказ ФСБ России от 22.04.2026 № 161 «Об утверждении Порядка аккредитации центров ГосСОПКА … и Требований к центрам …».

Позиции 7–10 Habr (№ 368/2018, № 196/2019, № 281/2019, № 282/2019) уже были обработаны в предыдущем КИИ-проходе и здесь закрыты как cross-section duplicates без повторного начисления GitHub-body статистики. Их repeal/successor status также уже зафиксирован ранее.

## GitHub search results

### FSB-366/2018

`GITHUB_FULL_TEXT = NOT_FOUND`

Найден только производный учебный материал:

- repo: `pikov-vitaliy/pikov-expert-lectures`
- commit: `3743195404811ac9c3468c948bc4e78c67b56561`
- path: `risk/materials.md`
- blob: `d71ef1d775fa4616b1186b0de63d58bec48550cc`
- size: `184214` bytes
- type: `Markdown`
- classification: `MENTION_ONLY / EDUCATIONAL_REFERENCE / REJECTED_AS_NORMATIVE_BODY`

Внутри имеется строка `Приказ от 24.07.2018 № 366 — НКЦКИ`, но документ сам определен как авторская лекция/раздаточный материал. Нормативное тело приказа и Положения не воспроизводится.

Distinctive-body search по фразам из Положения (`НКЦКИ является составной частью сил...`) полного тела на GitHub не дал.

### FSB-367/2018

`GITHUB_FULL_TEXT = NOT_FOUND`

Тот же файл `pikov-vitaliy/pikov-expert-lectures@3743195404811ac9c3468c948bc4e78c67b56561:risk/materials.md` содержит только строку-описание `Приказ от 24.07.2018 № 367 — Перечень информации, представляемой в ГосСОПКА, и порядок представления`.

- repo: `pikov-vitaliy/pikov-expert-lectures`
- commit: `3743195404811ac9c3468c948bc4e78c67b56561`
- path: `risk/materials.md`
- blob: `d71ef1d775fa4616b1186b0de63d58bec48550cc`
- size: `184214` bytes
- type: `Markdown`
- classification: `MENTION_ONLY / EDUCATIONAL_REFERENCE / REJECTED_AS_NORMATIVE_BODY`

Distinctive-body search по формулировкам Порядка полного текста не дал.

### FSB-161/2026

`GITHUB_FULL_TEXT = NOT_FOUND`

Найден подробный справочный конспект, но не нормативное тело:

- repo: `ale88andr/obs-vault`
- commit: `7c3b5dfa92bde4382d3148b9b16131080718c281`
- path: `InfoSec/Законодотельство ИБ/Указ 250 — подзаконная база и практика 2022-2026.md`
- blob: `6dd846416c5a5778594f8e4f4f8e3c86ee83f43e`
- size: `31272` bytes
- type: `Markdown`
- classification: `MENTION_ONLY / NPA_PRACTICE_SUMMARY / REJECTED_AS_NORMATIVE_BODY`

Файл прямо обозначен как `справка по НПА и практике`; он фиксирует № 161 и дату вступления в силу, но не воспроизводит полный Порядок и Требования.

Также найден AI/Copilot conversation в том же repo с упоминанием № 161; классифицирован как `AI_SESSION_MENTION_ONLY`, без повышения доверия.

Distinctive-body search по заголовкам приложений и требованиям к аккредитованным центрам полного нормативного тела на GitHub не дал.

## Primary-source / legal status validation

### № 366/2018

Primary regulator layer: текущий официальный ресурс НКЦКИ `cert.gov.ru` содержит карточку приказа № 366 и отдельно приказ ФСБ № 540 от 24.12.2025, вносящий изменения в Положение.

Official publication metadata:

- original act: publication date `2018-09-10`, Minjust `№ 52109`, official publication pointer `0001201809100001`;
- amendment: FSB order `№ 540` dated `2025-12-24`, Minjust `№ 84777`, official publication `2025-12-25`, pointer `0001202512250025`, effective `2026-01-30`.

Lifecycle classification:

- `CURRENT_EDITION_ADVANCED_2025-12-24`
- `CURRENT_TEXT_EFFECTIVE_FROM_2026-01-30`
- any GitHub copy reproducing only the 2018 body without № 540 => `OLD_EDITION`.

Direct official portal cards for the publication IDs timed out / were not directly resolved in this run; publication pointers are kept separately from direct-fetch status.

### № 367/2018

Primary regulator layer: current `cert.gov.ru` legal-basis list still includes № 367 alongside the post-2025 ГосСОПКА package.

Official publication metadata:

- signed `2018-07-24`
- Minjust `№ 52108`
- official publication date `2018-09-10`
- official publication pointer `0001201809100002`
- effective `2018-09-21`

No repeal or later amendment was confirmed in this pass. Status gate remains conservative: `CURRENT_PRIMARY_REGULATOR_LISTED / NO_REPEAL_FOUND`, not an inference that any GitHub copy is current or official.

### № 161/2026

Official publication metadata:

- signed `2026-04-22`
- Minjust `№ 86534` on `2026-05-20`
- official portal publication `2026-05-20`
- official publication pointer `0001202605200018`
- effective `2026-05-31`
- official PDF size reported by RG: about `1.9 MB`

Completeness gate for any future GitHub candidate:

`FULL_TEXT_CURRENT = order body + Appendix 1 (accreditation procedure) + Appendix 2 (requirements) + all internal annexes/forms referenced by those appendices`.

A heading-only copy, summary of accreditation stages, or reproduction of only Appendix 1 must not be promoted to `FULL_TEXT`.

Direct official portal card timed out in this run, so `OFFICIAL_PUBLICATION_POINTER_CONFIRMED != PRIMARY_PORTAL_DIRECT_FETCH_OK`.

## New counters for this pass

- `GITHUB_FULL_TEXT +0`
- `RELIABLE_GITHUB_CANDIDATE +0`
- `GITHUB_FULL_TEXT_BLOCKER +3` (№ 366, № 367, № 161)
- `GITHUB_MENTION_ONLY_REJECTED +2` (one shared educational file for № 366/367; one NPA-practice summary for № 161)
- `CURRENT_EDITION_ADVANCED_366_2025-12-24 +1`
- `PRIMARY_PUBLICATION_POINTER_CONFIRMED +3 targets` (+1 amendment pointer for № 540)
- `NEW_GITHUB_FULL_BODY_DUPLICATE +0`
- `NEW_GITHUB_BODY_IDENTITY_CONFLICT +0`
- `CROSS_SECTION_DUPLICATES_CLOSED_WITHOUT_RECOUNT = 4` (№ 368, № 196, № 281, № 282)

## Blockers

- `PRIMARY_PORTAL_DIRECT_FETCH_BLOCKER`: official publication portal direct fetch timed out for the checked publication IDs.
- `GITHUB_FULL_TEXT_BLOCKER`: no indexed full body / reliable full-body candidate for № 366, № 367, № 161.
- For № 367, no separate primary consolidated-edition card was resolved; current presence is confirmed through the current official NКЦКИ legal-basis list, while absence of repeal is not treated as proof from silence.

## Next boundary

Continue after ГосСОПКА № 161 into the next Habr section: `Персональные данные (ПДн)`, starting with the federal-law / presidential / government-level layer. Preserve cross-section deduplication against already processed 149-ФЗ/152-ФЗ and other common acts from the user list.
