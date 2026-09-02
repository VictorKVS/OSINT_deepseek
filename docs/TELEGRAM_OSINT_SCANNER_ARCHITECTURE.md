# Telegram OSINT Channel Scanner — architecture and MVP

## Goal
Build a lawful, evidence-preserving scanner for public Telegram OSINT / investigations / threat-intelligence channels that learns **how strong analysts present information**, not just what they publish.

The scanner is intended to collect, normalize and compare public posts and the presentation techniques used in them, so OSINT_deepseek can reuse **presentation patterns** while keeping its own evidence standards.

## Scope boundary
- Public channels and public posts, or channels the operator is lawfully authorized to access.
- No bypass of Telegram access controls, no private-channel intrusion, no credential theft, no deanonymization by prohibited means.
- Store provenance for every item: channel, message id, URL, timestamp, edit timestamp, forwarded-from metadata if public, media metadata, retrieval time and content hash.

## What the scanner should learn
The primary object is not only the claim but the **information-delivery pattern**.

### 1. Executive framing
Detect whether the post begins with:
- one-line conclusion;
- risk label;
- “what happened / why it matters” pair;
- decision / recommendation;
- uncertainty qualifier.

### 2. Evidence presentation
Extract patterns such as:
- direct source link;
- screenshot of source;
- quoted fragment;
- source grading;
- primary vs secondary source distinction;
- “confirmed / likely / unconfirmed” labels;
- timestamp and archive reference;
- hashes / document IDs / transaction IDs / registration numbers.

### 3. Visual language
Recognize and catalogue:
- relationship graphs;
- route maps;
- timelines;
- before/after maps;
- annotated screenshots;
- document excerpts with highlighted fields;
- tables of persons/companies;
- risk matrices;
- transaction-flow diagrams;
- geolocation panels;
- “one screen for management” summaries.

### 4. Narrative structure
Classify common templates:
- FACT → SOURCE → SIGNIFICANCE;
- EVENT → ACTOR → ASSET → ROUTE → BENEFICIARY;
- WHO → WHAT → WHEN → WHERE → HOW → SO WHAT;
- CLAIM → EVIDENCE → COUNTEREVIDENCE → VERDICT;
- BEFORE → CHANGE → AFTER;
- PERSON → COMPANIES → PARTNERS → MONEY → LOGISTICS;
- SOURCE A + SOURCE B → convergence / conflict;
- hypothesis ladder with confidence changes.

### 5. Analyst craftsmanship
Capture useful micro-techniques:
- short headings;
- bolding only decision-relevant facts;
- separate “not established” box;
- explicit confidence;
- numbered investigative questions;
- entity aliases / transliterations;
- map legends;
- link shortening / source cards;
- distinction between physical route and documentary route;
- “what would falsify this conclusion” section.

## Architecture

```text
CHANNEL REGISTRY
      ↓
TDLib Collector
      ↓
Raw Message Store (immutable)
      ↓
Normalizer
      ↓
Media Metadata + Screenshots/Attachments Index
      ↓
Entity / Claim / Source Extractor
      ↓
Presentation Pattern Extractor
      ↓
Pattern Library
      ↓
Scoring + Comparison
      ↓
FATHER / Main Analyst Report Composer
```

## Reuse of current OSINT_deepseek
Use the existing TDLib PoC/runtime as the acquisition layer instead of introducing a second Telegram stack. The scanner should be a new bounded module on top of the proven collection contract.

Recommended package:

```text
father_osint/telegram_scanner/
    collector.py
    channel_registry.py
    normalizer.py
    media_index.py
    presentation_patterns.py
    scoring.py
    models.py
    export.py
```

## Data model

### ChannelRecord
```json
{
  "channel_id": "tg:...",
  "username": "...",
  "title": "...",
  "language": ["ru","en"],
  "category": ["osint","investigations","threat_intel"],
  "trust_tier": "A|B|C|D",
  "active": true,
  "notes": "..."
}
```

### MessageRecord
```json
{
  "channel_id": "...",
  "message_id": 123,
  "published_at": "...",
  "edited_at": "...",
  "text": "...",
  "url": "...",
  "forward_origin": "...",
  "media": [],
  "retrieved_at": "...",
  "sha256": "..."
}
```

### PresentationPatternRecord
```json
{
  "message_ref": "tg:channel:123",
  "hook_type": "executive_summary",
  "has_timeline": true,
  "has_graph": true,
  "has_map": false,
  "has_source_card": true,
  "has_confidence_label": true,
  "has_not_established_section": true,
  "claim_source_ratio": 0.86,
  "visual_density": "medium",
  "management_read_time_sec": 75,
  "patterns": ["FACT_SOURCE_SIGNIFICANCE","CLAIM_COUNTEREVIDENCE_VERDICT"]
}
```

