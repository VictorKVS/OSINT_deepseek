# FATHER Local Model Learning & Experience Roadmap

**Status:** PLANNED CORE / subordinate to the P0 Knowledge Factory conveyor  
**Purpose:** turn verified project work, expert review and observed outcomes into a controlled learning loop for the local FATHER model without allowing unreviewed model output to become trusted knowledge.

## 1. Target loop

```text
LOCAL MODEL ON WORKSTATION
        ↓
receives task + governed KB context + method/version
        ↓
produces REVIEW CANDIDATE BUNDLE
        ↓
local deterministic checks
        ↓
Git branch / Pull Request
        ↓
CI: schema + provenance + tests + safety/regression
        ↓
EXPERT / CHATGPT / HUMAN REVIEW
        ├─ PASS
        ├─ PASS_WITH_LIMITATIONS
        ├─ REWORK
        └─ REJECT
        ↓
review comments + corrected/accepted answer
        ↓
CURATED EXPERIENCE CORPUS
        ├─ positive examples
        ├─ corrected examples
        ├─ rejected/error examples
        ├─ hard negatives
        └─ evaluation fixtures
        ↓
choose learning mechanism
        ├─ RAG / KB update
        ├─ prompt/policy/method update
        ├─ tool-routing update
        ├─ LoRA / SFT fine-tune
        └─ later preference optimization if justified
        ↓
NEW LOCAL MODEL / METHOD VERSION
        ↓
frozen benchmark + red-team + regression
        ↓
CHAMPION / CHALLENGER DECISION
        ↓
PROMOTE or ROLLBACK
```

## 2. Critical distinction: review is not weight training

GitHub comments do not directly change model weights. They create supervised evidence.

Every correction must first become a structured learning record. Only a separately executed training job may modify a model/adapter. This prevents accidental continuous self-training and catastrophic feedback loops.

Learning can occur at several layers:

1. **Knowledge/RAG learning** — add or correct governed KB objects; safest and first choice when the problem is missing/current factual knowledge.
2. **Method/prompt learning** — change instructions, routing, schemas, extraction procedure or tool policy when the problem is reasoning/workflow behavior.
3. **Evaluation learning** — convert a discovered failure into a permanent regression fixture.
4. **Parameter learning** — LoRA/SFT or another training method only when repeated evidence shows that behavior cannot be solved adequately by governed knowledge/method/tool changes.

The project should prefer the least invasive mechanism that fixes the measured failure.

## 3. Review Candidate Bundle

A model submission must not contain unverifiable free-form output only. Minimum machine-readable fields:

```text
run_id
model_id
model_version
adapter_version?
method_version
prompt/policy_version
knowledge_snapshot_id
retrieved_object_ids[]
task_id / competency_question_id?
input_scope
output_type
candidate_output
explicit_assumptions[]
evidence_refs[]
limitations[]
uncertainty/gaps[]
tool_calls_summary[]
test_results[]
metrics{}
created_at
```

Do not require or store hidden chain-of-thought. The reviewable object is the answer, evidence, assumptions, method lineage and concise decision rationale.

## 4. Review record

Each review creates a structured record:

```text
review_id
run_id
reviewer
reviewer_role
verdict: PASS | PASS_WITH_LIMITATIONS | REWORK | REJECT
finding_codes[]
comments[]
corrected_output?
missing_evidence[]
violated_constraints[]
regression_fixture_required: true|false
training_eligible: true|false
training_exclusion_reason?
reviewed_at
```

Common finding classes:

- unsupported factual claim;
- stale/incorrect source;
- wrong applicability;
- FACT/HYPOTHESIS/OPINION type error;
- missed conflict/counter-evidence;
- provenance loss;
- duplicate/reuse failure;
- unsafe autonomous action;
- calculation error;
- legal interpretation requires expert review;
- correct answer but poor structure/style;
- tool-routing inefficiency;
- hallucinated identifier/citation;
- overconfidence / missing limitation.

## 5. GitHub workflow — DEV control plane

During current DEV stage GitHub is the transparent review/control plane.

Recommended structure:

```text
learning/
  candidates/
  reviews/
  accepted/
  rejected/
  fixtures/
  datasets/
  manifests/
  model_cards/
```

Recommended branch naming:

```text
model/<model-id>/<run-id>
```

Each local run opens or updates a bounded PR. CI validates the bundle before expert review.

GitHub is **not** the long-term storage location for sensitive production material, private weights or protected organizational data. When the project moves to protected production infrastructure, this workflow migrates to a private/controlled Git service and artifact store while preserving stable IDs and review semantics.

