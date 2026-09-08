# FATHER Academy / Engineering Polygon — Product Concept v0.1

Status: **CAPTURED / DEFERRED PRODUCT CONCEPT**  
Date: **2026-08-14**  
Critical-path rule: this concept does not displace M5 closure or current PROGRAMMER_KB evidence work.

## 1. Product idea

Build a practice-first engineering learning platform where a learner receives realistic tasks from a synthetic or sanitized organization, performs them in isolated infrastructure, and is evaluated against the resulting system state rather than against a fixed command sequence.

The same task corpus and verifier should later evaluate FATHER professional agents.

Core loop:

```text
ORGANIZATION SCENARIO
  → CURRENT INFRASTRUCTURE STATE
  → WORK ORDER / INCIDENT / CHANGE REQUEST
  → LEARNER OR AGENT ACTIONS
  → STATE-BASED VERIFICATION
  → SECURITY / RELIABILITY / DOCUMENTATION CHECKS
  → SCORE + EVIDENCE
  → FAILURE / GAP MAP
  → NEXT TASK
```

## 2. Product distinction

The primary learning unit is not a technology chapter. It is a realistic engineering outcome.

Examples:
- onboard a new branch office;
- deploy and configure a Linux web/database stack;
- install and harden Windows Server roles;
- join workstations to a domain and apply policy;
- configure DNS/DHCP/VLAN/VPN/routing/firewall rules;
- deploy monitoring and backups;
- troubleshoot a broken service or connectivity path;
- replace an expiring certificate;
- migrate a service without unacceptable downtime;
- recover from an operational mistake;
- document the final state so another engineer can support it.

## 3. Initial infrastructure domains

1. Linux servers and services.
2. Windows Server / Active Directory / Group Policy.
3. User workstations / ARM endpoints.
4. TCP/IP, DNS, DHCP, VLAN, routing and switching.
5. Firewalls, VPN and network segmentation.
6. Web/application servers and reverse proxies.
7. PostgreSQL / common database administration.
8. Virtualization and basic cloud/IaaS concepts.
9. Containers and deployment only where justified by the scenario.
10. Monitoring, logging and observability.
11. Backup / restore / recovery.
12. Identity, certificates, secrets and access control.
13. Secure configuration and operational security.
14. Git / automation / scripting / infrastructure-as-code as the learner advances.

Vendor-specific lanes may be added only when legally usable images/licences and reproducible lab infrastructure exist.

## 4. Organization templates

Future scenarios should be built from reusable organization templates rather than isolated VMs.

Candidate templates:
- small office / SMB;
- retail branch network;
- school / education organization;
- clinic / healthcare organization using synthetic data only;
- software company;
- multi-branch enterprise;
- data-centre / service-provider slice;
- industrial/OT training environment only in isolated authorized simulators.

Each template defines:
- business roles;
- asset inventory;
- network topology;
- identity model;
- baseline services;
- security constraints;
- normal operating state;
- known failure/injection points;
- cost/resource envelope;
- observable evidence used by the verifier.

## 5. Task taxonomy

Tasks are indexed by independent dimensions rather than one vague difficulty score:

- profession/domain;
- competency;
- difficulty 1–10;
- everyday frequency 1–10;
- ambiguity;
- blast radius;
- security impact;
- reversibility;
- time pressure;
- number of dependent systems;
- troubleshooting depth;
- amount of missing information;
- expected documentation quality.

Task families:
- INSTALL;
- CONFIGURE;
- INTEGRATE;
- MIGRATE;
- TROUBLESHOOT;
- RECOVER;
- HARDEN;
- OPTIMIZE;
- AUDIT;
- DOCUMENT;
- AUTOMATE;
- INCIDENT / CHANGE / SERVICE REQUEST.

## 6. State-based verifier

The verifier should test the required properties of the final environment, not prescribe the exact path used to reach them.

Example checks:
- required process/service is healthy;
- port is reachable only from approved zones;
- DNS resolves correctly;
- routing/VLAN isolation matches policy;
- account/role permissions are correct;
- backup exists and restore is actually possible;
- monitoring detects a defined failure;
- certificate chain and expiry policy are acceptable;
- configuration survives restart;
- secrets are not exposed;
- logs contain required evidence without sensitive leakage;
- required documentation matches observable infrastructure state.

This allows alternative valid implementations while still detecting accidental partial success.

## 7. Human and agent parity

The same scenario contract should support both actors:

```text
HUMAN LEARNER  ─┐
                ├→ SAME LAB → SAME VERIFIER → COMPARABLE EVIDENCE
FATHER AGENT   ─┘
```

Human-specific outputs may include hints, explanations and learning paths.
Agent-specific outputs additionally include decision provenance, tool-call audit, permission boundaries and Principal Critic review.

The project must not give an agent privileged access to hidden acceptance criteria that a human learner does not receive.

## 8. Curriculum model

The platform should support both courses and free practice.

Possible progression:

