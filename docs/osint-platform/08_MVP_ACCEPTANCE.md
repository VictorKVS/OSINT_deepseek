# 08. Первый вертикальный MVP и приёмка

## Цель

Доказать полный путь одного вывода на синтетическом кейсе без изменения DEV v1.

```text
CASE-SYNTH-0001 → synthetic source → capture + SHA-256 → claim
→ two entities → typed relation → 3 independent opinions
→ disagreement matrix → human-reviewed finding
→ one-page report → redacted export manifest
```

## Этапы

- **M0 Contracts:** docs, ADR, schemas, fixtures, validation report.
- **M1 Read-only viewer:** case/source/graph/dossier/path-to-conclusion.
- **M2 Evidence workflow:** captures, claims, opinions, consensus, human review, audit.
- **M3 Three passive adapters:** DNS/cert metadata; web/archive; document metadata. Только synthetic/owned/authorized targets.
- **M4 Formal reporting:** report, annex links, redacted export, GitHub/Drive mapping.

## Acceptance gates

### Contracts
- [ ] Schemas проходят meta-schema validation.
- [ ] Fixtures проходят schemas.
- [ ] IDs стабильны, ссылки разрешимы.
- [ ] Нет реальных ПДн/доменов/обвинений.

### Evidence
- [ ] Claim содержит source_id.
- [ ] Capture содержит hash/timestamp/storage URI.
- [ ] Finding открывается до claims/sources.
- [ ] FACT имеет human approval.
- [ ] Hypothesis не показана как fact.

### Zoo
- [ ] Opinion хранит analyzer/version/input hash.
- [ ] First pass независим.
- [ ] Dissent не удаляется.
- [ ] Копии одной family не считаются независимыми.
- [ ] Remote analyzer не получает запрещённые классы.
- [ ] Analyzer не пишет FACT напрямую.

### Tools
- [ ] Нет запуска без adapter.
- [ ] Safety class проверяется policy.
- [ ] Active mode требует authorization + human confirmation.
- [ ] Raw/normalized output/run manifest связаны.

### Export
- [ ] Restricted/PROHIBITED блокируются.
- [ ] ПДн минимизированы.
- [ ] Metadata очищены.
- [ ] Manifest hashes совпадают.
- [ ] Reviewer утвердил экспорт.

### Baseline
- [ ] Diff ограничен `docs/osint-platform/**`.
- [ ] `father_osint/**`, `poc/**`, `legacy/**`, existing tests не изменены.
- [ ] PR показывает zero product-code diff.
- [ ] После будущего внедрения DEV v1 tests остаются green.

## Definition of Done v0.1

Отдельная ветка; draft PR к Issues #20/#21; schemas/fixtures validated; threat model/ADR; NO-PROD-CODE boundary; review до реализации.
