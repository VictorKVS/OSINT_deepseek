# Codex Execution Rules — FATHER Unified Analyst M4

## Mission

Build one local-first `FATHER Analyst Core` that turns case questions into evidence-backed analytical objects and only promotes reviewed knowledge into the Knowledge Factory.

Do not create another parallel mini-platform. Reuse verified components from existing project branches/PRs where contracts are sound; wrap or migrate them behind new unified interfaces.

## Canonical pipeline

`CASE -> QUESTIONS -> PLAN -> TOOL JOBS -> RAW RESULTS -> OBSERVATIONS -> EVIDENCE -> ENTITY/RELATION GRAPH -> ANALYSIS ZOO -> HYPOTHESIS GRAPH -> SOCRATES -> HUMAN REVIEW -> PROMOTION REQUEST -> D14/D15 -> KNOWLEDGE BASE`

## Non-negotiable semantic rules

1. Tool output is not a fact.
2. Observation != Evidence != Claim != Fact != Hypothesis != Conclusion.
3. Possible edge is only a candidate relation until evidence-backed and reviewed.
4. Absence of evidence is a GAP, not negative fact.
5. Source/tool failure does not reject a hypothesis.
6. Ten mirrors of one source do not equal ten independent confirmations.
7. No silent entity merge.
8. No silent hypothesis -> fact promotion.
9. Numeric confidence is forbidden without a named calibrated model and validation evidence.
10. Human review is mandatory before D14/D15 promotion.
11. Raw evidence and tool outputs stay local by default; LLMs receive compact evidence packets, IDs and minimal excerpts.
12. Existing frozen DEV v1 behavior must remain regression protected until an explicit migration gate retires it.

## Architectural boundaries

### Build as the new integration layer

`father_analyst/`
- case orchestration
- tool capability registry/router
- normalized observation/evidence contracts
- entity/relation candidate graph
- analysis zoo orchestration
- hypothesis/reasoning graph
- Socrates review contract
- human review decision
- Knowledge Factory promotion bridge
- local context/retrieval budget controls

### Reuse as donors, do not copy blindly

- `father_osint/**` — frozen/proven contracts, acquisition and Knowledge Factory primitives.
- `osint_workbench/**` — evidence-first collection, graph, coverage/gaps, analysis-zoo patterns.
- `screening_factory/**` — five-stream planning, bounded parallel workers, adapter/policy patterns.
- `father_osint/crypto/**` — Bitcoin evidence-safe primitives.
- Telegram TDLib/Telethon paths — existing transport/collection capability.
- `docs/10_investigation_workspace/**` and `config/hypothesis_graph_ontology.json` — Case and Graph Core product contracts.

Before migrating a donor component, write a compatibility test proving the semantics being retained.

## Tool adapter contract

Every adapter must declare:

- `tool_id`
- `version`
- `execution_profile`
- `input_types[]`
- `output_types[]`
- `possible_edge_types[]`
- `capabilities[]`
- `credential_requirements[]`
- `network_policy`
- `legal_mode`
- `parallelism_class`
- `rate_limit_policy`
- `cost_policy`
- `normalizer_version`
- `health_check`

Runtime output must be:

`ToolRun -> RawArtifact -> Observation[]`

Never `ToolRun -> Fact`.

## Local-first/token policy

Deterministic code handles:
- parsing
- hashing
- deduplication
- entity extraction where deterministic
- schema validation
- graph traversal
- source dependency checks
- cache lookup
- changed-object detection
- tool scheduling/rate limits

LLMs receive only a bounded `AnalysisPacket` containing:
- question/hypothesis IDs
- selected evidence IDs
- compact excerpts
- source/provenance summary
- unresolved conflicts/gaps
- explicit requested analytical task

Store raw material locally and reference it by ID/path/hash. Reuse cached analytical outputs when source/evidence versions are unchanged.

## Development order

### M4.0 Contract freeze
- unified IDs and object taxonomy
- tool adapter schema
- observation/evidence schema
- graph edge status model
- analysis packet schema
- human decision/promotion envelope

### M4.1 Local Tool Factory
- registry
- router
- five-stream bounded scheduler
- local execution profiles
- first synthetic adapters

### M4.2 Evidence Layer
- raw artifact receipt
- observation normalization
- content hash/provenance
- source independence group
- review state

### M4.3 Graph Core
- entity/relation candidate graph
- reasoning graph
- support/counter/gap/test edges
- append-only change history

### M4.4 Analysis Zoo
- independent analyzer runs
- consensus/dissent without fact promotion
- deterministic checks before LLM checks
- token/context budgets

### M4.5 Socrates + Human Gate
- challenge dependency/circularity
- alternative explanations
- identification errors
- missing discriminating evidence
- explicit PASS/REWORK/INCONCLUSIVE
- immutable human decision

### M4.6 Knowledge Factory Bridge
- promotion request from reviewed objects only
- exact binding to evidence/review versions
- D14/D15 fail-closed integration
- no direct KB write path from tools/LLMs

### M4.7 Real adapters
First controlled set only after M4.0-M4.6 synthetic vertical passes:
- Telegram
- RDAP/DNS
- Subfinder
- theHarvester
- Sherlock/Maigret
- ExifTool
- Shodan/Censys where credentials permit
- Bitcoin adapter

## Required vertical acceptance

One synthetic case must prove:
- 3 competing hypotheses
- 5 parallel collection streams
- at least 5 adapters
- raw artifacts preserved
- observations normalized
- evidence provenance verified
- at least one candidate relation rejected
- at least one source-dependency warning
- support and counter-evidence
- unresolved GAP + discriminating TEST
- Socrates challenge
- Human Review decision
- one approved object passes promotion bridge into D14/D15
- complete replay from KB object back to human decision, evidence, observation, tool run and raw artifact

A controlled real case is allowed only after the synthetic vertical is green.

## Working discipline

- Prefer small commits with tests.
- Never claim completion from code presence alone; attach test/run evidence.
- Keep a journal entry for every gate transition.
- Do not invent throughput, speedup, remaining-time or confidence metrics.
- If a donor branch conflicts semantically, stop and document the conflict instead of silently choosing one implementation.
