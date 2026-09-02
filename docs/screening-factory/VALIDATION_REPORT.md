# Screening Factory M3 validation report

**Executed:** 2026-09-03  
**Scope:** new `screening_factory/**`, docs, schemas and synthetic fixture.  
**Network:** disabled; no live subject data was collected.

## Actual result

```text
Python compileall                                  PASS
pytest                                             17 passed
profiles                                           4
unique check definitions                          44
profile-check assignments                         71
official source descriptors                       16
synthetic journal chain                           PASS
JSON Schema Draft 2020-12 meta-validation         PASS (5 schemas)
request/plan/run/source-registry fixtures          PASS
individual check-result fixtures                  PASS (17 results)
```

The fixture is not a benchmark of provider latency or investigative accuracy. It validates orchestration, terminal semantics, parallel waves, report/dashboard generation, source contracts and journal integrity.
