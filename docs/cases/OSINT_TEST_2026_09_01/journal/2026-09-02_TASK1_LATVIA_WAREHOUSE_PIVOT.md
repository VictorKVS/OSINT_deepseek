# Task 1 — Latvia warehouse/logistics pivot

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Status: ACTIVE

## J1-L011 — Astramar Liepāja direct TST contract lead
Source:
- LSM / Latvijas Televīzija De facto:
  https://www.lsm.lv/raksts/zinas/latvija/22.06.2025-de-facto-peta-sankciju-apiesanas-shemas-baltkrievu-karbamids-plust-eiropa-caur-latviju.a604247/

Result:
- De facto reports Astramar Liepāja contracted with TECHNOSPETSTRADING for urea in early 2025.
- Director Viesturs Andersons told journalists he received invoices/origin documentation and a payment order.
- Andersons said the request to help send the cargo came from an acquaintance in France.
- The French person/entity is not named in the published article.
Status: FOUND-B.
Next pivots: contract, invoice, vessel/port, French requester, consignee, payment origin.

## J1-L012 — Astramar physical logistics capability
Primary corporate source:
- https://www.astramarliepaja.lv/

Result:
- Astramar Liepāja publicly advertises ship agency, chartering, cargo forwarding, stevedoring, storage, bulk cargo handling and rail/road/sea logistics.
- Address: Bāriņu iela 7, Liepāja, LV-3401.
Status: FOUND-A for self-declared services.
Caveat: capability does not prove use of each service for the TST cargo.

## J1-L013 — Apeks serviss carried fertilizer from same Belarus supplier
Source:
- LSM / De facto.
Result:
- Journalists report Daugavpils company Apeks serviss also carried fertilizer from the same Belarusian TECHNOSPETSTRADING supplier.
- Apeks representatives declined comment.
Status: FOUND-B.

## J1-L014 — Apeks serviss customs warehouse
Sources:
- Latvian company/register aggregators
- Latvian Food and Veterinary Service public register

Result:
- SIA Apeks serviss, reg. no. 41503055853.
- Address: Spaļu iela 1P, Daugavpils, LV-5404.
- Main activity: warehousing/storage.
- Public register lists structural unit `MUITAS NOLIKTAVA 'APEKS SERVISS'` at Spaļu iela 1P.
- Latvia FVS lists Apeks serviss at same address as a feed-transshipment point in a customs warehouse, authorized for feed import/export with third countries.
Status: FOUND-A/B.
Analytical value: this is a real customs/rail logistics node, not merely a mailbox address.

## J1-L015 — Same Daugavpils warehouse advertised by Lithuanian TPC/LOGITRA
Primary corporate source:
- https://logitra.lt/en/kontaktai/

Result:
- UAB Tranzito paslaugų centras (TPC) / LOGITRA publicly lists `Warehouse in Daugavpils (Latvia), railway loading works` at exactly `Spalu iela 1p, Daugpilis`.
- TPC network also lists:
  - Klaipėda customs warehouse with railway loading;
  - customs brokers;
  - railway transport;
  - a dedicated certificates-of-origin service.
Status: FOUND-A for public infrastructure claims.
Critical caveat: NO evidence yet that TPC/LOGITRA handled the specific TECHNOSPETSTRADING fertilizer cargo or altered certificates/labels.

## J1-L016 — Historical TPC ↔ Apeks operational relationship
Secondary legal source found in Lithuanian court reporting:
- a separate, unrelated commodity transit case records cargo routed from Klaipėda to SIA Apeks Serviss in Daugavpils via UAB Tranzito paslaugų centras.
Result:
- supports that TPC ↔ Apeks is a real operational logistics relationship, not only same-address website duplication.
Status: FOUND-B.
Caveat: case concerns different goods and earlier period; not evidence regarding fertilizer or misconduct.

## J1-L017 — Why Spaļu iela 1P matters
Evidence-based node model:

```text
TECHNOSPETSTRADING
   ↓ reported by LSM
APEKS SERVISS
   ↓
Spaļu iela 1P, Daugavpils
   ├─ customs warehouse
   ├─ railway loading capability
   ├─ import/export / transit infrastructure
   └─ same warehouse address publicly used by TPC/LOGITRA
                ↓
        TPC network includes Klaipėda customs/rail node
        and origin-certificate services
```

Status: FACTS + INFERENCE.
Do not create an edge `TPC HANDLED TST FERTILIZER` until a CMR/CIM/customs declaration/contract confirms it.

## J1-L018 — Physical relabeling hypothesis re-tested
Search focus:
- repacking, bagging, labels, big-bags, warehouse handling, certificates, origin docs.
Result:
- no reliable public evidence of physical relabeling/rebagging found.
- documentary presentation of origin/producer remains the stronger evidence track.
Status: NO-HIT for physical relabeling.

## Priority next pivots
1. Recover TST ↔ Astramar contract/invoice and identify French requester/end buyer.
2. Recover TST ↔ Apeks CMR/CIM/customs declaration.
3. Determine whether Apeks or TPC was customs declarant under procedure 42.
4. Identify wagon numbers and route Grodno → Daugavpils/Liepāja → Hungary/other EU state.
5. Compare certificate-of-origin issuer, producer name, batch number, packaging and weights at each border/document stage.
6. Identify the Hungarian company and external payer from 2025 contracts.
