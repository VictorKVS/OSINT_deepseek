# FATHER / OSINT_deepseek — Commercial Product Opportunity Registry

**Status:** living product registry  
**Purpose:** track commercial products that can be built from reusable FATHER blocks without duplicating core capabilities.  
**Rule:** commercial reuse is reviewed **before development starts** and revisited at every material engineering gate. Product ideas do not bypass requirements, tests, donor review, benchmarks or architecture gates.

## Priority legend

- ★★★★★ — highest commercial attractiveness; broad demand, clear pain, reusable core, realistic MVP.
- ★★★★☆ — strong commercial candidate; good value but needs additional specialization or data.
- ★★★☆☆ — useful niche product or add-on.
- ★★☆☆☆ — exploratory / secondary opportunity.
- ★☆☆☆☆ — low priority or unclear business case.

Stars are **product-priority judgments**, not statistical scores and not market forecasts. They must be revised as we collect real customer evidence.

---

## Permanent Product-Reuse Gate

Every new requirement, module or material architecture change must answer the following **before implementation begins**:

```text
BUSINESS REQUIREMENT
      ↓
PRIMARY USE CASE
      ↓
PRODUCT-REUSE REVIEW
      ├── What other products can use this block?
      ├── Which data/metadata should be preserved now?
      ├── Which interfaces must stay domain-neutral?
      ├── What should remain product-specific outside the core?
      ├── Does this create a new commercial opportunity?
      └── Does an existing opportunity become stronger/weaker?
      ↓
REQUIREMENTS REVIEW
      ↓
ARCHITECTURE
      ↓
TESTS / IMPLEMENTATION / VERIFICATION
```

This review is **not one-time**. It is reopened at least at:

1. **Requirements / ТЗ** — before code: identify reusable value and commercial variants.
2. **Architecture review** — confirm interfaces support reuse without contaminating the core.
3. **Donor / technology selection** — check whether a technology creates lock-in that damages other product paths.
4. **Acceptance-test design** — preserve behavior/metadata needed by approved reuse scenarios where cost is low and justified.
5. **Verification / baseline freeze** — update which products are now technically feasible.
6. **Post-MVP / customer evidence** — revise stars, pricing hypotheses, scope and even retire weak ideas.

The purpose is **option preservation**, not speculative overengineering. A possible future product does not justify arbitrary complexity. We preserve reusable interfaces and low-cost metadata only when they do not weaken the primary requirement.

---

## Registry

