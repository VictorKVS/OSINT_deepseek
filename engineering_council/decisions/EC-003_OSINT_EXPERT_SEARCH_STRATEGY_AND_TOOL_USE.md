# EC-003 — OSINT Expert search strategy, leads, tools and sufficiency

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Council result:** PASS_WITH_RISK  
**Scope:** architecture contract; implementation of generic tool arsenal is deferred until Telegram M5 closes.

## Decision question

What is the correct responsibility boundary between Analyst, OSINT and Socrates, and how should mature external OSINT tools (including Linux/Kali utilities) fit into the future system without turning FATHER into a pile of wrappers?

## Decision

FATHER OSINT is promoted conceptually from a passive collector to an **OSINT Expert**.

The role boundaries are:

```text
Analyst   → defines what must be established and why.
OSINT     → decides how it can be established, where to search, which tactics/tools to use, and whether the search is sufficiently covered.
Socrates  → challenges whether the available evidence is sufficient to justify the claimed knowledge.
```

The Analyst may suggest sources or methods, but source selection and search tactics belong to OSINT Expert.

## Research operating cycle

```text
Analyst Research Request
        ↓
OSINT task decomposition
        ↓
observable indicators / hypotheses
        ↓
search strategy
        ↓
reconnaissance / primary sample
        ↓
Analyst + OSINT plan alignment
        ↓
deep search
        ↓
lead generation
        ↓
verification
        ↓
Material / evidence assessment
        ↓
research sufficiency gate
        ↓
Analyst
        ↓
Socrates
        ↓
PASS / CHALLENGE / RESEARCH_MORE
```

## Search sufficiency levels

Three explicit target levels are adopted:

- **MINIMUM** — enough evidence for a preliminary bounded answer;
- **GOOD** — professional working evidence package with diversity and counter-evidence search;
- **DESIRED** — maximum justified coverage for high-value/high-risk research.

These levels are not simple document counts. One hundred copies of one claim do not equal one hundred independent confirmations.

Future `ResearchSufficiency` must consider at least:

- coverage of requested questions;
- source diversity;
- source independence;
- primary vs secondary evidence;
- counter-evidence search;
- unresolved critical gaps;
- timeliness;
- directness of evidence.

## Evidence assessment

Evidence quality is multi-dimensional. A single `confidence` score is not sufficient.

Future assessment should preserve distinct dimensions such as:

- reliability;
- relevance;
- independence;
- recency;
- directness;
- corroboration;
- provenance quality.

Scores must not silently become calibrated truth probabilities without an approved calibration/evaluation process.

## Lead is not Material

External discovery tools commonly return candidate accounts, usernames, emails, domains, hosts or other hints. These results are **Leads**, not automatically verified evidence.

Conceptual future object:

```text
Lead
- lead_type
- tool
- query
- locator/value
- discovered_at
- raw_tool_result
- confidence_hint
- verification_required = true
```

A Lead becomes evidence only through explicit verification and conversion into canonical `Material` with provenance.

## External tool arsenal

OSINT Expert may later use proven third-party tools rather than reimplementing mature capabilities.

Possible execution environments include:

- local Python/native collectors;
- containerized tools;
- Kali/Linux VM or host;
- approved external APIs;
- manual/operator-assisted methods where automation is not justified.

The system selects tools by **capability**, not by hard-coded product names.

Conceptual future registry:

```text
ToolCapability
    ↓
ToolRegistry
    ↓
ToolAdapter
    ↓
raw tool output
    ↓
Lead
    ↓
Verification
    ↓
Material
```

A future Tool Registry should record name/version/environment/capability/input/output parser/limitations/runtime cost/network requirements/security status and reliability history.

## Senior / Principal Critic review

### Criticism 1 — Risk of building a giant wrapper platform
Accepted. Generic ToolRegistry/ToolAdapter code is **not approved now**. The architecture is recorded, but implementation waits until a concrete source/person/electronic-footprint requirement proves the need.

### Criticism 2 — Risk of treating tool output as truth
Accepted as a blocking invariant. Tool output produces a Lead unless it already meets canonical evidence/provenance criteria. Username/email/domain hits require verification before Analyst may treat them as evidence.

### Criticism 3 — OSINT and Analyst could overlap
Resolved by responsibility boundary: Analyst owns epistemic need; OSINT owns acquisition strategy; Socrates owns adversarial sufficiency review.

### Criticism 4 — Sufficiency levels can become arbitrary scores
Accepted. MINIMUM/GOOD/DESIRED are policy targets, not numeric truth. Calibration and domain-specific thresholds require later evaluation evidence.

### Criticism 5 — Search systems can reinforce confirmation bias
Accepted. Search plans for material questions must include explicit counter-evidence or alternative-explanation search unless the task contract states why it is not applicable.

## Result

`PASS_WITH_RISK`

The architecture is accepted. Generic external-tool orchestration is deferred. **Telegram M5 remains the active proving ground**, and its completion must exercise as many reusable OSINT Expert concepts as possible without speculative overengineering.

## Revisit trigger

Revisit implementation of `Lead`, `ToolRegistry`, `ToolAdapter` and Linux/Kali execution when a concrete approved task (for example person/username/electronic-footprint research) cannot be met efficiently by current native collectors and would materially benefit from a mature external tool.
