# OSINT Agent MVP v1

Status: IMPLEMENTATION BASELINE

## Role

OSINT Agent is the collection worker of the FATHER Knowledge Factory.

It does **not** decide what is true, choose technologies, or publish knowledge. It receives a research task, finds and preserves relevant materials, removes obvious duplicates, records provenance, and returns a material package to Analyst.

## Workflow

ANALYST → RESEARCH TASK → OSINT → MATERIAL PACKAGE → ANALYST

Analyst or Socrates may return a follow-up task when evidence is missing or counter-evidence is required.

## Input: ResearchTask

Minimum fields:

- task_id
- question
- topics
- source_types
- date_from / date_to (optional)
- max_items
- depth: FAST | NORMAL | DEEP | CRITICAL
- stop_when_enough
- requested_by

## Output: MaterialPackage

Minimum fields:

- package_id
- task_id
- created_at
- materials[]
- duplicates_skipped
- collection_errors[]
- notes

Each Material preserves:

- material_id
- source_type
- source_locator
- title
- raw_text or local_path
- published_at if known
- collected_at
- author/publisher if known
- content_hash
- metadata

## Stop rule

Stop when one of the following is true:

1. requested material quantity is reached;
2. Analyst-defined sufficiency condition is reached;
3. time/budget limit is reached;
4. no additional relevant sources are available.

The agent must report which stop condition fired.

## Occam constraints

MVP deliberately does not implement:

- truth/confidence engine;
- knowledge graph;
- entity resolution;
- causal reasoning;
- autonomous Knowledge Gate;
- autonomous expert recommendations.

Those stay in the architecture reserve until a real use case requires them.

## Safety boundary

Read-only collection by default. Respect authentication boundaries, platform terms, rate limits, privacy rules, copyright/licensing constraints, and applicable law. No credential theft, access bypass, intrusive collection, or autonomous account interaction.

## Implementation slice 1

The first code slice provides:

1. ResearchTask and Material data contracts;
2. append-only local MaterialStore (JSONL + raw files);
3. SHA-256 obvious deduplication;
4. MaterialPackage creation;
5. collector adapter contract so Telegram/GitHub/Web collectors can be plugged in later without changing the workflow.

The first real collector to be connected is Telegram Radar after transport PoC (TDLib vs GramJS).