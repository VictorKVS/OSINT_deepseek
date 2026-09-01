# PDn Knowledge Factory MVP — 152-FZ D0-D5 vertical

**Status:** IMPLEMENTED / CI GREEN / LIVE OFFICIAL RUN PENDING  
**Scope:** one official legal document → exact original → preliminary structure/chunks for later PDn knowledge analysis.

## Official anchor

Source family: Official Internet Portal of Legal Information (`pravo.gov.ru`, including `ips.pravo.gov.ru`).

MVP document: Federal Law of 27.07.2006 No. 152-FZ “On Personal Data”.

Configured locator is stored in `config/pdn_mvp_152fz.json`. The live runner must compute the artifact SHA-256 and MIME from the actual downloaded bytes; neither value is hard-coded.

## Vertical

```text
OfficialSource + SourcePolicy
  ↓
AcquisitionService
  ↓
exact bytes preserved in originals/<sha256>.bin
  ↓
DocumentVersion (URL, MIME, bytes, SHA-256, version date)
  ↓
D3 VERIFIED
  ↓
DocumentCompiler legal-preliminary-v1
  ↓
visible text
  ↓
DOCUMENT / CHAPTER / SECTION / ARTICLE structure nodes
  ↓
stable D5 chunks with document/version/article locator + artifact SHA-256
  ↓
manifest.json
```

No semantic legal interpretation is performed in this MVP. D6-D12 remain NOT_DONE.

## One-click Windows run

From a checkout of `agent/knowledge-factory-m1` run:

```text
RUN_PDN_152FZ_MVP.cmd
```

or:

```text
python scripts/run_pdn_152fz_mvp.py
```

## Expected local outputs

Under `data/knowledge_factory/pdn_mvp/`:

```text
official_sources.jsonl
documents.jsonl
acquisitions.jsonl
audit.jsonl
originals/<sha256>.bin
compiled/DOC-RU-FZ-152-2006/<version-id>/extracted_text.txt
compiled/DOC-RU-FZ-152-2006/<version-id>/structure.jsonl
compiled/DOC-RU-FZ-152-2006/<version-id>/chunks.jsonl
compiled/DOC-RU-FZ-152-2006/<version-id>/manifest.json
```

Successful runner status:

```text
PASS_D0_D5_PRELIMINARY
```

## CI evidence

PR #11 run `32575073589`:

```text
158 tests collected
158 passed
2 skipped
canonical run_dev_osint.py PASS
canonical run_dev_pipeline.py PASS
```

New PDn vertical tests verify:

- acquisition reaches D3 before compilation;
- exact original SHA remains the lineage anchor;
- chapters/articles are detected;
- chunks carry stable IDs and article/structure references;
- same version/parser gives the same structure/chunk IDs;
- tampered original is rejected before D4;
- unauthorized role cannot advance D4-D5;
- D6/D8 semantic states remain NOT_DONE.

## Live gate

The MVP is fully accepted only after one local live run against the configured official `ips.pravo.gov.ru` locator produces:

- real downloaded bytes;
- computed SHA-256;
- non-empty extracted text;
- detected articles;
- non-empty chunks;
- manifest and audit;
- no false D6+ promotion.

If the configured official locator has changed or the portal blocks the request, update only the source locator after re-verification; do not weaken the official-source or exact-byte gates.

## Next step after live PASS

Use the D5 chunks of 152-FZ to build the first PDn semantic layer:

1. terms/concepts;
2. explicit definitions from Article 3 and other definition-bearing clauses;
3. actors/entities;
4. atomic obligations/prohibitions/permissions;
5. applicability/conditions/deadlines;
6. source-linked requirement objects;
7. conflict/gap comparison against the next official PDn documents.
