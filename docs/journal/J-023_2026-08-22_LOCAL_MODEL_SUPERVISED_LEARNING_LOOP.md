# J-023 — Local model supervised learning loop

**Date:** 2026-08-22  
**Status:** ACCEPTED / FUTURE CORE  
**Parent roadmap:** `docs/LOCAL_MODEL_LEARNING_ROADMAP.md`

## Trigger

FATHER is intended to become not only a consumer of governed knowledge, but an improving local expert system. The project needs a controlled way to turn model outputs, expert corrections, implementation results and review findings into reusable training/evaluation evidence.

## Decision

Adopt a supervised learning loop in which the local workstation model produces bounded review candidates; GitHub is used during DEV as a transparent review/control plane; deterministic CI and expert review classify outputs as PASS / PASS_WITH_LIMITATIONS / REWORK / REJECT; reviewed records feed a curated experience corpus; model/method changes are evaluated as Champion/Challenger before promotion.

## Important boundary

GitHub review does not itself train model weights. Review creates labeled evidence. Parameter updates happen only through an explicit, versioned training/adaptation job.

The preferred correction order is:

```text
missing/current fact       -> governed KB / RAG
workflow/routing defect    -> method/prompt/tool policy
recurrent measurable skill -> LoRA/SFT candidate
new failure discovered     -> permanent regression fixture
```

This limits unnecessary retraining and keeps factual knowledge separate from model behavior.

## Review contract

Every local-model submission must expose answer/output, evidence references, assumptions, limitations, model/method/prompt/KB versions and test/metric results. Hidden chain-of-thought is neither required nor stored.

Review findings are structured and reusable for evaluation/training.

## Training corpus classes

- GOLD_POSITIVE
- CORRECTED_POSITIVE
- HARD_NEGATIVE
- ABSTAIN/GAP

Rejected or corrected examples are retained with finding codes so the model can later be trained/evaluated against recurring failure modes rather than only successful answers.

## Promotion rule

No trained adapter/model becomes production Champion until it passes the same frozen evaluation corpus and regression/safety gates as the existing Champion and receives an explicit promotion decision.

## Infrastructure direction

GitHub is acceptable as the current DEV review plane for non-sensitive/sanitized artifacts. Sensitive production material, private model weights and protected organizational data must migrate to controlled private infrastructure while stable IDs, manifests and review semantics remain unchanged.

## Result

The product architecture now has a closed improvement loop:

```text
Knowledge Factory
→ Local Model
→ Candidate Decision/Knowledge Work
→ Review
→ Correction
→ Experience Corpus
→ RAG/Method/Training Improvement
→ Evaluation
→ New Champion
→ Better Work
```

This is the planned mechanism by which the local FATHER model will accumulate verified experience rather than learn blindly from its own outputs.
