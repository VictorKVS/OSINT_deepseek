# FATHER / OSINT_deepseek — Operations Governance Model

**Status:** PLANNED OPERATIONS BASELINE  
**Purpose:** define how the system will later be operated, administered, secured and governed without mixing responsibilities.

## 1. Principle

Production operation is a separate capability and must be designed before deployment, not improvised after the system is built.

The minimum role model is:

```text
Director / Product Owner
        │
        ├── approves purpose, major risk acceptance, product scope
        │
Security Administrator / Security Officer
        │
        ├── security policy, threat register, vulnerabilities, access review
        │
System Administrator / DevOps
        │
        ├── runtime, deployment, backups, availability, updates
        │
Analyst / Operator
        │
        ├── approved research tasks, review of evidence, operational work
        │
End User / Consumer
        │
        └── uses approved outputs within granted access
```

Roles may be combined in DEV, but production permissions and audit semantics must remain logically separated.

## 2. Planned role responsibilities

| Role | Primary responsibility | Must not silently own |
|---|---|---|
| Director / Product Owner | purpose, business scope, major risk acceptance, product priorities | daily technical administration or unreviewed security exceptions |
| Security Administrator / Security Officer | threat register, vulnerability management, access review, security events, dependency/supply-chain posture, incident coordination | business approval of collection purpose or routine system administration without audit |
| System Administrator / DevOps | deployment, configuration, backups, recovery, availability, patch execution, platform health | self-approval of high-risk security exceptions |
| Analyst / Operator | create/execute approved research tasks, inspect evidence, produce analytical output | privileged security/config changes or uncontrolled data collection |
| End User / Consumer | consume approved reports/knowledge/products | administrative functions, source credentials, raw evidence beyond authorization |
| Developer / Maintainer | code, tests, fixes, dependency proposals | direct unreviewed production changes |

## 3. Segregation-of-duties target

Production should preserve at least these distinctions:

- who requests/approves a capability;
- who deploys it;
- who grants/reviews access;
- who monitors security;
- who accepts residual risk;
- who performs analytical work;
- who consumes the result.

A small installation may assign several roles to one person, but the system should still record **which role context an action belongs to**.

## 4. Operations control domains

Before production, the project must define and test:

1. identity/authentication and RBAC;
2. privileged access and MFA where justified;
3. secrets/session/key management;
4. change and release management;
5. vulnerability and patch management;
6. dependency/upstream monitoring;
7. security/event logging and alert ownership;
8. backup, restore and disaster recovery;
9. data classification, retention and deletion;
10. incident response and evidence preservation;
11. service health/capacity/rate-limit monitoring;
12. configuration baseline and drift detection;
13. user onboarding/offboarding and access recertification;
14. product/legal purpose controls for sensitive research modes;
15. audit reporting to management.

## 5. Operations evidence model

Every operationally important action should eventually answer:

```text
WHO
acted as WHICH ROLE
performed WHAT
on WHICH OBJECT
for WHICH APPROVED PURPOSE / CHANGE
WHEN
RESULT
EVIDENCE / TICKET / DECISION
```

Examples include role assignment, dependency upgrade, transport disable, secret rotation, backup restore, risk acceptance, new data source approval and production deployment.

## 6. Security officer dashboard target

The security role should be able to see, at minimum:

- open Critical/High security threats;
- dependencies with vulnerabilities or stale upstream;
- CISA KEV matches against actual inventory;
- pending Dependabot/security updates;
- CodeQL/SAST/SCA/secret findings;
- expiring/rotated credentials and session risks;
- privileged access changes;
- failed authentication/security events when auth exists;
- security-relevant configuration drift;
- unreviewed external services/donors;
- outstanding risk acceptances and owners;
- incidents and remediation state.

## 7. Administrator dashboard target

The system administrator/DevOps role should be able to see:

- service/process health;
- storage/capacity;
- queues/backlog;
- collection failures/rate limits;
- backup/restore state;
- dependency/runtime versions;
- deployment/build version;
- checkpoint/reconciliation health;
- integration availability;
- configuration drift requiring action.

Security-relevant administrator events remain visible to the security role.

## 8. Director / Product Owner dashboard target

Management should receive concise governance information rather than raw technical noise:

- current capability roadmap/gates;
- Critical/High accepted/open risks;
- major security incidents;
- product opportunities unlocked/blocked;
- operational availability/reliability summary;
- significant supplier/upstream risk;
- unresolved legal/privacy constraints;
- major decisions requiring owner acceptance.

## 9. User / Analyst experience target

Users should see only what they need for their assigned purpose:

- allowed tasks/sources;
- task status;
- evidence/provenance relevant to their work;
- explicit failures and limitations;
- analyst/Socrates review state;
- approved reports/exports.

They should not need access to Telegram sessions, infrastructure secrets, dependency controls, CI credentials or unrelated raw evidence.

## 10. Introduction sequence

Operations governance is introduced progressively:

```text
DEV
  roles documented, not fully enforced
      ↓
LIVE POC
  secrets + minimal privileged boundaries
      ↓
PRE-PROD
  RBAC + audit + operational/security runbooks
      ↓
PROD
  access reviews + monitoring + incident/change/backup controls
      ↓
MATURE OPERATION
  dashboards + drift + vulnerability/SBOM/upstream monitoring + periodic reviews
```

No production-readiness claim is valid until the in-scope operational controls have acceptance evidence.
