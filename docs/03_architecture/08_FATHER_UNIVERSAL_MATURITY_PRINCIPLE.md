# FATHER Universal Maturity Principle

Status: FOUNDATIONAL ARCHITECTURE PRINCIPLE
Scope: all FATHER products, agents, knowledge bases, tools, pipelines and research programs.

## Principle
Every FATHER system MUST be developed through explicit maturity levels rather than by indefinitely polishing isolated components.

The objective is to reach a usable end-to-end capability early, validate whether it is valuable, and only then invest in deeper sophistication.

## Mandatory maturity ladder
Each product defines its own domain-specific ladder, but must map to these universal stages:

- L0 — CONCEPT: problem, user, value, constraints and acceptance criteria are explicit.
- L1 — MINIMAL END-TO-END: the smallest professional path works from input to useful output.
- L2 — RELIABLE: repeatability, error handling, tests, provenance, security basics and operational recovery.
- L3 — EXPERT: domain knowledge, recognized methods, decision algorithms, calculations, explainability and critic review.
- L4 — INTEGRATED: interoperates with other FATHER roles/products through stable contracts and shared vocabulary.
- L5 — PROFESSIONAL MVP: an independent target user can complete the intended workflow without developer intervention.
- L6 — LEARNING: replay, benchmarks, A/B methods, calibration, regression history and controlled learning from experience.
- L7 — ADAPTIVE: selects methods/tools/tactics based on task state, evidence and measurable objectives.
- L8 — SHOWCASE/PRODUCTION: polished UX, deployment, documentation, security, observability, SLOs, auditability, reproducible demonstrations and formal review.

## Three passes inside every level
1. MIN — complete the whole path with the simplest professional implementation.
2. MED — improve reliability, edge cases, evidence, explainability, usability and tests.
3. MAX — advanced algorithms, optimization, automation and learning.

## Anti-polishing rule
Do NOT spend long periods maximizing one component while the next required end-to-end capability is absent.

Before starting MED or MAX work, ask:
1. Does this block the current maturity exit gate?
2. Is there evidence users/system need it now?
3. Can it be deferred without breaking architecture or safety?
4. Is the expected benefit measurable?

If answers indicate deferral, record the idea in backlog and continue toward the next maturity gate.

## Stop / continue decision
At every maturity exit, Engineering Council evaluates:
- VALUE: does the capability solve a real task?
- EVIDENCE: was it demonstrated end-to-end?
- QUALITY: are known failures acceptable for this level?
- COST: is further investment justified?
- REUSE: can the solution become a Golden Pattern?

Decision: ADVANCE / HOLD / REDESIGN / RETIRE.

A tool may be retired even if technically impressive when it does not improve the target workflow.

## Golden Pattern rule
A solution becomes GOLDEN only after repeated successful use across relevant cases and review against alternatives. Similar future tasks should reuse Golden Patterns before commissioning new research.

## Documentation requirements
Every product passport records:
- current maturity level and pass (MIN/MED/MAX);
- exit criteria;
- evidence proving completed gates;
- blockers;
- deferred improvements/backlog;
- next maturity target;
- estimated cost/time to next gate;
- Council/Critic decisions.

## Portfolio rule
FATHER portfolio reporting should prioritize movement between maturity gates, not raw commit count, lines of code or number of features.

Primary progress question: “What complete capability became possible that was not possible at the previous gate?”

## Application
This principle applies immediately to OSINT and should be reused for Security KB, Analyst, Programmer, Tester, Architect, Quant Lab, agent factory, OSINT tools, knowledge bases and future FATHER products.
