# 04. Управляемый аналитический «зоопарк»

## Решение

Разрешено использовать множество моделей, правил, алгоритмов и специализированных анализаторов. «Зоопарк» — не голосование за истину, а система независимых воспроизводимых мнений.

```text
Evidence Bundle
  ├─ deterministic extractor
  ├─ entity/link analyzer
  ├─ temporal consistency analyzer
  ├─ contradiction analyzer
  ├─ source reliability analyzer
  ├─ graph algorithms
  ├─ local text LLM A
  ├─ local text LLM B
  ├─ vision/audio/media pipeline
  ├─ legal/regulatory ruleset
  └─ Red Team analyzer
        ↓
  ANALYSIS_OPINIONS
        ↓
  Consensus + disagreement matrix
        ↓
  Human evidence review
        ↓
  FACT / INFERENCE / HYPOTHESIS / RISK
```

## Почему не одна модель

LLM собирает контекст, но может выдумывать связность; правила воспроизводимы, но узки; граф находит структуру, но не доказывает смысл; media pipeline зависит от качества; source-rater не устанавливает содержание; Red Team ищет альтернативы, но сам не устанавливает истину.

Разногласие — сигнал, который нельзя усреднять и скрывать.

## Реестр анализаторов

Каждый анализатор хранит:

- `analyzer_id`, family/type, provider/runtime;
- exact model/tool/version;
- modality;
- allowed access classes;
- local/remote data boundary и network policy;
- input/context limits;
- prompt/template hash и параметры;
- calibration dataset/version;
- known failure modes;
- cost/latency metrics;
- owner, approval, retirement/supersession.

Remote model не получает `AUTHORIZED_INTERNAL`/`RESTRICTED` без отдельного policy decision.

## Независимость

Для high-impact задач:

1. минимум два независимых анализа;
2. по возможности разные family/provider;
3. обязательный challenge/contrarian;
4. blind first pass;
5. arbiter не удаляет dissent;
6. reviewer видит majority и minority.

Пять копий одной model family не являются пятью независимыми экспертами.

## Opinion

Opinion не является finding. Он содержит task, input refs/hash, answer, supporting/contradicting refs, assumptions, limitations, confidence decomposition, data boundary, analyzer version, timestamp и output hash.

Число `confidence: 0.93` без драйверов запрещено.

## Consensus

Хранит common ground, disagreements, minority views, causes, unresolved questions, next collection и human-review requirement.

## Защита от groupthink

- dedup по model family;
- раздельные prompts extraction/analysis/challenge;
- blind first pass;
- contrarian slot;
- raw outputs;
- calibration fixtures;
- disagreement и unsupported-claim metrics;
- запрет самооценки модели как единственной меры качества.

## Специализации

- **Текст:** entity/claim extraction, translation, contradiction, chronology, report drafting.
- **Граф:** communities, shortest evidence path, temporal motifs, centrality, duplicate identity candidates.
- **Медиа:** metadata, segmentation, transcript, edit consistency, audio/subtitle mismatch.
- **Право:** applicable-source/version/effective-date/scope candidates.

Graph score не доказывает контроль/вину/причинность. Media признаки не означают «подделка» без экспертизы. Legal analyzer не заменяет заключение.

## Human gates

Обязательны для FACT, high/critical RISK, attribution, правового вывода, ПДн, public export, active tool run и решения руководителю.

## Метрики

Evidence coverage; unsupported claim rate; contradiction recall; analyst acceptance/rejection; false positives; disagreement; change after Red Team; reproducibility; cost per accepted finding; time to evidence-backed conclusion; cross-case leakage incidents = 0.
