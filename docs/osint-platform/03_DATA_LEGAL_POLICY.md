# 03. Данные, правовые ограничения и экспорт

> Архитектурная политика, а не заключение о праве для конкретного кейса.

## Классы доступа

| Класс | Назначение | Публичный экспорт |
|---|---|---|
| `PUBLIC` | открытые данные без дополнительных ограничений | после review |
| `PUBLIC_WITH_PERSONAL_DATA` | открытые данные с ПДн | после минимизации |
| `AUTHORIZED_INTERNAL` | законно доступные внутренние материалы | запрещён по умолчанию |
| `RESTRICTED` | чувствительные доказательства | запрещён |
| `PROHIBITED` | нельзя использовать | запрещён и изолирован |

Класс наследуется в сторону большей строгости. Пересказ не делает restricted material публичным.

## Обязательные поля контроля

Для дела: purpose, scope, requester, legal/contractual basis note, allowed classes, prohibited methods, retention, export profiles, reviewers.

Для существенно использованного ПДн: цель, необходимость, источник, категория, срок, доступ, редактирование, correction/deletion state.

## Запрещённые обходы

Платформа не должна обходить аутентификацию/paywall/CAPTCHA, использовать похищенные credentials, маскировать запрещённый метод под OSINT, автоматически принимать утечки в public-контур, собирать избыточные ПДн, запускать активные действия вне scope или публиковать raw captures без review.

## Экспорт блокируется, если

- найден `RESTRICTED` или `PROHIBITED`;
- ПДн не минимизированы;
- у вывода нет источников;
- отсутствует capture hash;
- claim представлен как fact;
- hypothesis не маркирована;
- есть неподтверждённое обвинительное утверждение;
- нет legal usage note;
- материал нельзя перепубликовывать;
- нет Red Team review для high-impact finding;
- нет reviewer;
- manifest не совпадает с хешами.

## Публичный GitHub

Допустимы contracts, code, synthetic/redacted fixtures, public URLs, hashes, provenance metadata и redacted reports.

Недопустимы raw real dossiers, паспорта, домашние адреса, частные контакты, утечки, secrets, restricted originals и allegations без статуса.

## Drive ↔ GitHub

- Drive: редактируемые служебные документы и закрытые приложения.
- GitHub: versioned contracts, methodology, redacted exports и provenance map.
- Связка: `case_id`, `document_id`, revision, SHA-256, access class.
- Синхронизация явная; автоматическая публикация restricted Drive → public GitHub запрещена.
