# FATHER / OSINT_deepseek — AI Agent, Container & Runtime Threat Model

**Status:** ACTIVE CROSS-CUTTING SECURITY MODEL  
**Applies when:** containers, LLM/agent tooling, executable tools, external connectors, browsers, parsers, sandboxes, schedulers or privileged runtime services are introduced.  
**Rule:** agent security is treated as a runtime security problem, not only a prompt-quality problem.

## 1. Security objective

FATHER agents must never obtain implicit authority merely because a model produced an instruction. The model may interpret, classify, plan or propose. Deterministic policy, explicit permissions and bounded runtime controls decide what is actually executed.

```text
UNTRUSTED CONTENT
      ↓
MODEL / AGENT
      ↓ proposes
POLICY + TOOL GATE
      ↓ permits / denies
DETERMINISTIC EXECUTOR
      ↓
SANDBOXED / LEAST-PRIVILEGE ACTION
      ↓
AUDIT + RESULT
```

## 2. Agent-specific threat families

### AG-01 Prompt injection
Malicious source text attempts to override task instructions, reveal secrets or cause unauthorized action.

Controls:
- all collected content is untrusted data;
- separate system/task instructions from source content;
- model output is never an authority token;
- high-impact actions require policy checks and, where appropriate, human approval;
- test corpus includes direct and indirect prompt injection.

### AG-02 Indirect prompt injection through web/PDF/Telegram/files
An attacker embeds instructions in material the analyst asks the agent to read.

Controls:
- source content cannot modify tool policy;
- extraction layer marks source boundaries and provenance;
- no hidden instruction field is copied into executable configuration;
- tool calls must be justified by the original ResearchTask, not by instructions discovered inside content.

### AG-03 Tool abuse / excessive agency
Agent attempts a technically valid tool action outside the approved purpose.

Controls:
- explicit tool allowlist per role/task;
- per-tool parameter validation;
- default deny;
- bounded counts, time, scope and destination;
- dangerous actions separated from read-only tools;
- no shell/tool execution simply because the LLM emitted syntax.

### AG-04 Confused deputy
A low-privilege user causes a more privileged agent/service to perform an action on their behalf.

Controls:
- propagate caller identity and authorization context;
- server-side authorization at each privileged action;
- agent does not inherit global administrator credentials;
- audit records who requested, who approved and what executor acted.

### AG-05 Secret exfiltration
Prompt or malicious content induces the agent to reveal API keys, sessions, environment values or system prompts containing secrets.

Controls:
- secrets never placed into prompts unless technically unavoidable;
- secret handles/references instead of plaintext;
- output redaction;
- network egress policy;
- canary/testing for secret disclosure;
- short-lived scoped credentials where possible.

### AG-06 Data exfiltration through tools
Agent sends evidence or sensitive data to an external URL/API/service.

Controls:
- outbound destinations allowlisted;
- data classification checked before external transfer;
- local-first processing for sensitive evidence;
- external connector registry and approval state;
- egress logging and review.

### AG-07 Memory / knowledge poisoning
Malicious or low-quality content is stored as durable memory/KB and influences later agents.

Controls:
- raw observation != knowledge;
- Analyst/Socrates/Knowledge Gate separation;
- provenance and review state mandatory;
- no automatic promotion from retrieved content to governed KB;
- correction/retraction and rollback supported.

### AG-08 Retrieval poisoning / RAG injection
Attacker manipulates indexed documents or retrieval ranking so malicious text dominates context.

Controls:
- provenance-aware retrieval;
- source trust is a signal, not absolute authority;
- diversity / source constraints where appropriate;
- retrieved instructions treated as content, not policy;
- suspicious corpus changes auditable.

### AG-09 Hallucinated tool/result treated as fact
Model claims it searched, downloaded, verified or executed something that deterministic code never did.

Controls:
- tool result objects originate only from executors;
- model cannot manufacture successful execution records;
- evidence/result IDs must resolve to stored artifacts/observations;
- UI distinguishes model narrative from verified execution.

### AG-10 Agent loop / runaway cost
Agent repeatedly calls tools or delegates to subagents.

Controls:
- hard max cycles/calls/time/data/cost;
- cancellation;
- supervisor budget independent of model instructions;
- fail closed when budget exhausted.

### AG-11 Cross-agent privilege escalation
One agent delegates to another with broader privileges than the originating task permits.

Controls:
- privilege is inherited downward or reduced, never silently expanded;
- delegation carries task scope and caller context;
- privileged agent actions require separate policy decision.

### AG-12 Agent impersonation / spoofed identity
A process or message claims to be a trusted agent/service.

Controls:
- authenticated service identity;
- signed/validated internal messages where warranted;
- do not trust display names;
- service-to-service authorization.

