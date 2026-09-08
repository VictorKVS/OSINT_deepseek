# Donor Compatibility Matrix — FATHER Unified Analyst M4

Status: PROVISIONAL / requires code-level compatibility tests

This matrix is the first Codex migration decision record. It is intentionally conservative: existing subsystems are donors, not automatically canonical.

## Decision vocabulary

- `KEEP` — semantics and implementation are suitable as-is behind a stable interface.
- `WRAP` — retain implementation but place a new M4 interface around it.
- `MIGRATE` — move selected logic into `father_analyst/**` with compatibility tests.
- `RETIRE` — stop extending the old path after the M4 replacement is proven.
- `CONFLICT` — donor semantics differ from the M4 contract; no silent merge.

## Matrix

| Donor | Valuable artifacts observed | Initial decision | M4 target | Required proof before integration |
|---|---|---|---|---|
| PR #23 `osint_workbench` | `analysis_zoo.py`, `analysis_models.py`, `analysis_builtins.py`, `graph.py`, `coverage.py`, `planner.py`, `jobs.py`, `policy.py`, evidence/store modules, workflow/service tests | `WRAP -> MIGRATE selectively` | Analysis Zoo, coverage/gaps, evidence/graph semantics | analyzer output cannot create FACT; failure isolation; consensus preserves dissent; graph edges retain evidence paths |
| PR #22 contract baseline | ADRs for FACT/CLAIM/OPINION, tool isolation, case/evidence models, tool-adapter/query-plan schemas, synthetic fixtures | `KEEP as contract donor` | M4 schemas/ADRs | map each old object to canonical M4 taxonomy; document unmapped fields; no schema copied without compatibility fixture |
| PR #31 `screening_factory` | `planner.py`, `runner.py`, `scheduler.py`, `registry.py`, `sources.py`, 5-stream model, honest BLOCKED states, schemas and validation | `WRAP` | Tool Factory scheduling and adapter health/policy | prove bounded parallelism; no active/intrusive execution; `NO_HIT_IN_SCOPE` remains scoped; adapter failure does not poison other workers |
| PR #26 Bitcoin | evidence-safe Bitcoin parsing, flow separation, source-conflict/provenance-contamination tests | `WRAP` | `CRYPTO/BITCOIN` adapter family | wallet/entity attribution stays candidate-only; mixed transaction semantics preserved; parser zero-result fails closed |
| Existing Telegram TDLib/Telethon | transport/session/collection capability and existing regression suite | `WRAP` | `TELEGRAM_*` adapters | read-only/passive policy; raw message provenance retained; rate-limit/session failures explicit; no message->fact shortcut |
| PR #32 D14/D15 | `knowledge_factory_store.py`, transition logic, D14 decision application, D15 promotion binding and tamper tests | `KEEP + bridge` | Knowledge Promotion boundary | exact evidence/review version binding; batch/atomic transition; D14/D15 tamper tests green; no direct KB bypass |
| PR #33 Investigation Workspace / Graph Core | case-centric product model, `hypothesis_graph_ontology.json`, Case store baseline, graph/table/timeline shell | `KEEP + extend` | Case + Reasoning Graph | persistent graph store, allowed edge validation, rejected/superseded history, entity/reasoning graph separation |
| PR #11 Knowledge Factory | D0-D15 conveyor, acquisition, artifact/version, document compiler/chunks, knowledge-method/constraint work | `KEEP downstream` | Knowledge Factory | M4 promotion request maps exactly to accepted D14/D15 input; no semantic downgrade of provenance/uncertainty |

## Object convergence decisions

### Keep distinct

The following object types must not be collapsed during migration:

`RAW_ARTIFACT != SOURCE_OBSERVATION != OBSERVATION != FINDING != EVIDENCE != CLAIM != FACT != HYPOTHESIS != CONCLUSION`

`RELATION_CANDIDATE != RELATION`

`ANALYST_OPINION != REVIEW_DECISION`

`REVIEW_DECISION != D14_REVIEW_RESULT`

### Required bridges

1. `ToolRun -> RawArtifact -> Observation[]`
2. `Observation -> Evidence` only through review state transition
3. `Evidence -> RelationCandidate` with explicit basis
4. `Evidence/Claim/Fact -> Hypothesis` through typed support/counter edges
5. `Analyzer -> AnalystOpinion`, never Fact
6. `Socrates -> ReviewChallenge/Disposition`, never KB write
7. `Human ReviewDecision -> PromotionRequest`
8. `PromotionRequest -> D14 -> D15 -> KnowledgeObject`

## First compatibility tests Codex must add

### C-M4-001 — Tool failure isolation
One synthetic tool fails; other workers complete; hypothesis is not rejected because of failure.

### C-M4-002 — Source independence
Ten mirrored observations map to one independence group and do not count as ten independent supports.

### C-M4-003 — Candidate relation discipline
A tool proposes `ALIAS_OF`; graph stores `RELATION_CANDIDATE`; only reviewed evidence can produce supported `RELATION`.

### C-M4-004 — Analysis Zoo discipline
Three analyzers disagree; all opinions are retained; consensus cannot set `FACT` or authorize promotion.

### C-M4-005 — Reasoning graph history
Counter-evidence weakens/rejects a hypothesis without deleting the prior state or provenance.

### C-M4-006 — D14/D15 binding
Changing any evidence/review version after Human Review invalidates the PromotionRequest and blocks D15.

### C-M4-007 — Token-bounded local context
Raw corpus remains local; AnalysisPacket contains only selected IDs/excerpts within a deterministic size budget.

### C-M4-008 — Full replay
A promoted KnowledgeObject can be traced back to D15, D14, Human Review, hypothesis/relation, evidence, observation, tool run and raw artifact.

## Immediate implementation decision

The first runtime code should **not** connect real external tools. It should implement canonical contracts and a synthetic Tool Factory vertical so compatibility tests can be written before donor migration.
