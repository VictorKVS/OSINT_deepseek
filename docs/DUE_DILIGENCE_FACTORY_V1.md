# FATHER OSINT Due Diligence Factory v1

## Purpose

Provide a repeatable, evidence-first production pipeline for checks of:

- Russian organizations and individual entrepreneurs (`RU_ORG`);
- people connected with Russian business or public roles (`RU_PERSON`);
- foreign organizations (`INTL_ORG`);
- foreign people (`INTL_PERSON`).

The factory produces research plans, jobs and auditable drafts. It does not make final employment, contracting, sanctions or guilt decisions.

## State model

```text
NEW → LEGAL_GATE → IDENTITY_LOCK → PLANNED → COLLECTING
→ NORMALIZING → ANALYZING → RED_TEAM → REVIEW
→ DECISION → MONITORING | CLOSED
```

A source job uses:

```text
PLANNED → QUEUED → RUNNING
→ FOUND | NO_HIT | BLOCKED | CONFLICT | ERROR
→ REVIEWED
```

`NO_HIT` is always scoped to a source, query, time and search boundary. It is not proof that a fact does not exist.

## Five permanent streams

1. `ENTITY_REGISTRY`
2. `BUSINESS_FINANCIAL_OPERATIONS`
3. `DIGITAL_FOOTPRINT`
4. `LEGAL_SANCTIONS_ADVERSE`
5. `RED_TEAM_SOURCE_QUALITY`

Streams fan out after the identity gate and write to one case, one evidence model and one journal.

## Identity Lock

Organization:

```text
official name + jurisdiction + registration/tax identifier
```

Person:

```text
full name in original spelling + jurisdiction + distinguishing context
+ at least two practical distinguishers
```

The engine never merges namesakes automatically. `automatic_merge_performed` must stay `false`.

## Evidence model

```text
SOURCE → CAPTURE → SOURCE_CLAIM / OBSERVATION
→ ENTITY / RELATION CANDIDATE
→ ANALYST FINDING
→ RISK → RECOMMENDATION → AUTHORIZED DECISION
```

Tool output, LLM output, fuzzy name similarity and sanctions name matches are not facts.

## Depth profiles

- `SCREENING`: minimum five-stream coverage and early risk triage.
- `STANDARD`: every mandatory source family in the selected profile.
- `ENHANCED`: standard plan plus cross-border, multilingual, intellectual-property, disciplinary and cross-case pivots.

## Country packs

International profiles require a country pack. A pack contains jurisdiction-specific source overrides, language/transliteration handling, sanctions packs and source-health controls. Country packs are data and must be versioned independently from code.

Initial templates:

- `RU`
- `GENERIC_INTL`
- `EU`
- `UK`
- `US`

They are planning templates, not a guarantee that every source adapter is connected or legally available.

## Parallel execution

The runner uses bounded workers and independent job outputs. Adapter failure is isolated. Missing adapters return `BLOCKED / ADAPTER_NOT_CONNECTED`; they are never silently treated as `NO_HIT`.

## Coverage gate

Ready for human review requires:

- all mandatory jobs represented;
- no non-terminal jobs;
- no unresolved `CONFLICT`;
- no mandatory `BLOCKED` or `ERROR` state;
- every negative result carrying a scoped `NO_HIT` explanation.

Technical coverage does not itself establish analytical sufficiency or truth.

## Journal

Every gate, plan and terminal job result is appended to a canonical JSON hash chain. A changed historical event invalidates subsequent verification.

## Current implementation boundary

The first increment contains:

- four profiles;
- five-stream planning;
- identity gate;
- passive-only policy gate;
- bounded parallel runner;
- synthetic adapters;
- coverage gate;
- hash-chain journal;
- atomic case package persistence;
- Russian Markdown review report;
- offline CLI demo and regression tests.

Live official/commercial source adapters are the next controlled increment. They must declare source identity, access method, version, rate limit, data boundary, evidence capture mode and legal limitations.
