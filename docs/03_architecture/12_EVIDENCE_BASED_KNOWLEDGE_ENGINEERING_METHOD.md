# Evidence-Based Knowledge Engineering Method for FATHER Knowledge Factory

**Status:** ACTIVE ARCHITECTURE CONTRACT  
**Applies to:** Knowledge Factory D0-D15  
**Priority:** P0  
**Purpose:** replace ad-hoc extraction with a reproducible knowledge-engineering method grounded in established ontology/knowledge-graph engineering practice.

## 1. Core decision

The Knowledge Factory does not treat `document -> LLM summary` as knowledge engineering.

The canonical method is:

```text
DOMAIN / USE CASE / COMPETENCY QUESTIONS
        ↓
REUSE CHECK: existing concepts, vocabularies, prior objects, prior decisions
        ↓
SOURCE / ORIGINAL / VERSION / PROVENANCE
        ↓
STRUCTURE + CHUNKS
        ↓
TERMS / CONCEPTS / DEFINITIONS
        ↓
TYPED ATOMIC KNOWLEDGE OBJECTS
        ↓
ENTITIES / RELATIONS / AXIOMS / APPLICABILITY
        ↓
CONSTRAINT VALIDATION
        ↓
CROSS-DOCUMENT ALIGNMENT + CONFLICT / GAP ANALYSIS
        ↓
COMPETENCY-QUESTION EVALUATION
        ↓
EXPERT / CRITIC REVIEW
        ↓
KB-READY + MONITORING / INVALIDATION / REUSE
```

This is iterative. A failed competency question, constraint, conflict check or review returns only the affected objects/stages to REWORK; it does not silently rebuild the entire corpus.

## 2. Scientific and standards basis

The following bodies of work are adopted as methodological anchors, not as labels for marketing:

### 2.1 Ontology Development 101 — scope, terms, hierarchy, properties, instances, iteration

Noy & McGuinness describe ontology development as an iterative process beginning with domain/scope, intended use/questions, reuse of existing ontologies, important terms, classes/hierarchy, properties and instances. FATHER adopts these ideas as the precondition for D6-D13.

Reference: https://protege.stanford.edu/publications/ontology_development/ontology101.pdf

### 2.2 Competency Questions — executable requirements for knowledge

Grüninger & Fox use competency questions as benchmarks that an ontology must be able to answer. FATHER uses them as requirements and acceptance fixtures for every domain KB.

A domain is not considered KB-ready because many nodes exist. It is KB-ready only if its approved competency questions can be answered with traceable evidence and known limitations.

Reference: DOI 10.1007/978-0-387-34847-6_3

### 2.3 METHONTOLOGY — explicit lifecycle and engineering activities

METHONTOLOGY established a structured ontology-engineering lifecycle and emphasized explicit activities, ordering and evolving prototypes. FATHER adopts the engineering discipline: specification, conceptualization, formalization/implementation, evaluation, documentation and maintenance are distinct concerns with traceable artifacts.

Reference: Fernández-López, Gómez-Pérez, Juristo, 1997, `METHONTOLOGY: from ontological art towards ontological engineering`.

### 2.4 NeOn Methodology — reuse, alignment, modularization and non-ontological resources

NeOn explicitly supports multiple ontology-engineering scenarios rather than one rigid workflow, including reuse/re-engineering, alignment, modularization, localization, ontology design patterns and transformation of non-ontological resources. This directly supports FATHER's reuse-first rule and multiple material profiles.

Reference: https://oa.upm.es/21469/ ; DOI 10.1007/978-3-642-24794-1_2

### 2.5 W3C PROV-O — provenance as first-class graph data

PROV-O supplies interoperable concepts for entities, activities and agents. FATHER does not require RDF storage in M1, but its provenance semantics must be mappable to PROV-O:

- `Entity`: original artifact, document version, chunk, knowledge object, review result;
- `Activity`: acquire, parse, chunk, extract, normalize, align, validate, review, publish-candidate;
- `Agent`: source authority, OSINT worker, parser/method, Analyst, Socrates/Critic, human reviewer.

Every derived object must expose `wasDerivedFrom`-equivalent lineage and method/version identity.

Reference: https://www.w3.org/TR/prov-o/

### 2.6 SKOS / OWL — concepts and formal semantics are separate layers

SKOS is the preferred semantic model for lightweight concept schemes: preferred/alternative labels, broader/narrower, related and mapping relations. Formal logical axioms should be introduced only where a domain/use case requires OWL-level semantics.

The Knowledge Factory must not force every extracted term into a heavy ontology class.

Reference: https://www.w3.org/TR/skos-reference/

