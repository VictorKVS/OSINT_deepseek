# Traceability Matrix

**Status:** INITIAL / MUST BE UPDATED AFTER TEST RUNS

| Requirement / AC | Architecture owner | Existing implementation | Existing test | Current status |
|---|---|---|---|---|
| AC-01 collect materials | OSINTAgent + Collector | `father_osint/agent.py`, `collectors/dev.py` | `test_father_osint_mvp.py` | UNVERIFIED |
| AC-02 deduplicate obvious identical content | MaterialStore | `father_osint/storage.py` | `test_father_osint_mvp.py` | UNVERIFIED |
| AC-03 explicit no-collector result | OSINTAgent | `father_osint/agent.py` | `test_father_osint_mvp.py` | UNVERIFIED |
| AC-04 bounded max_items | OSINTAgent | `father_osint/agent.py` | `test_father_osint_mvp.py` | UNVERIFIED |
| AC-05 collector failure isolation | OSINTAgent | `father_osint/agent.py` | coverage to confirm | UNVERIFIED |
| AC-06 generic Analyst handoff | MaterialPackage / Analyst | `models.py`, `analysis.py` | `test_simple_analyst.py` | UNVERIFIED |
| AC-07 follow-up research | Analyst | `analysis.py` | `test_simple_analyst.py` | UNVERIFIED |
| AC-08 hard maximum cycle | DEV Pipeline | `pipeline.py`, `review_pipeline.py` | `test_dev_pipeline.py` | UNVERIFIED |
| AC-09 Socrates PASS/RESEARCH_MORE | Socrates | `socrates.py`, `review_pipeline.py` | `test_simple_socrates.py` | UNVERIFIED |
| AC-10 no PROD dependency for DEV proof | Architecture | fixture collectors/local store | document inspection | PARTIALLY SUPPORTED |

## Rule

No row becomes VERIFIED because code exists. Verification requires an executed test or explicit review evidence linked back to the requirement.
