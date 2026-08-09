# Stage 04 — Acceptance Test Specification

**Status:** DRAFT FOR TEST REVIEW

The source of truth is `docs/OSINT_AGENT_TZ_V1.md`. These tests describe observable behavior; they do not require a particular implementation unless the architecture has already approved that boundary.

| ID | Given | When | Then / Oracle | Severity |
|---|---|---|---|---|
| AC-01 | valid ResearchTask and compatible DEV collectors with relevant fixtures | OSINT collection is executed | MaterialPackage is non-empty, task_id is preserved, each material has source_type and source_locator | BLOCKING |
| AC-02 | two different source observations contain identical raw payload | both are collected | both source observations remain represented; raw payload may be stored once; provenance for neither source is lost | BLOCKING |
| AC-03 | requested source type has no eligible collector | collection is attempted | MaterialPackage is empty, stop_reason is explicit and collection_errors is non-empty | MAJOR |
| AC-04 | collector can yield more items than task.max_items | collection is executed | delivered package never exceeds max_items and stop_reason identifies the limit | BLOCKING |
| AC-05 | one collector yields valid material and another collector raises an exception | collection is executed | valid material remains in package; failing collector is recorded in collection_errors; package is not corrupted | BLOCKING |
| AC-06 | MaterialPackage contains materials from different source types | Analyst consumes package | Analyst operates only on generic Material contract; no source-specific transport object is required | MAJOR |
| AC-07 | one requested source type is absent from package | Analyst processes package | gap is explicit and follow_up_task targets the missing source scope | MAJOR |
| AC-08 | follow-up research cannot resolve the gap | bounded DEV pipeline runs | number of cycles never exceeds configured max_cycles and final stop_reason reports the bound | BLOCKING |
| AC-09 | sourced analysis has no explicit gaps / or does contain a material gap | Socrates reviews it | first case => PASS with no follow-up; second case => RESEARCH_MORE with bounded ResearchTask | MAJOR |
| AC-10 | no live Telegram/Tor/production infrastructure is available | DEV acceptance suite is executed | required DEV acceptance tests can execute without production credentials or connectors | BLOCKING |

## Additional architecture-contract tests

These are not new product features; they protect Stage 03 decisions.

### AT-01 Collector isolation
A collector exception must not erase materials already returned by another collector.

### AT-02 Collector/transport separation
`TelegramCollector` accepts a transport through its minimal protocol and maps transport records into generic Material. The test must not require Teleproto itself.

### AT-03 DEV fixture determinism
The same fixture and ResearchTask should produce the same set of source locators and raw payloads, ignoring generated IDs/timestamps.

### AT-04 Storage restart semantics
After reopening the DEV store, previously stored raw payload hashes are known. However, this optimization must not cause provenance from a new source observation to disappear.

## Known expected failure before implementation change

**AC-02 is expected to fail against the current `MaterialStore` design.** Current code treats identical content hash as a reason to reject the second Material entirely. This expected failure is useful evidence of the Stage 03 defect and must be recorded, not hidden by weakening the test.
