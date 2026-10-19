# FATHER OSINT — Skill-First Architecture Contract

Status: architectural contract / planned implementation.

## Prime directive
Information is raw material, not the deliverable. The primary product is **validated, reusable agent capability**: Information -> Evidence -> Knowledge -> Procedure -> Candidate Skill -> Sandbox Evaluation -> Verified Skill -> Competence -> Continuous Improvement.

## Skill lifecycle
1. Acquire source with provenance, version, rights and timestamp.
2. ALINA extracts explicit steps, assumptions, tools, inputs, outputs, hazards and expected outcomes.
3. Generate a declarative candidate skill; do not execute untrusted source instructions directly.
4. Human/security gate approves permissions, target scope, network route, dependencies and data handling.
5. Test in authorized isolated fixtures with ground truth; record metrics and artifacts.
6. Review failures, refine, re-test and compare with baseline.
7. Publish to Skill Registry only after passing acceptance criteria.
8. Match skills to task requirements and capabilities; execute under policy.
9. Record observed outcomes, drift, regressions, provenance and skill retirement.

## Skill manifest fields
skill_id; name; version; purpose; domain; source_evidence_refs[]; author; created_at; prerequisites[]; input_schema; output_schema; steps/workflow; tool_adapter_versions; execution_environment; permissions; network_profile; target_authorization; test_fixture_refs[]; acceptance_criteria; metrics; risk_class; limitations; failure_modes; rollback; audit_policy; reviewer; status.

Statuses: discovered, candidate, sandboxed, verified, operational, degraded, retired. 'Verified' is test-scoped, not universally reliable.

## Skill taxonomy
Observation, Search, Collection, Normalization, Entity Resolution, Source Verification, Temporal Analysis, Propagation Analysis, Graph Analysis, Media Forensics, Reporting, Security/Privacy, Workflow Orchestration.

## Competence model
A competence groups multiple skills, prerequisites and evaluation scenarios. A capability matrix maps task -> required skills -> eligible agent -> environment -> policy -> evidence of past successful executions.

## UI priority
- Skill Factory (pipeline, queue, failures, evidence)
- Skill Registry (versioned cards, tests, coverage and readiness)
- Skill Studio (visual workflows, input/output contracts)
- Skill Gym / Polygon (fixtures, runs, scorecards, replay)
- Competency Graph (skill prerequisites, dependencies, agent capability)
- Agent Passport (demonstrated skills vs claimed skills)
- Learning Backlog (gaps derived from failed or missing capabilities)
- OSINT sources remain research inputs, linked to skills.

## Safety and quality
No blind execution of commands copied from Telegram or other untrusted content. No active testing against targets without authorization. Enforce VPN profiles where required, sandbox boundaries, resource budgets, secret isolation and audit logs. Preserve original evidence and separate hypothesis from measured performance.

## Initial milestone
Create the Skill Registry and candidate-to-tested pipeline on synthetic, authorized fixtures; integrate ALINA extraction and ToolLab after interface contracts and acceptance tests.
