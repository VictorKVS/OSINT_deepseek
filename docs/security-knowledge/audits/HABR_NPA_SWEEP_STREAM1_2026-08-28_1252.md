# Habr NPA sweep — Stream 1 — 2026-08-28 12:52 MSK

## Delta

- FULL_TEXT: +1
- Reliable format sibling candidate: +1
- Rejected secondary/identity-conflict candidate: +1
- Exact duplicates: 0

## Confirmed new finding: PP RF 21.03.2012 No. 211

Target: Постановление Правительства РФ от 21.03.2012 N 211 «Об утверждении перечня мер, направленных на обеспечение выполнения обязанностей, предусмотренных Федеральным законом "О персональных данных" и принятыми в соответствии с ним нормативными правовыми актами, операторами, являющимися государственными или муниципальными органами».

GitHub source:
- repo: VictorKVS/gpt-agent
- ref/commit: ef8b02c1e0e997e028efc1dd2f3d30dc7e1cdce8
- TXT path: дОКУМЕНТЫ ЗАГРУЖАЕМЫЕ В АГЕНТ/ПП Р Ф 2103 2012 г  N  211 Об утверждении перечня мер/Постановление Правительства РФ от 21 марта 2012 г. N 211 Об утверждении перечня мер .txt
- size: 16085 bytes
- type: TXT/blob
- blob SHA: e35cb53ce9a8995306eb99206b0759c8c19b6d79
- PDF sibling: Постановление Правительства РФ от 21 марта 2012 г N 211 Об утверждении перечня м (1).pdf
- PDF size: 94885 bytes
- PDF blob SHA: 61214187c156b729ae6bf69b51ce72870ebb3cbf

Body verification:
- body identifies Government of the Russian Federation, date 21 March 2012, No. 211 and matching title;
- operative part and attached list of measures are present;
- amendments listed: 20.07.2013, 06.09.2014, 15.04.2019;
- source footer identifies GARANT export dated 22.11.2024.

Classification:
FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / GARANT_EXPORT / REVISION_THROUGH_15.04.2019 / PRIMARY_OFFICIAL_LIFECYCLE_PENDING.

The PDF is only a format sibling candidate until binary-body verification is completed.

## Rejected candidate: Federal Law No. 160-FZ ratifying Convention 108

Repo: ShinyZero0/dstu-hack-2025-spring
Commit: 1faa7cf3b468260271919c77c72006ed5e2df47f
Path: ml_module/laws_prompts/law_6.txt

The file is an educational/prose summary of Convention 108, not the law text. It also states an inconsistent ratification date (27.07.2006) for No. 160-FZ; the target act is Federal Law of 19.12.2005 No. 160-FZ.

Classification:
SECONDARY_SUMMARY / WRONG_LAW_DATE / MENTION_ONLY / REJECT_FOR_PRIMARY_KB.

## New regression gate

`LAW_NUMBER_MATCH != LEGAL_IDENTITY` and `SUMMARY_WITH_LAW_REFERENCE != FULL_TEXT`.
A candidate must pass body-level checks for act type, issuing authority, exact date, number, title and normative structure before entering the primary-law layer.

## Open blockers from this pass

- Primary official lifecycle/currentness resolution for PP RF No. 211 remains pending because the primary official card was not reliably resolved in this pass.
- Standalone full GitHub copy of Federal Law 19.12.2005 No. 160-FZ remains pending.
