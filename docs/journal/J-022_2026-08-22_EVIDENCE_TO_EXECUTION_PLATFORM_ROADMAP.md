# J-022 — Evidence-to-Execution Platform: complete strategic product chain

**Date:** 2026-08-22  
**Status:** APPROVED ROADMAP DIRECTION  
**Current execution priority unchanged:** P0 Knowledge Factory Conveyor

## Trigger

The Knowledge Factory concept has matured beyond document acquisition and knowledge extraction. Once the system can reliably determine what a source says, what is required and to whom it applies, the next engineering questions are unavoidable:

1. how can the requirement be implemented;
2. which implementation alternatives are permissible;
3. what do they cost and how do they differ in time, reliability, quality, operational burden and risk;
4. which roles must perform/control/review the work;
5. what competence and capacity those roles require;
6. whether current staff can cover the requirement;
7. whether training, hiring, outsourcing, hybrid delivery or automation is the better sourcing model;
8. what evidence proves execution;
9. how actual outcomes should influence future decisions.

## Decision

Adopt the following strategic product chain:

```text
Knowledge Factory
    ↓
Regulation Engineering
    ↓
Compliance / Implementation Design
    ↓
Role & Responsibility Engineering
    ↓
Workforce & Competency Engineering
    ↓
Sourcing Alternatives
    ↓
Decision Intelligence
    ↓
Implementation & Evidence Tracking
    ↓
Outcome Feedback
    ↓
Golden Solutions
    ↓
Regulatory Digital Twin
```

This chain is now part of `docs/PROJECT_ROADMAP_AND_CONTROL.md`.

## Workforce & Competency Engineering is a core layer

It is not treated as a generic HR module.

Its purpose is to connect regulatory/technical obligations to the real ability of an organization to execute them:

```text
Requirement
 → Control
 → Process / Activity
 → Role
 → Competency
 → Required level/capacity
 → Person/Team/Supplier capability
 → Gap
 → Sourcing option
 → Decision
```

The system will eventually compare:

- keep current staff;
- upskill/train;
- hire;
- outsource;
- hybrid internal/external;
- automate part of the function where appropriate.

Comparison dimensions remain separate:

- TCO/cost components;
- time-to-competency/time-to-coverage;
- quality/rework observations;
- critical-function coverage;
- backup/bus-factor risk;
- SLA/dependency risk;
- reliability/availability where meaningful;
- operational burden;
- auditability/evidence quality.

No opaque employee or vendor “reliability percentage” is permitted without a separately justified calibrated model.

## Why this completes the product idea

The platform can ultimately move from source evidence to organizational action:

```text
What is required?
 → Does it apply?
 → What must be done?
 → What valid solutions exist?
 → Which solution fits our constraints?
 → Who must perform it?
 → What competence/capacity is required?
 → Do we have it?
 → Train / hire / outsource / hybrid / automate?
 → What was selected and why?
 → How is execution proven?
 → What happened in practice?
 → Should the solution become reusable GOLDEN experience?
```

This turns the platform from a knowledge repository into a governed evidence-to-execution system and provides the data foundation for a future Regulatory Digital Twin.

## Guardrail

This roadmap decision does **not** expand current implementation WIP. P0 remains the Knowledge Factory Conveyor. Later layers are allowed to receive only contract/data-model design that prevents future architectural dead ends; implementation capacity stays on the current P0 until its evidence gates are passed.

## Result

**Decision:** PASS / strategic roadmap approved.  
**Roadmap commit:** `fa0d4f01f6fa5f927dbc54cb5c98c009cea0f9b2`.  
**Next execution bottleneck:** mixed-profile D0-D3 acceptance, then D4-D15 through the same conveyor.
