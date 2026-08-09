# Configuration

This directory contains configuration/design profiles. Configuration is **not** a Knowledge Base and must not silently define business truth.

Current artifact:

- `high_technology_watchlist.yaml` — **DRAFT PRODUCT/DISCOVERY PROFILE**.

It currently mixes several logical concerns that must remain separate in the architecture:

```text
MISSION PROFILE
  what topics/signals matter?

SOURCE DISCOVERY PROFILE
  where should OSINT look?

FACTORY GOVERNANCE POLICY
  what may progress and who reviews it?

KNOWLEDGE ROUTING POLICY
  where does approved knowledge go?
```

The current YAML is preserved as one design artifact, but those sections are **not yet one approved runtime schema**.

## Important rules

1. Numeric `weight` / `priority` values are currently **uncalibrated preference hints**, not probabilities, trust scores or autonomous decision thresholds.
2. Source class does not prove a claim. Material quality is evaluated later by Analyst/Socrates with provenance.
3. OSINT collectors do not promote knowledge and do not route directly into KBs.
4. Escalation and promotion rules belong to Factory governance/orchestration, not ingestion.
5. New configuration keys require an approved requirement, owner/consumer and test.

Configuration lifecycle:

```text
approved requirement
        ↓
logical contract
        ↓
schema
        ↓
validated configuration
        ↓
runtime consumer
        ↓
acceptance evidence
```

See `docs/06_verification/08_CONFIG_DATA_AUDIT.md` for the current review decision.
