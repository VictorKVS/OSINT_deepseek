# 04. Windows ↔ Kali: производственное исполнение

## Три независимых канала

```text
COMMAND PLANE  — задания и статусы
EVIDENCE PLANE — captures, stdout/stderr, документы, hashes
AUDIT PLANE    — hash-chain journal, approvals, почтовое зеркало
```

## Ближайшая физическая схема

```text
WINDOWS CONTROL PLANE
  Case UI / Planner / Policy / Queue / Merge / Report
        ↓ signed typed job envelope
FILE SPOOL on G:  (MVP)  →  message bus with mTLS (target)
        ↓
WSL2 KALI WORKER
  registered adapter only
  Sherlock / Maigret / DNS / document tools / provider clients
        ↓
PER-JOB WORKSPACE
  manifest + stdout + stderr + raw result + SHA-256
        ↓
EVIDENCE VAULT
        ↓
WINDOWS NORMALIZER / ENTITY RESOLUTION / REPORT
```

Инструменты друг друга не вызывают. Каждый пишет только в собственный job directory; в общую модель пишет один merge service.

## Job envelope

Windows передаёт типизированный JSON, а не shell-строку:

```json
{
  "schema_version": "father-osint.screening-job.v1",
  "case_id": "CASE-001",
  "request_id": "REQ-001",
  "work_item_id": "WKI-...",
  "sequence": 17,
  "tool_id": "SHERLOCK",
  "adapter_version": "sherlock-v1",
  "input": {"type": "USERNAME", "value": "example"},
  "safety_class": "PASSIVE_PUBLIC",
  "network_policy": "PUBLIC_READ_ONLY",
  "timeout_seconds": 300,
  "expires_at_utc": "...",
  "payload_sha256": "..."
}
```

Worker обязан проверить schema, hash/signature, sequence, expiry, idempotency, adapter allowlist и policy. Пользовательское значение передаётся отдельным аргументом процесса, а не конкатенируется в shell.

## Файловая очередь MVP

```text
runtime/bus/
  outbox/
  accepted/
  running/
  completed/
  failed/
  blocked/
  cancelled/
  dead-letter/
  results/
  journal/
```

Запись выполняется через `.tmp → atomic rename`. Worker не читает незавершённые файлы.

## Почта

Закрытая почта используется как:

- зеркало значимых audit events;
- канал согласования sensitive jobs;
- аварийная доставка подписанных manifests.

Она не является основным job queue и не запускает вложения напрямую. Сырые доказательства в письма не прикладываются.

## Целевой transport

```text
FastAPI Control Plane
    ↓ mTLS
NATS JetStream / RabbitMQ
    ↓ mTLS
Windows / WSL2 / Kali VM / Container workers
    ↓ HTTPS/mTLS
Object Storage / Evidence Vault
```

Активные инструменты помещаются в отдельный тип дела и отдельную worker pool; screening factory остаётся пассивной.
