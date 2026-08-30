# PROGRAMMING_KB Source Cards — Batch B: Python / Backend

Status: **SOURCE_VERIFIED BATCH / 8 NEW CARDS**  
Verification date: **2026-08-14**

Purpose: begin the canonical source layer for the first bounded Programmer Agent MVP. These records identify what the official source can prove and, equally importantly, what it cannot prove.

---

## SRC-PKB-0008 — Python 3 documentation / Language Reference family

```yaml
source_id: SRC-PKB-0008
publisher: Python Software Foundation / Python documentation project
source_class: E1
canonical_locator: https://docs.python.org/3/
observed_stable_documentation: 3.14.6
status: CURRENT_OFFICIAL
retrieved_at: 2026-08-14
scope: Python language reference, standard library, setup/usage and official documentation
review_trigger:
  - project Python runtime changes
  - new Python feature series
  - relevant semantics/deprecation changes
```

**Important applicability rule:** the FATHER repository baseline currently reports Python 3.12 in its verified DEV v1 journal. Therefore a fact found only in Python 3.14 documentation cannot silently authorize a 3.12 implementation. Version-specific retrieval must target the runtime actually being used.

**Use for:** language semantics, syntax, built-ins/stdlib behavior, deprecations and official implementation-facing guidance.

**Caution:** the Python Language Reference itself explains that it aims to be precise but is not a completely formal language specification and warns against confusing implementation detail with language semantics. Implementation-specific claims therefore require CPython/version-specific evidence where relevant.

**PROGRAMMING_KB mappings:** D03, D02, D06, D08, D12.

---

## SRC-PKB-0009 — PEP 0 / Python Enhancement Proposal index

```yaml
source_id: SRC-PKB-0009
publisher: Python PEP Editors / Python community governance
source_class: E1
canonical_locator: https://peps.python.org/pep-0000/
version: active index
status: CURRENT_INDEX
retrieved_at: 2026-08-14
scope: authoritative index/metadata for Python Enhancement Proposals
review_trigger:
  - specific decision references a PEP
```

**Use for:** locating the controlling PEP and checking its type/status: Accepted, Final, Active, Deferred, Rejected, Superseded, Withdrawn, etc.

**Do not use:** PEP 0 is an index, not evidence that every listed proposal is implemented or appropriate. The individual PEP status and target Python version must be checked.

**PROGRAMMING_KB mappings:** D03, D04, D06, D10.

---

## SRC-PKB-0010 — Python version lifecycle / Developer Guide

```yaml
source_id: SRC-PKB-0010
publisher: Python Developer's Guide / Python core development project
source_class: E4
canonical_locator: https://devguide.python.org/versions/
status: CURRENT_OFFICIAL_LIFECYCLE
retrieved_at: 2026-08-14
observed_states:
  3.15: prerelease
  3.14: bugfix
  3.13: bugfix
  3.12: security
review_trigger:
  - runtime selection/reselection
  - support phase change
```

**Use for:** production runtime lifecycle/support decisions and upgrade pressure.

**Current implication:** `3.12` remains supported but is in the security-fixes phase, while `3.14` is in bugfix maintenance and `3.15` is prerelease as of the verification date. This is a decision input, not by itself a mandate to upgrade: compatibility, dependencies, testing cost and required features still need a D2 decision.

**PROGRAMMING_KB mappings:** D03, D10, D11.

---

## SRC-PKB-0011 — RFC 9110 / HTTP Semantics

```yaml
source_id: SRC-PKB-0011
publisher: IETF / RFC Editor
source_class: E1
canonical_locator: https://www.rfc-editor.org/rfc/rfc9110.html
identifier: RFC 9110 / STD 97
status: INTERNET_STANDARD
published_at: 2022-06
retrieved_at: 2026-08-14
scope: HTTP core semantics shared by HTTP versions
review_trigger:
  - RFC update/obsoletion
  - protocol-semantic decision
```

**Use for:** method semantics, status codes, representations, fields, conditional behavior and protocol conformance requirements.

**Do not replace with:** framework documentation when deciding what HTTP itself means. FastAPI/Starlette behavior is an implementation layer under the HTTP contract.

**PROGRAMMING_KB mappings:** D04, D01, D09.

---

## SRC-PKB-0012 — OpenAPI Specification

