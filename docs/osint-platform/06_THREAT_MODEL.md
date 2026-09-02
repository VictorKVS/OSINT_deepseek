# 06. Модель угроз OSINT-контура

## Активы

Captures/hashes; source registry; claims/findings/decisions; ПДн; authorization/scope; model/tool registry; prompts/rulesets/calibration; audit trail; reports; secrets; доверие руководителя.

## Доверительные границы

1. Internet → collector.
2. Capture quarantine → normalizer.
3. Evidence store → analysis zoo.
4. Local system → remote provider.
5. Analyst UI → backend.
6. Orchestrator → WSL/container/remote worker.
7. Restricted store → GitHub/Drive export.
8. Exploratory finding → official decision.

## Угрозы и меры

| Угроза | Контроль |
|---|---|
| Prompt injection в источнике | content-as-data, prompt isolation, schema, no tool authority |
| Data poisoning | source independence, captures, contradictions, Red Team |
| Hallucination | evidence refs, no direct FACT promotion |
| Cross-case leakage | case tenancy, scoped retrieval, access tests |
| Remote exfiltration | data-boundary policy, local-only profiles, redaction |
| Tool abuse | registry, safety class, scope, sandbox |
| Evidence tampering | immutable storage, SHA-256, audit/revision chain |
| Identity merge error | candidate merge, identifiers, human review |
| Groupthink | blind opinions, contrarian, dissent preservation |
| Malicious attachment | quarantine, no macros, isolated parser |
| SSRF/path traversal | allowlists, network policy, canonical paths |
| Secret leakage | secret store, log/export scanning |
| PII overcollection | purpose limitation, minimization, retention |
| Supply chain | pinned versions, hashes/signatures, sandbox |
| Model drift | exact version, calibration, regression fixtures |
| Stale law/source | effective-date/version checks |
| Misleading visualization | textual status, official view, reduced motion |

## Abuse cases

### AC-01: источник приказывает модели игнорировать политику
Текст остаётся evidence; модель не получает полномочий; output ссылается на source/locator.

### AC-02: пять агентов назвали лицо виновным
Это opinions, не sources; FACT не создаётся; reviewer видит отсутствие компетентного доказательства.

### AC-03: запуск активного scanner по внешней цели
`PASSIVE_PUBLIC` блокирует. Нужны `ACTIVE_AUTHORIZED`, target scope и human confirmation.

### AC-04: скрытые ПДн в metadata
Export очищает metadata и блокирует manifest при нарушении.

### AC-05: capture заменён после отчёта
Hash mismatch; report invalid; audit alert.

## Security acceptance

- zero unrestricted shell by default;
- zero direct model→tool authority;
- zero direct LLM→FACT;
- zero public export with restricted data;
- all captures hashed;
- all high-impact findings challenged;
- all runs reproducible at manifest level;
- all manual edits audited.
