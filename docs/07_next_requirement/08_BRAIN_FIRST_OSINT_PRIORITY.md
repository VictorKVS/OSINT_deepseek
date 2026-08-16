# OSINT Development Priority — BRAIN FIRST

**Status:** ACCEPTED PRIORITY OVERRIDE  
**Date:** 2026-08-16  
**Principle:** the quality of reasoning, evidence assessment and decision algorithms has priority over adding new tools, sources or automation depth.

## Why this overrides the previous execution order

Telegram M5 has already proved a useful end-to-end technical vertical. However, G7 Evidence Quality, G8 Research Sufficiency, G9 Counter-evidence and future Analyst conclusions currently use project-designed policy logic that is intentionally non-calibrated. Before treating these rules as expert-grade, the project must ground them in recognized intelligence-analysis, evidence-assessment and decision methodologies.

Therefore Telegram remains the proving ground, but it is no longer the primary research objective. It becomes the controlled dataset and live environment used to test the quality of the OSINT/Analyst reasoning methods.

## New priority order

### P0 — Intelligence Analysis Methods Research

Build `INTELLIGENCE_ANALYSIS_METHODS_KB` from recognized sources and published critique.

Research blocks, in order:

1. Source reliability vs information credibility
   - Admiralty / NATO-style source-information evaluation;
   - known variants, limitations and misuse risks.

2. Analytic standards and uncertainty language
   - ICD 203 and related standards;
   - separation of likelihood, confidence, evidence quality and sufficiency;
   - traceability requirements.

3. Structured analytic techniques
   - Analysis of Competing Hypotheses (ACH);
   - Key Assumptions Check;
   - Devil's Advocacy;
   - Team A / Team B;
   - Red Team techniques;
   - indicators/signposts and other relevant SAT methods.

4. Source independence / corroboration
   - derivative-source detection;
   - common-origin and propagation analysis;
   - independent evidence lines;
   - limits of simple source counting.

5. Research sufficiency / stopping rules
   - what accepted methods exist for deciding when evidence is sufficient;
   - explicit distinction between completeness, adequacy, confidence and truth;
   - domain-sensitive stop criteria rather than words such as "many", "few" or "enough".

6. Formal reasoning / uncertainty alternatives
   - Bayesian approaches where justified;
   - evidence theory / Dempster-Shafer and related approaches where applicable;
   - documented strengths, weaknesses and calibration requirements.

7. Practical CTI/OSINT implementations
   - MISP taxonomies and confidence practices;
   - STIX/TAXII evidence/context representation;
   - documented methods in mature OSINT/CTI products where publicly available;
   - no inference about proprietary algorithms without evidence.

## Required MethodRecord

Every admitted method must have a versioned record:

```text
method_id
name
purpose
source_refs[]
source_class
primary_or_secondary
inputs[]
outputs[]
algorithm_or_rules
scales_or_thresholds
assumptions[]
known_limitations[]
validation_evidence[]
known_criticism[]
applicability[]
non_applicability[]
implementation_notes
status: VERIFIED | SUPPORTED | EXPERIMENTAL | REJECTED
version
review_refs[]
```

No threshold, score or category becomes VERIFIED merely because it is common or intuitive.

## P1 — Re-audit current reasoning modules

After each research block, compare recognized methods with current implementation:

- `father_osint/evidence_quality.py` (G7)
- `father_osint/sufficiency.py` (G8)
- `father_osint/counter_evidence.py` and `sufficiency_g9.py` (G9)
- `father_osint/acquisition_report.py` (G10)
- current deterministic Analyst reasoning

For each difference create one of:

- KEEP — current behavior is supported;
- MODIFY — current behavior is useful but needs correction;
- REPLACE — stronger recognized method exists;
- EXPERIMENT — no accepted method is sufficient, so FATHER method remains experimental;
- DEFER — insufficient evidence to decide.

Existing working algorithms are not silently rewritten. Changes require test vectors, rationale, version bump and regression tests.

## P2 — Reasoning provenance

Formalize audit objects for the "brain":

### SufficiencyAssessmentRecord
Must preserve:
- requested level;
- achieved level;
- method and method version;
- criteria evaluated;
- inputs/evidence refs;
- passed/failed gates;
- critical gaps;
- uncertainty and limitations;
- reviewer/critic refs.

### ConclusionRecord
Must preserve:
- research question;
- hypotheses considered;
- supporting claims/evidence;
- contradicting claims/evidence;
- alternative explanations;
- reasoning method and version;
- assumptions;
- uncertainty;
- sufficiency assessment ref;
- analytic confidence (if methodologically justified);
- Critic/Socrates review refs;
- knowledge/method versions.

A conclusion without reasoning provenance is not expert-grade output.

## P3 — A/B and retrospective validation

Where multiple defensible methods exist, retain alternatives and compare them on historical/synthetic cases.

Example:

```text
same evidence package
    ├─ method A → assessment A
    ├─ method B → assessment B
    └─ senior/critic review → measured differences
```

Track false promotion, false rejection, instability, sensitivity to derivative sources, missing primary evidence and counter-evidence handling.

The goal is not to make FATHER unique by invention; the goal is to adopt, test and improve well-founded methods with evidence.

## P4 — Telegram M5 calibration and closure

Only after P0-P2 provide the first evidence-based methodological baseline:

1. rerun multi-channel Telegram reconnaissance;
2. run a real hypothesis scenario;
3. run counter-evidence search;
4. calculate sufficiency using the revised/versioned method;
5. create reasoning-provenance records;
6. integrated live run;
7. security/session hygiene;
8. Principal Critic / Engineering Council review;
9. G11 / M5 DONE.

M5 may remain technically functional while methodological gates are under review. Do not call the reasoning layer expert-grade until the research review is complete.

## P5 — Tools and new source families

Only after the reasoning baseline is stable enough to judge their output:

- Web/search sources;
- documents/archives;
- GitHub;
- entity/identity tools;
- external Kali/Linux OSINT tools;
- generic ToolRegistry;
- additional automation.

**Rule:** a new tool is valuable only if the system already knows how to judge what the tool returned.

## Prohibited vague terms

Machine reasoning and formal reports must not use the following as terminal criteria without a method reference:

- many / few;
- enough / insufficient (without criteria);
- reliable;
- likely / unlikely;
- strong / weak evidence;
- independent;
- confirmed;
- high confidence.

Each such category must resolve to a named, versioned method, its inputs and an auditable assessment.

## Priority summary

```text
1. METHODS / RESEARCH / INTELLIGENCE_ANALYSIS_METHODS_KB
2. REASONING PROVENANCE + VERSIONED ALGORITHMS
3. RE-AUDIT G7–G10 + A/B TESTS
4. TELEGRAM AS CALIBRATION / LIVE PROVING GROUND
5. M5 FINAL REVIEW
6. NEW SOURCES AND TOOLS
```

The project principle is therefore:

> BRAIN BEFORE TOOLS. First learn how to judge information and produce defensible conclusions; then increase how much information the system can collect.