## 6. What the reviewer checks

Review must distinguish at least:

### Correctness / evidence
- Is every material claim traceable?
- Is the source current and applicable?
- Is there conflicting/counter evidence?
- Is the object typed correctly?

### Method
- Did the model reuse existing verified objects before creating new ones?
- Did it follow required competency questions and constraints?
- Did it stop on gaps rather than fabricate?

### Engineering
- Is the proposed implementation actually compliant with the requirement?
- Are alternatives materially considered?
- Are cost/time/risk/reliability claims supported by data/assumptions?

### Safety/governance
- Did the model attempt a privileged/publication action it was not authorized to perform?
- Did it leak secrets/private data?
- Is the recommendation high-impact and therefore subject to human approval?

## 7. Curated learning corpus

Do not train on every PR blindly.

A record becomes training-eligible only after review and deduplication.

The corpus should preserve four classes:

1. `GOLD_POSITIVE` — strong accepted example.
2. `CORRECTED_POSITIVE` — model answer plus reviewer-corrected target.
3. `HARD_NEGATIVE` — plausible but materially wrong answer with finding codes.
4. `ABSTAIN/GAP` — examples where the correct behavior is to state uncertainty, request evidence or stop.

This teaches not only answers but also when **not** to answer.

## 8. Split training and evaluation

Training, validation and frozen evaluation sets must be separated by stable IDs and source families where appropriate.

Rules:

- no evaluation fixture is silently copied into training;
- near-duplicates are grouped before splitting;
- changed document versions are lineage-aware;
- benchmark version is frozen before Champion/Challenger comparison;
- benchmark results record model, adapter, prompt/method and KB snapshot versions.

## 9. Metrics for local model development

Do not use one opaque “intelligence score”. Report separate dimensions:

- task/competency-question success;
- evidence/provenance coverage;
- unsupported-claim rate;
- applicability error rate;
- conflict/counter-evidence miss rate;
- abstention correctness on GAP/UNKNOWN cases;
- schema/constraint conformance;
- tool-routing success/failure;
- review PASS / REWORK / REJECT rates;
- human correction effort/time;
- regression pass rate;
- latency and local compute cost;
- RAG reuse vs new research;
- answer stability under repeat runs where relevant.

For extraction/classification tasks with a reviewed gold set, use precision/recall/F1 with corpus/version provenance.

## 10. Champion / Challenger promotion

Every trained or materially changed model/method is a Challenger first.

```text
CURRENT CHAMPION
      vs
NEW CHALLENGER
      ↓
same frozen evaluation corpus
      ↓
quality + provenance + safety + cost + latency + correction burden
      ↓
independent review
      ├─ PROMOTE
      ├─ LIMITED_TO_CONTEXT
      └─ REJECT / ROLLBACK
```

A Challenger cannot replace the Champion merely because training loss improved.

## 11. Local workstation deployment stages

### LM0 — Review-only local assistant
Local model reads governed context, produces candidate bundles, no training and no autonomous KB publication.

### LM1 — Feedback corpus
GitHub review records produce curated accepted/corrected/rejected examples and permanent regression fixtures.

### LM2 — RAG/method adaptation
Improve retrieval, prompts, policies, schemas and routing from measured failures.

### LM3 — Parameter-efficient training
Run controlled LoRA/SFT on curated data when justified by repeated evidence. Keep base model, adapter, dataset manifest and model card versioned separately.

### LM4 — Automated evaluation harness
Every candidate adapter/model runs the frozen benchmark, red-team and regression suite locally/CI before review.

### LM5 — Controlled continuous improvement
New reviewed experience periodically produces a new Challenger. No online self-modifying production weights.

### LM6 — Specialist model/adapter family
Where data supports it, separate adapters/skills may emerge for Legal/Compliance, Security, Programming, Architecture, Analyst/Critic and other domains, all consuming the same governed Knowledge Factory.

## 12. Hardware-aware principle

Local training plans must be selected against actual available compute and memory. Small/medium parameter-efficient adapters, quantized inference, bounded datasets and local evaluation are preferred over pretending the workstation can safely train a large foundation model from scratch.

## 13. Completion criterion

The learning loop is operational when one real local-model task can reproducibly complete:

```text
local inference
→ candidate bundle
→ GitHub PR
→ CI
→ expert review with structured findings
→ corrected/accepted learning record
→ regression fixture
→ curated dataset manifest
→ Challenger adaptation
→ frozen benchmark
→ promotion/rollback decision
```

No stage may silently promote unreviewed model conclusions into the governed KB or production model.
