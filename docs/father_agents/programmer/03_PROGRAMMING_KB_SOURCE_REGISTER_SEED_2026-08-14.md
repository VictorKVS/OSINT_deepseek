# PROGRAMMING_KB Source Register — Seed 2026-08-14

Status: **SOURCE_VERIFIED SEED / INCOMPLETE BY DESIGN**

This register contains the first authoritative sources verified for the Programmer Agent knowledge track. It is a seed, not a claim of full coverage.

## A. Verified authoritative baseline

| ID | Source | Class | Verified status on 2026-08-14 | Primary use |
|---|---|---|---|---|
| SRC-PKB-0001 | IEEE Computer Society — SWEBOK Guide V4.0a | E3 consensus body of knowledge | V4.0a is the latest published SWEBOK revision; IEEE page notes minor revision dated 2025-09-25 | profession map, requirements, design, construction, testing, quality, architecture, operations, security |
| SRC-PKB-0002 | ISO/IEC 25010:2023 SQuaRE Product Quality Model | E1 standard | published edition 2, 2023-11 | measurable software/product quality characteristics and acceptance criteria |
| SRC-PKB-0003 | NIST SP 800-218 — SSDF v1.1 | E1 official guidance | FINAL, published 2022-02-03 | secure SDLC baseline and secure-development practices |
| SRC-PKB-0004 | NIST SP 800-218 Rev.1 — SSDF v1.2 | E1 official draft | INITIAL PUBLIC DRAFT, published 2025-12-17; not final | future-delta monitoring only; must not silently replace final SSDF v1.1 |
| SRC-PKB-0005 | OWASP ASVS 5.0.0 | E1 open verification standard | latest stable version reported by OWASP project page | application-security requirements and testable security controls |
| SRC-PKB-0006 | SLSA Specification v1.2 | E1 consensus specification | APPROVED; current version | source/build provenance and software-supply-chain integrity |
| SRC-PKB-0007 | OpenSSF Scorecard | E4 official ecosystem practice/tool | active OpenSSF project | automated dependency/project security-risk signals; evidence input, never sole approval gate |

## B. Canonical URLs

```text
SRC-PKB-0001 https://www.computer.org/education/bodies-of-knowledge/software-engineering
SRC-PKB-0002 https://www.iso.org/standard/78176.html
SRC-PKB-0003 https://csrc.nist.gov/pubs/sp/800/218/final
SRC-PKB-0004 https://csrc.nist.gov/pubs/sp/800/218/r1/ipd
SRC-PKB-0005 https://owasp.org/www-project-application-security-verification-standard/
SRC-PKB-0006 https://slsa.dev/spec/v1.2/
SRC-PKB-0007 https://openssf.org/scorecard/
```

## C. Source interpretation notes

### SWEBOK
Use as the top-level map of generally accepted software-engineering knowledge and as a curated path to deeper references. Do not convert a SWEBOK topic title directly into a coding rule without examining the underlying references and task context.

### ISO/IEC 25010:2023
Use to prevent vague goals such as "reliable", "maintainable" or "secure" from remaining unmeasured. Map quality characteristics to explicit acceptance criteria and measurements. Full copyrighted standard content is not copied into the repository; store identifiers, metadata, allowed notes and derived project mappings only.

### NIST SSDF
Current final baseline is v1.1. The v1.2 revision is a draft as of the verification date, so the KB must track it as `DRAFT_MONITOR`, not as controlling final guidance.

### OWASP ASVS
Use testable requirement IDs as traceable application-security evidence. ASVS does not replace threat modeling, architecture review or context-specific security requirements.

### SLSA
Use supply-chain/source/build tracks and provenance concepts to structure software artifact integrity evidence. Version pinning matters; old SLSA v1.1 pages are retired relative to current v1.2.

### OpenSSF Scorecard
Use as one automated signal for upstream project risk. A score is not equivalent to a dependency acceptance decision; source health, release history, vulnerabilities, maintainer model, license, transitive dependencies and project-specific exposure must still be evaluated.

## D. Immediate acquisition backlog — official/specification layer

The next SOURCE_VERIFIED wave should add canonical source families for:

1. Python language reference + CPython documentation and PEP index.
2. Go language specification + memory model + official diagnostics/profiling guidance.
3. Rust Reference + Rustonomicon/official unsafe guidance + Cargo supply-chain documentation.
4. Java Language Specification + JVM Specification + current LTS platform documentation.
5. ECMAScript specification + TypeScript official handbook/specification material.
6. PostgreSQL current documentation: transactions, isolation, indexes, planner, replication.
7. SQLite documentation for embedded/local-first decision cases.
8. HTTP semantics and related IETF RFCs; TLS and authentication protocol RFCs as needed.
9. OpenAPI specification and JSON Schema specifications.
10. Kubernetes, OCI and container-runtime specifications only when the task actually requires orchestration/container boundaries.
11. OpenTelemetry specifications for traces, metrics and logs.
12. Git and GitHub official documentation for repository/change/CI mechanics used by FATHER.

## E. Scientific evidence lane

A separate acquisition lane must collect peer-reviewed evidence (E2), not mix arbitrary papers into the same trust level as standards.

Priority research questions:
- effectiveness and limits of code review;
- defect prediction and static analysis precision/recall;
- property-based and mutation testing effectiveness;
- reliability effects of retries/timeouts/circuit breakers;
- distributed consistency trade-offs;
- programming-language memory-safety evidence;
- technical-debt and maintainability measurement;
- software architecture erosion and modularity;
- vulnerability introduction/remediation patterns;
- software supply-chain attack/mitigation evidence;
- AI-assisted coding defect/security evidence.

Acquisition targets: IEEE, ACM, USENIX, Springer/peer-reviewed venues and systematic reviews. Each paper enters only after methodology, scope, reproducibility and applicability are summarized.

## F. Textbook / durable engineering lane

Start from the curated SWEBOK V4.0a consolidated reference set, then create bibliographic cards for durable textbooks by knowledge area. Textbooks are guidance/education evidence (E3), not proof that a specific implementation is correct in our environment.

Initial book families to prioritize from SWEBOK and established curricula:
- software requirements;
- software design;
- algorithms/data structures;
- operating systems;
- databases;
- distributed systems;
- software testing;
- software quality assurance;
- architecture;
- secure software engineering;
- performance engineering.

## G. Practice evidence lane

Practice evidence enters only with provenance:

```text
upstream project/repository
exact version/commit
problem/context
implementation choice
measured result
known limitations
source date
reproduction status
```

Open-source repositories are not treated as "best practice" merely because they are popular.

## H. Source freshness control

Every source card SHALL include:

```yaml
source_id: SRC-PKB-XXXX
canonical_locator: "..."
source_class: E1|E2|E3|E4|E5|E6
publisher: "..."
version: "..."
status: CURRENT|DRAFT|RETIRED|SUPERSEDED|UNKNOWN
published_at: null
retrieved_at: 2026-08-14
review_after: null
superseded_by: null
license/copyright_notes: "..."
```

Version-sensitive official sources should be rechecked before they are used in D2/D3 decisions if the stored verification is no longer fresh.
