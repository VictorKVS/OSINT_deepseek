# ALINA Research Advisor — contract v0.1

Status: **local browser prototype implemented**; live RAG, LLM, Telegram discovery and task execution **not connected**.

## Purpose
Help a human analyst turn an OSINT topic into a traceable search strategy, discover and shortlist relevant public Telegram channels, and prepare a machine-readable research plan. A right-hand advisor panel is implemented as a standalone linked page pending integration into the main channel workspace.

## Modes
- `auto`: calculate a candidate shortlist using the user-defined threshold and limit. Does **not** start collection or bypass authorization.
- `review` (default): calculate shortlist, mark it `awaiting_human_approval`; analyst can adjust checkboxes.
- `manual`: only explicitly checked channels are selected.

## Input and output
Input: topic, goal, language, selection mode, score threshold, maximum sources, optional JSON channel catalog. Supported catalog: array of channels or `{channels:[...]}`, including output of `tools/telegram_channel_catalog.py`.

Output: `father_telegram_research_plan.json` with prompt, query suggestions, selection mode, selected channels, reasons, weights and caveats. No backend/network transmission.

## Explainable initial scoring
60 points: lexical topic overlap with title/topics/notes.
20 points: verified status.
10 points: nonzero evidence count **and** verification date.
10 points: subscriber/post measurements **and** verification date.
Language mismatch excludes candidate. Scores are **preliminary relevance heuristics**, not authoritative channel rankings. Empty metrics do not imply zero subscribers or zero quality. No synthetic example should be mistaken for a real channel.

## Future RAG pipeline
Task -> policy/authorization -> retrieval from ALINA's versioned knowledge graph and evidence corpus -> cited search-query expansion -> candidate discovery adapters -> identity resolution -> observation snapshots -> explainable ranking -> human review / controlled auto-selection -> authorized collection -> ALINA Skill Factory.

RAG output must include source reference, passage, retrieval timestamp, confidence and evidence limits. Model suggestions never become facts without source verification. Prompt-injection defenses: treat retrieved Telegram text as untrusted data, not execution instructions.

## Acceptance checks
1. Page loads with visible demo-only candidates.
2. Topic/language filters affect score and selection.
3. Default review mode proposes channels but does not execute a collector.
4. Manual mode respects only checked entries.
5. Auto mode applies threshold and maximum.
6. Imported catalog supports registry schema; malformed or oversized input is rejected.
7. Exported JSON contains chosen IDs, reasons, criteria, generated time, search prompts and nonexecution caveats.
8. No credentials, sessions, API keys or client data are accessed.
9. Verify integration navigation from index and Telegram workspace.

## Next implementation
Connect the advisor to a real verified registry, implement retrieval-backed citations and a queue requiring policy approval before any network collection. Keep ALINA LAB independent of B2B client datasets.
