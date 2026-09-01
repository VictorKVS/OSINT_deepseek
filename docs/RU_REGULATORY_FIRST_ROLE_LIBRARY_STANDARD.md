# FATHER — Russia-first role library standard

Status: MANDATORY

## Principle

Every professional role knowledge base starts with the Russian regulatory and national-standards layer. Global practices are a second layer, not a replacement for the Russian baseline.

`ROLE → RU REGULATORY BASELINE → applicability/currentness review → global authoritative practice → books/courses/cases → Knowledge Factory`

## Why

A role can be technically competent and still be professionally incomplete in the Russian operating context. The library therefore keeps three things separate:

1. what is legally or contractually mandatory;
2. what is a national standard / normative reference whose applicability must be checked;
3. what is international or industry best practice.

The system must never silently treat a voluntary national standard as universally mandatory, and must never treat a superseded standard as current.

## Stage 0 — RU regulatory baseline

For every role order the first stage records:

- laws and government acts relevant to the role;
- regulator orders and methodologies;
- national standards (ГОСТ / ГОСТ Р);
- official status and effective date;
- supersession chain;
- applicability class;
- legal-force class;
- official source URL;
- verification state;
- explicit research gaps.

The role maturity claim is blocked if the Russian baseline is missing, unverified, or closed only with superseded documents.

## PROGRAMMER initial baseline

The first verified official-metadata seed includes:

- ГОСТ 19.101-2024 — program/document types;
- ГОСТ 19.102-77 — development stages;
- ГОСТ Р ИСО/МЭК 12207-2010 — software life-cycle processes;
- ГОСТ Р 56939-2024 — secure software development;
- ГОСТ Р 58412-2019 — information-security threats during software development;
- ГОСТ Р 71207-2024 — software static analysis.

Known superseded documents are preserved as history, not current truth:

- ГОСТ 19.101-77 → ГОСТ 19.101-2024;
- ГОСТ Р 56939-2016 → ГОСТ Р 56939-2024.

This is a core seed, not a claim that the entire Russian programming normative field is exhausted. Expansion work must cover the rest of the ESPD family, conditional GOST 34-series applicability, regulator requirements for regulated systems, and sector-specific rules.

## Global layer

Only after the Russian baseline is represented and currentness/applicability are explicit do we add:

- ISO/IEC/IEEE standards;
- OWASP;
- NIST SSDF;
- vendor/project official documentation;
- reference implementations;
- books, courses, case studies and postmortems.

Global sources may improve engineering quality but do not erase Russian obligations or national documentation requirements.

## UI requirement

A library order card must show the layers separately:

`RU REGULATORY` → `GLOBAL PRACTICE` → `CORPUS` → `KNOWLEDGE`.

For every Russian document the UI should expose designation, current status, effective date, applicability and official source. Superseded items must be visually distinct.

## Acceptance

A role library is not `MIN` merely because files were downloaded. At minimum it needs:

- Russian regulatory baseline represented;
- currentness verified from official metadata;
- applicability unresolved items surfaced for human review;
- authoritative engineering basis;
- practical method/implementation material;
- validation/failure evidence;
- provenance and SHA-256 for acquired artifacts;
- no autonomous KB promotion.
