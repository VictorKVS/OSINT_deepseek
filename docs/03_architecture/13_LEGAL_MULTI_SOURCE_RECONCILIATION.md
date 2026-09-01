# Legal multi-source reconciliation

## Decision

Knowledge Factory must not treat one web page as the whole legal truth source. Legal documents are represented by a source bundle with distinct roles:

`publication evidence + government copy + authoritative consolidated reference(s)`.

## Roles

- `PUBLICATION_EVIDENCE` — A0/A1 evidence of official publication or official state placement. It answers: was this act officially issued/published and what was the published text/version?
- `GOVERNMENT_COPY` — A1 state-hosted downloadable/inspectable copy. It is preferred for exact-byte acquisition when the original publication channel is technically inaccessible or unsuitable for machine download.
- `CONSOLIDATED_REFERENCE` — A2 authoritative legal information system (for example GARANT or ConsultantPlus). It is used to reconcile current edition, amendment history and clause-level differences. It is not promoted to official publication evidence.
- `VERIFICATION_REFERENCE` — additional authoritative comparison source when needed.

## Acquisition and rights boundary

A0/A1 sources may be `AUTO_FETCH` or `OPERATOR_IMPORT` acquisition candidates subject to source policy, identity checks, exact bytes, SHA-256 and provenance.

A2 legal systems default to `VERIFY_ONLY`. Their pages may be referenced and compared within permitted access, but Knowledge Factory must not blindly mirror or republish their protected presentation/content. `VERIFY_ONLY` and `REFERENCE_ONLY` representations are never treated as acquired originals.

## Reconciliation

For each legal document:

1. establish publication evidence;
2. acquire one exact A0/A1 artifact when possible;
3. identify the artifact edition/version;
4. compare structural units against A2 consolidated references;
5. record amendment/version differences explicitly;
6. create `VERSION_DIFFERENCE` or `SOURCE_CONFLICT` candidates when texts or applicability differ;
7. require expert review before semantic promotion.

No majority vote converts disagreement into truth. Agreement across sources increases corroboration but does not erase provenance or legal status differences.

## PDn MVP

`config/pdn_source_bundles.json` is the first implementation seed. It currently covers:

- 152-FZ;
- PP 1119;
- FSTEC Order 21;
- FSB Order 378.

The legacy `config/pdn_official_documents.json` remains the D0-D5 acquisition execution registry until the bundle-aware acquisition planner is wired in. This separation prevents a schema migration from breaking the already tested exact-acquisition path.