```yaml
source_id: SRC-PKB-0012
publisher: OpenAPI Initiative
source_class: E1
canonical_locator: https://spec.openapis.org/oas/
observed_latest_listed_version: 3.2.0
status: CURRENT_SPEC_FAMILY
retrieved_at: 2026-08-14
scope: machine-readable HTTP API description contract
review_trigger:
  - project OpenAPI version changes
  - new OAS release
```

**Use for:** API contract structure, operations, schemas and interoperability expectations.

**Important source rule:** the official OpenAPI site notes that schemas can detect many errors but are not guaranteed to detect every specification violation; if schema and specification text disagree, specification text controls. Therefore a schema-validation PASS cannot be treated as complete contract conformance proof.

**PROGRAMMING_KB mappings:** D04, D08, D01.

---

## SRC-PKB-0013 — PostgreSQL current concurrency / transaction isolation documentation

```yaml
source_id: SRC-PKB-0013
publisher: PostgreSQL Global Development Group
source_class: E4
canonical_locator: https://www.postgresql.org/docs/current/transaction-iso.html
observed_current_major_docs: 18
status: CURRENT_OFFICIAL_IMPLEMENTATION_DOC
retrieved_at: 2026-08-14
scope: PostgreSQL transaction isolation and concurrency behavior
review_trigger:
  - project PostgreSQL major version changes
  - transaction/concurrency decision
```

**Use for:** exact PostgreSQL behavior of Read Committed, Repeatable Read and Serializable, concurrency anomalies, serialization failures and retry expectations.

**Do not infer:** generic SQL/database semantics for every DBMS. PostgreSQL explicitly documents implementation details that may differ from other systems.

**PROGRAMMING_KB mappings:** D05, D06, D08, D11, D12.

---

## SRC-PKB-0014 — pytest stable documentation

```yaml
source_id: SRC-PKB-0014
publisher: pytest project
source_class: E4
canonical_locator: https://docs.pytest.org/en/stable/
status: CURRENT_OFFICIAL_IMPLEMENTATION_DOC
retrieved_at: 2026-08-14
scope: pytest execution, assertions, fixtures, parametrization, plugins and test integration
review_trigger:
  - pytest major behavior/version change
  - testing architecture decision
```

**Use for:** correct use of pytest and framework-specific test mechanics.

**Do not use alone for:** proving test strategy quality. The existence of tests or a passing pytest run does not prove adequate test selection, oracle quality, mutation resistance, property coverage or system acceptance.

**PROGRAMMING_KB mappings:** D08.

---

## SRC-PKB-0015 — OpenTelemetry Specification

```yaml
source_id: SRC-PKB-0015
publisher: OpenTelemetry project
source_class: E1
canonical_locator: https://opentelemetry.io/docs/specs/otel/
observed_spec_version: 1.59.0
status: CURRENT_SPEC
retrieved_at: 2026-08-14
scope: telemetry API/SDK/data concepts for traces, metrics and logs
review_trigger:
  - specification version change
  - observability architecture decision
```

**Use for:** vendor-neutral telemetry concepts, API/SDK separation, traces/metrics/logs and conformance vocabulary.

**Design note:** OpenTelemetry's own specification principles emphasize stability, consistency and simplicity and state that abstractions should justify their cost. PROGRAMMING_KB treats this as supporting evidence for the broader smallest-sufficient-complexity rule, not as proof for unrelated architecture choices.

**PROGRAMMING_KB mappings:** D11, D10, D12.

---

## Batch B quality check

```text
new source cards                      8
cumulative source cards              15
Python/runtime canonical cards        3
API/protocol cards                    2
PostgreSQL/data cards                 1
testing framework cards               1
observability specification cards     1
version/applicability warning          8/8
explicit evidence boundary             8/8
```

## What this batch enables next

These cards are enough to start producing **specific Knowledge Objects**, but not enough to declare any domain `MIN-COVERED`.

First candidate Knowledge Objects:

1. `Python version-sensitive recommendation must match project runtime`.
2. `Accepted/Final PEP status must be checked before a PEP is treated as implemented guidance`.
3. `HTTP method semantics come from RFC 9110, not from framework convention`.
4. `OpenAPI schema validation is necessary but not sufficient for full OAS conformance`.
5. `PostgreSQL Serializable requires an application retry path for serialization failures`.
6. `Passing pytest is execution evidence, not test-strategy sufficiency evidence`.
7. `Observability API and SDK responsibilities should remain decoupled where OTel integration is used`.

Each of these must still be converted into a Knowledge Object with applicability limits, counter-evidence/limitations and a verification method before being marked VALIDATED.
