# PROGRAMMING_KB Knowledge Objects — Seed v0.1

Status: **PROVISIONAL / 7 LIMITED OBJECTS**  
Date: **2026-08-14**

These are the first objects that transform source cards into actionable engineering knowledge. They are deliberately `LIMITED`, not `VALIDATED`: the evaluation corpus and independent review gate do not exist yet.

---

## PKB-0001 — Match Python evidence to the actual project runtime

```yaml
knowledge_id: PKB-0001
status: LIMITED
claim: "A Python recommendation that depends on language/runtime behavior must be checked against the Python version actually used by the target project."
knowledge_domain: D03
source_refs: [SRC-PKB-0008, SRC-PKB-0010]
source_classes: [E1, E4]
retrieved_at: 2026-08-14
applies_when:
  - behavior, syntax, stdlib, concurrency, deprecation or runtime semantics may differ by Python version
assumptions:
  - target runtime can be identified
known_risks:
  - using current Python documentation for an older runtime can introduce unsupported syntax or changed behavior
verification_method: "Read target runtime from project/CI/runtime evidence and retrieve the matching official documentation before accepting the recommendation."
confidence_state: PROVISIONAL
```

Project-context note: the current FATHER journal records a verified Python 3.12 DEV v1 baseline; therefore Python 3.14-only behavior is not automatically applicable to that baseline.

---

## PKB-0002 — PEP status is part of applicability

```yaml
knowledge_id: PKB-0002
status: LIMITED
claim: "A Python PEP must not be treated as implemented/current guidance solely because it exists; its type, status and target/relevant Python version must be checked."
knowledge_domain: D03
source_refs: [SRC-PKB-0009]
source_classes: [E1]
applies_when:
  - a technical decision cites a PEP
known_risks:
  - Accepted may not yet mean implemented
  - Rejected, Deferred, Superseded or Withdrawn proposals can be misread as current behavior
verification_method: "Resolve the PEP from PEP 0, record its status/type, then verify implementation/version evidence in the relevant Python release documentation."
confidence_state: PROVISIONAL
```

---

## PKB-0003 — HTTP semantics precede framework convention

```yaml
knowledge_id: PKB-0003
status: LIMITED
claim: "When a backend decision depends on the meaning of HTTP methods, status codes, representations or protocol requirements, the controlling semantic evidence is the applicable HTTP RFC rather than a web framework convention."
knowledge_domain: D04
source_refs: [SRC-PKB-0011]
source_classes: [E1]
applies_when:
  - designing or reviewing HTTP API behavior
known_risks:
  - framework defaults may be convenient but can be mistaken for protocol semantics
verification_method: "Map the API behavior to RFC 9110 requirements, then separately verify framework implementation behavior."
confidence_state: PROVISIONAL
```

Framework documentation remains necessary for implementation details; the rule only separates protocol semantics from implementation mechanics.

---

## PKB-0004 — OpenAPI schema PASS is not complete OpenAPI conformance evidence

```yaml
knowledge_id: PKB-0004
status: LIMITED
claim: "Passing an OpenAPI schema validator is not sufficient evidence of complete conformance with the OpenAPI Specification."
knowledge_domain: D04
source_refs: [SRC-PKB-0012]
source_classes: [E1]
applies_when:
  - OpenAPI document validation is used as an acceptance gate
known_risks:
  - schema-valid documents can still violate specification text
verification_method: "Run schema validation, then test material contract requirements against the specification text and consumer/provider behavior."
confidence_state: PROVISIONAL
```

The official specification site explicitly states that schemas are not guaranteed to catch all specification violations and that specification text controls on disagreement.

---

## PKB-0005 — PostgreSQL Serializable requires retry-aware application design

```yaml
knowledge_id: PKB-0005
status: LIMITED
claim: "If PostgreSQL Serializable isolation is used for concurrent write/read workloads, application logic must be prepared to retry transactions that fail with serialization failures."
knowledge_domain: D05
source_refs: [SRC-PKB-0013]
source_classes: [E4]
applies_when:
  - PostgreSQL Serializable isolation is selected
known_risks:
  - treating serialization failure as an unrecoverable ordinary error can break otherwise valid concurrent workflows
  - retries without bounded/idempotent transaction design can create secondary failures
verification_method: "Integration test creates a controlled serialization conflict, verifies SQLSTATE handling, bounded retry behavior, invariant preservation and final transaction outcome."
confidence_state: PROVISIONAL
```

This object does **not** say Serializable is always the best isolation level. Selecting isolation level is a separate D2 decision based on invariants, contention and measured cost.

---

## PKB-0006 — Test execution success is not test-strategy sufficiency

```yaml
knowledge_id: PKB-0006
status: LIMITED
claim: "A green pytest run proves that the collected tests passed under the observed environment; it does not by itself prove that the selected tests are sufficient for the requirement or risk."
knowledge_domain: D08
source_refs: [SRC-PKB-0014, SRC-PKB-0002]
source_classes: [E4, E1]
applies_when:
  - pytest results are presented as acceptance evidence
known_risks:
  - untested behaviors, weak assertions, missing negative cases and absent integration/security scenarios can remain invisible
verification_method: "Trace requirements/risks to tests, inspect test oracles and negative cases, and add mutation/property/contract/integration evidence where justified by the decision class."
confidence_state: PROVISIONAL
```

This is a sufficiency rule, not criticism of pytest: pytest is the execution framework; adequacy belongs to test design and requirement/risk coverage.

---

## PKB-0007 — OpenTelemetry API and implementation responsibilities should remain distinguishable

```yaml
knowledge_id: PKB-0007
status: LIMITED
claim: "When OpenTelemetry is adopted, application/library-facing telemetry API responsibilities should remain distinguishable from SDK/implementation/export responsibilities."
knowledge_domain: D11
source_refs: [SRC-PKB-0015]
source_classes: [E1]
applies_when:
  - OpenTelemetry is selected for observability
known_risks:
  - tight coupling to a concrete exporter/backend can reduce portability and make instrumentation changes harder
verification_method: "Architecture review checks dependency direction and an integration test proves telemetry can be routed/configured without rewriting domain instrumentation."
confidence_state: PROVISIONAL
```

This object does not authorize OpenTelemetry for every project. The decision to add telemetry infrastructure remains a D2 architecture/operations decision if it materially changes dependencies or runtime behavior.

---

## Seed status

```text
Knowledge Objects created       7
VALIDATED                       0
LIMITED                         7
PROVISIONAL                     7
independent critic reviewed      0
end-to-end evaluated             0
```

This status is intentional. The next promotion gate is not “add more citations”; it is **evaluate the objects in concrete engineering scenarios and let Principal Critic challenge applicability, counter-evidence and unnecessary complexity**.
