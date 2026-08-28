# Habr NPA sweep — поток 1 — 2026-08-28 18:53 MSK

## Дельта прохода

- `FULL_TEXT`: +0
- новые `METADATA_BODY_IDENTITY_CONFLICT`: +3
- новый `SECONDARY_EXCERPT`: +1
- exact-дубликаты: +0
- новый gate: `FRONTMATTER_METADATA != BODY_IDENTITY`; `VERSION_DATE_BEFORE_ENACTMENT => HARD_REJECT`

## Новые подтвержденные конфликты

### 1. ПП РФ №1119 — ложная разметка поверх другого НПА

Repo: `BEaStia/legal-raggy`
Commit: `5d509da1f44bd43866d14b21adb45e446438415e`
Path: `data/raw/laws/pp1119_personal_data_security.md`
Size: 3032 bytes
Type: Markdown / blob
Blob SHA: `75704ab71d1abbe2bb1cb3a0391bae94219b2cab`

Frontmatter заявляет ПП РФ №1119 о защите ПДн в ИСПДн, но тело файла начинается как ПП РФ от 04.04.2000 №294 «Об утверждении Порядка расчетов за природный газ» и далее содержит служебный текст страницы КонсультантПлюс.

Классификация: `METADATA_BODY_IDENTITY_CONFLICT / DIFFERENT_ACT_PP294_2000 / SCRAPE_POISONING / REJECT_FOR_PRIMARY_KB`.

### 2. Архивный файл №1119 — не полный НПА

Repo/commit: те же.
Path: `data/raw/laws/archive/pp1119_personal_data_security_21.12.2018.md`
Size: 2601 bytes
Type: Markdown / blob
Blob SHA: `9cd6a5801e7554f7c1066d5c989f6872fa09f0e9`

Frontmatter содержит `source: official`, однако рядом прямо указано `version_note: manual excerpt for MVP`. Тело — краткая тематическая выжимка по уровням защищенности и мерам, а не нормативное тело постановления и приложенных Требований.

Классификация: `MANUAL_EXCERPT / SECONDARY_SUMMARY / SOURCE_LABEL_OVERCLAIM / NOT_FULL_TEXT`.

### 3. 149-ФЗ — ложная разметка поверх распоряжения №1034-р

Repo/commit: те же.
Path: `data/raw/laws/149fz_information.md`
Size: 2985 bytes
Type: Markdown / blob
Blob SHA: `e5e271224f9aa4a134f8011d7bf0fc6fd8927996`

Frontmatter заявляет 149-ФЗ «Об информации, информационных технологиях и о защите информации», но тело — распоряжение Правительства РФ от 10.08.2007 №1034-р об утверждении перечня аэродромов совместного базирования.

Классификация: `METADATA_BODY_IDENTITY_CONFLICT / DIFFERENT_ACT_1034-R_2007 / SCRAPE_POISONING / REJECT_FOR_PRIMARY_KB`.

### 4. 187-ФЗ — ложная разметка и невозможная дата редакции

Repo/commit: те же.
Path: `data/raw/laws/187fz_kii.md`
Size: 3269 bytes
Type: Markdown / blob
Blob SHA: `5f2dbcac072e884ce066311a568726561e3eee82`

Frontmatter заявляет 187-ФЗ о безопасности КИИ и `version_date: 20.11.2015`, хотя целевой 187-ФЗ принят в 2017 году. Тело файла — приказ Росимущества от 25.09.2014 №367 о закупочной комиссии.

Классификация: `PRE_ENACTMENT_VERSION_DATE_CONFLICT / METADATA_BODY_IDENTITY_CONFLICT / DIFFERENT_ACT / SCRAPE_POISONING / REJECT_FOR_PRIMARY_KB`.

## Официальный статус / lifecycle

В этом проходе прямые первичные lifecycle-страницы для старых 149-ФЗ/187-ФЗ не разрешились стабильно, поэтому никакой GitHub-кандидат не повышен до `CURRENT` или `OFFICIAL`. Для №1119 юридическая идентичность подтверждается отдельно официальными государственными источниками, но найденные GitHub-файлы выше отвергаются исключительно по содержимому тела.

## Новый regression gate

1. `frontmatter/source/title/version_date` — только подсказка, не доказательство.
2. При конфликте metadata ↔ body приоритет у body-level identity + первичного официального источника.
3. `version_date < enactment_date` для заявленного акта — hard reject до ручного разбора.
4. Метка `source: official` не делает пересказ официальным текстом.

## Открытые блокеры

Из этой серии кандидатов самостоятельные корректные GitHub `FULL_TEXT` всё ещё не подтверждены для ПП РФ №1119, 149-ФЗ и 187-ФЗ.
