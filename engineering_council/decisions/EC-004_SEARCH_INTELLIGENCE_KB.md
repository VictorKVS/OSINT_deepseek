# EC-004 — Search Intelligence KB for OSINT Expert

**Date:** 2026-08-12
**Status:** APPROVED ARCHITECTURE DIRECTION
**Scope:** design now; implementation after Telegram M5 search-planning proof unless a blocking dependency emerges.

## Decision

Create a dedicated **Search Intelligence Knowledge Base (SI-KB)** for the OSINT Expert. It is distinct from the future factual Knowledge Base / Knowledge Graph that stores knowledge about the outside world.

The SI-KB stores professional search competence: what capabilities exist, which methods and tools implement them, under what conditions they are appropriate, how to operate them, what their limitations/failure modes are, and what measured experience the project has accumulated.

## Separation of knowledge domains

```text
WORLD / FACT KB
- people, organizations, events, claims
- evidence relationships
- timelines
- source-derived factual knowledge

SEARCH INTELLIGENCE KB
- search capabilities
- search methods/tactics
- tools/adapters
- environment requirements
- authorization/operation constraints
- inputs/outputs
- parsing/normalization rules
- known limitations and false positives
- source peculiarities
- reliability/quality history
- observed operational failures
- verified runbooks
- lessons learned and measured performance
```

No tool or method may become implicitly trusted merely because it is present in SI-KB.

## Core model

Primary relationship:

```text
Capability
  -> Method
  -> Tool / Native Collector / Manual Procedure
  -> Preconditions
  -> OperationMode / Authorization constraints
  -> Environment
  -> Inputs
  -> Execution contract
  -> Output parser
  -> Lead/Material semantics
  -> Verification requirements
  -> Failure modes
  -> Evidence / Proven experience
```

Suggested records:

### SearchCapability
Examples: TELEGRAM_PUBLIC_COLLECTION, USERNAME_DISCOVERY, EMAIL_FOOTPRINT, DOMAIN_DISCOVERY, ARCHIVE_LOOKUP, SOURCE_VERIFICATION.

Fields: capability_id, purpose, applicable task types, interaction level, required authorization class, expected output type, known risks.

### SearchMethod
Fields: method_id, capability_id, strategy description, preconditions, sequencing guidance, counter-evidence applicability, stop conditions, common errors.

### ToolProfile
Fields: tool_id, name, version, upstream/source, environment, install/run contract, accepted inputs, output format, parser, limits, network requirements, authentication needs, operation modes, prohibited contexts, known false positives, maintenance/freshness state.

### ToolExperience
Fields: tool_id/version, scenario, date, environment, result, measured success/failure, latency/cost where relevant, defects, workaround, evidence reference, confidence in the experience record.

### SourcePlaybook
Captures source-specific professional knowledge, e.g. Telegram identifiers, channel/message semantics, edits, forwards, access/session behavior, pagination/history behavior, rate-limit patterns, source-specific provenance rules.

## Retrieval requirement

The OSINT Expert must query SI-KB during SearchPlan construction and tool selection. The planning trace should be able to explain why a method/tool was selected or rejected.

Example:

```text
Need: establish likely public accounts for a known username
  -> capability USERNAME_DISCOVERY
  -> retrieve candidate methods/tools
  -> filter by OperationMode, authorization, platform availability, freshness
  -> choose bounded tool set
  -> results become Leads, not automatically Evidence
  -> verification workflow
```

## Learning requirement

SI-KB must evolve from verified project experience, not from unreviewed agent self-assertion.

Allowed learning inputs:
- passed acceptance/live runs;
- verified defects and fixes;
- tool/version changes verified from source;
- analyst/critic review outcomes;
- measured false positives/false negatives where a corpus exists;
- approved runbooks.

The agent may propose a new lesson, but promotion into trusted SI-KB requires a validation gate.

## Versioning and freshness

Tool and source behavior changes. Records must support `verified_at`, version/applicability range, evidence reference, status (`CURRENT`, `STALE`, `EXPERIMENTAL`, `RETIRED`) and revisit triggers.

## Safety / authorization invariant

**Capability is not Permission.**

Tool selection must be constrained by OperationMode, AuthorizationContext, target scope and interaction level. Knowledge that a tool can perform an action is never itself authorization to execute that action.

## Principal Critic constraints

1. Do not build a giant ontology before Telegram M5 proves the minimum retrieval needs.
2. Do not duplicate tool documentation wholesale; preserve operationally relevant, verified knowledge and references.
3. Do not mix external factual intelligence with internal search competence.
4. Do not allow an LLM to silently rewrite trusted tool behavior records without evidence/version trace.
5. Keep an explicit distinction between `Lead`, `Material`, `Evidence`, and `ToolResult`.
6. Search-plan decisions should be explainable from retrieved SI-KB records and current task constraints.

## Extraction boundary

SI-KB should be designed so it can later become an independent reusable repository/service, e.g. `father-search-intelligence`, without coupling to Telegram or to one LLM provider.

## Immediate action

Return to Telegram M5. Use Telegram as the first SourcePlaybook and SearchPlan proving ground. During G5-G10, record exactly what SearchPlanner needs to know. Implement only the smallest SI-KB surface justified by those measured needs.
