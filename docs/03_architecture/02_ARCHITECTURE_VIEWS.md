# Stage 03 — Architecture Views

**Status:** DRAFT FOR REVIEW  
**Rule:** diagrams describe responsibilities and information movement, not a final technology stack.

## 1. System context

```mermaid
flowchart LR
    U[Project / Requester] --> A[Analyst]
    A -->|ResearchTask| O[FATHER OSINT Worker]
    O -->|MaterialPackage| A
    A -->|Analysis| S[Socrates]
    S -->|RESEARCH_MORE| A
    S -->|PASS| K[Knowledge Gate - planned]
    K --> KB[(Knowledge Base - planned)]
    KB --> RA[Role Agents - future]
```

The current repository implements only the DEV research side of this context. Knowledge Gate, production KB and FATHER orchestration are future boundaries, not approved implementation scope.

## 2. Logical component view

```mermaid
flowchart TB
    RT[ResearchTask contract]
    OA[OSINTAgent]
    CI[Collector interface]
    FC[FixtureCollector DEV]
    TC[TelegramCollector contract]
    TA[Transport Adapter experimental]
    MS[MaterialStore DEV]
    MP[MaterialPackage contract]
    AN[SimpleAnalyst DEV]
    SO[SimpleSocrates DEV]

    RT --> OA
    OA --> CI
    CI --> FC
    CI --> TC
    TC -. experimental .-> TA
    FC --> OA
    TC --> OA
    OA --> MS
    OA --> MP
    MP --> AN
    AN --> SO
    SO -->|targeted follow-up| RT
```

### Why each component exists

| Component | Reason | Current status |
|---|---|---|
| `ResearchTask` | stable order between Analyst and OSINT | candidate contract |
| `OSINTAgent` | bounded orchestration across source collectors | candidate implementation |
| `Collector` | isolate source-specific acquisition | candidate architecture |
| `FixtureCollector` | prove behavior without production infrastructure | DEV approved candidate |
| `TelegramCollector` | preserve future source boundary without locking transport | contract experiment |
| transport adapter | isolate MTProto/vendor mechanics | experimental / frozen |
| `MaterialStore` | inspectable DEV persistence and exact dedup | candidate implementation |
| `MaterialPackage` | stable research delivery object | candidate contract |
| `SimpleAnalyst` | verify handoff/gap cycle before LLM integration | DEV test double / prototype |
| `SimpleSocrates` | verify review/follow-up handoff | DEV test double / prototype |

## 3. Process view

```mermaid
sequenceDiagram
    participant Analyst
    participant OSINT
    participant Collector
    participant Store
    participant Socrates

    Analyst->>OSINT: ResearchTask
    OSINT->>Collector: collect(task)
    Collector-->>OSINT: Material(s) / error
    OSINT->>Store: preserve + exact hash dedup
    Store-->>OSINT: accepted / duplicate
    OSINT-->>Analyst: MaterialPackage
    Analyst->>Socrates: Analysis + package context
    alt evidence sufficient
        Socrates-->>Analyst: PASS
    else evidence gap matters
        Socrates-->>Analyst: RESEARCH_MORE
        Analyst->>OSINT: targeted ResearchTask
    end
```

## 4. Data flow view

```mermaid
flowchart LR
    R[ResearchTask] --> P1((P1 Collector selection))
    P1 --> P2((P2 Source acquisition))
    P2 --> M[Material]
    M --> P3((P3 Preserve / exact dedup))
    P3 --> DS[(DEV Material Store)]
    P3 --> P4((P4 Package result))
    P4 --> MP[MaterialPackage]
    MP --> P5((P5 Analyst review))
    P5 --> A[Analysis]
    A --> P6((P6 Socrates review))
    P6 --> PASS[PASS]
    P6 --> FU[Follow-up ResearchTask]
```

### Data ownership

- ResearchTask is owned by the requester/Analyst boundary.
- Raw Material is owned by the research collection stage after capture.
- MaterialPackage is the OSINT delivery unit.
- Analysis belongs to Analyst.
- Review belongs to Socrates.
- None of these DEV objects is automatically `Knowledge`.

## 5. Failure view

```mermaid
flowchart TD
    T[ResearchTask] --> C1[Collector A]
    T --> C2[Collector B]
    T --> C3[Collector C]
    C1 -->|success| M1[Materials]
    C2 -->|failure| E[collection_errors]
    C3 -->|success| M3[Materials]
    M1 --> P[MaterialPackage]
    M3 --> P
    E --> P
    P --> A[Analyst sees both evidence and coverage gap]
```

Architecture requirement: one source failure should be visible without automatically discarding useful results from other independent collectors.

## 6. DEV/PROD boundary

```mermaid
flowchart LR
    subgraph DEV[Current DEV / simplified]
      F[Fixtures]
      LC[Local collectors]
      LS[Local inspectable storage]
      SA[SimpleAnalyst]
      SS[SimpleSocrates]
    end

    subgraph PROD[Future PROD - not approved]
      TG[Real Telegram MTProto]
      WEB[Web/RSS crawler]
      DARK[Isolated Tor/Dark Web]
      SCH[Scheduler/retries/rate limits]
      SEC[Secrets/proxy/monitoring]
      PKB[Production Knowledge Gate/KB]
    end

    DEV -. same contracts where justified .-> PROD
```

The purpose of DEV is to prove the business contract before buying operational complexity.

## 7. C4-style container-neutral view

```mermaid
flowchart TB
    EXT[External information sources]
    COL[Acquisition boundary]
    ORCH[Research orchestration]
    STORE[Material persistence]
    ANA[Analysis boundary]
    REV[Review boundary]

    EXT --> COL
    COL --> ORCH
    ORCH --> STORE
    ORCH --> ANA
    ANA --> REV
    REV -->|follow-up| ORCH
```

No database engine, queue, framework or LLM provider is implied by this view.

## 8. Interface boundaries to verify before Stage 4

### Analyst → OSINT

`ResearchTask` must be sufficient to execute bounded acquisition without requiring hidden conversation context.

### Collector → OSINT

Collector must return source-specific material through a common `Material` boundary or a visible failure. It must not decide final truth.

### OSINT → Analyst

`MaterialPackage` must preserve materials plus coverage/error/stop information. It must not hide incomplete collection.

### Analyst/Socrates → OSINT

Follow-up must be expressible as another bounded `ResearchTask`; no side-channel instructions should be required.

## 9. Architecture questions still open

1. Is exact hash deduplication enough for DEV acceptance, or is source-locator dedup also required?
2. Should `MaterialStore` own task/package persistence or only material persistence?
3. Do `pipeline.py` and `review_pipeline.py` represent two valid scenarios or accidental duplication?
4. Is `SimpleSocrates` part of the OSINT repository scope or only a DEV harness for the wider Knowledge Factory?
5. Which fields in `ResearchTask`, `Material` and `MaterialPackage` are mandatory versus convenience fields?
6. Which existing legacy scripts/services have any approved requirement mapping?

These questions must be resolved in the formal architecture review before new code is added.
