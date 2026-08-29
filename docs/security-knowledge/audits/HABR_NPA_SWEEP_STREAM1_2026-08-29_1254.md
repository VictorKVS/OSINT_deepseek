# Habr NPA sweep — поток 1 — 2026-08-29 12:54 MSK

Продолжен системный проход по Habr 432466 (версия 28.05.2026): Приказы Роскомнадзора №180/2022, №187/2022, №140/2025; параллельно повторно открыт blocker ПП РФ №228/2009 через обход дерева GitHub-репозитория.

## Итог прохода

- FULL_TEXT: +0
- BINARY_PDF_CANDIDATE: +1
- GITHUB_FULL_TEXT_BLOCKER: +3 по приказам Роскомнадзора +1 body-inspection blocker по ПП №228
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +2 (Роскомнадзор №180 и №140)
- OFFICIAL_PUBLICATION_CORROBORATED: +1 (Роскомнадзор №187 через «Российскую газету»; прямая карточка publication.pravo.gov.ru в этом проходе не разрешена)
- SEARCH_INDEX_FALSE_NEGATIVE_FOR_BINARY: +1
- exact duplicates: +0
- подтвержденные body-level identity conflicts: +0

## 1. ПП РФ от 16.03.2009 №228 «О Федеральной службе по надзору в сфере связи, информационных технологий и массовых коммуникаций»

### Новый GitHub-кандидат

Обход дерева репозитория `VictorKVS/gpt-agent` выявил бинарный PDF, который ранее не был найден точным GitHub Code Search:

- repo: `VictorKVS/gpt-agent`
- commit: `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8`
- path: `дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/Государственные регуляторы/Роскомнадзор/Постановление Правительства РФ от 16 марта .pdf`
- size: `160639` bytes
- type: `PDF / GitHub file blob`
- blob SHA: `9b56ca9727c8a9be49fdd5774922a2518b170733`

Имя файла и каталог делают его сильным кандидатом на ПП №228, но нормативная идентичность внутри PDF пока **не подтверждена**: GitHub connector возвращает бинарный объект, но не дает UTF-8 body, а web-fetch GitHub PDF завершился cache miss. Поэтому файл не повышается до `FULL_TEXT` и не получает `CORRECT_BODY_IDENTITY`.

Статус: `BINARY_PDF_CANDIDATE / METADATA_ONLY / BODY_IDENTITY_UNVERIFIED / NOT_FULL_TEXT_YET / NON_OFFICIAL_GITHUB_COPY / BINARY_INSPECTION_BLOCKER`.

Отдельный важный результат: прежний exact Code Search zero оказался неполным именно для бинарного PDF. Gate: `EXACT_CODE_SEARCH_ZERO != NO_BINARY_FILE_IN_REPOSITORY`.

### Официальная/актуальная сторона

Портал Правительства России в собственных документах однозначно ссылается на постановление Правительства РФ от 16.03.2009 №228 с названием «О Федеральной службе по надзору в сфере связи, информационных технологий и массовых коммуникаций». Прямую первичную консолидированную lifecycle-карточку в этом проходе не разрешили. Вторичные правовые системы показывают редакцию от 21.04.2026, но это не переносится в `VERIFIED_CURRENT` без первичного подтверждения.

Статус актуальности: `PRIMARY_IDENTITY_CORROBORATED / CURRENT_LIFECYCLE_PRIMARY_UNRESOLVED`.

## 2. Приказ Роскомнадзора от 28.10.2022 №180

Habr target: «Об утверждении форм уведомлений о намерении осуществлять обработку персональных данных, об изменении сведений, содержащихся в уведомлении о намерении осуществлять обработку персональных данных, о прекращении обработки персональных данных».

### GitHub

Точный GitHub Code Search по `Приказ Роскомнадзора от 28.10.2022` + `180` дал `total_count=0`, `incomplete_results=false`.

Воспроизводимого blob-кандидата нет; `repo/commit/path/size/type/blob_sha = null`.

Статус: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

### Первичный источник

