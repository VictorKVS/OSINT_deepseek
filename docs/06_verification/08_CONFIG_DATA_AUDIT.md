# Stage 06 — Configuration and Data Boundary Audit

**Status:** REVIEWED / BOUNDARIES DEFINED / NO RUNTIME EXPANSION APPROVED

## Purpose

Review `config/` and `data/` against the current requirements-first FATHER OSINT architecture and prevent four different concepts from being mixed:

1. mission/business profile;
2. runtime configuration;
3. test fixtures;
4. verified knowledge/evidence.

The governing rule is:

```text
business intent
    ↓
approved contract
    ↓
configuration
    ↓
runtime

and separately:

test scenario
    ↓
fixture
    ↓
expected result
```

Configuration is not knowledge. Test data is not evidence. A watchlist is not a Knowledge Base.

---

## 1. `config/high_technology_watchlist.yaml`

### What it currently contains

The file combines several conceptually different layers:

- mission/profile metadata;
- technology topic priorities;
- numeric topic weights;
- signal taxonomy;
- source classes and numeric source priorities;
- routing targets for future Knowledge Bases;
- escalation rules;
- output/promotion policy.

This is useful as a product-design artifact, but it is **too broad to be treated as one runtime configuration contract**.

### Architectural finding A — uncalibrated weights

Examples include topic weights such as `1.0`, `0.95`, `0.75` and source priorities such as `0.9`, `0.65`, `0.4`.

There is currently no approved calibration method, benchmark, dataset, business equation, or consumer that proves what these numbers mean.

Therefore they MUST NOT currently be interpreted as probabilities, trust scores, ranking truth, or autonomous decision thresholds.

**Decision:** preserve them only as draft preference hints. Before executable use, either:

- replace with ordered/non-numeric priority classes; or
- define semantics, owner, calibration procedure and acceptance tests.

### Architectural finding B — source class is not evidence quality

`primary`, `independent_technical`, `specialist_media`, `community_signal`, and `telegram_signal` can be useful discovery classes. However, class membership alone cannot prove a specific claim.

A Telegram post may link directly to a primary document. An official source can contain marketing language or later corrections. Therefore source class may influence discovery/routing, but claim confidence must be evaluated later by Analyst/Socrates using the actual material and provenance.

### Architectural finding C — KB routing is outside the OSINT collector contract

The `routing` section maps topics to future targets such as `AI_LLM_KB`, `ARCHITECTURE_KB`, `SECURITY_KB`, and `TECHNOLOGY_HORIZONS`.

The current OSINT role is:

```text
ResearchTask
    ↓
collect material
    ↓
MaterialPackage
```

OSINT must not decide what becomes knowledge. Therefore KB routing belongs to a later Knowledge/Publication layer, not to collectors.

**Decision:** retain routing as future design input, but do not wire it into `OSINTAgent`.

### Architectural finding D — escalation belongs to orchestration/governance

Rules such as "impacts current architecture materially" or "contradicts an ACTIVE Survival Rule" require interpretation of existing architecture and knowledge. A collector cannot evaluate them reliably.

**Decision:** future Analyst/Socrates/Factory Orchestrator responsibility.

### Architectural finding E — output policy crosses multiple boundaries

The file currently contains:

- `default_status: DISCOVERED`;
- `autonomous_verified_promotion: false`;
- provenance requirement;
- Socrates requirement;
- corroboration requirement.

These are valuable governance principles, but they are not merely watchlist settings.

**Decision:** treat them as future Knowledge Factory governance requirements. They should eventually move into an approved policy/requirements document or dedicated policy configuration after its consumer is defined.

---

## 2. Proposed logical split — design only

No file restructuring is approved yet. The architecture should first recognize four logical contracts:

```text
MISSION PROFILE
  what do we care about?
       │
       ├── topics
       ├── signal types
       └── discovery priorities

SOURCE DISCOVERY PROFILE
  where should OSINT look?
       │
       ├── source classes
       └── source selection hints

FACTORY GOVERNANCE POLICY
  what may progress and who decides?
       │
       ├── promotion gates
       ├── provenance requirements
       ├── review requirements
       └── escalation rules

KNOWLEDGE ROUTING POLICY
  where does approved knowledge go?
       │
       └── target KBs / domains
```

Only after requirements and consumers exist should this become physical YAML schemas/files.

---

## 3. `data/dev/` fixtures

### Current role

`github_fixture.json` and `telegram_fixture.json` provide deterministic material to `FixtureCollector`.

This is appropriate for DEV because the same input can be replayed without network access, credentials, Telegram sessions, rate limits or external changes.

**Decision:** `KEEP / DEV TEST DATA`.

### Important boundary

The fixture strings resemble real intelligence material. One GitHub fixture uses the real TDLib repository locator; other entries use `example` names/URLs. Telegram fixtures also contain realistic technology assertions.

These records MUST NOT be interpreted as current verified facts merely because they look realistic.

The invariant is:

> **Fixture data proves software behavior, not world truth.**

### Required future improvement

Before fixtures expand significantly, define a small fixture schema/convention that makes test status explicit, for example a metadata marker such as `fixture: true` / `synthetic: true`, scenario ID, and expected purpose.

This is a **test-design requirement**, not an instruction to change runtime models now.

### Production data

Production evidence/raw storage remains out of scope for the current DEV gate. Do not put downloaded real-world OSINT evidence into `data/dev/`.

Future production storage must separately address:

- immutable/raw evidence;
- source observation metadata;
- hashes;
- acquisition time;
- retention;
- quarantine for unsafe files;
- access controls;
- privacy/legal constraints;
- reproducible lineage.

---

## 4. Ownership matrix

| Artifact/concept | Owner in architecture | Current decision |
|---|---|---|
| technology mission/topics | Product/Analyst requirements | KEEP as DRAFT PROFILE |
| numeric topic/source weights | Not yet defined | DO NOT EXECUTE AS SCORES |
| source discovery classes | OSINT discovery design | KEEP as HINTS |
| signal taxonomy | Analyst/domain design | KEEP / REVIEW LATER |
| escalation rules | Factory orchestration/governance | DEFER |
| KB routing | Knowledge publication layer | DEFER |
| provenance requirement | Cross-cutting governance | KEEP AS REQUIREMENT |
| Socrates promotion gate | Factory workflow | KEEP AS REQUIREMENT |
| `data/dev/*.json` | DEV testing | KEEP |
| production raw evidence | Future storage architecture | NOT YET DESIGNED |

---

## 5. Stage decision

No new runtime code is justified by this audit.

Allowed next:

1. document the logical boundaries in `config/README.md` and `data/README.md`;
2. keep existing fixture-based DEV tests;
3. during the next test-contract revision, make fixture identity explicit;
4. continue repository classification.

Not allowed yet:

- automatic ranking using the current numeric weights;
- autonomous trust scores from source class;
- OSINT writing directly to any KB named in `routing`;
- treating fixture assertions as verified intelligence;
- growing the YAML with new policy fields without an approved consumer.

## Result

**CONFIG/DATA GATE: PASS WITH BOUNDARY CORRECTIONS.**

The files may remain, but their semantics are now constrained by architecture rather than inferred from their names or fields.
