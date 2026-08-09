# Stage 06 — VIP legacy subsystem audit

**Status:** REVIEWED / REMOVE IMPLEMENTATION AFTER EVIDENCE CAPTURE  
**Scope:** `vip/`  
**Decision class:** repository rationalization

## Executive decision

The current `vip/` package is a pre-FATHER prototype and is not part of the approved OSINT DEV architecture. Repository search found no approved current dependency on `vip` or `CompleteVIPSystem` outside the subsystem itself.

The package mixes several unrelated concerns:

```text
VIP orchestration
├── IP / proxy rotation
├── generated personas / sockpuppets
├── temporary phone / SMS gateway
├── evidence capture / chain of custody
└── pricing / feature tiers
```

This violates the present FATHER rule of narrow components owned by explicit requirements.

## Component disposition

| Area | Decision | WHY |
|---|---|---|
| `vip/integration.py` | DELETE | monolithic legacy orchestrator; no current requirement or dependency |
| `vip/__init__.py` | DELETE | legacy tier/product wrapper |
| `vip/config/tiers.yaml` | DELETE | fictional/commercial tier model is unrelated to current architecture |
| `vip/anonymity/` | DELETE IMPLEMENTATION / PRESERVE REQUIREMENT IDEA | networking anonymity requires a separate OPSEC/threat-model stage; must not be silently coupled to collection |
| `vip/phone/` | DELETE IMPLEMENTATION / PRESERVE REQUIREMENT IDEA | temporary-number/SMS automation is not an approved OSINT requirement |
| `vip/sockpuppet/` | DELETE IMPLEMENTATION / PRESERVE REQUIREMENT IDEA | persona management is a separate controlled capability and requires policy, legal/ethical scope and audit before implementation |
| `vip/evidence/chain_of_custody.py` | DELETE IMPLEMENTATION / ADAPT CONCEPT LATER | contains useful hashing, original preservation and audit-chain ideas but current implementation is not the approved Artifact/Evidence model |

## Evidence module — useful lessons retained

The legacy evidence code already contains several concepts aligned with the new Artifact roadmap:

```text
capture original bytes/data
    ↓
SHA-256
    ↓
metadata record
    ↓
append audit/chain entry
    ↓
verify current bytes against original hash
```

These ideas are retained as requirements, not copied as production code.

### Problems that prevent direct reuse

1. Evidence identity and persistence are tied to an in-memory `hashes` dictionary, so verification after process restart is not robust without reconstructing state.
2. Metadata and chain files are mutable JSON files with no tamper-evident chaining/signing.
3. `actor` is hard-coded to `system`; there is no principal/tool/run identity.
4. No distinction between original artifact, normalized derivative and analytical output.
5. No explicit source-observation provenance model.
6. `MetadataSanitizer` is mixed into evidence custody even though sanitization creates a derivative and must never replace the original.
7. Extension-based routing is used for sanitization; future ingestion must verify declared MIME + detected signature.
8. Error handling returns strings instead of typed results/errors.

## Future Evidence / Artifact contract requirements

When a real use case opens this stage, design from requirements first. Minimum intended concepts:

```text
Artifact
├── artifact_id
├── source_observation_id
├── original_name
├── declared_mime
├── detected_mime
├── size
├── sha256_original
├── original_storage_ref
├── acquired_at
├── acquisition_method
└── provenance

Derivative
├── parent_artifact_id
├── transformation
├── tool + version
├── parameters
├── sha256_output
└── storage_ref

CustodyEvent
├── artifact_id
├── action
├── actor/tool/run
├── timestamp
├── reason
└── previous_event linkage / tamper evidence
```

The final model may differ after requirements, ADR and benchmark; this is a requirements seed only.

## Security/architecture principle retained

> **Original evidence is immutable. Sanitization, transcription, OCR, conversion and translation create derivatives; they never overwrite the original.**

This directly supports future local-first transcription and multi-format ingestion.

## OPSEC-related modules

Anonymity, temporary phone numbers and personas are not discarded as ideas, but they must not be hidden inside a generic OSINT worker.

Future shape, if a legitimate requirement appears:

```text
Research policy / approved case
        ↓
OPSEC requirement
        ↓
Threat + legal/policy review
        ↓
Architecture / provider-donor review
        ↓
Acceptance tests
        ↓
Controlled OPSEC adapter
```

No such component is approved in the current DEV baseline.

## Cleanup gate

Preconditions satisfied:

- current product boundary is `father_osint/`;
- clean-checkout CI is green;
- no current approved dependency on VIP subsystem found;
- reusable evidence ideas are captured in documentation;
- future ingestion/transcription roadmap already preserves originals and hashes.

**Decision:** remove the `vip/` implementation from the active repository, then run clean CI. Git history remains the implementation archive.
