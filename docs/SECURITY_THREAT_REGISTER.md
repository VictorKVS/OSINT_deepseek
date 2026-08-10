# FATHER / OSINT_deepseek — Security & Software Supply-Chain Threat Register

**Status:** living register  
**Scope:** source code, dependencies, donor projects, CI/CD, secrets, build/release chain, runtime integrations, containers, agentic tooling and future AI/file-processing surfaces.  
**Scoring:** qualitative until evidence supports calibration.

## States

- `OPEN` — threat exists; control incomplete.
- `CONTROLLED` — mitigation implemented and evidenced, but threat remains relevant.
- `MONITOR` — low current exposure; watch for changes.
- `ACCEPTED` — explicitly accepted with WHY and owner.
- `CLOSED` — threat removed from architecture or no longer applicable.

## Register

| ID | Threat | Surface | Likelihood | Impact | Required control / evidence | Current state | Reopen trigger |
|---|---|---|---|---|---|---|---|
| S01 | Dependency with known vulnerability enters baseline | Python/npm/future packages | Medium | High/Critical | SCA; dependency inventory; review before freeze; regression after upgrade | OPEN | new dependency/advisory |
| S02 | Upstream project becomes stale/archived or loses maintainers | TDLib/GramJS/future donors | Medium | High | donor lifecycle; maintenance/activity review; replaceable adapter; recheck before ADR/freeze | OPEN | archive, stale releases, unanswered security issues |
| S03 | Malicious/compromised package or maintainer update | package ecosystem | Low/Medium | Critical | pinning; trusted source; changelog/diff review for material upgrades; minimal dependencies; SBOM | OPEN | maintainer/package ownership/release anomaly |
| S04 | Dependency confusion / typosquatting | package install | Low/Medium | Critical | exact canonical names; trusted registries; lock/pin strategy; review additions | OPEN | new registry/package |
| S05 | Compromised GitHub Action executes in CI | CI/CD | Medium | Critical | least permissions; pin reviewed third-party actions to immutable commit; minimize third-party actions | OPEN | workflow/action change |
| S06 | Secret/API key/Telegram session committed to Git | repo/history | Medium | Critical | secret scanning; .gitignore; no credentials in examples; rotation procedure | OPEN | secret finding / auth integration |
| S07 | Secret/session emitted in logs or workflow artifacts | logging/CI | Medium | Critical | log-redaction tests; no session dump; artifact review; least debug output | OPEN | live Telegram integration |
| S08 | CI token has excessive permissions | GitHub Actions | Medium | High | explicit least-privilege `permissions`; avoid write unless required | OPEN | new workflow/job |
| S09 | Unreviewed automatic dependency update breaks security/behavior | update automation | Medium | High | automated PR only; no blind auto-merge; regression + security review | OPEN | Dependabot/update bot introduction |
| S10 | Vulnerable/transitive dependency is invisible to developers | future package graph | Medium | High | lock/inventory; SBOM; SCA of transitive graph | OPEN | first non-trivial runtime dependency set |
| S11 | Build/release artifact differs from reviewed source | release pipeline | Low/Medium | Critical | traceable/reproducible build; release provenance; immutable artifact hashes | MONITOR | first external release |
| S12 | Base image contains vulnerable/stale packages | future containers | Medium | High | pinned base/digest policy; image scan; rebuild/update path | MONITOR | Docker/container introduction |
| S13 | Downloaded binary/tool is replaced or tampered with | ffmpeg/OCR/browser/future tools | Low/Medium | Critical | trusted source; package manager/checksum/signature where available; version inventory | MONITOR | binary tooling introduced |
| S14 | License change or incompatible license contaminates product | dependencies/donors | Medium | High | license verification at SOURCE_VERIFIED and before upgrade/release | OPEN | new version/upstream/license file change |
| S15 | Telegram transport flaw leaks session or account access | M5 transport | Medium | Critical | transport security review; session isolation; log tests; replacement/disable path | OPEN | TDLib/GramJS PoC/live credentials |
| S16 | Flood/rate behavior causes account restriction or operational outage | Telegram | Medium | High | bounded collection; explicit rate handling; per-source isolation; backoff tests | OPEN | live Telegram PoC |
| S17 | Checkpoint corruption/loss causes missing or duplicated evidence | ingestion state | Medium | Critical | checkpoint-after-durable-save; restart/reconciliation tests | OPEN | M5 implementation |
| S18 | Malicious source content exploits parser/client bug | Telegram / future web/files | Medium | Critical | keep libraries supported; limit parsing surface; isolation; fuzz/negative cases where justified | OPEN | new parser/input type |
| S19 | Malicious file exploits media/document parser | M6 files | Medium | Critical | type/signature validation; sandbox/isolation; limits; patch monitoring; dangerous content policy | MONITOR | M6 starts |
| S20 | Archive/decompression bomb exhausts resources | M6 ingestion | Medium | High | size/depth/ratio limits; bounded extraction; timeout/quota | MONITOR | archive support |
| S21 | External AI/transcription service receives sensitive evidence | M7/API | Medium | Critical | local-first; explicit data classification; provider privacy review; human approval for sensitive use | MONITOR | external provider enabled |
| S22 | External service changes retention/privacy/terms silently | APIs | Medium | High | provider registry; periodic re-verification; replaceable interface | MONITOR | provider approval/change |
| S23 | AI model/tool-call injection causes untrusted content to drive actions | agentic Analyst/tool layer | Medium | Critical | model proposes, deterministic policy/code executes; tool allowlist; untrusted-content boundary; approval gates | MONITOR | executable LLM tools introduced |
| S24 | Model/package provenance unknown or tampered | local AI models | Medium | High | source/license/hash/model version inventory; controlled download/update | MONITOR | local model adoption |
| S25 | Security scanner becomes false assurance | all | Medium | High | scanners are evidence inputs, not approval authority; manual architecture/threat review remains | CONTROLLED | any "green scan = secure" decision |
| S26 | Security findings are discovered but not tracked to closure | governance | Medium | High | finding → register/issue → owner/gate → evidence → close/reopen | OPEN | first automated security findings |
| S27 | Unsupported old version remains because upgrade risk is feared | all dependencies | Medium | High | lifecycle status; supported-version review; upgrade/replace decision with WHY | OPEN | upstream EOS/deprecation |
| S28 | New dependency unnecessarily increases attack surface | architecture | Medium | High | dependency budget mindset; stdlib/existing capability first; architecture justification | CONTROLLED | dependency proposal |
| S29 | Supply-chain security monitoring stops after baseline freeze | governance | Medium | Critical | APPROVED → MONITORED lifecycle; event-driven recheck; future automation/watch | OPEN | any frozen baseline |
| S30 | Security controls block delivery through uncontrolled tool sprawl | DevSecOps process | Medium | Medium | smallest useful toolchain; one control per threat where possible; evidence-driven additions | CONTROLLED | security-tool proposal |
| S31 | Direct prompt injection overrides agent intent | LLM/agent | Medium | Critical | content is untrusted; policy/tool gate; no model-authorized execution; security regression corpus | MONITOR | LLM agent introduced |
| S32 | Indirect prompt injection in Telegram/web/PDF/file content | retrieval/ingestion | High when agentic | Critical | source boundary; retrieved instructions never modify policy; action justification tied to ResearchTask | MONITOR | agent reads external content |
| S33 | Agent tool abuse / excessive agency | tool runtime | Medium | Critical | default deny; allowlists; parameter validation; quotas; separate read/write tools; approval for high-impact actions | MONITOR | executable tools introduced |
| S34 | Confused-deputy privilege escalation | agents/services | Medium | Critical | propagate user/task auth context; server-side auth; no global admin credential inheritance | MONITOR | multi-role/runtime services |
| S35 | Agent exfiltrates secrets through output/tool/network | LLM/tools/egress | Medium | Critical | secrets out of prompts; scoped credentials; output redaction; egress policy/logging | MONITOR | secrets + agents coexist |
| S36 | Memory/KB poisoning | KB/memory | Medium | Critical | observation != knowledge; Knowledge Gate; provenance; retraction/rollback; review state | MONITOR | persistent memory/KB introduced |
| S37 | RAG/retrieval poisoning manipulates context | retrieval index | Medium | High/Critical | provenance-aware retrieval; corpus change audit; content != instruction; source diversity controls | MONITOR | retrieval layer introduced |
| S38 | Hallucinated tool execution/result is accepted as real | agent orchestration | Medium | Critical | executor-issued result IDs only; evidence references must resolve; UI separates narrative vs execution | MONITOR | tool-calling agents |
| S39 | Agent runaway loop causes cost/rate/resource exhaustion | orchestration | Medium | High | hard limits on cycles/calls/time/data/cost; cancellation; fail closed | MONITOR | autonomous loops |
| S40 | Cross-agent delegation increases privilege | multi-agent | Medium | Critical | delegation cannot raise privilege; task scope propagated; privileged step independently authorized | MONITOR | multi-agent system |
| S41 | Generated code/script executes unsafely | code interpreter/sandbox | Medium | Critical | treat generated code as untrusted; sandbox; no host secrets/network by default; limits; audit | MONITOR | generated code execution |
| S42 | Model/provider update changes security behavior | AI supply chain | Medium | High | model/provider version inventory; security/eval regression; auth kept outside model | MONITOR | model upgrade/provider change |
| S43 | Privileged/root container compromises host | containers | Medium | Critical | non-root where practical; no privileged mode; least capabilities; runtime hardening | MONITOR | containers introduced |
| S44 | Docker/container socket exposure grants host-level control | containers/orchestrator | Medium | Critical | no ordinary app mount of Docker socket; isolate exceptional orchestrator | MONITOR | container orchestration |
| S45 | Dangerous host mounts enable escape/data theft | containers | Medium | Critical | explicit minimal mounts; no broad host/home/SSH/secrets mounts; read-only where possible | MONITOR | containers introduced |
| S46 | Excessive Linux capabilities/device exposure | containers | Medium | Critical | drop capabilities; add only justified; no devices without review | MONITOR | containers introduced |
| S47 | Mutable/compromised container image enters runtime | container supply chain | Medium | Critical | trusted registry; digest/version inventory; scan; SBOM/provenance; promotion policy | MONITOR | images introduced |
| S48 | Container escape/runtime/kernel vulnerability | container runtime | Low/Medium | Critical | supported runtime/kernel; patch watch; isolation-in-depth; do not treat containers as perfect sandbox | MONITOR | containers introduced |
| S49 | Secrets baked into container image/layers | images/build | Medium | Critical | build/runtime secret mechanisms; image/history scan; no secret ARG/COPY | MONITOR | container builds |
| S50 | Unrestricted container/agent egress enables exfiltration/SSRF | network | Medium | Critical | egress allowlist/deny-by-default for risky sandboxes; destination policy; DNS/redirect validation | MONITOR | containers/agents introduced |
| S51 | Lateral movement between services | service network | Medium | Critical | segmentation; service identity; least privilege; no shared global secrets | MONITOR | multi-service deployment |
| S52 | Container/parser resource exhaustion | runtime | Medium | High | CPU/memory/PID/storage/time quotas; queue/input limits | MONITOR | containers/parsers introduced |
| S53 | Shared writable volume poisons code/config/evidence | containers/storage | Medium | High/Critical | minimize shared mutable volumes; permissions; separate evidence from executable/config paths | MONITOR | shared volumes |
| S54 | SSRF reaches internal/cloud metadata or management endpoints | web/agents/connectors | Medium | Critical | destination validation; network segmentation; block metadata/management networks; egress policy | MONITOR | URL fetch/tool introduced |
| S55 | Command injection through adapters/parsers/tools | runtime | Medium | Critical | no shell by default; structured APIs; argument allowlists; escaping not sole control | MONITOR | external command execution |
| S56 | Path traversal / arbitrary file access | file handling | Medium | Critical | canonical paths; rooted storage; deny traversal/symlink abuse; tests | MONITOR | M6/file writes |
| S57 | Unsafe deserialization / object injection | APIs/storage | Low/Medium | Critical | safe formats; schema validation; never load untrusted executable serialization | MONITOR | serialization introduced |
| S58 | XXE / unsafe XML parsing | document/API parsers | Low/Medium | High/Critical | external entities disabled; hardened parser; resource limits | MONITOR | XML support |
| S59 | Web UI attacks (XSS/CSRF/clickjacking) | future UI | Medium | High | framework protections; CSP; CSRF protection; output encoding; security headers | MONITOR | UI introduced |
| S60 | Authentication/session replay or token theft | future API/UI | Medium | Critical | secure session/token lifecycle; expiry/rotation; MFA for privileged roles; replay controls where applicable | MONITOR | authenticated UI/API |

