# Prebuilt Russian-Law-MCP data — 100-law audit decision

Status: **DATA REJECTED / CONTENT QUARANTINED / INFRASTRUCTURE REFERENCE ALLOWED**

## Evidence

Observed local workstation audit over a deterministic sample of 100 donor rows whose `source_url` points to `pravo.gov.ru`:

- sampled: `100`;
- `VERIFIED_MATCH=0`;
- `IDENTITY_COLLISION=24`;
- `AMBIGUOUS=76`;
- `UNVERIFIED_TRANSPORT=0`;
- `AUDIT_ERROR=0`;
- duplicate `nd` groups in the full eligible donor set: `20`;
- observed confirmed-collision share in this sample: `0.24`;
- wall-clock audit: `10.664 s` with 5 workers.

The previously diagnosed 152-ФЗ record is a confirmed semantic/source identity collision: donor metadata says `152-ФЗ / О персональных данных`, while `source_url` points to `nd=102108264` and the provision content has the 149-ФЗ signature.

## Interpretation

`24%` is **not** an estimate of the total true error rate. It is only the confirmed collision share under this verifier. The remaining `76%` are ambiguous, not verified-good. Therefore the only safe adoption conclusion is fail-closed:

`0 verified + 24 confirmed collisions + 76 unresolved => prebuilt donor content cannot be trusted for candidate import or canonical knowledge.`

No further sample-size expansion is required for the current P0 architecture decision. Additional donor-data forensics would be investigative work, not a blocker for Knowledge Factory.

## Adoption split

### Keep / reference

- SQLite schema patterns;
- FTS5/search architecture;
- MCP tooling patterns;
- local warm-query design;
- update/drift-check ideas;
- Apache-2.0 implementation patterns subject to normal code/license review.

### Reject / quarantine

- bundled `data/database.db` content;
- donor law-to-source mappings;
- donor legal currentness/status as truth;
- donor provision text as canonical/candidate import;
- donor cross-references as trusted legal relations.

## Central policy

The decision is enforced in `config/external_assets.seed.jsonl` and `father_osint/external_assets.py`.

- `ansvar-russian-law-mcp-prebuilt-db` => `adoption=REJECT`, `content_reuse_mode=NONE`;
- `ansvar-russian-law-mcp-code` => algorithm/reference reuse only;
- `ruslawod-corpus` => `CANDIDATE_ONLY`, never direct promotion;
- `publication-pravo-official-api` => `PROOF_ADAPTER`, pending runtime acceptance.

External assets can never directly authorize canonical promotion. D14/D15 remain the governance boundary.

## Architecture consequence

Stop spending P0 capacity on repairing or validating the prebuilt donor database. Move the critical path to:

`Official publication API/OpenData -> exact/source-backed acquisition -> local evidence/cache -> RusLawOD candidate bootstrap where useful -> FATHER canonical verification/enrichment -> review/promotion.`

The next implementation target is the official publication adapter behind the existing acquisition boundary, with fail-closed identity, bytes, MIME/signature, SHA-256, provenance, retry/circuit-breaker behavior and local cold-once/warm-many reuse.
