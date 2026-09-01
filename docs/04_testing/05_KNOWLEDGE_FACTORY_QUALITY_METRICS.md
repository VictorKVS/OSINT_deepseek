# Knowledge Factory Quality Metrics and Evaluation Contract

**Status:** ACTIVE / P0 QUALITY CONTRACT  
**Applies to:** D0-D15, method experiments, production telemetry  
**Rule:** no single opaque “knowledge quality” or “truth probability” score.

## 1. Measurement model

Metrics are grouped into six independent families:

1. source/evidence integrity;
2. extraction quality;
3. semantic/graph quality;
4. task/competency adequacy;
5. lifecycle/reuse/maintenance;
6. production efficiency.

A gate may require several metrics simultaneously. Metrics are operational observations unless a separate calibration contract states otherwise.

## 2. Gold-set metrics for extraction

Where a reviewed gold corpus exists, use standard information-retrieval metrics separately for each object/relation type:

```text
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
F1        = 2 * precision * recall / (precision + recall)
```

Required reporting granularity:
- per type: TERM, DEFINITION, REQUIREMENT, ENTITY, RELATION, CONFLICT classification;
- micro aggregate;
- macro aggregate where multiple classes/types are evaluated;
- gold-set ID/version and annotation policy.

No P/R/F1 number is valid without the gold-set and matching policy used to calculate TP/FP/FN.

## 3. Evidence and provenance metrics

### 3.1 Provenance coverage

```text
provenance_coverage = accepted_knowledge_objects_with_complete_lineage / accepted_knowledge_objects
```

Complete lineage minimally includes:
`artifact/document version -> locator/chunk -> extraction method/version -> review state`.

D15 target: **1.0** for accepted KB-ready objects.

### 3.2 Exact-locator coverage

```text
locator_coverage = derived_objects_with_exact_source_locator / derived_objects_requiring_locator
```

D15 target: **1.0** where the source format permits deterministic location.

### 3.3 Source-verification coverage

```text
verified_source_coverage = accepted_objects_backed_by_verified_or_explicitly_allowed_source / accepted_objects
```

Discovery-only evidence must remain distinguishable and must not inflate this metric.

## 4. Structure/chunk metrics

### 4.1 Structure coverage

Percentage of source content bytes/pages/blocks represented by a structure node, excluding deliberately ignored material with a reason.

### 4.2 Chunk traceability

```text
chunk_traceability = chunks_with_parent_structure_and_source_locator / chunks
```

D5 gate target: **1.0**.

### 4.3 Orphan rate

```text
orphan_rate = knowledge_objects_without_required_parent_or_evidence_edge / knowledge_objects
```

D13-D15 target: **0** for accepted objects.

## 5. Semantic and graph quality dimensions

Derived from ontology/KG quality practice (OQuaRE and KG-quality literature). Report separately:

### Accuracy / correctness
When a gold or expert-reviewed set exists: fraction of reviewed assertions classified correct in the stated scope.

### Completeness
Task-relative, not universal. Measure against expected competency-question evidence/object requirements, not against an unknowable “all world knowledge”.

### Consistency
- shape/constraint violations;
- logical/domain invariant violations;
- unresolved same-context contradictions.

### Timeliness / freshness
- age since source-status verification;
- age since last source-version check;
- stale-object count against profile-specific freshness policy.

### Trustworthiness / provenance
Source class, verification basis, independence/dependency and review history; never collapsed automatically into truth probability.

### Availability / accessibility
Whether metadata/provenance remain queryable even if original source becomes temporarily unavailable.

### Interoperability
Conformance to stable IDs, typed relations, export schema and selected vocabulary mappings.

## 6. Constraint metrics

SHACL-style/internal shape validation produces:

- `objects_validated`;
- `objects_conformant`;
- `violations_total`;
- violations by severity/type;
- `constraint_conformance = objects_conformant / objects_validated`.

D15 target for mandatory shapes: **1.0**; warnings may remain only with explicit review disposition.

## 7. Competency-question metrics

For each approved `CQ-*`:

- `ANSWERED_TRACEABLE`;
- `ANSWERED_WITH_LIMITATIONS`;
- `INCONCLUSIVE`;
- `GAP`;
- `NOT_APPLICABLE`.

Report:

