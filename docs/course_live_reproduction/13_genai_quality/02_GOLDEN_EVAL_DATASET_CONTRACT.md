# Golden / Evaluation Dataset Contract

Status: `CANDIDATE / OWNER REVIEW REQUIRED`

## 1. Purpose

Create a versioned, reproducible evaluation set for RAG/model decisions so that Model A, Model B, retrieval variants and prompt/policy changes are compared on the same evidence.

## 2. Unit of evaluation

Each case should contain at minimum:

```text
case_id
question_or_task
scope / allowed source classes
input_snapshot_refs
expected_evidence_refs
critical_facts_or_expected_points
known_acceptable_variants
known_unacceptable_claims
security_or_injection_payloads_if_applicable
difficulty / scenario tags
owner / reviewer
version
status
```

Optional fields:

```text
reference_answer
required_citations
forbidden_sources
time_boundary
expected_unknown
expected_research_more
cost_or_latency_class
```

## 3. Case families

The first dataset should cover:

- direct evidence lookup;
- multi-source synthesis;
- conflicting sources;
- missing evidence / correct `UNKNOWN`;
- stale vs current source/version;
- same payload from multiple source observations;
- relation/graph reasoning where applicable;
- retrieval noise / distractors;
- prompt injection / malicious source content;
- bounded follow-up research;
- citation/provenance resolution;
- Russian/English technical material where relevant.

## 4. Split policy

Keep separate:

- `DEV/CALIBRATION` — used for prompt/rubric/tool development;
- `REGRESSION` — stable set used in CI;
- `HOLDOUT` — not used for routine tuning;
- `SECURITY` — adversarial cases;
- `PRODUCTION_SHADOW` — sanitized/approved real-world samples when policy allows.

Do not tune on the entire regression/holdout set.

## 5. Evidence ground truth

The ground truth is not merely a reference answer.

For FATHER, the stronger object is:

```text
question
  ↓
expected evidence set / acceptable alternatives
  ↓
expected facts / UNKNOWN boundaries
  ↓
answer rubric
```

This lets the evaluation distinguish:

- correct answer from wrong evidence;
- plausible answer with unsupported claims;
- incomplete but honest answer;
- correct decision to return `UNKNOWN` or `RESEARCH_MORE`.

## 6. Versioning

Every dataset release gets:

- dataset ID/version;
- manifest hash;
- case hashes;
- source snapshot references;
- owner/reviewer;
- change log;
- reason for additions/removals;
- compatibility notes with metric/rubric versions.

A changed expected answer/evidence set produces a new dataset version. History is not silently rewritten.

## 7. Governance

### Producer

QA / Evaluation Engineer + Domain SME.

### Reviewers

- Product/Domain owner for usefulness;
- Security for adversarial/security cases;
- Data/Legal where case data requires policy review;
- independent reviewer for material benchmark sets.

### Human calibration

A reviewed subset should be scored by humans and used to calibrate automated judges/rubrics.

## 8. Leakage controls

Prevent:

- test questions leaking into prompts/few-shot examples;
- holdout cases entering training/tuning data;
- reference answers being exposed to the candidate model during inference;
- future information leaking into point-in-time cases.

## 9. Current state

`GOLDEN_EVAL_DATASET = NOT YET BASELINED`.

The contract is ready; actual case population and human review are the next evidence-producing step.
