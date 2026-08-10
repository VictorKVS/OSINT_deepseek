# FATHER / OSINT_deepseek — Security & Software Supply-Chain Threat Register

**Status:** living register  
**Scope:** source code, dependencies, donor projects, CI/CD, secrets, build/release chain, runtime integrations and future AI/file-processing surfaces.  
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
| S23 | AI model/tool-call injection causes untrusted content to drive actions | future agentic Analyst/tool layer | Medium | Critical | model proposes, deterministic policy/code executes; tool allowlist; untrusted-content boundary; approval gates | MONITOR | executable LLM tools introduced |
| S24 | Model/package provenance unknown or tampered | local AI models | Medium | High | source/license/hash/model version inventory; controlled download/update | MONITOR | local model adoption |
| S25 | Security scanner becomes false assurance | all | Medium | High | scanners are evidence inputs, not approval authority; manual architecture/threat review remains | CONTROLLED | any "green scan = secure" decision |
| S26 | Security findings are discovered but not tracked to closure | governance | Medium | High | finding → register/issue → owner/gate → evidence → close/reopen | OPEN | first automated security findings |
| S27 | Unsupported old version remains because upgrade risk is feared | all dependencies | Medium | High | lifecycle status; supported-version review; upgrade/replace decision with WHY | OPEN | upstream EOS/deprecation |
| S28 | New dependency unnecessarily increases attack surface | architecture | Medium | High | dependency budget mindset; stdlib/existing capability first; architecture justification | CONTROLLED | dependency proposal |
| S29 | Supply-chain security monitoring stops after baseline freeze | governance | Medium | Critical | APPROVED → MONITORED lifecycle; event-driven recheck; future automation/watch | OPEN | any frozen baseline |
| S30 | Security controls block delivery through uncontrolled tool sprawl | DevSecOps process | Medium | Medium | smallest useful toolchain; one control per threat where possible; evidence-driven additions | CONTROLLED | security-tool proposal |

## Current priority queue

### Must address before / during M5 transport implementation

`S02, S05, S06, S07, S08, S14, S15, S16, S17, S26, S29`

### Must address before M6 freeze

Add `S18, S19, S20`.

### Must address before M7 / external AI-service use

Add `S21, S22, S23, S24` as applicable.

### Must address before product release

Add `S03, S04, S10, S11, S12, S13, S27` according to the actual release architecture.

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

No threat is removed because a tool currently reports zero findings. Risks tied to third-party software, credentials, upstream maintenance and supply-chain integrity remain living controls for the lifetime of the project.
