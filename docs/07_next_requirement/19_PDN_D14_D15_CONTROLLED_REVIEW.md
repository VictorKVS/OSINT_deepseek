# PDn D14-D15 controlled review gate

## Current accepted corpus state

The bounded four-document PDn corpus has passed the automated D0-D13 conveyor on real locally preserved A0 captures.

Observed real-corpus acceptance evidence:

- D4-D5 quality: 4/4 PASS;
- D6-D9 quality: 4/4 PASS;
- D10-D12 quality: PASS;
- D13 quality: PASS;
- 168 term candidates;
- 16 definition candidates;
- 106 requirement candidates;
- 152 entity mention candidates;
- 121 internal relations;
- 11 cross-document relations;
- 2 conflict/overlap candidates;
- 159 graph nodes;
- 355 graph edges;
- 0 missing graph endpoints;
- D14 = NEEDS_REVIEW;
- D15 = blocked from autonomous promotion.

## Why D14 is not automated approval

D0-D13 may be deterministic and fail-closed, but semantic acceptance is a governance decision. Automation may prepare evidence, verify lineage, group candidates by deterministic extraction rule, and produce recommendations. It may not silently turn review candidates into verified KB facts.

## Compact review strategy

`prepare_pdn_d14_review.py` reduces hundreds of candidate objects to a small set of review decisions:

1. D6 controlled-term extraction rule;
2. D7 explicit-definition extraction rule;
3. D8 normative-trigger requirement rule;
4. D9 controlled-entity extraction rule;
5. D10 term-defined-by relation rule;
6. D10 requirement-mentions-entity relation rule;
7. D11 shared-term relation rule;
8. D11 shared-entity relation rule;
9. each D12 conflict/overlap candidate individually.

For the current corpus this means eight rule-class decisions plus two D12 candidate decisions instead of reviewing every candidate row one by one.

All machine prechecks remain structural only. Every decision starts as `PENDING`.

## D14 application

The human reviewer edits `reports/pdn_live/D14_DECISIONS.jsonl` and provides:

- an allowed decision;
- reviewer identity;
- a short reason.

`apply_pdn_d14_decisions.py` verifies the exact packet hash, decision set, allowed values, reviewer/reason presence, and rejects any unresolved `PENDING` or `ESCALATE` item. Only then can D14 become VERIFIED.

A D15 promotion request is created, but no D15 promotion occurs automatically.

## D15 explicit approval

`promote_pdn_d15.py` requires an explicit `--approve` flag and reviewer identity. It also requires:

- D14 VERIFIED;
- exact D14 result hash match;
- all rule classes ACCEPTED;
- every D12 candidate resolved as `CONFIRMED_CONFLICT`, `NOT_CONFLICT`, or `OVERLAP_ONLY`;
- no unresolved review state.

Only then is the local corpus marked D15 `KB_READY` and an audited manifest is written. The one-click automatic conveyor never calls this promotion step.

## Invariant

No autonomous KB promotion. Review evidence and approval identity must remain traceable to the exact corpus, candidate packet and decision hashes.
