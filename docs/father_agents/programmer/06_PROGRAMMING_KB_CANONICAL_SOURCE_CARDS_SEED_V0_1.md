# PROGRAMMING_KB Canonical Source Cards — Seed v0.1

Status: **SOURCE_VERIFIED SEED / 7 CARDS**  
Verification date: **2026-08-14**

These cards turn the initial source register into operational evidence records. They are intentionally short: later ingestion may split them into machine-readable objects, but the semantic fields are fixed first.

---

## SRC-PKB-0001 — IEEE SWEBOK Guide V4.0a

```yaml
source_id: SRC-PKB-0001
publisher: IEEE Computer Society
source_class: E3
canonical_locator: https://www.computer.org/education/bodies-of-knowledge/software-engineering
version: V4.0a
status: CURRENT
retrieved_at: 2026-08-14
scope: profession-wide software engineering body of knowledge
review_trigger:
  - new SWEBOK revision
  - major restructuring of knowledge areas
```

**Use for:** profession map, terminology, durable engineering knowledge areas, curated deeper-reference discovery.

**Do not use alone for:** proving that a specific framework, language or architecture is the best choice for a concrete project.

**PROGRAMMING_KB mappings:** D01-D12, especially D01/D07/D08/D10.

---

## SRC-PKB-0002 — ISO/IEC 25010:2023

```yaml
source_id: SRC-PKB-0002
publisher: ISO/IEC
source_class: E1
canonical_locator: https://www.iso.org/standard/78176.html
version: 2023 / edition 2
status: CURRENT
retrieved_at: 2026-08-14
scope: product quality model
copyright_handling: metadata and derived mappings only; do not copy protected full standard text
review_trigger:
  - new edition/amendment
```

**Use for:** converting vague non-functional goals into named quality characteristics and measurable project acceptance criteria.

**Do not use alone for:** selecting a technology or proving a system meets a quality target without project measurements.

**PROGRAMMING_KB mappings:** D01, D08, D09, D11, D12.

---

## SRC-PKB-0003 — NIST SP 800-218 SSDF v1.1

```yaml
source_id: SRC-PKB-0003
publisher: NIST
source_class: E1
canonical_locator: https://csrc.nist.gov/pubs/sp/800/218/final
version: 1.1
status: CURRENT_FINAL_BASELINE
published_at: 2022-02-03
retrieved_at: 2026-08-14
scope: secure software development framework
review_trigger:
  - final publication of SP 800-218 revision
  - NIST withdrawal/supersession notice
```

**Use for:** secure-SDLC practices, organizational/development control mapping and DevSecOps baseline requirements.

**Do not use alone for:** application-specific threat modeling or proving implementation security.

**PROGRAMMING_KB mappings:** D09, D10 plus cross-cutting D01/D08.

---

## SRC-PKB-0004 — NIST SP 800-218 Rev.1 / SSDF v1.2 draft

```yaml
source_id: SRC-PKB-0004
publisher: NIST
source_class: E1
canonical_locator: https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
version: 1.2 initial public draft
status: DRAFT_MONITOR
published_at: 2025-12-17
retrieved_at: 2026-08-14
scope: proposed SSDF revision
review_trigger:
  - new draft
  - final publication
```

**Use for:** change monitoring and future migration analysis.

**Do not use as:** silent replacement for the current final SSDF v1.1 baseline.

**PROGRAMMING_KB mappings:** D09, D10.

---

## SRC-PKB-0005 — OWASP ASVS 5.0.0

```yaml
source_id: SRC-PKB-0005
publisher: OWASP Foundation / OWASP ASVS project
source_class: E1
canonical_locator: https://owasp.org/www-project-application-security-verification-standard/
version: 5.0.0
status: CURRENT_STABLE
retrieved_at: 2026-08-14
scope: application security verification requirements
review_trigger:
  - new stable ASVS release
```

**Use for:** traceable application-security requirements and verification/test mapping.

**Do not use alone for:** enterprise risk acceptance, system-specific threat modeling, supply-chain assurance or proof that a scanner found every vulnerability.

**PROGRAMMING_KB mappings:** D09, D08, D01.

---

## SRC-PKB-0006 — SLSA Specification v1.2

```yaml
source_id: SRC-PKB-0006
publisher: SLSA project / OpenSSF ecosystem
source_class: E1
canonical_locator: https://slsa.dev/spec/v1.2/
version: 1.2
status: APPROVED_CURRENT
retrieved_at: 2026-08-14
scope: software supply-chain source/build assurance and provenance
review_trigger:
  - new approved SLSA specification
```

**Use for:** source/build provenance, build integrity, supply-chain assurance design and evidence vocabulary.

**Do not use alone for:** dependency vulnerability acceptance, application security or runtime security.

**PROGRAMMING_KB mappings:** D10, D09.

---

## SRC-PKB-0007 — OpenSSF Scorecard

```yaml
source_id: SRC-PKB-0007
publisher: OpenSSF
source_class: E4
canonical_locator: https://openssf.org/scorecard/
version: rolling project/tool
status: ACTIVE
retrieved_at: 2026-08-14
scope: automated signals about open-source project security practices
review_trigger:
  - major tool/check model change
  - project deprecation
```

**Use for:** one input into dependency/upstream project risk review and automated evidence collection.

**Do not use as:** a single-number dependency approval gate. A high/low score cannot replace version-specific vulnerability, maintainer, release, license, transitive-dependency and project-exposure analysis.

**PROGRAMMING_KB mappings:** D10, D09.

---

## Seed quality check

```text
cards created                       7
E1 authoritative/spec cards         5
E3 profession consensus cards       1
E4 official practice/tool cards     1
version/status recorded             7/7
canonical locator recorded          7/7
explicit use boundary               7/7
review trigger                      7/7
```

These seven cards do **not** satisfy a single FATHER domain MIN gate yet. They form the top evidence layer from which detailed Knowledge Objects are derived.

## Next source-card batch

Priority Batch B:

1. Python language reference.
2. Python standard library reference.
3. Python PEP index + selected normative PEPs tied to concrete decisions.
4. CPython lifecycle/version support source.
5. IETF HTTP semantics.
6. OpenAPI specification.
7. PostgreSQL current documentation: transaction isolation.
8. PostgreSQL indexing/planner documentation.
9. pytest official documentation.
10. OpenTelemetry specification.

Batch B completion does not automatically validate claims; each Knowledge Object still needs applicability, limitations and verification method.
