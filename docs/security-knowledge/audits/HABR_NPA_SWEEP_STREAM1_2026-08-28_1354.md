# Habr NPA Sweep — Stream 1 — 2026-08-28 13:54 MSK

Delta: FULL_TEXT +2; exact duplicates +0; path/date conflicts +1.

## 1. Постановление Правительства РФ от 15.09.2008 №687

- repo: `MobileCommerceLab/privacy_law_corpus`
- commit/ref: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Decree of the Government of 15 December 2008 No. 687 on Approving the Provision Regarding Properties of Personal Data Processing without Software).txt`
- size: `72800` bytes
- type: `TXT`
- blob: `d75270aeb0e5291a9f77e53783c1541510b7139c`
- body identity: verified — Government of the Russian Federation, 15.09.2008, No. 687; normative parent act plus attached Regulation are present.
- conflict: filename says `15 December 2008`; body and official Government source say `15 September 2008`.
- currentness: Government Resolution No. 12 of 18.01.2025 amends No. 687; the GitHub text does not contain that 2025 amendment marker.
- status: `FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / PATH_DATE_CONFLICT / STALE_BEFORE_PP12_2025`.

## 2. Постановление Правительства РФ от 06.07.2008 №512

- repo: `MobileCommerceLab/privacy_law_corpus`
- commit/ref: `1d791bb64741f86f8cc160485dc005230f720042`
- path: `corpus_documents/plain_text_files/non_english_text_files/Russia (Decree of the Government of 6 July 2008 No. 512 on Approving the Requirements to Biometric Personal Data Tangible Carrier and such Data Storage Outside of Personal Data Information Systems).txt`
- size: `37978` bytes
- type: `TXT`
- blob: `6c15cbb6726e9815e160e9acb6061b38381ddb4c`
- body identity: verified — Government of the Russian Federation, 06.07.2008, No. 512; operative part plus attached Requirements are present.
- revision evidence in body: explicitly contains `В редакции Постановления Правительства Российской Федерации от 27.12.2012 г. N 1404` and the corresponding amended clauses.
- currentness: current legal-reference cards checked in this pass show edition 27.12.2012; no later amendment was established in this pass. Primary official lifecycle of the old 2008 parent act was not fully resolved.
- status: `FULL_TEXT / NON_OFFICIAL_GITHUB_COPY / REVISION_INCLUDES_PP1404_2012 / CURRENT_CANDIDATE / PRIMARY_OFFICIAL_LIFECYCLE_PENDING`.

## New regression gate

`PATH_DATE_METADATA != BODY_IDENTITY`.

A date encoded in a GitHub filename must never override the legal identity established from the normative body and a primary official source. Canonical identity remains based on act type + issuing authority + exact date + number + normalized title/body identity.
