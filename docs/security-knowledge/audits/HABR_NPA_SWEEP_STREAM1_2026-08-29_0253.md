# Habr NPA sweep — Stream 1 — 2026-08-29 02:53 MSK

## Delta

- New standalone GitHub FULL_TEXT: **0**.
- New reliable GitHub metadata/source-pointer candidates: **2 acts** (160-ФЗ/2005, 367-ФЗ/2021).
- New corpus-level source candidate: **1** (`shodenis/Russian-Law-MCP/data/census.json`).
- New external-corpus blocker: **1** (`irlcode/RusLawOD` stores corpus archives outside GitHub, so there is no per-act GitHub blob to accept automatically).
- Exact duplicates: **0**.

## 1. Federal Law 19.12.2005 No. 160-FZ

Target: `Федеральный закон от 19.12.2005 N 160-ФЗ «О ратификации Конвенции Совета Европы о защите физических лиц при автоматизированной обработке персональных данных»` (Habr 432466, PDn item 1).

### GitHub candidate

- repo: `shodenis/Russian-Law-MCP`
- commit: `bd5a0daca23c600c99e74874abf5b5cb840ef934`
- path: `data/census.json`
- size: `7,204,691 bytes`
- type: `JSON/blob`
- blob SHA: `39dcf0807698959aa4cf93ed134b5a81eecb29b3`
- corpus generated_at: `2026-02-25T16:38:34Z`
- corpus-declared source: `RusLawOD (irlspbru/RusLawOD) via pravo.gov.ru`

Exact record inside the GitHub file:

- id: `fz-160-2005`
- nd: `102103722`
- title: `О ратификации Конвенции Совета Европы о защите физических лиц при автоматизированной обработке персональных данных`
- identifier: `160-ФЗ`
- law_type: `federal_law`
- registry status: `in_force`
- registry effective_date: `2005-12-19`
- classification: `ingestable`
- source pointer: `http://pravo.gov.ru/proxy/ips/?docbody=&nd=102103722`

Classification: `RELIABLE_METADATA_CANDIDATE / CORRECT_IDENTITY_AT_REGISTRY_LEVEL / SOURCE_POINTER / NOT_DOCUMENT_BODY / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY`.

Body-level completeness cannot be checked against this GitHub file because the file contains only census metadata. Exact GitHub searches for a standalone act body did not produce a confirmed full-text blob in this pass.

Primary-source check: direct fetch of the state `pravo.gov.ru` IPS document and of the official-publication portal was not stable in this run. Do **not** promote the registry label `in_force` to `OFFICIAL_CURRENT` until a primary official lifecycle/publication record is resolved.

Blocker remains: `GITHUB_FULL_TEXT_160-FZ_2005`.

## 2. Federal Law 19.11.2021 No. 367-FZ

Target: `Федеральный закон от 19.11.2021 N 367-ФЗ «О ратификации Соглашения о взаимной правовой помощи по административным вопросам в сфере обмена персональными данными»` (Habr 432466, PDn item 5).

### GitHub candidate

Same registry file:

- repo: `shodenis/Russian-Law-MCP`
- commit: `bd5a0daca23c600c99e74874abf5b5cb840ef934`
- path: `data/census.json`
- size: `7,204,691 bytes`
- type: `JSON/blob`
- blob SHA: `39dcf0807698959aa4cf93ed134b5a81eecb29b3`

Exact record:

- id: `fz-367-2021`
- nd: `602562351`
- title: `О ратификации Соглашения о взаимной правовой помощи по административным вопросам в сфере обмена персональными данными`
- identifier: `367-ФЗ`
- law_type: `federal_law`
- registry status: `in_force`
- registry effective_date: `2021-11-19`
- classification: `ingestable`
- source pointer: `http://pravo.gov.ru/proxy/ips/?docbody=&nd=602562351`

Classification: `RELIABLE_METADATA_CANDIDATE / CORRECT_IDENTITY_AT_REGISTRY_LEVEL / SOURCE_POINTER / NOT_DOCUMENT_BODY / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY`.

Exact GitHub searches did not reveal a standalone full-text act body. The official-publication card expected for the 19.11.2021 publication could not be fetched reliably in this run, so official/current status remains a separate primary-source blocker.

Blocker: `GITHUB_FULL_TEXT_367-FZ_2021`; primary verification: `PRIMARY_OFFICIAL_CARD_FETCH_BLOCKER`.

## 3. Corpus-level source findings

### `shodenis/Russian-Law-MCP`

The repository is useful as a discovery/identity registry, but it is not a self-contained GitHub corpus of act bodies. `src/index.ts` expects `../data/database.db`; the committed `data/` directory contains `.gitkeep` and `census.json`, not `database.db`. Therefore the per-law records in `census.json` must not be treated as full texts.

Gate: `REGISTRY_RECORD != FULL_TEXT` and `SOURCE_URL_TO_PRAVO != OFFICIAL_GITHUB_COPY`.

### `irlcode/RusLawOD`

- repo: `irlcode/RusLawOD`
- commit: `44b8e34ec35e4d30c32085dc129035987185bd6b`
- `data.txt`: 512 bytes, blob `9cb530932b9434755e155267aeba0a2361835af6`, type `TXT/blob`.

`data.txt` contains links to multipart corpus archives in Yandex Object Storage; the individual legal texts are not committed as GitHub blobs. The project README states that version 3 covers 1991–2025, uses the state IPS `Законодательство РФ` at pravo.gov.ru, explicitly notes that this IPS is **not official publication**, and also states that the corpus keeps **only first versions**, not current consolidated texts.

Classification: `EXTERNAL_CORPUS_POINTER / NOT_PER_ACT_GITHUB_BLOB / ORIGINAL_VERSIONS_ONLY / NON_OFFICIAL_REFERENCE_SOURCE`.

Gate: `REPO_ADVERTISES_CORPUS != PER_ACT_GITHUB_FULL_TEXT`; any act extracted from the external archive still needs its own identity/completeness/hash/lifecycle verification before admission to the primary KB layer.
