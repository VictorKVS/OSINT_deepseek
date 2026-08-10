# FATHER / OSINT_deepseek — Security Top-100 Control Catalog

**Status:** LIVING SECURITY BASELINE / FRAMEWORK  
**Purpose:** maintain a broad, project-specific set of security weaknesses, attack patterns and supply-chain failure modes that must be considered across design, implementation and operation.  
**Important:** this is an internal FATHER **Top-100 coverage catalog**, not a claim that a single external organisation publishes an official universal "Top 100" list.

## 1. Source families

The catalog is built and periodically refreshed from authoritative source families:

- OWASP Top 10 (current web/application risk baseline);
- MITRE CWE Top 25 and relevant CWE weakness families;
- CISA Known Exploited Vulnerabilities (KEV) for real-world exploitation priority;
- NIST SSDF / secure software development guidance;
- GitHub security findings and dependency advisories;
- project-specific threat models, incidents, donor reviews and supply-chain observations.

These sources have different purposes. We do not merge their scores mechanically. They are evidence inputs into project risk decisions.

## 2. Top-100 model

The internal catalog contains up to 100 active control topics, grouped by attack surface. A topic may represent a CWE family, a supply-chain failure mode, a runtime abuse case or a project-specific threat.

### A. Access, authentication and authorization — 01–10

1. Broken access control
2. Excessive privilege
3. Missing authorization checks
4. Insecure direct object/resource reference
5. Privilege escalation
6. Weak authentication
7. Session/token theft
8. Session fixation/reuse
9. Missing MFA for privileged roles where required
10. Unsafe account recovery / credential reset

### B. Secrets, cryptography and sensitive data — 11–20

11. Secrets committed to source control
12. Secrets exposed in logs/artifacts
13. Weak secret storage
14. Secret reuse / no rotation
15. Cryptographic failure / weak algorithms
16. Incorrect key management
17. Sensitive data transmitted without appropriate protection
18. Sensitive data retained longer than required
19. Sensitive data exposed through backups/exports
20. Metadata leakage

### C. Injection and untrusted input — 21–30

21. Command injection
22. SQL/NoSQL injection
23. Path traversal
24. Template/code injection
25. XML external entity and unsafe XML handling
26. Unsafe deserialization
27. Server-side request forgery
28. Cross-site scripting where UI exists
29. Header/request manipulation where HTTP services exist
30. Prompt/tool injection when executable LLM tooling exists

### D. File, media and parser safety — 31–40

31. Malicious document/parser exploit
32. Malicious image/media parser exploit
33. Archive/decompression bomb
34. Polyglot / disguised file type
35. Extension/MIME/signature mismatch
36. Unbounded parser memory/CPU usage
37. Unsafe temporary file handling
38. Embedded active content/macros/scripts
39. Metadata parser vulnerabilities
40. Unsafe transcoder/converter execution

### E. Software supply chain — 41–55

41. Known-vulnerable direct dependency
42. Known-vulnerable transitive dependency
43. Stale/archived upstream
44. Compromised maintainer/package release
45. Dependency confusion
46. Typosquatting
47. Unpinned or weakly pinned CI action
48. Compromised CI action
49. Excessive CI token permissions
50. Untrusted binary/tool download
51. Mutable container base tag / compromised image
52. Missing SBOM/dependency inventory
53. License incompatibility/change
54. Build artifact differs from reviewed source
55. Missing release provenance / integrity evidence

### F. Configuration, platform and deployment — 56–65

56. Security misconfiguration
57. Debug mode in production
58. Unsafe default configuration
59. Overexposed network/service surface
60. Missing resource limits
61. Insecure filesystem permissions
62. Unsafe environment-variable handling
63. Insecure temporary/runtime directories
64. Missing hardening for container/runtime when introduced
65. Unsupported OS/runtime/component version

### G. Availability, resilience and state integrity — 66–75

66. Unbounded retries
67. Unbounded collection/backfill
68. Rate-limit/FloodWait mishandling
69. Single-source failure blocks all work
70. Checkpoint advances before durable save
71. Checkpoint corruption/loss
72. Duplicate/replay processing breaks evidence semantics
73. Lost update / race condition
74. Resource exhaustion / queue saturation
75. Missing rollback/recovery path

### H. Evidence, provenance and analytical integrity — 76–85

76. Provenance lost during normalization/deduplication
77. Original evidence silently overwritten
78. Hash not calculated or calculated after destructive transformation
79. Source identity/locator lost
80. Edit/delete history silently erased
81. Correlation presented as causality
82. Earliest observed presented as true origin/authorship
83. Entity/account identity falsely resolved
84. Unverified AI output promoted to fact
85. Retraction/correction not propagated to knowledge state

### I. Monitoring, logging and incident response — 86–93

86. Security-relevant events not logged
87. Sensitive information overlogged
88. Alerts not routed to an owner
89. Security finding discovered but not tracked
90. No vulnerability triage process
91. No emergency disable/containment path
92. No incident evidence preservation
93. Monitoring stops after baseline freeze

### J. Governance, privacy and human operation — 94–100

94. Purpose/scope creep in data collection
95. Excessive retention or collection beyond approved need
96. Missing role separation / conflicting privileges
97. Administrator/security role actions not auditable
98. Automated analytical conclusion used without required human review
99. Risk accepted without named owner/WHY
100. Security controls or complexity grow without threat/requirement justification

## 3. Coverage record

Each Top-100 topic receives one of:

- `NOT_APPLICABLE_NOW` — surface does not yet exist;
- `PLANNED` — surface will exist and control is specified before implementation;
- `OPEN` — exposure exists and control is incomplete;
- `CONTROLLED` — control exists with evidence;
- `MONITOR` — residual risk remains and must be watched;
- `ACCEPTED` — named owner accepted residual risk with WHY;
- `CLOSED` — threat surface was removed.

`NOT_APPLICABLE_NOW` is not permanent. Introduction of a new UI, API, parser, model, role, container, database or external service reopens the relevant topics automatically.

## 4. Mandatory use at gates

At every material requirement/architecture/freeze gate:

```text
new capability
      ↓
identify new attack surfaces
      ↓
map to Top-100 topics
      ↓
add project-specific threats if Top-100 is insufficient
      ↓
security requirements + tests
      ↓
implementation
      ↓
SAST/SCA/secrets/runtime evidence
      ↓
update threat register
      ↓
freeze only when blocking controls are evidenced
```

The Top-100 is a checklist for coverage, **not a substitute for threat modelling**.

## 5. Prioritization

Priority is driven by actual exposure:

1. actively exploited vulnerability affecting our deployed component;
2. credential/session compromise or evidence integrity loss;
3. remotely reachable critical weakness;
4. supply-chain compromise possibility;
5. high-impact local/configuration weakness;
6. currently non-applicable future surface.

A low position in this catalog never overrides real exploitability or CISA KEV evidence.

## 6. Update triggers

The catalog is re-reviewed when:

- OWASP/CWE baselines change;
- CISA KEV adds a vulnerability affecting our inventory;
- dependency/upstream status changes;
- a new runtime/service/parser/model is introduced;
- a security finding or incident occurs;
- architecture or user roles change;
- a product opportunity introduces a new data class or exposure.
