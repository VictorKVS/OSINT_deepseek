# FATHER OSINT Agent Standard v1

Status: ACCEPTED FOR MVP

## Occam principle

Do not add an agent, layer, rule, metric, or data structure unless the current task needs it for acceptable quality or risk.

## Responsibility boundary

OSINT Agent is a collection worker.

It receives a ResearchTask from Analyst and returns a MaterialPackage.

It SHALL:
- search allowed sources;
- download/preserve relevant material;
- record source, time and locator;
- perform obvious content deduplication;
- report collection errors and stop reason;
- accept follow-up research tasks.

It SHALL NOT:
- decide what is true;
- select technologies or products;
- publish Knowledge Objects;
- assign final confidence to claims;
- replace Analyst or Socrates;
- perform intrusive collection or access bypass.

## Knowledge Factory handoff

ANALYST → ResearchTask → OSINT → MaterialPackage → ANALYST → Analysis → SOCRATES → Review → Knowledge Gate → KB

Analyst may request more material. Socrates may request counter-evidence or fresher sources. The loop stops when additional research is unlikely to materially change the decision, or the task budget/time limit is reached.

## Depth modes

- FAST — minimum search, routine/learning tasks.
- NORMAL — standard collection and basic source diversity.
- DEEP — broad source coverage and follow-up research.
- CRITICAL — maximum justified depth, independent checks and human approval where required.

## MVP data objects

Only four objects are mandatory in the OSINT component:

- ResearchTask
- Material
- MaterialPackage
- Collector adapter

Storage/audit files are implementation details and may evolve.

## First delivery

The Python package `father_osint` implements the contracts, append-only local storage, SHA-256 obvious deduplication, collector isolation and MaterialPackage handoff. Telegram is the first planned real collector after transport PoC.