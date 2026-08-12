# OSINT Telegram Methods Corpus — Plan

**Status:** PLANNED / START AFTER G5 SEARCHPLAN CONTRACT

## Purpose

Use selected public OSINT/security Telegram channels as the first curated training/evidence corpus for the future Search Intelligence KB (SI-KB).

The objective is not to archive posts for their own sake. The objective is to extract reusable professional knowledge for OSINT Expert:

```text
research need
  -> capability
  -> method
  -> tool
  -> prerequisites
  -> operation mode / authorization
  -> execution environment
  -> expected output
  -> verification
  -> limitations / failure modes
  -> evidence quality
  -> proven experience
```

## Initial channel set

### 1. OSINT mindset — @osint_mindset
Role in corpus:
- search methodology;
- OSINT mindset and verification;
- GEOINT and investigation exercises;
- AI/LLM use in OSINT;
- tools and conference materials;
- practitioner case studies.

### 2. OSINT CLUB — @osint_club_channel
Role in corpus:
- practical OSINT methods;
- translated and original materials;
- Google dorking/search techniques;
- geolocation cases;
- Telegram/account-search methods;
- practice/community learning patterns.

### 3. CyberYozh — @cyberyozh_official
Role in corpus:
- tool-oriented OSINT;
- security/pentest overlap;
- Linux/Kali utilities;
- reconnaissance tools;
- privacy/anonymity/operator environment topics;
- useful negative examples where marketing/tool claims require independent verification.

### 4. Bellingcat RU — @bellingcat
### 5. Bellingcat EN — @bellingcat_en
Role in corpus:
- completed investigations;
- evidence chains;
- source corroboration;
- geolocation/chronolocation/open-source verification patterns;
- analytical presentation and traceability.

## Extraction schema

For every potentially reusable methodological item, extract:

- `source_channel`
- `source_message_id`
- `published_at`
- `observed_at`
- `content_hash`
- `topic`
- `capability`
- `research_problem`
- `method_name`
- `method_description`
- `input_requirements`
- `output_type`
- `tool_names`
- `tool_versions` when known
- `environment`
- `operation_mode`
- `authorization_requirements`
- `collection_posture`
- `step_summary`
- `verification_method`
- `known_limitations`
- `failure_modes`
- `false_positive_risks`
- `source_reliability_notes`
- `independent_confirmation`
- `status = candidate | verified | deprecated | rejected`
- `applicability`
- `related_methods`

## Important separation

Telegram posts are not automatically trusted professional knowledge.

Pipeline:

```text
Telegram Material
      ↓
Method Candidate
      ↓
verification against documentation / live test / independent source
      ↓
Method Evidence
      ↓
Council / expert gate when material
      ↓
Search Intelligence KB
```

A channel's popularity, author reputation, or number of reposts does not by itself promote a method into trusted SI-KB.

## Corpus analysis goals

The first pass should answer:

1. Which recurring OSINT capabilities are discussed most often?
2. Which methods are source-independent versus platform-specific?
3. Which tools repeatedly appear for the same capability?
4. Which tools/methods have explicit limitations or false positives?
5. Which methods require active interaction versus passive collection?
6. Which methods belong to CIVIL_OSINT, SECURITY_OSINT, AUTHORIZED_PENTEST_RECON, or TRAINING_LAB?
7. Which methodologies describe verification, not only discovery?
8. Which posts distinguish Lead from Evidence?
9. Which methods can be reproduced in our lab?
10. Which knowledge should become a SourcePlaybook, ToolCard, MethodCard, or Runbook?

## Sampling strategy

Do not ingest the complete history blindly at first.

Phase 1 — reconnaissance:
- bounded recent sample per channel;
- classify themes, tools and method density;
- estimate useful-vs-noise ratio.

Phase 2 — targeted historical search:
- search by capability/tool/method terms;
- retrieve referenced files/presentations where relevant;
- identify repeated methods and updates/deprecations.

Phase 3 — verification:
- compare important claims with primary tool documentation;
- run safe reproducible tests in TRAINING_LAB where appropriate;
- record measured behavior/version/time.

Phase 4 — SI-KB promotion:
- only verified items become trusted professional memory.

## Quality rules

- Separate discovery from verification.
- Separate source reliability from information credibility.
- Track time/version because tools and platforms change.
- Track propagation/reposts so repeated content is not counted as independent knowledge.
- Preserve original Telegram provenance and raw payload hash.
- Record contradictions and deprecated techniques instead of silently overwriting history.
- Never interpret capability as permission.

## Expected outputs

- capability taxonomy;
- initial MethodCards;
- initial ToolCards;
- Telegram SourcePlaybook;
- candidate runbooks;
- tool/version reliability history;
- known failure/false-positive registry;
- backlog of tools to reproduce in lab;
- gaps where external authoritative sources are required.

## Scope guard

This corpus supports G5-G10 but must not delay the current M5 SearchPlan contract. The first actual corpus collection begins once SearchPlan can express research goal, scope, source selection, time bounds, operation mode and sufficiency target.