### AG-13 Unsafe generated code
LLM generates code/scripts that are executed during analysis.

Controls:
- generated code is untrusted input;
- sandboxed execution only when an approved requirement exists;
- no host filesystem/network/secrets by default;
- resource quotas and timeout;
- static/security checks where practical;
- generated code execution is auditable.

### AG-14 Model/provider compromise or behavior change
External/local model update changes security behavior.

Controls:
- model version/source/hash inventory;
- evaluation/security regression before material upgrade;
- provider change triggers review;
- critical authorization remains outside model.

## 3. Container/runtime threat families

### CT-01 Privileged container / root execution
Control: non-root where practical; no `--privileged`; least Linux capabilities; read-only filesystem where compatible.

### CT-02 Docker/container socket exposure
Control: never mount host Docker socket into ordinary app/agent containers; if orchestration requires it, isolate a dedicated tightly controlled component.

### CT-03 Host filesystem escape / dangerous mounts
Control: explicit mounts only; no broad `/`, home, SSH, secrets or repository write mounts; read-only by default where possible.

### CT-04 Excessive Linux capabilities / device exposure
Control: drop capabilities; add only justified capabilities; no host devices unless requirement reviewed.

### CT-05 Container image supply-chain compromise
Control: trusted registry/source; version/digest inventory; vulnerability scan; rebuild policy; SBOM/provenance before releases.

### CT-06 Mutable image tags
Control: production/release baselines use immutable digest or controlled promotion strategy; tag alone is insufficient provenance.

### CT-07 Vulnerable base image / packages
Control: supported minimal base; vulnerability monitoring; regular rebuild even if application code did not change.

### CT-08 Container escape/runtime vulnerability
Control: supported container runtime/kernel; patch monitoring; isolation boundaries; do not treat containers as a perfect sandbox.

### CT-09 Secrets baked into image/layers
Control: build-time/runtime secret mechanisms; scan image/history; no credentials in Dockerfile, ARG, copied config or layer history.

### CT-10 Unrestricted network egress
Control: agent/extractor containers receive only required network routes/destinations; high-risk parsers/code sandboxes default to no egress.

### CT-11 Lateral movement between services
Control: network segmentation; per-service identity; least privilege; no shared global secrets.

### CT-12 Resource exhaustion
Control: CPU/memory/PID/storage/time quotas; request/job limits; decompression/parser limits.

### CT-13 Writable shared volumes poison other components
Control: minimize shared mutable volumes; ownership/permissions; content validation; separate raw evidence from executable/config paths.

### CT-14 Unsafe container logs
Control: no sessions/secrets/evidence bodies by default; retention/access policy; structured security events.

## 4. Network/API/runtime attacks to include

The security register must cover, as applicable: broken access control, SSRF, command injection, SQL/NoSQL injection, path traversal, unsafe deserialization, XXE, template/code injection, XSS/CSRF for future UI, request smuggling/header abuse where relevant, authentication/session attacks, DoS/resource exhaustion, race conditions, replay, dependency attacks, malicious files/parsers, service impersonation, MITM/TLS misconfiguration, DNS/redirect abuse, webhook spoofing, exposed management interfaces and insecure defaults.

## 5. Mandatory agent execution invariants

1. **Content never grants authority.**
2. **Model output never bypasses authorization.**
3. **Tool execution is deterministic, validated and auditable.**
4. **Default deny for tools, destinations and privileges.**
5. **Every task has bounded time/calls/data/cost.**
6. **Secrets are not normal prompt context.**
7. **Sensitive external transfer requires policy approval.**
8. **Raw observations cannot self-promote into KB.**
9. **Agent delegation cannot silently increase privilege.**
10. **A container is isolation-in-depth, not a security proof.**
11. **Generated code is untrusted.**
12. **Every executable integration has an emergency-disable path.**

## 6. Security testing packs by capability

```text
M5 Telegram
  session theft / log leakage / malicious messages / rate abuse / replay

M6 Artifact
  polyglots / parser exploits / bombs / path traversal / active content / resource exhaustion

M7 Local AI / transcription
  malformed media / model provenance / local service exposure / unsafe external fallback

M8 Knowledge Gate
  memory poisoning / provenance bypass / unauthorized publication / retraction integrity

Future agent tools
  prompt injection / indirect injection / tool abuse / SSRF / command execution /
  cross-agent escalation / secret exfiltration / runaway loops / unsafe generated code

Future containers
  privilege / capabilities / mounts / socket / image CVEs / secrets / egress / escape /
  lateral movement / quotas
```

## 7. Freeze rule

Any milestone introducing agentic execution, containers or externally reachable services must include a threat-model delta and security acceptance tests. In-scope critical agent/container threats without verified controls block the baseline freeze.
