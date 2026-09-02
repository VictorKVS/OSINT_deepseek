# ADR-001 — Границы хранения
**Статус:** Proposed · **Дата:** 2026-09-01

## Контекст
Дело содержит public URLs, captures, ПДн, restricted annexes и публичную методику. Хранение всего в public GitHub неприемлемо.

## Решение
1. Public GitHub — contracts, code, synthetic/redacted data, URLs, hashes.
2. Restricted Evidence Store — raw captures, attachments, ПДн.
3. Drive Workspace — editable service documents/controlled annexes.
4. Audit Store — append-only evidence.

## Последствия
Трассируемость и снижение утечек; требуется revision mapping и multi-store governance.

## Запрет
Отсутствие restricted store не разрешает временно помещать raw material в public repo.
