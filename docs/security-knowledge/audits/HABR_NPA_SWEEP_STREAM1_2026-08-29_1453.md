# Habr NPA sweep — Stream 1 — 2026-08-29 14:53 MSK

Scope: next unprocessed PDn/information acts from Habr 432466 and the user-maintained NPA queue. GitHub copies are treated only as non-official corpus artifacts. Legal identity/currentness are separate gates.

## Delta

- FULL_TEXT: +0
- RELIABLE_GITHUB_CANDIDATE: +0
- GITHUB_FULL_TEXT_BLOCKER: +5
- PRIMARY_INITIAL_PUBLICATION_CONFIRMED: +1 (Roskomnadzor Order No. 201/2022)
- PRIMARY_DIRECT_FETCH_BLOCKER: +4 (PP RF No. 857/2015; RKN Orders No. 84/2015 and No. 85/2015; PP RF No. 940/2012)
- EXACT_DUPLICATE: +0
- BODY_IDENTITY_CONFLICT: +0

## New checked targets

### PP RF 19.08.2015 No. 857
Title: `Об автоматизированной информационной системе «Реестр нарушителей прав субъектов персональных данных»`.

GitHub exact code search: `total_count=0`, `incomplete_results=false`. Semantic GitHub search also returned no reproducible artifact. Tree/path traversal of `VictorKVS/gpt-agent` at commit `ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8` confirmed that the Roskomnadzor directory contains only the previously registered binary PP RF 16.03.2009 candidate and does not add No. 857.

File metadata: `repo=null, commit=null, path=null, size=null, type=null`.
Classification: `GITHUB_FULL_TEXT_BLOCKER / EXACT_SEARCH_ZERO_NOT_PROOF_OF_ABSENCE`.

Habr identity matches date/number/title. A Government URL `government.ru/docs/all/103104/` is identifiable, but direct primary fetch timed out in this pass. Secondary legal corpora consistently show amendment by PP RF 13.11.2019 No. 1443; because the primary amendment card was not directly resolved here, current lifecycle remains `PRIMARY_CURRENT_LIFECYCLE_UNRESOLVED`.

### Roskomnadzor Order 22.07.2015 No. 84
Title: `Об утверждении Порядка взаимодействия оператора реестра нарушителей прав субъектов персональных данных с провайдером хостинга и Порядка получения доступа к информации, содержащейся в реестре нарушителей прав субъектов персональных данных, оператором связи`.

GitHub exact code search: `total_count=0`, `incomplete_results=false`; semantic search also returned no reproducible artifact.

File metadata: `repo=null, commit=null, path=null, size=null, type=null`.
Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Habr identity and Minjust registration No. 38532 are corroborated by legal-publication mirrors, but no direct primary current-lifecycle card was resolved in this pass: `PRIMARY_DIRECT_CARD_UNRESOLVED`.

### Roskomnadzor Order 22.07.2015 No. 85
Title: `Об утверждении формы заявления субъекта персональных данных о принятии мер по ограничению доступа к информации, обрабатываемой с нарушением законодательства Российской Федерации в области персональных данных`.

GitHub exact code search: `total_count=0`, `incomplete_results=false`.

File metadata: `repo=null, commit=null, path=null, size=null, type=null`.
Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Habr identity and Minjust registration No. 38544 are corroborated by publication mirrors. Direct primary current-lifecycle remains unresolved: `PRIMARY_DIRECT_CARD_UNRESOLVED`.

### PP RF 18.09.2012 No. 940
Title: `Об утверждении Правил согласования проектов решений ассоциаций, союзов и иных объединений операторов об определении дополнительных угроз безопасности персональных данных ... с ФСБ России и ФСТЭК России`.

Important normalization: canonical date is **18.09.2012**, not 21.09.2012. Habr carries the correct date.

GitHub exact code search by number and characteristic title fragment: `total_count=0`, `incomplete_results=false`.

File metadata: `repo=null, commit=null, path=null, size=null, type=null`.
Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Secondary current legal corpora label the unchanged 18.09.2012 edition as acting, but no direct primary lifecycle card was resolved, so no `VERIFIED_CURRENT` flag is assigned.

### Roskomnadzor Order 15.12.2022 No. 201
Title: `Об обработке персональных данных в Федеральной службе по надзору в сфере связи, информационных технологий и массовых коммуникаций`.

GitHub exact code search: `total_count=0`, `incomplete_results=false`; semantic search also returned no reproducible artifact.

File metadata: `repo=null, commit=null, path=null, size=null, type=null`.
Classification: `GITHUB_FULL_TEXT_BLOCKER`.

Primary official publication directly confirmed: registered 19.05.2023 No. 73374; official publication No. `0001202305220004` dated 22.05.2023. The act has nine approved annexes; a future GitHub artifact missing any required annex must not be classified `FULL_TEXT`. Full current lifecycle after initial publication remains a separate gate.

## Gates reinforced

1. `EXACT_CODE_SEARCH_ZERO + SEMANTIC_SEARCH_ZERO != PROOF_OF_GITHUB_ABSENCE`.
2. `NO_REPRODUCIBLE_ARTIFACT => repo/commit/path/size/type remain NULL`.
3. `INITIAL_OFFICIAL_PUBLICATION != VERIFIED_CURRENT_LIFECYCLE`.
4. `ACT_WITH_MULTIPLE_APPROVED_ANNEXES => FULL_TEXT requires the complete normative package, not only the order header/body`.
5. Date normalization is part of identity verification before searching (`PP 940 = 18.09.2012`).
