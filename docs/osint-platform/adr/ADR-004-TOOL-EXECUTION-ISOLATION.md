# ADR-004 — Изоляция инструментов и Kali-адаптеры
**Статус:** Proposed · **Дата:** 2026-09-01

## Контекст
Kali содержит passive, active и exploitation tools. «Установлено» не означает «разрешено».

## Решение
Только adapter registry: input/output contract, exact version, execution profile, network policy, safety class, scope, limits, policy, approval, raw/normalized hashes. Default UI — jobs/read-only logs, не unrestricted shell.

## Последствия
Контролируемость; каждый tool требует adapter/parser/tests.
