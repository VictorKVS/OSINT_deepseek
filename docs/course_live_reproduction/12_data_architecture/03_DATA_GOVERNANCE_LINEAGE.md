# Data Governance & Lineage

Status: `CANDIDATE GOVERNANCE MODEL / BUILT ON CURRENT PROVENANCE RULES`

## 1. Governance objective

Every important derived object must remain traceable to the original source observation and the transformation/version chain that produced it.

## 2. Canonical lineage chain

```text
Source Locator / Source Version
→ Source Observation
→ Raw Payload Hash / Original File
→ Parser Version
→ Structural Block
→ Chunk Version
→ Enrichment / Extraction Model Version
→ Embedding / Index Generation (if used)
→ Retrieval Hit
→ Claim / Entity / Relation Candidate
→ Analyst Review
→ Independent Review
→ Knowledge Candidate
→ Knowledge Gate Decision
```

## 3. Minimum metadata per data object

Depending on type, preserve as applicable:

- stable object ID;
- project/workspace ID;
- source locator;
- source/publisher/author when known;
- acquisition/publication/version timestamps;
- SHA-256 or integrity identifier;
- parser/chunker/model/index version;
- parent/source object refs;
- data class/sensitivity;
- processing/external-sharing policy;
- owner/custodian;
- review state;
- current/superseded/retracted state;
- deletion/retention policy;
- audit trail.

## 4. Data ownership

| Object | Primary accountable owner |
|---|---|
| Source registry / source trust metadata | OSINT/Knowledge curator + reviewer |
| Raw source observation | evidence/data custodian |
| Data classification / sharing / retention | Data Owner + Legal/Security as applicable |
| Parsed/chunked derivative | data pipeline owner |
| Embedding/index | retrieval/data platform owner |
| Claim/entity/relation candidate | Analyst/Knowledge layer |
| Reviewed knowledge | Knowledge owner / gate authority |
| Audit/approval history | governance/system owner |

LLM/model output cannot become the data owner.

## 5. Data quality dimensions

Track by stage rather than one generic score:

- source provenance completeness;
- integrity/hash validity;
- parse success/read order;
- chunk/source-span coverage;
- metadata completeness;
- freshness;
- duplicate payload vs independent observation distinction;
- schema/version compatibility;
- embedding/index consistency;
- evidence reference resolvability;
- human rejection/rework rate for semantic candidates.

## 6. Retention and deletion/retraction

Retention cannot be one global number before data classes/legal purposes are defined.

A Production design needs policy per data class/purpose:

```text
raw original
observation metadata
derivatives/chunks
embeddings/index entries
knowledge candidates
approved knowledge
audit/approval records
```

When data must be deleted/retracted, derived indexes and candidates must be invalidated/rebuilt as required. Audit history may retain a tombstone/reference only if policy permits; it must not silently keep prohibited content.

## 7. Version consistency

No mixed-version serving without an explicit migration policy.

Examples:

- chunks produced by `chunker-v2` should record that version;
- embeddings must identify embedding model + dimension + index generation;
- a new embedding model normally creates a new index generation rather than mixing incompatible vectors;
- parser changes create new derivatives while raw evidence remains stable;
- model/prompt changes that affect semantic extraction create new candidate versions.

## 8. External processing policy

Before data reaches an external LLM/model/service, the system must know:

- data classification;
- whether external processing is allowed;
- provider/region/retention requirements;
- redaction/minimization rules;
- purpose and lawful/contractual basis where relevant;
- what output/evidence can be persisted.

UNKNOWN/unclassified data fails closed for external processing.

## 9. Reproducibility

A material analytical result should be reproducible enough to answer:

```text
Which source snapshot?
Which transformation versions?
Which retrieval/index generation?
Which model/prompt version?
Which evidence refs?
Which review/gate decision?
```

This is especially important for later automatic LLM document review and Model Zoo decisions.

## 10. Governance gate

A Production data pipeline is not ready if any material object class lacks an owner, provenance, versioning rule, retention decision or retraction propagation path.