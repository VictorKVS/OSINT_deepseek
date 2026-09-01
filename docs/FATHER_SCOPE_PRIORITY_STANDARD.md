# FATHER Scope & Priority Standard

## Mandatory rule

Every managed area in FATHER is classified on **two independent axes**:

1. **Maturity depth:** `MIN → MEDIUM → MAX`.
2. **Importance:** `NECESSARY → DESIRABLE → INTERESTING_LATER`.

The axes must never be collapsed into one score. `MAX` does not mean high priority, and `NECESSARY` does not mean maximum depth.

Canonical machine-readable policy: `config/father_scope_priority_standard.json`.
Initial cross-product matrix: `config/father_area_priority_matrix.json`.

## Meaning of maturity

### MIN

Minimum professionally usable, testable end-to-end baseline. It closes the critical path and keeps gaps explicit.

### MEDIUM

Normal production-grade professional depth: variants, independent evidence, examples, controls, conflicts, regression and operator usability.

### MAX

Expert/advanced target for the current product horizon: monitoring, benchmarks, optimization, deep edge cases, measured reuse/rework and challengeable golden decisions.

## Meaning of importance

### NECESSARY

Required for legality, safety, correctness, core usefulness, acceptance, or a declared professional competency. Unresolved `NECESSARY` work at or below the requested maturity blocks completion.

### DESIRABLE

Materially improves quality, reliability, usability, coverage or economics, but does not block the minimum acceptance gate.

### INTERESTING_LATER

Potentially useful research, experiment, rare specialization or future opportunity. It remains visible in HOLD/backlog and is not silently deleted.

## 3×3 planning matrix

| | NECESSARY | DESIRABLE | INTERESTING_LATER |
|---|---|---|---|
| **MIN** | Do first; closes basic critical path | Improve basic usability/coverage | Keep as low-cost future idea |
| **MEDIUM** | Production-quality obligations | Strong professional improvement | Optional breadth/specialization |
| **MAX** | Advanced capability required by current target | Expert optimization | Research/future frontier |

## Execution order

Default work order is:

1. `MIN + NECESSARY`
2. `MEDIUM + NECESSARY`
3. `MAX + NECESSARY` when the declared target requires MAX
4. `MIN/MEDIUM/MAX + DESIRABLE` according to available capacity and value
5. `INTERESTING_LATER` only after core work is closed or when a concrete trigger raises its importance

This ordering does not prohibit a `MAX + NECESSARY` item. Example: exact historical reconstruction can be MAX-depth but necessary for a concrete audit dispute. Likewise, a `MIN + INTERESTING_LATER` item can exist if the idea is easy to prototype but currently non-essential.

## Applies to

The standard applies to documents and applicability bindings, regulatory sectors, role topics and competencies, library orders, product features, modules, project tasks, source targets, research hypotheses, UI work and backlog items.

## Regulatory rule

For Russian regulatory scope, currentness and applicability of relevant mandatory/conditional requirements are normally `MIN + NECESSARY`. Additional explanatory materials may be `MIN/MEDIUM + DESIRABLE`. Historical versions without a concrete point-in-time need normally remain `MAX + INTERESTING_LATER`.

A document's legal status is not its priority. A current document may be `INTERESTING_LATER` for a role if it is not applicable. A future-effective act may be `NECESSARY` if it will affect the current project horizon.

## Reuse rule

Classification never creates duplicate canonical documents. One document remains in the Global Document Registry; each role/project/domain binding carries its own `maturity_level` and `importance_class`.

Example:

- `152-ФЗ` → `LEGAL_COMPLIANCE`: `MIN + NECESSARY`
- the same `152-ФЗ` → `PROGRAMMER` when software processes PDn: `MIN + NECESSARY`
- the same document → an unrelated standalone utility project: binding may be `NOT_APPLICABLE`, not a duplicate document.

## Completion rule

A scope may be declared complete at target maturity only when every applicable `NECESSARY` item at that maturity or below is `PASS`, `REUSED`, `NOT_APPLICABLE` with evidence, or an explicitly accepted GAP according to the relevant gate. `DESIRABLE` and `INTERESTING_LATER` work must remain visible but do not silently block the core gate unless promoted to `NECESSARY` with a traced reason.

## Change control

Any change of `maturity_level` or `importance_class` must preserve:

- who changed it;
- why;
- previous value;
- new value;
- task/command/trace ID;
- evidence or project trigger when applicable.
