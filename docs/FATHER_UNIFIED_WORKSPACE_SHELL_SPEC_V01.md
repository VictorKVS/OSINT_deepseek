# FATHER Unified Workspace — Shell and OSINT integration contract v0.1
Date 2026-10-16. State: UI PROTOTYPE, not integrated or deployed.

## Core UX
Single FATHER visual canvas, global left tabbed explorer, shared right inspector, global trace and security status. No separate OSINT/ALINA sites. Current demo: local standalone HTML preview, synthetic data, no accounts or API connections.

Left tabs:
1. Agents: every registered FATHER agent, expandable internal folders: Overview, Prompt, RAG/Knowledge, Database, Memory, Tools/MCP, Workflows, Channels, CRM/Signals, Security/RBAC, Evaluation/Tests, Logs/Trace, Versions.
2. Channels: catalog grouped by messaging, social/marketplaces, websites/email/API and extension adapters. Telegram, MAX, WhatsApp Business, VK, Viber, Signal, Discord, Slack, MS Teams, Matrix, WeChat, LINE, Avito, YouTube, Rutube, Dzen, Odnoklassniki, Reddit, Habr, GitHub, GitLab, RSS, webhooks, websites, email, VoIP/SMS and more. **Listing is not a claim that official APIs permit ingestion.** Each adapter requires capability, provider and terms verification.
3. CRM: Contacts/Abonents, incoming signals, linked channel identities, conversations, tickets/cases, subscriptions, alerts, tasks and approvals.
4. Security & DevSecOps: policy, RBAC/ABAC, source provenance, protected data boundaries, SAST/SCA/SBOM, dependency/license guard, audit and retention.

## One service, many agent views
CRM is a shared service; inside each agent CRM folder contains permission-filtered references to assigned contacts and their signals. No duplicate CRM databases per agent unless documented tenancy/isolation requirements demand it.
RAG, DB and Memory likewise are logical resource views under each agent, backed by shared or isolated physical services depending on security boundaries.
No credentials in frontend or public git.

## Channel adapter contract
AdapterRegistry(id, provider, capability_flags, verified_at, API/ToS review, data_types, permitted_scope, credential_ref, rate_budget, enable_status, schema_version).
Incoming: ChannelEvent -> dedup -> privacy/source permission -> assigned agent routing -> CRM Signal -> TraceID -> human-reviewed output.
Implement no unauthorized private messaging collection, hidden-source extraction, anti-bot bypass or automation of personal attribution. Avito and other marketplaces only via authorized supported integrations.

## Unified trace
correlation_id, project_id, agent_id, workflow_run_id, source_event_ref, contact_ref (pseudonymous), signal_id, claim_id, evidence_ref, decision_id, actor_role, policy_rule_id, code/model/prompt versions, elapsed time, cost, result.
All edges ACL-filtered server side; UI must not leak restricted links/counts.

## UI design tokens (candidate, align with actual FATHER tokens before merge)
left 300px, inspector 320px, header 60px, footer 34px, deep navy background, outlined nodes, progressive panel disclosure; use existing platform tokens if available. Interactive demo is a visual exploration/reference, not the source of truth for final design tokens.

## Integration dependency and gates
First discover/confirm actual FATHER frontend repository, component naming, existing design system and runtime. Merge shell implementation into existing frontend with tests, do not create second product.
No new OSINT live collectors or production CRM integrations until prior FATHER Site + Agent Zoo/Model Zoo E2E and Security G7 gates are satisfied. Standalone local visual prototype is not a release.
## Acceptance
- Tabs and tree expanded/collapsed, agent resource folders accessible with keyboard.
- One common canvas for OSINT and ALINA, matching themes and node contracts.
- Single CRM registry presented in global and agent-scoped views, with tenant authorization.
- Channel capability catalog with verification state, no false connected status.
- Read-only trace across channel -> signal -> agent -> evidence -> review.
- Secrets excluded from DOM, tests for XSS, ACL and prompt-injection attempted actions.
- CI guards, license/asset scan, versioned releases, fallbacks for provider outages.

## Screen reference
Standalone prototype: father_workspace/index.html created in working artifact directory; not published to production.
