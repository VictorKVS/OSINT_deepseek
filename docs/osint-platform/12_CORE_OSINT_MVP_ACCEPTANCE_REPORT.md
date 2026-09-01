# 12. Core OSINT MVP v0.1 — отчёт приёмочной проверки

**Дата локального прогона:** 2026-09-02  
**Объект:** новый пакет `osint_workbench`; замороженный `father_osint` не изменялся.  
**Данные:** полностью синтетические.  
**Сетевой сбор:** не выполнялся.

## Результаты

```text
Python compileall: PASS
Core unit/integration tests: 14 passed
Synthetic vertical demo: PASS
Baseline schemas used: 18
Generated schema-bound objects: 50 PASS
Query-plan canonical SHA-256: PASS
Journal sequence + SHA-256 chain: PASS
Graph reference/evidence-path integrity: PASS
```

## Проверенные сценарии

- пяти-поточный план и запрет active scope;
- регистрация активного инструмента только как disabled inventory;
- public export redaction gate;
- immutable content-addressed capture;
- extraction without silent attribution;
- detection of journal tampering;
- namesake/stable-identifier conflict without auto-merge;
- two-family analysis zoo and prohibition of FACT creation;
- rejection of false independence from two analyzers of one family;
- graph/evidence path/report generation;
- monitoring change detection;
- loopback read-only API and rejection of POST;
- blocking private, credential-bearing and non-HTTP URLs;
- public DNS resolution policy tested by mock without network request.

## Синтетический выход

```text
CASE-SYNTH-CORE-0001
3 sources / 3 captures
9 entities
5 claims / 5 relations
1 entity match
1 transform / 1 acquisition job
1 human-approved finding
1 research gap / 1 coverage
1 analysis run / 2 opinions / 1 consensus
1 graph / 1 report / 1 monitor snapshot
12 journal entries, hash chain valid
```

## Ограничение заявления

Этот отчёт подтверждает локальный прогон нового пакета и contract fixtures. Полный regression run всего GitHub-репозитория и GitHub Actions фиксируются отдельно после публикации ветки. Отсутствие регрессии нельзя объявлять только по локальному isolated run.