Официальный портал подтверждает:
- приказ от 28.10.2022 №180;
- точное название;
- регистрацию Минюста 15.12.2022 №71532;
- номер опубликования `0001202212150022`;
- дату опубликования 15.12.2022.

Статус: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_LIFECYCLE_UNRESOLVED`.

## 3. Приказ Роскомнадзора от 14.11.2022 №187

Habr target: «Об утверждении Порядка и условий взаимодействия Федеральной службы по надзору в сфере связи, информационных технологий и массовых коммуникаций с операторами в рамках ведения реестра учета инцидентов в области персональных данных».

### GitHub

Точный GitHub Code Search по `Приказ Роскомнадзора от 14.11.2022` + `187` дал `total_count=0`, `incomplete_results=false`. Более широкий поиск по фразе `реестра учета инцидентов персональных данных` дал единственный нерелевантный словарный файл, который отвергнут как false positive.

Воспроизводимого нормативного blob-кандидата нет; `repo/commit/path/size/type/blob_sha = null`.

Статус: `GITHUB_FULL_TEXT_BLOCKER / FALSE_POSITIVE_REJECTED / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

### Официальная сторона

«Российская газета» подтверждает дату/номер/название, регистрацию Минюста 28.12.2022 №71851, публикацию 29.12.2022 и указывает, что документ опубликован на официальном интернет-портале правовой информации 28.12.2022. Прямую карточку publication.pravo.gov.ru в этом проходе не удалось разрешить, поэтому не ставится `PRIMARY_DIRECT_VERIFIED` и не утверждается полный current lifecycle.

Статус: `OFFICIAL_PUBLICATION_CORROBORATED / PRIMARY_DIRECT_CARD_UNRESOLVED / CURRENT_LIFECYCLE_UNRESOLVED`.

## 4. Приказ Роскомнадзора от 19.06.2025 №140

Habr target: «Об утверждении требований к обезличиванию персональных данных и методов обезличивания персональных данных, за исключением случаев, указанных в пункте 9.1 части 1 статьи 6 Федерального закона от 27 июля 2006 г. №152-ФЗ “О персональных данных”».

### GitHub

Точный GitHub Code Search по `Приказ Роскомнадзора от 19.06.2025` + `140` дал `total_count=0`, `incomplete_results=false`.

Воспроизводимого blob-кандидата нет; `repo/commit/path/size/type/blob_sha = null`.

Статус: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

### Первичный источник

Официальный портал Роскомнадзора на publication.pravo.gov.ru подтверждает:
- приказ от 19.06.2025 №140;
- точное название;
- регистрацию 31.07.2025 №83110;
- номер опубликования `0001202508010002`;
- дату опубликования 01.08.2025;
- официальный PDF: 427 Кб, 10 страниц.

Статус: `PRIMARY_INITIAL_PUBLICATION_CONFIRMED / CURRENT_LIFECYCLE_UNRESOLVED`.

## Новые/закрепленные gates

1. `EXACT_CODE_SEARCH_ZERO != NO_BINARY_FILE_IN_REPOSITORY`: code index может не показать PDF, присутствующий в дереве repo.
2. `BINARY_FILENAME_MATCH + RELEVANT_DIRECTORY != BODY_IDENTITY_VERIFIED`.
3. Невозможность прочитать бинарный PDF означает `BINARY_INSPECTION_BLOCKER`, а не автоматический `FULL_TEXT`.
4. `OFFICIAL_PUBLICATION_CORROBORATION != PRIMARY_DIRECT_CURRENT_LIFECYCLE`.
5. Для GitHub-копий официальный статус по-прежнему не наследуется ни от имени файла, ни от каталога, ни от совпадения номера/даты.

## Следующая очередь

Продолжить Роскомнадзор после №140 и расширенный поиск открытых blockers через tree/path traversal, PDF/DOCX filenames и крупные юридические корпуса; отдельно попытаться получить/прочитать PDF-кандидат ПП №228 и проверить внутри документа номер, дату, название, наличие постановления + полного Положения и редакционные маркеры.