| Product | Priority | Customer / buyer | Core blocks reused | Value proposition | Key additional work | Status |
|---|---:|---|---|---|---|---|
| **Competitive & Channel Intelligence** | ★★★★★ | marketing, strategy, owners, competitive intelligence teams | Telegram Radar, provenance, Analyst, later KB | monitor competitors' channels; short daily/weekly briefs; themes, products, prices, hiring, campaigns, reactions | dashboards, topic tracking, watchlists, report templates | PLANNED |
| **Content Origin & Propagation Analytics** | ★★★★★ | media, PR, agencies, brand teams, researchers | Telegram Radar, timestamps, content hashes, forwards/replies, later Artifact hashes | show earliest observed publication, reuse chains, propagation waves, channels that repeatedly copy/amplify material | similarity engine, propagation graph, temporal analysis | PLANNED |
| **Brand / Reputation Monitoring** | ★★★★★ | companies, PR, executives, public-facing organisations | Telegram Radar, web ingestion later, Analyst | mentions, narratives, sudden spikes, negative/positive themes, origin of information waves | entity dictionary, alerting, reporting | PLANNED |
| **Technology / Market Radar** | ★★★★★ | investors, R&D, product teams, strategy, technology companies | Telegram Radar, future web/PDF ingestion, Analyst, Socrates, KB | detect emerging technologies, suppliers, projects, patents/news signals, changes in competitor activity | broader source connectors, taxonomy, horizon reports | PLANNED / STRATEGIC |
| **Consent-Based Risk Intelligence / Screening** | ★★★★☆ | corporate security, compliance, insider-risk teams | Person OSINT, Telegram Radar, identity evidence, Analyst, Socrates | evidence-backed public risk signals with human review; no automated guilt/risk verdict | legal policy, identity-resolution, risk scenarios, access controls, audit trail | FUTURE / CONTROLLED |
| **Insider / Asset Leakage Signal Assistant** | ★★★★☆ | industrial security, internal security departments | Risk Intelligence, Telegram/Web ingestion, provenance | detect public signals around resale of company assets, leaks, suspicious marketplace activity, company-specific terms | organisation-specific scenarios, false-positive handling, human review | FUTURE / CONTROLLED |
| **Media Intelligence Briefing Service** | ★★★★☆ | executives, analysts, press offices | Radar, Analyst, Socrates, summarization | concise source-grounded daily brief: what happened, who started it, who amplified it, contradictions | report UX, scheduling, multi-source ingestion | PLANNED |
| **Source / Channel Quality Analytics** | ★★★★☆ | analysts, journalists, researchers | provenance, history, propagation data | show which channels originate information, which mostly repost, correction frequency, source relationships | longitudinal metrics, correction tracking | FUTURE |
| **Trend & Narrative Radar** | ★★★★☆ | marketing, policy analysis, research, product teams | Radar, temporal history, Analyst | identify a topic from first weak signal through acceleration, peak and decay | topic clustering, time-series layer | FUTURE |
| **Supplier / Third-Party Open-Source Monitoring** | ★★★★☆ | vendor risk, procurement, security | multi-source OSINT, KB, Analyst | monitor suppliers for incidents, ownership/news changes, outages, sanctions/compliance/public security signals | entity registry, web/news connectors, policy packs | FUTURE |
| **Executive / Company Digital Exposure Report** | ★★★☆☆ | companies, executives, security teams | Person/Entity OSINT, Artifact ingestion, Analyst | consensual public digital-footprint review with evidence and remediation suggestions | identity resolution, privacy controls, report templates | FUTURE |
| **Research Archive & Evidence Workspace** | ★★★☆☆ | researchers, investigative teams, analysts | Artifact ingestion, hashing, provenance, KB | collect material locally, preserve originals, provenance and searchable evidence packages | universal ingestion, local search, export | FUTURE |
| **Local Meeting / Interview Intelligence** | ★★★☆☆ | SMEs, consultants, internal teams | Artifact ingestion, local transcription, Analyst | local/private transcription + summaries + tasks without sending sensitive media to third-party servers | M6/M7, UI/integrations | FUTURE |
| **White-label OSINT Analyst Platform** | ★★★☆☆ | consultancies, security integrators, niche research firms | entire modular FATHER stack | reusable branded OSINT/analysis platform configured by domain and source packs | tenancy, RBAC, deployment, billing | LONG-TERM |

---

## Most attractive current opportunities

### ★★★★★ Competitive & Channel Intelligence

Minimal commercial scenario:

```text
customer watchlist
      ↓
Telegram Radar
      ↓
competitor/source history
      ↓
Analyst
      ↓
Daily / Weekly brief
      ├── important publications
      ├── new products / offers / prices
      ├── repeated themes
      ├── reactions / amplification
      └── links to original evidence
```

Reason for attractiveness: can be built early from M5 plus a thin reporting layer; the customer receives recurring value without requiring Person OSINT or a complex Knowledge Gate.

### ★★★★★ Content Origin & Propagation Analytics

Core question:

> Where did this information appear first in our observed source universe, how did it spread, and which channels amplified or reused it?

Important wording: the system may establish **earliest observed source + temporal/similarity evidence**. It must not automatically accuse a channel of plagiarism or claim true authorship without evidence.

Future output:

