# Stage 06 — LLM Gateway Disposition

**Object:** `services/llm-gateway/`  
**Stage:** M2 — dependency and legacy/experiment cleanup  
**Decision:** remove implementation from this repository; preserve the engineering lesson in documentation.  

## Why this review was required

The directory name suggested a production-style LLM gateway, but the implementation was a separate experimental policy-control prototype. Keeping it inside the active OSINT repository creates false architectural coupling and invites accidental reuse before requirements exist.

## What the experiment actually contains

```text
HTTP/API
   ↓
Sphinx intent/risk heuristics
   ↓
Enigma / policy logic
   ↓
Judge
   ↓
ALLOW / DENY / QUARANTINE / SIMULATE
```

The tree includes API, Judge, Sphinx heuristics, Enigma YAML rules, a second policy engine, simulation placeholder and historical text/stat outputs.

## Findings

1. It is not a real provider/model gateway: no approved model routing, cost control, provider fallback, token accounting, quota management or provider abstraction is established.
2. Risk/intent behavior relies on heuristic and uncalibrated values from the earlier prototype.
3. Policy responsibility is duplicated between Enigma and another policy engine.
4. It has no current dependency path from the verified `father_osint` DEV product.
5. The useful pattern is conceptual, not implementation-specific:

```text
interpreted request/context
        ↓
versioned deterministic policy
        ↓
decision
  + reason
  + matched rule
  + policy version
  + audit evidence
```

## Decision

**REMOVE FROM ACTIVE REPOSITORY TREE.**

This is not a statement that policy control or an LLM gateway will never exist in FATHER. It means they must return through the normal engineering chain:

```text
business requirement
    ↓
requirements review
    ↓
architecture / threat / cost analysis
    ↓
interface contract
    ↓
acceptance tests
    ↓
donor/product evaluation
    ↓
implementation / benchmark
    ↓
ADR
```

If a future FATHER requirement needs model routing, the system will be designed as a real LLM Gateway. If a future requirement needs policy enforcement, it will be designed as a distinct Policy Gate. They must not be conflated because an old folder already exists.

## Preservation rule

The historical source remains recoverable through Git history. The engineering conclusions are preserved in Stage 06 documentation and the development journal. No copy of the implementation is required in the active tree.

## Cleanup gate

After deletion, clean CI must still prove:

- `father_osint` import;
- test collection;
- all current tests;
- `run_dev_osint.py`;
- `run_dev_pipeline.py`.

Only then is this cleanup considered PASS.
