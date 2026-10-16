# FATHER Ecosystem — Agent Registry, Project Lifecycle and Integration Blueprint v0.1
Status: DRAFT, architectural plan, not deployed. Date: 2026-10-16.

## Constitutional rule
FATHER is the non-deletable platform root, not a user-removable agent. Agents may be embedded within FATHER, project-scoped, or separately deployed via an adapter. Projects and agents are different entities. No deletion of FATHER via product UI or API; infrastructure deletion governed separately by privileged operations.

## Core graph
FATHER (platform) -> Workspace -> Project -> AgentInstance -> AgentDefinition -> capabilities/configurations; AgentDefinition -> PromptVersion, RAGCollection, MemoryPolicy, ModelRoute, ToolGrant, ChannelBinding, CRMView, Workflow, Evaluator, Observability, SecurityPolicy. All have versioned IDs, ownership, privacy controls and provenance.

## Agent registry groups
1. Research/Analysis: ALINA Analyst; OSINT Research/Watchtower; Legal/IB knowledge; Research Curator; Auditor.
2. Engineering: Architect; Python/Backend; Frontend/Makar; DevOps; DevSecOps; SRE; QA/Evaluator; Security Defender; Security Scanner; Threat Modeling; Documentation/Release.
3. Creative: ALINA Creative Director; Book Writer/Editor; Script Writer; Image Studio; Avatar Producer; Video/Podcast Producer; Site Design/Maintenance; Game Studio; Prototyping/3D/AR/VR; Visual Systems/Infographics. These may be different agent definitions or profiles sharing creative engine.
4. Education: Lesson Ingestor (authorized web sources, documents, videos); Course Analyst; Curriculum Builder; Exercise/Lab Builder; Course Editor/ALINA; Course QA/Update Watcher. Source lesson ownership, copyrights and permitted uses mandatory.
5. Operations: CRM/Signal Triage; Channel Operator; Integration Operator; Project Manager/Planner; Dependency & License Guard.
These are target capabilities, not claims that all agents currently exist or are live. Catalog is extensible via approved manifests.

## Agent lifecycle
DRAFT -> REGISTERED -> CONFIGURED -> TESTED -> APPROVED -> ACTIVE -> PAUSED -> ARCHIVED -> RESTORED. Deletion request after archival uses impact assessment and soft-delete/tombstone, retention/legal hold checks, owner approval and irreversible cleanup after retention. Shared definitions can't be deleted if referenced by active projects; platform FATHER itself is immutable in UI. Deleting agent does not delete shared CRM, evidence, or canonical knowledge.
Project template and agent template support clone/fork preserving lineage, separate IDs and access limits.

## Omnichannel and service adapters
Google Workspace/Drive/Gmail/Calendar/Docs/Sheets; Microsoft 365/Outlook/OneDrive/Teams; OpenAI/ChatGPT API where available; Telegram, MAX, WhatsApp Business, VK, Discord, Slack, Web, RSS, Avito permitted integration; GitHub/GitLab; model vendors and on-prem Ollama/vLLM; additional connectors via registry. Availability and exact actions depend on provider API, user permissions and separately confirmed licensing. Never assume all ChatGPT-connected tools can be redistributed into a custom app; implement with documented provider APIs or explicit authorized connectors.
MCP/tool adapter manifest must include capability list, scoped authorization, credential vault ref, input/output schema, rate/cost budget, data residency, egress boundaries, privacy review and fallback. No universal autonomous access to third-party accounts.

## Unified visual shell
Sidebar: Platform / Projects / Agents / Channels / CRM / Creative / Education / Engineering / Security / Integrations. Agent tree: Prompt, RAG, DB, Memory, Models, Tools/MCP, Workflow, Channels, CRM, Assets, Evaluation, Logs, Security, Versions. Project detail: owned agents, assignment, lifecycle, artifacts, permissions, run history. Single FATHER Canvas and visual token library; cards support group/search, live statuses only from monitored runtime.

## Education ingestion pipeline
Approved URL/video/course materials -> source/license/access check -> media metadata/transcript using lawful permission/API and captions, where available -> content extraction -> lesson decomposition -> concept/entity graph -> quiz/lab/checklists -> citation/edition/source review -> proposed lesson updates -> ALINA editorial approval -> versioned course publication. Do not bypass paywalls/DRM, copy entire copyrighted videos or redistribute without authorization. Audio transcription only when lawfully obtained.
Videos may require permission and technical tooling; status not supported until verified.

## DevSecOps and evidence across every agent
RBAC/ABAC; least-privileged tokens; secrets vault; PII; guarded external tools; prompt injection control; integrity and signatures, SBOM, SCA/SAST, license checks, malware isolation, threat modeling, SIEM, tracing, eval, human gate. All execution events get correlation_id (agent, project, channel, tools, model, prompt, evidence, decision, cost, runtime).

## Work sequencing
P0 inventory existing GitHub and local artifacts, confirm true FATHER frontend source, registry types, storage and open issues.
P1 build a versioned declarative registry, lifecycle and explorer spec based on existing UI prototype.
P2 validate one ALINA Analyst + OSINT project end to end using synthetic authorized data and shared trace.
P3 creative pilot (book -> script -> image -> avatar) and website maintenance pilot.
P4 learning factory pilot (authorized lesson -> notes -> exercises -> ALINA update proposal).
P5 connectors and DevSecOps integration, provider by provider, with explicit scopes.
Gating: FATHER site and zoos existing E2E requirements remain, no actual new runtime implementation, deployments or third party connection without review.