```text
09:03 Channel A — earliest observed matching publication
09:17 Channel B — high-similarity publication
09:24 Channel C — forwarded / derivative wave
09:31 Channel D — second-order amplification
09:46 Channel E — second-order amplification
```

This product strongly reuses M5 fields: stable source/message IDs, timestamps, forward/reply metadata, original text, source URL and hashes. M6 later extends the same approach to images, video and documents.

### ★★★★★ Brand / Reputation Monitoring

Commercial value comes not from counting mentions but from answering:

- what narrative is growing;
- who initiated or amplified it;
- what evidence the claim is based on;
- whether different channels repeat the same source;
- whether the narrative is changing;
- what new item requires human attention.

### ★★★★★ Technology / Market Radar

This is strategically aligned with FATHER's original long-term concept: reusable expert knowledge built from continuously refreshed public evidence. The same base can later support domain packs such as AI, cybersecurity, robotics, energy, biotech and industrial technologies.

---

## Reusable-block principle

```text
CORE BLOCKS

Telegram Radar
Artifact / Ingestion
Local Extraction / Transcription
Provenance / Evidence
Analyst
Socrates
Knowledge Gate / KB
Identity / Entity layer (when required)
        │
        ▼
PRODUCT ASSEMBLY
        │
        ├── Competitive Intelligence
        ├── Content Propagation
        ├── Brand Monitoring
        ├── Technology Radar
        ├── Risk Intelligence
        ├── Supplier Monitoring
        └── Research Workspace
```

A new commercial idea should first answer:

1. Which existing blocks provide most of the required capability?
2. What genuinely product-specific layer is missing?
3. Can the product be delivered without contaminating the reusable core with domain-specific logic?
4. Is there a recurring buyer problem rather than only an interesting technical demo?
5. Can value be demonstrated with a small bounded MVP?
6. Which current requirement or block should preserve a low-cost option for this product?
7. What evidence would cause us to lower its star priority or remove it entirely?

---

## Product registry governance

Every new opportunity receives:

```text
Product name
Target customer
Problem / job-to-be-done
Reusable FATHER blocks
Missing product-specific capabilities
Data / legal constraints
Possible pricing model
MVP definition
Evidence of customer demand
Priority stars
Status
WHY
Last reviewed
Next review gate
```

Priority stars must be revisited after customer interviews, competitor research, cost estimates and MVP results.

### Mandatory review record for every engineering milestone

Each milestone/requirement should contain a compact section:

```text
COMMERCIAL / REUSE REVIEW

Primary capability:
Reusable core block(s):
Existing products strengthened:
New product opportunities discovered:
Low-cost metadata/interfaces worth preserving now:
Product-specific logic that must stay outside core:
Commercial risks / lock-in:
Registry changes:
Next review gate:
```

A valid result may be **"no commercial change"**. The requirement is to ask the question and record the answer, not to invent a product for every module.

---

## Engineering sequence

Commercial/reuse analysis is now part of the formal engineering chain:

```text
BUSINESS REQUIREMENT / ТЗ
      ↓
COMMERCIAL + REUSE REVIEW
      ↓
REQUIREMENTS REVIEW
      ↓
BUSINESS / PROCESS ANALYSIS
      ↓
ARCHITECTURE
      ↓
COMMERCIAL + REUSE RECHECK
      ↓
ARCHITECTURE REVIEW
      ↓
ACCEPTANCE TEST DESIGN
      ↓
IMPLEMENTATION
      ↓
VERIFICATION
      ↓
PRODUCT REGISTRY RECHECK
      ↓
BASELINE / EXPERIENCE / KB
```

Current core roadmap remains:

```text
M5 Telegram Radar
      ↓
M6 Artifact / universal ingestion
      ↓
M7 Local transcription / extraction
      ↓
M8 Knowledge Gate
```

Commercial thinking influences interface design and reusable metadata, but **does not justify speculative complexity and does not bypass engineering gates**.