### 2.7 SHACL-style constraints — graph/schema validation before promotion

SHACL defines constraint validation for graph data. FATHER adopts the principle even while internal storage remains Python/JSONL: every knowledge-object type has machine-verifiable shape/constraints, and promotion fails closed on shape violations.

Reference: https://www.w3.org/TR/shacl/

SHACL 1.2 remains a W3C working-draft line in 2026; the production reference remains the 2017 Recommendation until a newer Recommendation replaces it.

### 2.8 FAIR — machine-actionable findability, interoperability and reuse

FAIR requires persistent identifiers, rich metadata, qualified references, provenance and community standards. FATHER applies FAIR principles to knowledge objects and processing workflows, including retained metadata after an underlying artifact becomes unavailable.

Reference: Wilkinson et al., Scientific Data 3, 160018 (2016), DOI 10.1038/sdata.2016.18.

### 2.9 OQuaRE / ontology quality and KG quality literature

Ontology/KG quality is multidimensional. FATHER must not collapse quality into one uncalibrated score. Relevant dimensions include structural quality, functional adequacy, compatibility/interoperability, maintainability, consistency, completeness, timeliness/freshness, trust/provenance and availability.

References:
- OQuaRE: Duque-Ramos et al., PLOS ONE 2014, DOI 10.1371/journal.pone.0104463.
- Knowledge Graph Quality Management survey: accuracy, completeness, consistency, timeliness, trustworthiness and availability.
- OOPS!: Poveda-Villalón, Gómez-Pérez, Suárez-Figueroa, 2014, DOI 10.4018/IJSWIS.2014040102.

## 3. Mandatory domain-start contract

Before D6 semantic extraction for a new domain/profile, create a `KnowledgeScope` containing:

- `scope_id`;
- domain and material profiles;
- target users/agents;
- intended decisions/use cases;
- out-of-scope questions;
- approved `competency_questions[]` with stable IDs;
- required evidence/source classes;
- required concept schemes or external vocabularies to reuse/check;
- forbidden implicit casts (for example hypothesis -> fact);
- review authority;
- freshness/lifecycle policy;
- minimum acceptance fixture set.

No semantic extractor may invent domain scope from document contents alone.

## 4. Reuse-first ontology and concept workflow

For each candidate concept/definition/relation:

```text
candidate
  ↓
lookup stable existing object / vocabulary / synonym / mapping
  ├─ exact same meaning + applicable context -> REUSE
  ├─ same core meaning, context-qualified -> MAP / CONTEXTUALIZE
  ├─ overlapping but distinct -> KEEP DISTINCT + relation
  ├─ incompatible definition/rule -> CONFLICT_CANDIDATE
  └─ no reusable object -> CREATE PROVISIONAL
```

A new concept is justified by at least one of:
- a competency question requires it;
- authoritative source explicitly defines/uses it as a domain distinction;
- a relation/requirement cannot be represented without it;
- reuse/alignment analysis proves existing objects are semantically insufficient.

Similarity alone never merges concepts automatically.

## 5. Knowledge object taxonomy

Minimum typed separation:

- `TERM_MENTION` — lexical occurrence only;
- `CONCEPT` — normalized domain concept;
- `DEFINITION` — explicit source-backed definition;
- `ENTITY` — individual/actor/system/object;
- `FACT` — source-supported statement accepted as fact under explicit scope;
- `REQUIREMENT` — obligation/prohibition/permission/condition;
- `RULE` — deterministic/business/legal/technical rule;
- `CLAIM` — assertion not yet promoted to FACT;
- `HYPOTHESIS` — testable explanatory proposition;
- `OPINION` — attributed judgement;
- `METHOD` — procedure/algorithm/calculation;
- `CONTROL` — safeguard/measure;
- `GAP` — missing information;
- `CONFLICT_CANDIDATE` — unresolved potential incompatibility;
- `REVIEW_DECISION` — human/critic disposition.

No implicit cast is permitted between these object types.

## 6. Atomicity method

A knowledge statement is atomic when one review decision can accept/reject it without changing the meaning of another independent statement.

For each source clause/chunk:

1. preserve exact locator and source text range/hash;
2. detect coordinated obligations/conditions/exceptions;
3. split only when the split preserves normative/semantic meaning;
4. attach shared context/conditions explicitly rather than duplicating hidden assumptions;
5. preserve parent/source clause relation;
6. record extraction method/version;
7. mark uncertainty rather than filling omitted values.

The original clause remains the evidence anchor even when decomposed into several atomic objects.

## 7. Relation taxonomy method

Relations are typed; free-form edges are not sufficient for D13.

