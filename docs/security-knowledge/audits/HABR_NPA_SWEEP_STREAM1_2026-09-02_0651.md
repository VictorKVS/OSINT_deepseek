# Habr NPA sweep — Stream 1 — 2026-09-02 06:51 MSK

Scope: Habr 432466, раздел «Персональные данные. Блокировка нарушителей», позиции 1–3: ПП РФ 19.08.2015 №857; приказы Роскомнадзора 22.07.2015 №84 и №85. Правило: GitHub-копия не считается официальным источником; полнота/идентичность GitHub-body и официальный/current status проверяются раздельно.

Примечание о непрерывности: предыдущий интерактивный проход по ПДн 41–43 и правительственному слою безопасности ПДн (№940/№211/№1119) сообщил `PROGRESS_WRITE_PENDING_VERIFICATION`; настоящий файл возобновляет подтверждённую commit-chain с нового блока и не пересчитывает те результаты повторно.

## Итог партии

- GITHUB_FULL_TEXT: 0
- RELIABLE_GITHUB_BODY_CANDIDATE: 0
- GITHUB_FULL_TEXT_BLOCKER: 3
- GITHUB_WRONG_TARGET_BODY_REJECTED: 1
- GITHUB_CANDIDATE_TARGET_IDENTITY_MISMATCH: 1
- NEW_GITHUB_FULL_BODY_DUPLICATE: 0
- NEW_GITHUB_BODY_IDENTITY_CONFLICT: 0
- CURRENT_EDITION_ADVANCED: 1 (ПП №857 → редакция 13.11.2019 по вторичным консолидированным источникам)
- NUMBER_COLLISION: 1 (№857 встречается у иных постановлений других лет; номер без даты/названия не является identity key)
- PRIMARY_DIRECT_PUBLICATION_OR_CURRENT_STATUS_BLOCKER: 3

## Позиции

| Habr | Документ | GitHub | Классификация GitHub | Актуальность / официальный слой | Блокеры / gates |
|---|---|---|---|---|---|
| Блокировка-1 | ПП РФ 19.08.2015 №857 «Об автоматизированной информационной системе “Реестр нарушителей прав субъектов персональных данных”» | Exact/full-body search: нет. Ложноположительный кандидат: `edekeulenaar/global-digital-regulations@633e8261d64910a2dc8913a1cfd8faa7fe78314c`, `data/policies/2252.md`, blob `71bb6fb2df6d76a92cca84a5e3a948b76f02623b`, Markdown, `size=UNRESOLVED_CONNECTOR_METADATA` | Внутри файла явно указан другой акт: ФЗ 21.07.2014 №242-ФЗ. Фраза о «Реестре нарушителей…» содержится только в описании последствий 242-ФЗ. `MENTION_IN_DIFFERENT_NORMATIVE_BODY / REJECTED_AS_TARGET_BODY` | Вторичные консолидированные источники показывают действующую редакцию №857 от 13.11.2019, сформированную ПП РФ №1443; исходный акт вступил в силу 01.09.2015, редакция 2019 — с 26.11.2019. | `PRIMARY_DIRECT_PUBLICATION_POINTER_BLOCKER`; current full-text gate = постановление + Правила + Критерии + изменение №1443/2019. Любая копия только редакции 2015 = `OLD_EDITION`. `NUMBER_COLLISION_857`: требуется дата+название, не только номер. |
| Блокировка-2 | Роскомнадзор 22.07.2015 №84, Минюст №38532 | Exact title / distinctive-body search: full-body не найден; `repo/commit/path/size/type=null` | `GITHUB_FULL_TEXT_BLOCKER` | Вторичная текущая правовая репродукция: редакция 22.07.2015, статус «Действует», регистрация Минюста 14.08.2015 №38532, вступление 01.09.2015; официальная публикация указана 18.08.2015. | Primary direct RKN/pravo.gov copy и точный publication ID не разрешены: `PRIMARY_DIRECT_PUBLICATION_OR_CURRENT_STATUS_BLOCKER`. Full-text gate = приказ + приложение №1 (взаимодействие с провайдером) + приложение №2 (доступ оператора связи). |
| Блокировка-3 | Роскомнадзор 22.07.2015 №85, Минюст №38544 | Exact title / distinctive-body search: full-body не найден; `repo/commit/path/size/type=null` | `GITHUB_FULL_TEXT_BLOCKER` | Вторичная текущая правовая репродукция: редакция 22.07.2015, статус «Действует», регистрация Минюста 17.08.2015 №38544, вступление 01.09.2015; официальная публикация указана 18.08.2015. | Primary direct RKN/pravo.gov copy и точный publication ID не разрешены: `PRIMARY_DIRECT_PUBLICATION_OR_CURRENT_STATUS_BLOCKER`. Full-text gate = приказ + полностью утверждённая форма заявления. |

## Новые подтверждённые находки / конфликты / блокеры

1. `GITHUB_CANDIDATE_TARGET_IDENTITY_MISMATCH`: поиск по названию реестра выводит `data/policies/2252.md`, но внутренние реквизиты однозначно идентифицируют 242-ФЗ, а не ПП №857. Такой hit нельзя принимать ни как full text, ни как reliable candidate №857.
2. `CURRENT_EDITION_ADVANCED_857_2019-11-13`: для №857 исходный текст 2015 года недостаточен; current body должен учитывать ПП РФ №1443 от 13.11.2019.
3. `NUMBER_COLLISION_857`: в поисковой выдаче существуют иные ПП РФ №857 других лет. Identity gate для всех GitHub-кандидатов усилен до `number + date + title + internal body`.
4. Для №84/№85 надежных GitHub-body кандидатов не найдено. Вторичные правовые системы показывают оба приказа действующими, но отсутствие прямого первичного RKN/pravo.gov экземпляра сохраняется как отдельный blocker; secondary status не повышается до primary-confirmed автоматически.

## Следующая граница Stream 1

Habr «Персональные данные. Особые случаи обработки ПДн», первые федеральные акты: 27-ФЗ от 01.04.1996, 39-ФЗ от 22.04.1996, 57-ФЗ от 27.05.1996, Воздушный кодекс 60-ФЗ от 19.03.1997, 143-ФЗ от 15.11.1997. Продолжать с дедупликацией ранее встречавшихся общих актов и отдельным primary-status gate.
