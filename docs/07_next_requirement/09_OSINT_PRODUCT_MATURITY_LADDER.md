# OSINT Product Maturity Ladder

Status: ACTIVE ROADMAP
Principle: BRAIN BEFORE TOOLS, but each maturity level must produce a usable end-to-end product.

## M0 — Lab / transport proof
Goal: prove safe, reproducible acquisition from one Telegram source.
Exit: authorized local session; bounded collection; RAW preserved; provenance; restart/reuse; tests GREEN.

## M1 — Minimal useful Telegram collector
Goal: Analyst gives a topic/task; OSINT Expert searches configured channels, collects relevant messages, text, URLs and metadata, follows explicit Telegram forward/source references where technically observable, and returns a package to Analyst.
Required: query/topic filter; multi-channel input; message text; URLs; timestamps; channel/message IDs; explicit forward origin; UNKNOWN when origin cannot be established; deduplication; provenance; acquisition report.
Exit: one command completes the flow on live Telegram and produces an auditable package.

## M2 — Reliable Telegram research assistant
Goal: reconnaissance before deep collection and controlled expansion along observable source/link chains.
Required: source map; entities/terms/domains; link extraction; forward/repost lineage; bounded chain traversal; checkpoints; failures; gaps; coverage; repeatable live tests.
Exit: multi-channel live scenario survives restart and returns the same evidence lineage.

## M3 — Evidence-aware OSINT Expert
Goal: evaluate what was collected, not merely collect it.
Required: Intelligence Analysis Methods KB; source reliability vs information credibility; provenance quality; independence/common-origin; corroboration/contradiction; primary/secondary evidence; versioned algorithms; CalculationRecord.
Exit: every qualitative label is backed by a named/versioned method and decision trace.

## M4 — Analytical reasoning system
Goal: turn evidence into traceable analytical judgments.
Required: hypotheses; competing hypotheses; counter-evidence; assumptions; uncertainty; sufficiency; stopping criteria; ConclusionRecord; reasoning provenance; Critic review.
Exit: conclusion can be reconstructed from evidence, methods, calculations, assumptions and critic decisions.

## M5 — Multi-source OSINT Expert MVP
Goal: apply the same evidence standard beyond Telegram.
Sources: Web/search, documents, GitHub/public code, archives and other approved open sources.
Required: unified Source/Material/Evidence contracts; cross-source deduplication; entity resolution; evidence-line graph; Analyst ↔ OSINT protocol.
Exit: one research request can be answered through several source classes with a unified AcquisitionReport and reasoning trace.

## M6 — Professional investigation workspace
Goal: product usable by a professional analyst repeatedly.
Required: case workspace; search-plan editor; evidence browser; graph/timeline; source cards; claim/hypothesis matrix; citations; audit log; export; reproducible reports; role/access model; secret hygiene; observability.
Exit: independent analyst can operate the product without developer intervention.

## M7 — Learning and calibration platform
Goal: improve algorithms from accumulated cases without corrupting evidence history.
Required: immutable historical cases; replay harness; gold/benchmark cases; human/critic labels; algorithm A/B; calibration metrics; error taxonomy; regression suite; Golden/Experimental method registry.
Learning sequence: supervised/replay evaluation first; preference learning where justified; reinforcement learning only with explicit reward functions, safe simulation/sandbox, measurable outcomes and rollback. Do not call ordinary KB accumulation “deep learning”.
Exit: a new algorithm version can demonstrate measurable improvement over the previous version on held-out cases.

## M8 — Advanced adaptive expert system
Goal: dynamically select research tactics and analytical methods by task class and evidence state.
Required: policy selection; cost/time/risk budgets; adaptive search; active learning; tool capability registry; safe external-tool orchestration; uncertainty-aware escalation to humans; longitudinal source-history models.
Exit: system improves research efficiency while maintaining or improving calibrated analytical quality.

## M9 — Showcase / serious product
Goal: product that can be demonstrated publicly to professional customers without excuses.
Required gates:
- polished UX and documented workflows;
- installation/deployment and demo dataset;
- security review and threat model;
- privacy/legal boundaries;
- complete audit/reasoning provenance;
- benchmark report with limitations;
- reproducible demo cases;
- reliability/SLOs/monitoring/backups;
- documentation for analyst, administrator and developer;
- Engineering Council + Principal Critic sign-off;
- no secrets/test sessions in repository;
- clear statement of what the system knows, does not know and cannot prove.
Exit: repeatable end-to-end demonstration from ResearchRequest to cited ConclusionRecord, with evidence graph, calculations, critic review and reproducible report.

## Development rule
For every level use three passes:
1. MIN — complete end-to-end path, simplest professional implementation.
2. MED — reliability, edge cases, explainability, better tests and usability.
3. MAX — advanced methods, optimization, automation and learning.

Do not begin MAX work at a lower level while a higher-priority MIN end-to-end path is broken.

## Immediate queue
1. Finish M1 Telegram collector as a simple useful product.
2. Finish M2 observable chain traversal/reconnaissance.
3. Build M3 Intelligence Analysis Methods KB and replace unsupported qualitative judgments.
4. Build M4 reasoning provenance/ConclusionRecord/CalculationRecord.
5. Close current Telegram M5/G11 acceptance using the matured algorithms.
6. Add new source classes only after the Telegram reference implementation is stable.
7. Build learning/calibration platform after enough versioned cases and measurable labels exist.
