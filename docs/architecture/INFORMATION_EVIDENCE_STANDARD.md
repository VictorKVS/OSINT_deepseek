# Information & Evidence Standard

**Status:** foundational architecture standard  
**Scope:** all future FATHER expert subsystems, beginning with OSINT / Telegram M5.

## Principle

FATHER is an expert system. Information is not accepted as an unstructured blob. Every material, observation, evidence item and claim must preserve enough context to answer:

- what is this;
- where did it come from;
- when did it exist / when was it observed;
- how was it acquired;
- whether it is primary, derivative or reposted;
- what other sources repeat or independently corroborate it;
- where the information propagated;
- what part of the research question it can support;
- what it cannot support;
- what contradictory information exists;
- what search coverage was achieved;
- what important gaps remain.

## Mandatory dimensions

### 1. Source identity
- source type;
- source locator;
- stable source/account/channel/site/document identifier where available;
- source owner/author when known;
- source class: primary / secondary / tertiary / unknown.

### 2. Temporal context
Preserve distinct timestamps where possible:
- event time;
- publication time;
- edit/update time;
- acquisition/observation time;
- archival snapshot time.

Do not collapse these into one generic `timestamp`.

### 3. Provenance and acquisition context
- acquisition method;
- transport/tool and version when material;
- query/search-plan step that produced the item;
- operator/agent run identity;
- raw payload hash;
- transformations/normalization performed;
- original/raw preservation status.

### 4. Propagation / diffusion
Where applicable record:
- origin candidate;
- forwards/reposts/copies;
- references/links;
- first-seen and later-seen observations;
- channels/platforms reached;
- propagation path confidence;
- whether copies are independent evidence or derivative repetitions.

A hundred copies of one original report are not treated as one hundred independent confirmations.

### 5. Information quality dimensions
Keep dimensions separate:
- source reliability;
- information credibility;
- relevance;
- independence;
- recency;
- directness;
- corroboration;
- provenance quality.

No uncalibrated aggregate number is treated as probability of truth.

### 6. Coverage and sufficiency
For each research package preserve:
- intended search scope;
- source classes targeted;
- sources attempted;
- sources successfully searched;
- source failures/exclusions;
- temporal coverage;
- geographic/entity coverage where relevant;
- counter-evidence search coverage;
- critical gaps;
- achieved sufficiency level: MINIMUM / GOOD / DESIRED / INSUFFICIENT.

### 7. Contradictions and alternatives
The system must be able to represent:
- evidence supporting a hypothesis;
- evidence contradicting it;
- alternative explanations;
- unresolved ambiguity;
- evidence that is merely consistent but not confirmatory.

### 8. Evidence-to-claim traceability
Every analytical claim must be traceable to evidence/material IDs. Claims must not silently inherit the apparent authority of a source without explicit evidence linkage.

## Canonical information lineage

```text
SOURCE
  ↓
RAW PAYLOAD
  ↓
OBSERVATION
  ↓
MATERIAL
  ↓
EVIDENCE ASSESSMENT
  ↓
EVIDENCE PACKAGE
  ↓
CLAIM
  ↓
ANALYTICAL CONCLUSION
  ↓
KNOWLEDGE GATE
```

Each transformation preserves provenance to the prior layer.

## Expert responsibilities

### OSINT Expert
Owns search strategy, source discovery, acquisition, provenance, verification, propagation mapping, coverage accounting and evidence-package preparation.

### Analyst
Owns interpretation of what the collected evidence means. Analyst must receive enough metadata to understand source class, provenance, quality, coverage, contradictions and limitations rather than receiving a folder of opaque files.

### Socrates / Critic
Challenges whether evidence actually supports the claim, whether search coverage is sufficient, whether independent confirmation exists, whether counter-evidence was sought and whether alternative explanations remain.

## Search Intelligence vs world knowledge

Separate:

1. **Search Intelligence KB** — how to search, source/platform/tool knowledge, runbooks, failure modes and validated operational experience.
2. **Investigation / Evidence KB** — what was observed and collected in investigations.
3. **Analytical Knowledge / Graph** — conclusions that passed analytical review / Knowledge Gate.

Do not merge professional search know-how with facts about the world.

## Telegram proving-ground implications

Telegram M5 must begin exercising this standard through:
- channel/account identity;
- message identity;
- publication/edit/acquisition time;
- forwards/replies/links where available;
- repeated/copy propagation recognition;
- source/channel coverage;
- counter-evidence channel/search branch;
- sufficiency reporting;
- acquisition report for Analyst.

The standard is source-neutral; Telegram is only the first complete proving ground.
