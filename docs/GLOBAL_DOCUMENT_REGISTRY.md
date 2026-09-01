# FATHER Global Document Registry

## Purpose

FATHER uses one canonical document registry across all roles, domains, projects and knowledge bases.

A law, GOST, regulator order, standard, methodology or other controlled document is registered **once**. `PROGRAMMER`, `SECURITY_ENGINEER`, `LEGAL_COMPLIANCE`, `SYSTEM_ANALYST`, sector overlays and project profiles reference that canonical `document_id` through applicability bindings.

This prevents separate role libraries from drifting to different revisions or legal statuses.

## Canonical model

```text
DOCUMENT
  ├─ DOCUMENT_VERSION
  ├─ SOURCE_OBSERVATION ... N
  ├─ DOCUMENT_RELATION ... N
  └─ APPLICABILITY_BINDING ... N
          ├─ ROLE
          ├─ KNOWLEDGE_BASE
          ├─ DOMAIN
          ├─ PROJECT_TYPE
          ├─ SYSTEM_CLASS
          └─ SECTOR
```

### DOCUMENT

Stable identity: designation/title/issuer/jurisdiction. One canonical `document_id`.

### DOCUMENT_VERSION

Current, future-effective, superseded, repealed or draft state belongs to document/version history, not to a role-specific copy.

### SOURCE_OBSERVATION

Independent observations are preserved. Two registries observing the same GOST do not create two documents. They create two provenance observations attached to one canonical document.

### DOCUMENT_RELATION

Examples: `SUPERSEDES`, `AMENDS`, `REFERENCES`, `DEPENDS_ON`.

### APPLICABILITY_BINDING

Applicability is contextual. Example:

```text
DOC-RU-FZ-152-2006
  ROLE SECURITY_ENGINEER -> applicable to PDN protection work
  ROLE PROGRAMMER        -> conditional when software processes PDN
  ROLE LEGAL_COMPLIANCE  -> applicable to legal/compliance analysis
  DOMAIN PERSONAL_DATA   -> core domain document
```

`CURRENT` does **not** mean `mandatory for every role`.

## Existing registries during migration

The current PDN, ESPD, GOST 34 and role regulatory files are retained as import sources and projections while migration is additive. They are no longer intended to become independent corporate truths.

Configured inputs are listed in `config/global_document_registry_sources.json`.

The builder writes:

- `reports/global_document_registry/GLOBAL_DOCUMENT_REGISTRY.json`
- `reports/global_document_registry/APPLICABILITY_BINDINGS.json`
- `reports/global_document_registry/REGISTRY_CONFLICTS.json`

Run manually:

```powershell
.\RUN_GLOBAL_DOCUMENT_REGISTRY.cmd
```

Library orders rebuild the shared registry before creating an order and attach only shared `document_id` references and applicability bindings to the order.

## Conflict policy

A source must never silently overwrite another source.

Conflicting claims such as `CURRENT` versus `SUPERSEDED` create a `REGISTRY_CONFLICT` and block shared-use acceptance until reviewed.

Missing exact text does not delete a document from the registry. Metadata/currentness and exact source bytes are different acquisition states.

## Migration rule

New role/domain implementations MUST use the global registry. Existing domain registries are migrated incrementally so the currently working PDN/Security pipelines remain regression-protected.