## Scoring
Do not rank by popularity alone. Separate at least five dimensions:

1. **Evidence discipline** — traceable source per material claim.
2. **Clarity** — conclusion is understood quickly.
3. **Visual utility** — image/map/graph carries analytical value rather than decoration.
4. **Uncertainty hygiene** — facts, source claims, inference and hypothesis are separated.
5. **Actionability** — reader understands the next investigative step or decision.

Score 0–5 for each dimension and keep the explanation.

## MVP

### MVP-1 — Collector
- registry of 20–30 public OSINT/TI channels;
- fetch latest N messages;
- preserve raw text, timestamps, links, media metadata and hashes;
- deduplicate forwarded/reposted content;
- append-only collection journal.

### MVP-2 — Presentation analyzer
For each post detect:
- headline / hook;
- conclusion sentence;
- source links;
- presence of image/document/map/graph;
- entities and identifiers;
- uncertainty phrases;
- recommendation / next step;
- structure template.

### MVP-3 — “Best techniques” digest
Daily/weekly output:

```text
TOP PRESENTATION PATTERNS THIS PERIOD
1. One-screen executive summary — 7 examples
2. Route map + documentary route split — 4 examples
3. Claim / counterclaim / verdict — 9 examples
4. Annotated primary document — 12 examples
5. Timeline with confidence changes — 6 examples
```

For each pattern save 1–3 source examples and a neutral reusable template.

### MVP-4 — Report composer integration
When Main Analyst builds a report, suggest presentation components based on evidence shape:
- many locations → route map;
- many owners/directors → relationship graph;
- many dated events → timeline;
- source conflict → comparison table;
- complex uncertainty → fact/inference/hypothesis matrix;
- management audience → 1-page executive brief first.

## Channel registry strategy
Do not hard-code “best channels” once. Maintain categories:
- OSINT methodology;
- corporate investigations;
- sanctions / trade / logistics;
- crypto investigations;
- geolocation;
- cyber threat intelligence;
- verification / fact-checking;
- investigative journalism;
- data visualization / mapping.

Each channel gets a reason for inclusion and a trust grade.

## Search and monitoring modes

### Mode A — Presentation learning
Scan broadly and learn formatting / analytical patterns.

### Mode B — Case watch
Search selected channels for case entities, aliases, company names, registration numbers, wallet addresses, domains and route locations.

### Mode C — Trend watch
Detect emerging tools, databases, workflows, Telegram bots, public datasets and visualization techniques mentioned repeatedly by independent channels.

## UI idea
Add a **Telegram Scanner** page to OSINT_deepseek:

```text
[CHANNELS] [NEW POSTS] [PATTERNS] [TOOLS] [CASE HITS] [BEST EXAMPLES]

Post card:
Channel | date | trust | topic
Conclusion
Sources: 4
Visuals: graph + document
Patterns: FACT→SOURCE→SIGNIFICANCE
Score: Evidence 5 / Clarity 4 / Visual 5 / Uncertainty 5 / Actionability 4
[Open original] [Save pattern] [Attach to case]
```

## Tool / technique extraction
Create a separate `TechniqueRecord` when posts mention a reusable OSINT technique or tool.

Fields:
- tool / service name;
- use case;
- source channel/message;
- platform / OS;
- input/output;
- legality / access notes;
- duplicate mentions across channels;
- verification status;
- candidate for local lab test.

This becomes a controlled **OSINT capability radar** rather than an uncurated tool list.

## Acceptance gates
MVP is accepted only when:
- a repeated run does not duplicate the same Telegram message;
- every stored post has channel/message/timestamp/retrieved_at/hash;
- forwarded copies are linked, not silently merged;
- presentation-pattern extraction is explainable from observable features;
- no private-channel bypass is implemented;
- at least 20 channels and 500 posts can be processed reproducibly;
- best-pattern digest links every example back to its Telegram source;
- Main Analyst can consume selected patterns without copying unsupported claims.

## First implementation order
1. Channel registry schema.
2. TDLib collection adapter using current PoC.
3. Raw append-only store + deduplication.
4. Presentation pattern extractor.
5. Technique/tool extractor.
6. Digest generator.
7. UI cards.
8. Case-watch integration.

## Core principle
The scanner must learn **how good OSINT is communicated** while OSINT_deepseek keeps stricter provenance than the source channels themselves.

We copy the *pattern*, never the unsupported conclusion.
