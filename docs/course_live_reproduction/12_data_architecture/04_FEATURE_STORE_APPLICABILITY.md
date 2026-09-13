# Feature Store Applicability & Training–Serving Consistency

Status: `CONDITIONAL / NOT CURRENTLY REQUIRED FOR CORE OSINT EVIDENCE FLOW`

## 1. Why this document exists

OTUS Lesson 12 explicitly checks understanding of Feature Store and Training–Serving Skew. For the current OSINT Agent, a Feature Store is **not automatically required**, because the verified core is evidence collection/provenance, not an online supervised model serving engineered features.

## 2. When Feature Store becomes justified

Promote a Feature Store or equivalent governed feature registry when a model uses reusable structured features both:

- offline for training/evaluation; and
- online for inference/ranking/classification.

Potential future OSINT examples:

- source-quality/risk classifier;
- document relevance ranker;
- anomaly/spam classifier;
- source prioritization model;
- entity-resolution model;
- propagation/risk scoring model.

If these models use shared engineered features, offline and online feature definitions must remain identical/versioned.

## 3. Training–Serving Skew

Skew occurs when the model sees one feature definition/distribution during training and a different one in Production.

Examples:

- offline feature uses a 30-day window while online uses 7 days;
- null/default handling differs;
- entity mapping/version differs;
- timestamp/timezone logic differs;
- offline pipeline includes future data unavailable at serving time;
- feature code is duplicated and drifts.

## 4. Controls

```text
one canonical feature definition
→ versioned transformation
→ point-in-time correct offline materialization
→ same definition for online serving
→ feature/model version trace
→ monitoring for drift/skew
```

Required metadata:

- feature ID/name;
- semantic definition;
- transformation/version;
- source dataset refs;
- freshness/TTL;
- owner;
- data class;
- point-in-time semantics;
- offline/online store mapping;
- compatible model versions.

## 5. Current project decision

```text
FEATURE_STORE = NOT_REQUIRED_FOR_CURRENT_CORE
```

Reason: current OSINT core does not have a verified supervised online feature-serving requirement.

This is not `NOT_APPLICABLE_FOREVER`. It is a conditional decision with a trigger.

### Revisit trigger

A Feature Store review becomes mandatory when an approved model requires shared structured features in both offline training/evaluation and online inference.

## 6. RAG consistency is related but different

RAG usually does not need a Feature Store merely to serve embeddings. However it has an analogous **retrieval consistency** problem:

- chunking version;
- embedding model/version;
- metadata schema;
- index generation;
- filtering policy;
- document version.

Training/eval and Production retrieval must not silently compare different index/config generations.

```text
Eval corpus + retrieval config vN
        ↓
quality measurement
        ↓
Production retrieval config vN
```

If Production uses vN+1, it requires a new evaluation/canary evidence set.

## 7. Conclusion

The lesson requirement is satisfied by understanding **when** Feature Store solves a real consistency problem, not by inserting one into every AI architecture.