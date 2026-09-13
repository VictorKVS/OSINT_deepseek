# Lesson 05 — Sequence Scenarios

Status: `CURRENT DEV + FUTURE ADAPTER NOTES`

## Scenario A — successful bounded collection

```mermaid
sequenceDiagram
    participant Analyst
    participant OSINT as OSINTAgent
    participant Collector
    participant Store as MaterialStore

    Analyst->>OSINT: run(ResearchTask)
    OSINT->>Store: save_task(task)
    OSINT->>Collector: collect(task)
    loop until collector exhausted or max_items reached
      Collector-->>OSINT: Material
      OSINT->>Store: save_material(material)
      Store-->>OSINT: payload_reused true/false
    end
    OSINT->>Store: save_package(package)
    OSINT-->>Analyst: MaterialPackage
```

## Scenario B — no eligible collector

```mermaid
sequenceDiagram
    participant Analyst
    participant OSINT as OSINTAgent
    participant Store as MaterialStore

    Analyst->>OSINT: ResearchTask(source_types=X)
    OSINT->>Store: save_task
    Note over OSINT: no registered collector intersects X
    OSINT->>Store: save_package(stop=no_eligible_collectors)
    OSINT-->>Analyst: package + explicit error
```

## Scenario C — partial source failure

```mermaid
sequenceDiagram
    participant Analyst
    participant OSINT
    participant C1 as Collector A
    participant C2 as Collector B
    participant Store

    Analyst->>OSINT: ResearchTask
    OSINT->>C1: collect
    C1-->>OSINT: Material A
    OSINT->>Store: save Material A
    OSINT->>C2: collect
    C2--xOSINT: exception
    Note over OSINT: map to safe collector error
    OSINT->>Store: save package with material + error
    OSINT-->>Analyst: partial MaterialPackage
```

## Scenario D — provenance-preserving payload reuse

```mermaid
sequenceDiagram
    participant OSINT
    participant Store

    OSINT->>Store: save Material observation #1 / payload H
    Store-->>OSINT: payload_reused=false
    OSINT->>Store: save Material observation #2 / same payload H, different source locator
    Store-->>OSINT: payload_reused=true
    Note over Store: observation #1 and #2 remain separately traceable
```

## Scenario E — bounded follow-up research

```mermaid
sequenceDiagram
    participant OSINT
    participant Analyst
    participant Reviewer

    OSINT-->>Analyst: MaterialPackage cycle 1
    Analyst->>Reviewer: Analysis + cumulative evidence
    Reviewer-->>Analyst: RESEARCH_MORE(missing source class)
    Analyst->>OSINT: targeted ResearchTask cycle 2
    OSINT-->>Analyst: MaterialPackage cycle 2
    Analyst->>Reviewer: updated analysis + cumulative evidence
    Reviewer-->>Analyst: PASS or another bounded request
```

## Sequence invariants

- earlier evidence is not silently forgotten in follow-up cycles;
- source errors are visible;
- max_items/cycle limits are enforced before uncontrolled work;
- payload reuse does not equal observation deduplication;
- reviewer request cannot bypass ResearchTask contract;
- future API/network adapters must preserve these semantics.
