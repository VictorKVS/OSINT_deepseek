# Stage 03 — Business Analysis

**Project:** OSINT_deepseek / FATHER Knowledge Factory  
**Scope:** first practical Knowledge Factory worker and its handoff to Analyst/Socrates  
**Status:** DRAFT FOR ARCHITECTURE REVIEW

## 1. Business objective

The system must reduce the cost and inconsistency of repeated technology research. It should preserve research materials and make them reusable by later analysts and FATHER role agents instead of forcing each new project to rediscover the same sources from scratch.

The OSINT worker is therefore a **supplier of research material**, not a truth engine and not a final expert.

### Business result

```mermaid
flowchart LR
    P[Project / Expert needs evidence] --> Q[Research request]
    Q --> O[OSINT collection]
    O --> A[Analyst]
    A --> S[Socrates review]
    S --> K[Knowledge Gate / KB]
    K --> R[Role Agents / Projects]
    R --> X[New experience]
    X --> K
```

The value is created when later work can reuse checked material and knowledge with known provenance.

## 2. Business boundaries

### In scope for DEV

- receive a research task from Analyst;
- acquire materials through approved DEV collectors/fixtures;
- preserve source locator, raw content or file reference, collection time and metadata;
- remove obvious exact duplicates;
- return a bounded Material Package;
- allow Analyst to request additional research;
- allow Socrates to request additional evidence;
- keep the process inspectable and reproducible enough for tests.

### Out of scope for DEV

- autonomous truth determination;
- autonomous publication into production KB;
- production Telegram/Tor credential operations;
- complex source trust scoring;
- knowledge graphs;
- autonomous purchasing, intrusion or access-control bypass;
- production scheduler, proxy rotation or large-scale crawling.

## 3. Actors and responsibilities

| Actor | Responsibility | Must not do |
|---|---|---|
| Requester / Project | expresses information need | dictate an unverified technical solution |
| Analyst | converts need into a ResearchTask; interprets returned materials | pretend missing evidence exists |
| OSINT Agent | finds/preserves requested material | decide final truth or architecture |
| Collector | acquire one source class and map it to Material | perform cross-domain analysis |
| Socrates | challenge material sufficiency and analysis | generate endless questions without decision impact |
| Knowledge Gate | future publication control | replace Analyst/Socrates reasoning |
| FATHER | future orchestration and role/KB assignment | act as the domain expert itself |

## 4. SIPOC

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| Analyst, project context, source systems | ResearchTask, topics, source types, limits | collect → normalize → deduplicate → package | MaterialPackage | Analyst |
| Analyst | MaterialPackage | analyze → identify findings/gaps | Analysis / follow-up task | Socrates / OSINT |
| Socrates | Analysis + materials | challenge material sufficiency | PASS / RESEARCH_MORE | Knowledge Gate / OSINT |

## 5. Value stream

```mermaid
flowchart TD
    N[Information need] --> T[ResearchTask]
    T --> C[Collect]
    C --> P[Preserve provenance]
    P --> D[Exact deduplication]
    D --> M[MaterialPackage]
    M --> A[Analysis]
    A --> G{Evidence gaps?}
    G -->|yes| T2[Follow-up ResearchTask]
    T2 --> C
    G -->|no| S[Socrates review]
    S --> R{Material weakness changes decision?}
    R -->|yes| T3[Targeted research]
    T3 --> C
    R -->|no| O[Stage output]
```

### Stop principle

Research stops when the current decision can proceed with the accepted uncertainty, or when the configured time/item/cycle limit is reached. More information is not automatically more value.

## 6. IDEF0-style functional decomposition

```mermaid
flowchart LR
    I1[Input:\nResearchTask] --> F0[F0\nProvide research material]
    C1[Controls:\nТЗ, depth, source types, max_items, DEV policy] --> F0
    M1[Mechanisms:\nOSINTAgent, collectors, store] --> F0
    F0 --> O1[Output:\nMaterialPackage]
```

Decomposition:

```mermaid
flowchart TD
    F0[F0 Provide research material] --> F1[F1 Validate task]
    F0 --> F2[F2 Select eligible collectors]
    F0 --> F3[F3 Acquire materials]
    F0 --> F4[F4 Preserve + exact deduplicate]
    F0 --> F5[F5 Package results/errors]
    F0 --> F6[F6 Return to Analyst]
```

## 7. Information contract from a business perspective

### ResearchTask — order to the research worker

Must answer at minimum:

- what question is being investigated;
- which topics are relevant;
- which source classes are requested;
- optional time boundaries;
- work depth;
- maximum material count / stop condition;
- who requested the work.

### Material — acquired evidence candidate

Must answer at minimum:

- where it came from;
- what was captured;
- when it was collected;
- source publication time if known;
- author if known;
- metadata needed by the source class;
- stable content hash where possible.

### MaterialPackage — delivery note

Must answer at minimum:

- which task it fulfils;
- which materials were found;
- which obvious duplicates were skipped;
- which collection failures occurred;
- why collection stopped.

## 8. Business rules

1. OSINT may return **zero** materials; this is a valid result and must be visible.
2. Collector failure does not automatically destroy results from other collectors.
3. Missing source type is a gap, not a fabricated result.
4. Exact duplicate removal may reduce storage/analysis noise, but does not prove source dependence or truth.
5. Analyst or Socrates may return a targeted follow-up request.
6. DEV loops are bounded to prevent endless research.
7. All production-only concerns remain explicitly deferred until DEV behavior is accepted.

## 9. Business risks

| Risk | Impact | Architectural response in DEV |
|---|---|---|
| research loops never stop | cost/time explosion | max cycles / max items |
| source failure hides coverage gap | false confidence | collection_errors + gap reporting |
| OSINT starts making expert conclusions | role contamination | Material contract only |
| implementation grows before requirements stabilize | long rework | NO CODE BEFORE CONTRACT gate |
| legacy/experimental code is mistaken for approved architecture | maintenance risk | explicit repository status and architecture review |
| same material appears many times | analyst noise | exact content hash deduplication |

## 10. Success criteria for Stage 3

Architecture is business-acceptable only if every major arrow in the diagrams has:

- an owner;
- a defined input;
- a defined output;
- an error/stop behavior;
- a reason for existing;
- a requirement or business rule that justifies it.

Anything that cannot satisfy those six questions is a candidate for `DELETE`, `DEFER` or redesign.
