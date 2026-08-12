# J-021 — OSINT Expert role clarified; focus returns to Telegram M5

**Date:** 2026-08-12  
**Stage:** Stage 07 / M5 Telegram Radar  
**Result:** PASS / architecture clarified, implementation focus unchanged

## Trigger

Project discussion clarified that the OSINT component must not be reduced to a passive source collector. Analyst should formulate what must be established; OSINT should be the expert in how to obtain the necessary material, including search strategy, tactics, reconnaissance, tool selection and sufficiency assessment.

Person/electronic-footprint investigations may later justify running mature third-party OSINT tools in Kali/Linux/container environments instead of reimplementing established capabilities.

## Architecture clarification

```text
Analyst
  ↓ what must be established
OSINT Expert
  ↓ how/where to establish it
Search strategy / reconnaissance / tools
  ↓
Leads
  ↓ verification
Materials / evidence
  ↓ sufficiency
Analyst
  ↓ claims
Socrates
  ↓ adversarial review
PASS / CHALLENGE / RESEARCH_MORE
```

Adopted conceptual distinctions:

- Analyst owns the information need and analytical question.
- OSINT Expert owns acquisition strategy and search tactics.
- External tool output is normally a Lead, not automatically evidence.
- Verification converts suitable Leads into canonical Material.
- Evidence reliability and research sufficiency are distinct concepts.
- Sufficiency targets use MINIMUM / GOOD / DESIRED levels.
- Search plans should include counter-evidence/alternative-explanation work to reduce confirmation bias.

Detailed Council decision: `engineering_council/decisions/EC-003_OSINT_EXPERT_SEARCH_STRATEGY_AND_TOOL_USE.md`.

## Important scope decision

The project will **not** leave M5 to build a generic Kali/Linux tool orchestration framework now.

Telegram remains the active proving ground. We will use Telegram to exercise the general architecture end to end before opening another source/tool family.

## Telegram M5 goals already proven

- Windows Telegram network path through approved local VPN: live PASS.
- authorized Telethon reference adapter: live PASS.
- transport-neutral `TelegramMessage` and `TelegramCollector`: contract PASS.
- live Telegram → canonical Material: PASS.
- SHA-256 raw payload reuse without collapsing observations: live repeat-run PASS.
- live MaterialPackage: PASS.
- deterministic EvidenceClaim with material references: PASS.
- deterministic Socrates evidence-integrity review: live PASS.
- save-before-checkpoint ordering: contract PASS.
- checkpoint persistence across process restart: contract PASS.
- bounded FloodWait behavior: contract PASS.
- per-channel failure isolation: contract PASS.

## Telegram M5 goals still open

1. **Live checkpoint/restart/reconciliation proof** — not only a unit contract.
2. **Telegram search strategy contract** — convert Analyst research need into channel/query/source plan without hard-coding one fixed source list.
3. **Reconnaissance → deeper collection cycle** — primary sample, plan refinement, then targeted collection.
4. **Evidence quality model** — preserve source/evidence dimensions without inventing calibrated truth scores.
5. **Research sufficiency gate** — MINIMUM / GOOD / DESIRED plus explicit critical gaps.
6. **Counter-evidence search behavior** — ensure OSINT does not only collect confirming material.
7. **Explicit collection error/report semantics** — Analyst must see what was searched, what failed and what was not covered.
8. **Live restart proof with provenance preservation and no evidence loss.**
9. **M5 final Council review / acceptance record / ADR update.**

## Next action

Return immediately to Telegram and close the remaining goals in order, beginning with live checkpoint/restart/reconciliation. Do not implement generic ToolRegistry/Lead orchestration until M5 is accepted or a concrete approved requirement proves it is needed earlier.