Minimum families:

- taxonomic: `BROADER`, `NARROWER`, `INSTANCE_OF`;
- lexical/mapping: `SAME_AS_CANDIDATE`, `SYNONYM_OF`, `RELATED_TO`, `MAPS_TO`;
- provenance: `DERIVED_FROM`, `EXTRACTED_FROM`, `REVIEWED_BY`;
- document/version: `AMENDS`, `REPEALS`, `SUPERSEDES`, `VERSION_OF`, `EFFECTIVE_FROM`;
- applicability: `APPLIES_TO`, `EXCLUDES`, `CONDITIONED_BY`, `CONTEXT_SPLIT`;
- knowledge/evidence: `SUPPORTS`, `CHALLENGES`, `DEPENDS_ON`, `CONTRADICTS_CANDIDATE`;
- operational: `SATISFIED_BY`, `IMPLEMENTED_BY`, `VERIFIED_BY`.

Every edge requires provenance/evidence, method/version and review state unless explicitly marked as a structural/system edge.

## 8. Conflict method

Conflict detection is a classification pipeline, not a boolean text-difference check:

```text
semantic difference found
  ↓
CONFLICT_CANDIDATE
  ↓
check source/version/scope/jurisdiction/time/actor/condition/dependency
  ├─ same context + incompatible propositions -> CONFIRMED_CONFLICT
  ├─ different scope/context -> CONTEXT_SPLIT_REQUIRED
  ├─ later valid version replaces earlier -> VERSION_RESOLVED
  ├─ lexical difference, same meaning -> NOT_CONFLICT / MAP
  ├─ insufficient evidence -> INCONCLUSIVE / GAP
  └─ dependency/circularity -> DEPENDENCY_WARNING
```

A difference in definitions is never automatically a legal/technical contradiction.

## 9. Competency-question acceptance

Each `CQ-*` must specify:

- question;
- expected answer type;
- minimum required evidence;
- required object/relation types;
- allowed uncertainty states;
- forbidden answer shortcuts;
- test fixture/golden answer where available.

A CQ result is one of:

- `ANSWERED_TRACEABLE`;
- `ANSWERED_WITH_LIMITATIONS`;
- `INCONCLUSIVE`;
- `GAP`;
- `NOT_APPLICABLE`.

The system is penalized for a confident unsupported answer; `GAP` is a valid and often preferable result.

## 10. Validation gates by D-stage

| Stage | Mandatory methodological gate |
|---|---|
| D0-D3 | exact artifact identity + trust/provenance/version |
| D4 | structure coverage and locator integrity |
| D5 | stable chunk identity + complete locator linkage |
| D6 | terminology normalization + reuse check |
| D7 | definition-vs-mention separation + source attribution |
| D8 | atomicity + modality/condition/exception preservation |
| D9 | entity resolution without unsafe merge |
| D10 | relation type + endpoints + provenance shape |
| D11 | alignment/version/applicability semantics |
| D12 | conflict candidate classification + gaps/dependencies |
| D13 | graph/table/document projection reconciliation + shape validation |
| D14 | competency-question evaluation + expert/critic review |
| D15 | provenance complete + constraints green + promotion boundary green |

## 11. Method evolution: Champion / Challenger / Golden

Knowledge methods are versioned and evaluated like product algorithms.

```text
current method (CHAMPION)
      ↕ controlled same-corpus evaluation
candidate method (CHALLENGER)
      ↓
quality metrics + CQ results + error analysis + cost/time
      ↓
review
      ├─ GOLDEN / promote
      ├─ LIMITED / context-specific
      └─ REJECTED_METHOD / retain evidence
```

No method becomes GOLDEN from popularity, model reputation or a single successful example.

## 12. No single truth/confidence score

The platform must expose separate dimensions rather than one synthetic percentage:

- evidence/provenance coverage;
- extraction precision/recall/F1 where a gold set exists;
- schema/constraint conformance;
- competency-question coverage;
- conflict/gap state;
- source/lifecycle freshness;
- reviewer disposition;
- reuse/rework/cost/latency observations.

Numeric confidence about truth is blocked unless a separately reviewed calibrated model defines meaning, training/calibration evidence and validation conditions.

## 13. References / method register

The above references form the first `KNOWLEDGE_ENGINEERING_METHOD` source family. New methods can be added only with source identity, applicability, what problem they solve, operational mapping into D0-D15 and an evaluation plan.

This document is the architecture-level method contract. The executable metric definitions are maintained in `docs/04_testing/05_KNOWLEDGE_FACTORY_QUALITY_METRICS.md` and `father_osint/knowledge_quality.py`.