## Current priority queue

### Must address before / during M5 transport implementation

`S02, S05, S06, S07, S08, S14, S15, S16, S17, S18, S26, S29`

### Must address before M6 freeze

Add `S19, S20, S56, S58` plus parser/container controls if those surfaces exist.

### Must address before M7 / external AI-service use

Add `S21, S22, S24, S42` as applicable.

### Must address before executable agent tooling

Add `S23, S31-S41, S54, S55` and any auth/network controls exposed by the tool surface.

### Must address before containerized production

Add `S12, S43-S53` plus SBOM/image provenance and runtime patch monitoring.

### Must address before product release

Add `S03, S04, S10, S11, S13, S27` according to the actual release architecture.

## Finding lifecycle

```text
DETECTED
   ↓
TRIAGED
   ↓
AFFECTED COMPONENT / BASELINE IDENTIFIED
   ↓
FIX / MITIGATE / REPLACE / ACCEPT
   ↓
REGRESSION + SECURITY EVIDENCE
   ↓
CONTROLLED / CLOSED
   ↓
MONITOR
   ↓
REOPEN ON NEW EVIDENCE
```

## Rule

No threat is removed because a tool currently reports zero findings. Risks tied to third-party software, credentials, upstream maintenance, agent authority, runtime isolation and supply-chain integrity remain living controls for the lifetime of the project.

Detailed agent/container model: `AI_AGENT_SECURITY_THREAT_MODEL.md`.
