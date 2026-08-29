# Habr NPA sweep — Stream 1 — 2026-08-29 04:52 MSK

## Delta
- FULL_TEXT: +0
- RELIABLE_METADATA_CANDIDATE: +1
- GITHUB_FULL_TEXT_BLOCKER: +3
- EXACT_DUPLICATE: +0
- IDENTITY_CONFLICT: +0

## 5-ФЗ / 14.06.1994
Target: Федеральный закон от 14.06.1994 № 5-ФЗ «О порядке опубликования и вступления в силу федеральных конституционных законов, федеральных законов, актов палат Федерального Собрания».

Habr anchor: https://habr.com/ru/articles/432466/ — раздел «Основы законодательства».

GitHub candidate:
- repo: `shodenis/Russian-Law-MCP`
- commit: `bd5a0daca23c600c99e74874abf5b5cb840ef934`
- path: `data/census.json`
- size: `7204691` bytes
- type: `JSON/blob`
- blob: `39dcf0807698959aa4cf93ed134b5a81eecb29b3`
- record: `id=fz-5-1994`, `nd=102030627`, `identifier=5-ФЗ`, exact title, `law_type=federal_law`.

Assessment: `RELIABLE_METADATA_CANDIDATE / CORRECT_IDENTITY_AT_REGISTRY_LEVEL / SOURCE_POINTER / NOT_FULL_TEXT / NON_OFFICIAL_GITHUB_COPY`.

The repository field `status=in_force` is project metadata and is not accepted as primary official lifecycle evidence.

Primary official check: current `ips.pravo.gov.ru` document for `nd=102030627` verifies the exact identity and exposes the consolidated amendment chain through Federal Law of 01.05.2019 № 83-ФЗ. The GitHub registry record is not an official publication and does not contain the act body.

Blocker: standalone GitHub `FULL_TEXT` for 5-ФЗ/1994 is not confirmed.

## Next «Основы законодательства» blockers

### Указ Президента РФ от 23.05.1996 № 763
Exact GitHub code searches by full title and by date/number returned zero hits in this pass. Classification: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`. Direct primary official lifecycle card was not resolved in this pass.

### Постановление Правительства РФ от 13.08.1997 № 1009
Exact GitHub code search by the full title returned zero hits in this pass. Classification: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`. Direct primary official lifecycle card was not resolved in this pass.

## Gates
- `REGISTRY_IDENTITY_MATCH != FULL_TEXT`
- `PROJECT_STATUS_IN_FORCE != PRIMARY_OFFICIAL_LIFECYCLE`
- `EXACT_GITHUB_CODE_SEARCH_ZERO != PROOF_OF_ABSENCE`
