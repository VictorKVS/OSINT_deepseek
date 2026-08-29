# Habr NPA sweep — Stream 1 — 2026-08-29 08:55 MSK

## Delta

- `FULL_TEXT +0`
- `RELIABLE_METADATA_CANDIDATE +3`
- `REFERENCE_LIST_STALE_TITLE_CONFLICT +1`
- `GITHUB_FULL_TEXT_BLOCKER +3`
- `EXACT_DUPLICATE +0`
- `BODY_IDENTITY_CONFLICT +0`

## 1. Federal Law 24.04.2020 No. 123-FZ

Habr 432466 (version 28.05.2026) still lists the original title: «О проведении эксперимента по установлению специального регулирования в целях создания необходимых условий для разработки и внедрения технологий искусственного интеллекта в субъекте Российской Федерации — городе федерального значения Москве и внесении изменений в статьи 6 и 10 Федерального закона “О персональных данных”».

### GitHub candidate

- repo: `shodenis/Russian-Law-MCP`
- commit: `bd5a0daca23c600c99e74874abf5b5cb840ef934`
- path: `data/census.json`
- size: `7,204,691 bytes`
- type: `JSON/blob`
- blob SHA: `39dcf0807698959aa4cf93ed134b5a81eecb29b3`
- record: `id=fz-123-2020`, `nd=102722375`, `identifier=123-ФЗ`
- record title matches the original 2020 title.

Classification: `RELIABLE_METADATA_CANDIDATE / CORRECT_ORIGINAL_IDENTITY_AT_REGISTRY_LEVEL / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY`.

The record is metadata only; it does not contain the normative body of the act. An exact GitHub code search for `123-ФЗ + О проведении эксперимента` returned zero independent files in this pass. This is only a search blocker, not proof that no full text exists on GitHub.

### Primary-source check and title conflict

- Official initial publication: 24.04.2020, publication No. `0001202004240030`.
- Federal Law 08.08.2024 No. 233-FZ, official publication No. `0001202408080031`, amended both 152-FZ and 123-FZ.
- After the amendment, official 2025 Government material (PP RF 01.08.2025 No. 1154) cites 123-FZ under the expanded title including: «…об особенностях обработки персональных данных при формировании региональных составов данных и предоставления доступа к региональным составам данных…».

Therefore the Habr 28.05.2026 entry and the GitHub census generated 25.02.2026 both retain a stale pre-amendment title.

Status: `REFERENCE_LIST_STALE_TITLE_CONFLICT / GITHUB_REGISTRY_STALE_TITLE / CURRENT_TITLE_REQUIRES_PRIMARY_NORMALIZATION`.

Blocker: `GITHUB_FULL_TEXT_123-FZ_2020 = OPEN`.

## 2. Federal Law 01.04.2025 No. 41-FZ

Target from Habr general information / state information systems list: «О создании государственной информационной системы противодействия правонарушениям, совершаемым с использованием информационных и коммуникационных технологий, и о внесении изменений в отдельные законодательные акты Российской Федерации».

### GitHub candidate

Same corpus file:

- repo: `shodenis/Russian-Law-MCP`
- commit: `bd5a0daca23c600c99e74874abf5b5cb840ef934`
- path: `data/census.json`
- size: `7,204,691 bytes`
- type: `JSON/blob`
- blob SHA: `39dcf0807698959aa4cf93ed134b5a81eecb29b3`
- record: `id=fz-41-2025`, `nd=608501034`, `identifier=41-ФЗ`
- title matches Habr and the official publication.
- repository field says `status=amended`; this field is not accepted as primary lifecycle proof.

Classification: `RELIABLE_METADATA_CANDIDATE / CORRECT_IDENTITY_AT_REGISTRY_LEVEL / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY`.

Exact GitHub code search by the distinctive full title returned zero independent files in this pass.

### Primary-source check

Official publication confirms date, number and title: 01.04.2025 No. 41-FZ, publication No. `0001202504010010` (44-page official PDF).

Current consolidated lifecycle / the amendment implied by the GitHub `status=amended` field was not independently resolved from a primary lifecycle card in this pass. Do not promote to `VERIFIED_CURRENT` from the registry flag.

Blockers: `GITHUB_FULL_TEXT_41-FZ_2025 = OPEN`; `PRIMARY_CURRENT_LIFECYCLE_41-FZ = OPEN`.

## 3. Federal Law 24.06.2025 No. 156-FZ

Target from Habr general information / state information systems list: «О создании многофункционального сервиса обмена информацией и о внесении изменений в отдельные законодательные акты Российской Федерации».

### GitHub candidate

Same corpus file:

- repo: `shodenis/Russian-Law-MCP`
- commit: `bd5a0daca23c600c99e74874abf5b5cb840ef934`
- path: `data/census.json`
- size: `7,204,691 bytes`
- type: `JSON/blob`
- blob SHA: `39dcf0807698959aa4cf93ed134b5a81eecb29b3`
- record: `id=fz-156-2025`, `nd=604495947`, `identifier=156-ФЗ`
- title matches Habr and the official publication.
- repository field says `status=in_force`; this field is not accepted as primary lifecycle proof.

Classification: `RELIABLE_METADATA_CANDIDATE / CORRECT_IDENTITY_AT_REGISTRY_LEVEL / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY`.

Exact GitHub code search by the distinctive full title returned zero independent files in this pass.

### Primary-source check

Official publication confirms date, number and title: 24.06.2025 No. 156-FZ, publication No. `0001202506240021` (14-page official PDF).

No GitHub full-text body was confirmed in this pass. The census `in_force` flag is retained only as repository metadata, not as our legal-currentness determination.

Blocker: `GITHUB_FULL_TEXT_156-FZ_2025 = OPEN`.

## Gates reinforced

1. `CORPUS_GENERATED_AFTER_AMENDMENT != TITLE_FRESHNESS` — a 2026-generated registry may still retain a pre-amendment title.
2. `REGISTRY_STATUS_AMENDED/IN_FORCE != PRIMARY_LIFECYCLE_VERIFICATION`.
3. `EXACT_CODE_SEARCH_ZERO != PROOF_OF_GITHUB_ABSENCE`.
4. `OFFICIAL_REFERENCE_TO_CURRENT_TITLE > SECONDARY/HABR TITLE` for normalization, while the original title is retained as an alias for search/traceability.
