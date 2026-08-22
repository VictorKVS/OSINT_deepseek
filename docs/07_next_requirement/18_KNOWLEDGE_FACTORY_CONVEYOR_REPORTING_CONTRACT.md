# Knowledge Factory Conveyor — Production Reporting Contract

**Status:** ACTIVE

Every execution pass must report measured progress, not narrative optimism.

## Required counters

### Work
- tasks_opened
- tasks_completed
- tasks_blocked
- source_candidates
- sources_verified
- sources_rejected
- acquisition_attempts
- acquisition_successes
- acquisition_failures
- bytes_acquired
- artifacts_created
- artifacts_reused
- unique_hashes
- versions_created
- versions_changed
- documents_by_stage_D0_D15
- structures_created
- chunks_created
- chunks_reused
- concepts_created
- concepts_reused
- definitions_created
- definitions_reused
- facts_requirements_claims_created
- facts_requirements_claims_reused
- entities_controls_methods_created
- relations_created
- conflict_candidates
- confirmed_conflicts
- context_splits
- gaps_unknowns
- analyst_pass
- analyst_rework
- analyst_inconclusive
- kb_ready_packages

### Quality/rework
- stage_failures_by_reason
- objects_reprocessed
- objects_reused
- corrective_work_items
- regression_failures
- registry_audit_mismatches

### Time/cost, only when measured
- elapsed_processing_seconds
- human_review_minutes
- tool_calls
- machine_cost
- time_to_first_verified_artifact
- time_to_D15

## Derived metrics

Derived metrics may be calculated only from measured denominators:

```text
acquisition_success_rate = successes / attempts
reuse_ratio = reused_objects / eligible_objects
rework_ratio = corrective_work_items / completed_work_items
stage_conversion_Dn_to_Dn1 = advanced / eligible
```

Comparison with a one-stream baseline requires an actual comparable one-stream sample. If unavailable, the report must say `BASELINE_NOT_AVAILABLE`; it must not invent an acceleration percentage.

Completion forecast requires:
1. measured remaining scope;
2. stable unit definition;
3. enough recent throughput observations;
4. known blocking dependencies.

Otherwise report `FORECAST_NOT_JUSTIFIED`.

## Report body

Every run closes with:

```text
RUN ID / date
active P0 task IDs
lane progress
new evidence
regression result
production counters: pass + cumulative
reuse/rework observations
blocked items and reason
single next bottleneck
speed vs one-stream baseline: measured value or BASELINE_NOT_AVAILABLE
remaining-volume forecast: value/range or FORECAST_NOT_JUSTIFIED
```

## Reconciliation rule

Reported counters must be derivable from registries/audit/test outputs. If the dashboard number cannot be reconciled to machine-readable evidence, it is informational only and cannot close an acceptance gate.