```text
cq_traceable_rate = ANSWERED_TRACEABLE / applicable_CQs
cq_coverage_rate  = (ANSWERED_TRACEABLE + ANSWERED_WITH_LIMITATIONS) / applicable_CQs
cq_gap_rate       = GAP / applicable_CQs
```

A high CQ coverage with poor provenance does not pass D14/D15.

## 8. Conflict-analysis metrics

Track separately:

- conflict candidates detected;
- confirmed same-context conflicts;
- context splits;
- version-resolved differences;
- lexical/not-conflict mappings;
- dependency warnings;
- inconclusive conflicts/gaps;
- false-positive and false-negative conflict classifications on gold/red-team fixtures.

Conflict detection precision/recall/F1 is reported when a reviewed conflict gold set exists.

## 9. Reuse and maintenance metrics

### 9.1 Reuse ratio

```text
reuse_ratio = reused_verified_objects / (reused_verified_objects + newly_created_objects)
```

Interpretation is contextual: a low ratio in a new domain may be normal. It is an efficiency observation, not quality by itself.

### 9.2 Rework ratio

```text
rework_ratio = objects_reprocessed_after_initial_completion / processed_objects
```

Report by reason: changed bytes, new version, method version, applicability change, conflict/gap, failed review, regression failure.

### 9.3 Invalidated-subgraph ratio

```text
invalidated_ratio = objects_invalidated_by_change / total_objects_in_KB_scope
```

Used to verify bounded change propagation; smaller is not always better if dependencies genuinely require wider invalidation.

### 9.4 Artifact reuse

- acquisition attempts;
- newly stored blobs;
- reused blobs;
- new document versions;
- unchanged version observations;
- bytes downloaded;
- bytes avoided/reused where measurable.

## 10. Production / throughput metrics

Per run and cumulatively:

- wall-clock processing time;
- human review minutes;
- machine/tool cost where measurable;
- documents/hour;
- source pages or bytes/hour where meaningful;
- chunks/hour;
- accepted knowledge objects/hour;
- accepted relations/hour;
- conflict candidates reviewed/hour;
- time to first usable evidence;
- time to D15;
- failure counts by stage/reason;
- queue/wait time separately from processing time where measurable.

## 11. Research-efficiency metric — experimental only

Retain the previously proposed research-efficiency concept only as an uncalibrated experiment:

```text
research_efficiency_observation = measured_uncertainty_reduction / (human_time + machine_cost + acquisition_cost)
```

It may not be used for production gating until:
- uncertainty reduction has an explicit measurable operational definition;
- heterogeneous cost units are normalized transparently;
- calibration/evaluation evidence exists;
- reviewer approves the interpretation.

Until then, report the component metrics separately.

## 12. Champion / Challenger method metrics

A method experiment must use the same corpus/gold-set and report at least:

- P/R/F1 by extraction type where gold exists;
- provenance and locator coverage;
- constraint conformance;
- CQ outcomes;
- conflict classification errors;
- accepted-object throughput;
- review/rework burden;
- cost/time;
- object identity stability;
- regression impact.

A challenger is promoted only when its improvement is material for the intended use and it does not violate provenance, safety or regression gates.

## 13. Annotation / reviewer reliability

For human-labelled gold corpora, report agreement when multiple reviewers are used. Suitable statistics depend on label/task design; raw agreement alone is insufficient for ambiguous multi-class tasks. The chosen statistic and annotation guideline version must be recorded with the gold set.

## 14. Gate thresholds

Thresholds are domain- and maturity-specific and must be stated before the evaluation run. The only universal hard gates currently are:

- D3 accepted original: actual bytes + computed SHA-256 + size + source/version provenance;
- D5 accepted chunk: complete structure/source traceability;
- D15 accepted object: complete required provenance;
- D15 mandatory-shape conformance: 1.0;
- autonomous direct promotion: 0 permitted bypasses;
- silent FACT/HYPOTHESIS implicit cast: 0 permitted;
- registry/audit reconciliation mismatches: 0 unresolved at gate.

Do not invent thresholds such as “F1 >= 0.95” until the corpus, task, error costs and reviewer policy justify them.

## 15. Required metric provenance

Every published metric record must include:

- metric ID and version;
- formula/aggregation;
- input object set or corpus ID/version;
- method/parser/extractor version;
- gold-set/review-policy version where applicable;
- timestamp;
- run ID;
- exclusions/null-handling;
- raw numerator/denominator or confusion counts where applicable.

A metric without this provenance is an observation draft, not acceptance evidence.
