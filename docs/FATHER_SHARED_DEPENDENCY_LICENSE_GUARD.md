# FATHER Shared Dependency & License Guard — Integration Standard v0.1
Date: 2026-10-16. DRAFT / not deployed.

## Architectural rule
One common policy and evidence format for all FATHER products; a small repo-local adapter in every project. This is a cross-project shared-service capability, not a standalone OSINT implementation. No runtime deployment or code changes here.

## Coverage registry
| Workspace | Focus | Required integration |
|---|---|---|
| OSINT_deepseek + OSINT_TRICOLOR | TDLib/MTProto adapters, document parsers, threat intel APIs | transport supply-chain, permissions, approved collectors |
| alina-knowledge-worker | parsing, RAG, embeddings, model usage | data governance, parser/model licenses |
| BOOKCRAFT-SITE / Makar Frontend Factory | npm, frontend assets, image/model provenance | lockfile audit, font/media assets rights, API outage |
| CyberED | security training and pentest tools | isolated tools, explicit licenses, sandbox and provenance |
| OTUS Architect / OSUT | platform diagrams, containers, K8s/IaC | image signing, IaC module versions, SBOM |
| Agent Zoo / Model Zoo | model checkpoints, datasets, plugins, tools | license/use restrictions, model artifacts, remote endpoints |
| FATHER shared platform | all products | central exceptions registry, change watch, policy-as-code and release gates |

## Control sequence
Discover dependency → exact version/commit and license copy → SPDX/CycloneDX SBOM → transitive dependency and network dependency inventory → SCA/secrets/provenance → dependency owner → offline/remote outage scenario → alternative or rollback → security + license approval → lock & monitored update.

## Mandatory decision rules
- Open-source license change in new version is NOT by itself a reason to shut down already approved pinned builds. Examine actual licensed version and compliance.
- A compromised release may require emergency quarantine under documented incident authorization; never silent destructive auto-disable of production.
- SaaS license/activation services can fail remotely; provider adapters must degrade gracefully and support replacement.
- AGPL, copyleft, source-available, proprietary, dataset and model licenses require distinct legal review.
- No auto-install/auto-update of third-party donor packages into live production pipeline.
- Preserve original license text and evidence of lawfully obtained package artifact, without implying any universal right to redistribute.
- Never publish secrets, private models or copyrighted source in public dependency inventory.

## Shared deliverables (design targets)
FATHER-DEPENDENCIES.yaml manifest schema: component, version, commit, checksum, SPDX, NOTICE, supplier, legal_use, package_origin, network_endpoints, model/data_license, owner, fallback, criticality.
Policy rules: fail build for secret leak, known malicious artifact, unapproved source or unresolved critical vulnerabilities under agreed severity; warn/review for new license metadata or source archival.
Interfaces: local CI adapter → aggregated evidence metadata → central risk register → human gate → release audit. Central service should not need to access private source code.

## Architecture and implementation gates
G0 business requirements; G1 source/legal classification; G2 alternative choice; G3 SBOM schema; G4 security model; G5 sandbox PoC; G6 cost/offline and fallback tests; G7 explicit approval. No implementation before FATHER site/Agent Zoo/Model Zoo E2E for related blocked projects.

## References
https://opensource.org/faq
https://cyclonedx.org/capabilities/sbom/
https://spdx.dev/
