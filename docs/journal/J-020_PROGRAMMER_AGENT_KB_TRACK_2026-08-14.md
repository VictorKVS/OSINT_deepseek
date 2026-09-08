# J-020 — Programmer Agent / PROGRAMMING_KB research track

Date: **2026-08-14**  
Status: **ACTIVE / PARALLEL RESEARCH TRACK**  
Critical-path impact: **NONE — M5 Telegram remains the active delivery milestone**

## Trigger

FATHER requires a Programmer Agent that can implement approved engineering tasks while explaining and proving material choices through sources, alternatives, risk analysis and verification evidence.

## Decision

Start a dedicated `docs/father_agents/programmer/` research track before executable agent code.

The first baseline contains:
- product passport and D0-D3 decision classes;
- PROGRAMMING_KB evidence model;
- verified authoritative-source seed register;
- measurable MIN/MEDIUM/MAX roadmap;
- 12-domain coverage matrix and explicit P0 gaps;
- append-only `TF-0015` record.

## WHY

The existing FATHER rule `NO CODE BEFORE CONTRACT` applies directly. Building another coding runtime before defining what counts as sufficient evidence would hard-code arbitrary technology preferences, uncalibrated confidence and citation theater.

The research track therefore proves the decision/evidence machinery first. Initial executable scope, when later authorized, is intentionally bounded to professional Python/backend tasks.

## Evidence baseline

Initial authoritative/consensus anchors verified for the source register:
- IEEE Computer Society SWEBOK Guide V4.0a;
- ISO/IEC 25010:2023;
- NIST SP 800-218 SSDF v1.1 FINAL;
- NIST SP 800-218 Rev.1 SSDF v1.2 draft — monitor, not controlling baseline;
- OWASP ASVS 5.0.0;
- SLSA v1.2;
- OpenSSF Scorecard.

The coverage matrix uses SWEBOK V4.0a as the profession map and reduces it into 12 operational FATHER Programmer domains. Initial unresolved blocking gaps: **10 P0**. MIN requires **0 P0**.

## Controls introduced

1. Material choices are classified D0-D3 so evidence depth scales with impact.
2. Sources are classified E0-E6 by evidential role.
3. A source count is never treated as sufficiency by itself.
4. Version-sensitive knowledge records source version/date/review/supersession.
5. D2/D3 decisions preserve alternatives, counter-evidence, residual risks and revisit conditions.
6. Context-dependent performance/reliability claims require reproducible project experiment evidence.
7. No synthetic confidence score is accepted before calibration on reviewed decisions.
8. Smallest sufficient complexity is the default; microservice/distributed boundaries require evidence.

## Result

**PARTIAL PASS.** The knowledge track, governance model, source seed and measurable roadmap exist. No Programmer Agent runtime is authorized yet.

## Next gate

1. Build canonical Python/PEP/CPython source cards.
2. Build HTTP/IETF, OpenAPI and PostgreSQL canonical source cards.
3. Create first validated Knowledge Objects.
4. Execute one complete D2 worked decision.
5. Principal Critic reviews evidence sufficiency and unnecessary-complexity controls.
6. Start the evaluation corpus before runtime orchestration is designed.

---

## RU — краткая фиксация

Создан отдельный исследовательский трек **Агента-программиста / PROGRAMMING_KB** внутри FATHER. Его задача — не просто писать код, а оставлять проверяемую цепочку:

```text
Требование → варианты → источники → применимость → риски → эксперимент → решение → код → тесты → доказательства
```

Текущий M5 Telegram не тормозится и не меняется. Исполняемый агент пока **не разрешён**: сначала должны быть доказаны правила работы базы знаний, достаточность источников, актуальность версий, counter-evidence и evaluation corpus.

Стартовые метрики MIN: 12/12 доменов, не менее 120 проверенных/ограниченно-применимых Knowledge Objects, не менее 20 decision scenarios, не менее 10 end-to-end реализаций и ноль P0-пробелов. Текущий стартовый P0 backlog: **10**.
