# FATHER OSINT Agent Standard v0.1

Status: DRAFT / FOUNDATION
Purpose: define how OSINT_deepseek becomes a disciplined intelligence supplier for FATHER.

## Mission

The OSINT agent continuously discovers, preserves, evaluates and routes externally available information that may improve FATHER decisions, projects and expert knowledge bases. It is not a truth engine and must not silently promote collected material into verified knowledge.

## Core pipeline

SOURCE → OBSERVATION → NORMALIZATION → DEDUPLICATION → ENTITY/EVENT/CLAIM EXTRACTION → SOURCE ASSESSMENT → ANALYST HANDOFF → SOCRATES CHALLENGE → KNOWLEDGE CANDIDATE → DOMAIN KB / AGENT VIEW.

## FATHER invariants

Every material output preserves WHAT, WHY, SOURCE, WHEN, PROVENANCE, CONFIDENCE, APPLICABILITY, CONTRADICTIONS and NEXT ACTION.

Raw evidence is immutable or append-only where practical. LLM summaries are derivative artifacts, never substitutes for original provenance.

No material claim may be marked VERIFIED only because an LLM produced it.

## Source Registry

Each source receives a stable Source ID and records:
- source type and canonical location;
- domain/topic tags;
- publisher/author/organization when known;
- primary/secondary/tertiary classification;
- authority/reputation notes;
- commercial/vendor interest;
- historical reliability;
- freshness expectations;
- access method and rate limits;
- legal/licensing/terms notes where applicable;
- collection priority;
- last successful collection;
- health/status;
- known bias and known failure history.

## Observation object

An Observation is what was actually collected before interpretation.

Minimum fields:
- observation_id;
- source_id;
- source_native_id if available;
- observed_at;
- published_at if known;
- raw locator / URL / channel+message / repo+commit;
- content hash;
- content type;
- author/publisher metadata;
- raw text or storage reference;
- attachment references;
- language;
- collector version;
- collection trace;
- legal/access classification;
- deduplication group.

## Analyst handoff

The OSINT layer may propose extracted objects but must distinguish extraction from analysis:
- EventCandidate;
- ClaimCandidate;
- TechnologyCandidate;
- OrganizationCandidate;
- Person/TeamCandidate where lawful and relevant;
- RiskSignal;
- OpportunitySignal;
- FailureCaseCandidate;
- EvidenceCandidate;
- CompetitorMoveCandidate;
- HorizonSignal.

Each candidate links back to one or more Observations.

## Confidence is decomposed

Do not store one unexplained confidence number. Preserve components such as:
- source authority;
- source independence;
- corroboration count/quality;
- recency;
- directness (primary vs retold);
- methodological quality;
- ambiguity;
- potential bias/conflict of interest;
- contradiction severity;
- applicability to our context.

A computed score may exist, but the drivers remain visible.

## Collection profiles

The same engine SHALL support multiple mission profiles. Initial profile: HIGH_TECH_INTELLIGENCE.
Future profiles may include Security Intelligence, Competitor Intelligence, Legal/Regulatory Intelligence, Architecture/Engineering Intelligence, Market Intelligence and Domain-specific research.

## Required connectors — staged

MVP:
- GitHub repositories/releases/issues/advisories;
- web/RSS/Atom;
- arXiv or equivalent research metadata where legally accessible;
- official vendor/company engineering blogs and docs;
- standards/regulator/public institution sources;
- Telegram public channels where access is authorized and technically/legal compliant.

Later:
- patents;
- conference programs/proceedings;
- package registries;
- job postings and skill-demand signals;
- benchmark repositories;
- public datasets;
- additional social/community sources according to policy.

## Source priority

Prefer primary and authoritative evidence where possible:
1. standards/regulators/official specifications;
2. peer-reviewed or reputable research and conference material;
3. official technical documentation/source code/release notes;
4. independent technical evaluation and benchmark with reproducible method;
5. high-quality specialist reporting;
6. community/social signals as discovery leads rather than final authority.

Telegram/social content is normally a signal source. Important claims should be traced to primary evidence when possible.

## High-value detection

The collector should prioritize items likely to change one of:
- FATHER architecture;
- agent capability;
- cost/performance profile;
- security posture;
- regulatory/legal constraints;
- technology horizon readiness;
- build/buy/integrate decision;
- competitor position;
- reusable algorithm/method/pattern;
- failure/survival rule;
- business model assumptions.

## Routing

Examples:
- new model/runtime → AI/LLM KB + Architecture KB;
- new database benchmark → Developer KB + Architecture KB + FinOps KB;
- security incident → Security KB + Failure KB + Survival Rules candidate;
- new orchestration pattern → Agent Engineering KB;
- competitor platform move → Competitive Landscape;
- new regulation → Legal/Compliance KB;
- new chip/accelerator → Infrastructure/Compute KB + Cost KB;
- scientific method → Research/Algorithm KB.

One knowledge object may serve multiple domain views; avoid duplicate truths.

## Safety and legality

Collect only data that is lawfully and appropriately accessible for the defined mission. Respect authentication boundaries, access controls, platform terms, applicable privacy/data-protection rules, copyright/licensing constraints and collection rate limits. The agent must not use credential theft, access bypass or intrusive collection methods.

## Observability

Track collector health, source failures, lag, items/hour, duplicates, storage growth, extraction success, analyst acceptance rate, false-positive rate, downstream KB usage and cost per useful knowledge candidate.

## Human effort principle

Humans should curate priorities and resolve high-impact ambiguity, not manually copy information between systems.

## First implementation target

Build Source Registry + Observation schema + HIGH_TECH_INTELLIGENCE profile. Run initially in read/collect/draft mode; no autonomous promotion into VERIFIED knowledge.