```text
FOUNDATIONS
→ SMALL ISOLATED TASKS
→ MULTI-SERVICE TASKS
→ ORGANIZATION CHANGE REQUESTS
→ INCIDENTS / FAILURES
→ END-TO-END ORGANIZATION PROJECT
→ HIDDEN QUALIFICATION EXAM
→ CONTINUOUS WEAKNESS-DRIVEN PRACTICE
```

The learner should not be forced through already-mastered material. Diagnostic tasks produce a competency graph and the next route is selected from demonstrated gaps.

## 9. Task sources and legal rule

Potential task sources:
- project-original tasks;
- open-licensed educational tasks;
- public standards/specifications converted into original practice scenarios;
- sanitized/anonymized industry cases contributed with explicit rights;
- AI-generated variants derived from approved task templates;
- failures observed in project-owned environments, normalized and scrubbed of secrets/customer data.

Commercial books/courses are references, not a corpus to copy into a public repository unless licence permits it.

## 10. AI case generator

AI may generate new scenarios but is not the authority that marks them valid.

Generator input:

```text
domain
+ competency target
+ difficulty
+ everyday frequency
+ ambiguity
+ organization template
+ infrastructure size
+ security constraints
+ failure mode
+ allowed tools
+ novelty requirement
```

Validation pipeline:

```text
AI candidate
→ schema validation
→ duplicate/similarity check
→ solvability check
→ hidden expected-state generation
→ independent verifier execution
→ Critic review sample
→ OPEN / TRAINING / HIDDEN-EVAL classification
```

## 11. Safety and isolation

Labs involving security-sensitive administration or adversarial scenarios must run only in authorized isolated environments.

Controls should include:
- per-lab isolation;
- controlled or disabled Internet egress according to scenario;
- synthetic credentials and data;
- resettable snapshots/state;
- resource/time quotas;
- action audit;
- explicit allowlists for destructive/adversarial tools;
- automatic teardown;
- no route from learner labs to production/control-plane infrastructure.

## 12. Storage separation

GitHub should contain:
- schemas;
- task definitions that are safe/open;
- infrastructure templates small enough for source control;
- verifier code;
- documentation;
- public tests;
- aggregate evaluation results;
- stable IDs and references to external artifacts.

Keep outside public GitHub:
- copyrighted source archives;
- VM images and large binary artifacts;
- credentials/secrets;
- customer/company raw cases;
- hidden tests and hidden expected states;
- proprietary weights/decision graph sections;
- full tournament/failure corpus;
- large logs/traces/snapshots.

## 13. Accessible-learning principle

The content layer should be designed so that a useful learning path can remain free/open where infrastructure cost permits.

Heavy remote labs have real compute/storage/network cost, so affordability should come from architecture rather than from pretending those costs do not exist:
- local-first labs where possible;
- lightweight containers/VMs before full multi-VM ranges;
- time-limited remote environments;
- reusable snapshots;
- optional paid compute/mentor/certification layers later;
- organization-sponsored practice pools where possible.

## 14. MVP sequence

### ACADEMY-MIN-0 — Task contract
- common Task object;
- competency links;
- difficulty/frequency dimensions;
- open vs hidden classification;
- expected-state contract.

### ACADEMY-MIN-1 — Linux single-node polygon
Build 20–30 original tasks around:
- users/permissions;
- packages;
- systemd;
- logs;
- storage;
- networking;
- nginx;
- PostgreSQL basics;
- firewall;
- backup/restore.

Gate: environment can be created, solved, automatically verified and reset reproducibly.

### ACADEMY-MIN-2 — Small organization
One synthetic organization with approximately:
- router/firewall;
- 2–3 server roles;
- 2 network segments;
- several synthetic users/workstations;
- DNS/DHCP;
- monitoring;
- backup.

Create 10–20 cross-system work orders and incidents.

### ACADEMY-MIN-3 — Human learning UI
Add:
- task selection;
- lab launch;
- hints;
- evidence/results;
- competency map;
- recommended next task.

### ACADEMY-MIN-4 — Agent qualification lane
Give selected tasks to PROGRAMMER / later ARCHITECT / SECURITY agents using the same lab and verifier.

Gate: agent receives no hidden answer, actions are fully audited, and human can inspect the final environment plus decision evidence.

## 15. Long-term expansion

Future lanes:
- Linux Professional;
- Windows/AD Engineer;
- Network Engineer;
- DevOps/SRE;
- Database Engineer;
- Security Engineer;
- Security Architect;
- SOC/IR;
- Cloud Engineer;
- Software Engineer;
- cross-profession organization projects.

Eventually the platform can become both:
1. a practical learning product for humans;
2. the qualification and regression polygon for FATHER professional agents.

## 16. Current disposition

**CAPTURED.**

Immediate product implementation is deferred until current M5 / PROGRAMMER_KB gates permit additional WIP. Task schema and original task-bank design may evolve in parallel because they directly support PROGRAMMER evaluation corpus work.
