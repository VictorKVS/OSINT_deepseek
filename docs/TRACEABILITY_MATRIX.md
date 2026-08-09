# Traceability Matrix

**Status:** STAGE 03 REVIEWED / STAGE 04 TEST DESIGN PENDING

| Requirement / AC | Architecture owner | Existing implementation | Existing test | Architecture decision | Current status |
|---|---|---|---|---|---|
| AC-01 collect materials | OSINTAgent + Collector | `father_osint/agent.py`, `collectors/dev.py` | `test_father_osint_mvp.py` | KEEP | UNVERIFIED |
| AC-02 preserve distinct source observations while reusing identical raw payload | MaterialStore + Material contract | `father_osint/storage.py` currently rejects later identical payload observation | existing dedup test is insufficient / semantically outdated | CHANGE REQUIRED | TEST MUST BE REDESIGNED |
| AC-03 explicit no-collector result | OSINTAgent | `father_osint/agent.py` | `test_father_osint_mvp.py` | KEEP | UNVERIFIED |
| AC-04 bounded max_items | OSINTAgent | `father_osint/agent.py` | `test_father_osint_mvp.py` | KEEP | UNVERIFIED |
| AC-05 collector failure isolation | OSINTAgent | `father_osint/agent.py` | coverage to confirm/add | KEEP | UNVERIFIED |
| AC-06 generic Analyst handoff | MaterialPackage / DEV Analyst | `models.py`, `analysis.py` | `test_simple_analyst.py` | KEEP contracts; Analyst = DEV HARNESS | UNVERIFIED |
| AC-07 follow-up research | DEV Analyst | `analysis.py` | `test_simple_analyst.py` | KEEP DEV HARNESS | UNVERIFIED |
| AC-08 hard maximum cycle | DEV orchestration | `review_pipeline.py` target; `pipeline.py` frozen duplicate candidate | `test_dev_pipeline.py` currently targets older pipeline | KEEP review pipeline / RETIRE candidate old pipeline | TEST REALIGNMENT REQUIRED |
| AC-09 Socrates PASS/RESEARCH_MORE | DEV Socrates | `socrates.py`, `review_pipeline.py` | `test_simple_socrates.py` | KEEP DEV HARNESS | UNVERIFIED |
| AC-10 no PROD dependency for DEV proof | Architecture | fixture collectors/local store | document inspection | KEEP; transports deferred | PARTIALLY SUPPORTED |

## Stage 03 file disposition summary

| File/group | Decision |
|---|---|
| `models.py` | KEEP; contract terminology/semantics under test review |
| `agent.py` | KEEP |
| `collectors/dev.py` | KEEP DEV ONLY |
| `collectors/telegram.py` | KEEP CONTRACT; live use deferred |
| `storage.py` | CHANGE REQUIRED after approved failing test |
| `analysis.py` | KEEP DEV HARNESS |
| `socrates.py` | KEEP DEV HARNESS |
| `review_pipeline.py` | KEEP PROVISIONALLY as target DEV orchestration |
| `pipeline.py` | FREEZE / RETIRE-DELETE CANDIDATE after regression evidence |
| `transports/teleproto.py` | DEFER / FROZEN |
| `telegram_bridge/` | DEFER / FROZEN |
| legacy `core/`, `services/`, old scripts | LEGACY / OUTSIDE CURRENT ARCHITECTURE |

## Rule

No row becomes VERIFIED because code exists. Verification requires an executed test or explicit review evidence linked back to the requirement. No implementation change is made solely because architecture review found a defect: first Stage 04 defines the expected test, then the test is run/fails as evidence, then implementation is changed.
