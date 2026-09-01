# Task 1 logistics deep-dive — search journal

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Result codes
- FOUND-A — primary/official evidence
- FOUND-B — strong secondary/document-based source
- FOUND-C — hypothesis / analytical inference
- NO-HIT — no reliable result
- BLOCKED — source unavailable
- CONFLICT — sources disagree

## J1-L001 — GrandGranit production/storage node
Queries:
- `GrandGranit magazyn hala Mińsk nawozy`
- `GrandGranit warehouse Minsk fertilizer equipment`
- `GrandGranit Grodno Azot warehouse`

Primary sources:
- KAS/MSWiA GrandGranit notice and decision
  - https://www.gov.pl/web/kas/spolka-grandgranit-llc-z-wniosku-szefa-kas-zostala-wpisana-na-liste-sankcyjna
  - https://www.gov.pl/attachment/63c420a4-5fdb-4a6f-8d3c-759ccef05c89

Results:
- GrandGranit LLC, reg. no. 191768505.
- Official address: Belarus, 220070 Minsk, Radialnaya 11B, room 7B, office 6.
- Since March 2025 GrandGranit rented a small warehouse/production hall near Minsk.
- The hall lacked external industrial-scale fertilizer infrastructure such as pipelines or external tanks.
- GrandGranit had equipment intended by the manufacturer for preparing liquid multi-component fertilizers for farms.
- GrandGranit itself indicated production occurred on the Grodno Azot site, Kosmonautov 100, Grodno.
- GrandGranit used Grodno Azot infrastructure.
- Goods imported to Poland were dispatched from Grodno.
Status: FOUND-A.
Pitfall: legal address != rented hall. Exact rented-hall address is not disclosed in the public decision.
Next pivot: identify lease contract, landlord, exact property, photos/satellite image, equipment model.

## J1-L002 — Direct contracts anchoring GrandGranit to Grodno Azot
Primary source:
- TST PL MSWiA decision dated 2025-10-09
  - https://www.gov.pl/attachment/24038b12-876c-4991-8b93-5d7ea1e716ea

Results:
- GrandGranit had direct contracts with Grodno Azot for equipment lease and raw-material supply.
- GrandGranit had a contract with AzotSpetstrans, a Grodno Azot subsidiary, for transport services on the Grodno Azot site.
- The decision states GrandGranit used Grodno Azot installations, equipment, products/raw materials and transport resources.
Status: FOUND-A.
Analytical implication: change of exporter did not correspond to a comparable change in the physical production/logistics core.

## J1-L003 — Claimed own production vs actual producer
Primary source:
- TST PL MSWiA decision, pages 4–5.

Result:
- Polish authorities state TECHNOSPETSTRADING LLC, TECHNOSPETSTRADINGEXPORT LLC, WORLD CHEM, GrandGranit and analogous exporters presented fertilizer as originating from their own production while KAS assessed the actual producer as Grodno Azot.
Status: FOUND-A for the official position.
Important distinction:
- Evidence supports documentary presentation of another exporter/producer.
- No public evidence in this pass proves physical replacement of bag labels, stickers or packaging.
Next pivot:
- obtain bag/big-bag photos;
- certificates of origin/quality;
- batch numbers;
- CIM/CMR;
- customs declarations;
- warehouse packing/filling acts.

## J1-L004 — Turkmenistan raw-material claim
Primary source:
- GrandGranit MSWiA decision.

Result:
- GrandGranit claimed sourcing raw materials from Turkmenistan.
- KAS regarded this explanation as not credible in context of the company’s real infrastructure and simultaneous use of Grodno Azot resources.
Status: FOUND-A for KAS position.
Do not state that Turkmenistan origin is disproved independently without underlying import records.

## J1-L005 — 2025 Latvia/Hungary restructuring
Primary source:
- TST PL MSWiA decision.

Results:
- From February 2025 the main supplier of TST PL became a Hungarian entity.
- Belarus-origin fertilizer was customs-cleared in Latvia, with Hungary declared as destination/movement country.
- Hungarian company had a urea supply agreement directly with TECHNOSPETSTRADING LLC.
- Agreement allowed an external payer.
- 2025-01-10: contract with a Latvian entity where TST PL was payer despite not being a party to the contract; goods continued to the Hungarian company.
- 2025-02-21: TECHNOSPETSTRADING LLC signed direct contract with Hungarian entity, again with external-payer clause.
Status: FOUND-A.
Analytical implication: after sanctions, seller / contractual party / payer / customs country / declared destination became separated.
Next pivot: identify Latvian company, Hungarian company, external payer, VAT/EORI numbers, bank accounts, final consignee.

## J1-L006 — Customs procedure 42
Sources:
- official Polish decision/search-indexed text.
Result:
- public decision materials describe Latvia import using customs procedure 42 in the relevant flow.
- Procedure 42 itself is a lawful EU customs/VAT mechanism for import into one Member State followed by intra-EU supply/movement to another.
Status: FOUND-A/B depending on exact sub-document.
Analytical rule: procedure 42 is not adverse by itself; relevant questions are origin, producer, importer, VAT/EORI identities, payer, destination and sanctions applicability.

## J1-L007 — OCCRP/BIC Latvia rail corridor
Secondary source:
- https://www.occrp.org/en/news/belarusian-state-fertilizer-company-dodges-eu-sanctions-leaked-documents-show

Results:
- OCCRP/BIC report renewed Belarus fertilizer rail flow into Latvia in 2025.
- One invoice showed TECHNOSPETSTRADING shipment to Hungary via Latvia.
- Investigative materials referenced at least 278 railcars in the broader Belarus-fertilizer flow into Latvia.
Status: FOUND-B.
Pitfall: 278 railcars is a broader flow and must not be attributed entirely to TECHNOSPETSTRADING.

## J1-L008 — Physical relabeling / repackaging search
Queries:
- `TECHNOSPETSTRADING relabel fertilizer`
- `Техноспецтрейдинг маркировка удобрения`
- `GrandGranit packaging fertilizer Grodno Azot`
- Polish terms for labels/repacking/certificates.
Result:
- No reliable public source found proving physical replacement of labels, sacks, big-bags or packaging at the Minsk-area hall or elsewhere.
Status: NO-HIT.
Current conclusion:
- documentary change of represented exporter/producer: supported by official Polish material;
- physical relabeling/repackaging: unproven hypothesis.

## J1-L009 — Physical node model
Derived from FOUND-A evidence:

```text
GRODNO AZOT, Kosmonautov 100, Grodno
  ├─ industrial production
  ├─ equipment/raw-material contracts
  ├─ AzotSpetstrans internal transport
  └─ rail dispatch from Grodno
       ↓
TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / GrandGranit
       ↓
Latvia customs node → Hungary → TST PL / EU
```

Parallel auxiliary node:
```text
GrandGranit small rented hall near Minsk
  └─ equipment for liquid multi-component fertilizer preparation
```

Status: FOUND-A + INFERENCE.
Interpretation: legal/auxiliary facilities and actual industrial production node are different layers of the network.

## J1-L010 — Google Docs package update
Updated/created:
- Appendix 6 — deep corporate/logistics analysis.
- Appendix 7 — supply routes, production/storage nodes, route changes.
- Source registry entries for official TST PL and GrandGranit decisions plus OCCRP.
- Task 1 package index updated with Appendices 6 and 7.
Status: FOUND-A / DOCUMENTED.

## Priority pivots
1. Exact address and landlord of GrandGranit rented hall near Minsk.
2. Equipment make/model and capacity at that hall.
3. GrandGranit ↔ Grodno Azot equipment lease and raw-material contracts.
4. GrandGranit ↔ AzotSpetstrans transport contract.
5. Latvian entity from 2025-01-10 contract.
6. Hungarian entity from 2025-02-21 contract.
7. External payer identity and bank/payment path.
8. Latvia customs declarations under procedure 42, EORI/VAT IDs, customs representative.
9. CIM/CMR, wagon numbers, batch numbers, certificates of origin/quality.
10. Packaging/label imagery before and after shipment to test physical relabeling hypothesis.
