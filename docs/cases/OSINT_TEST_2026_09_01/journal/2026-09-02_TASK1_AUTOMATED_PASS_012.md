# Task 1 — Automated deep-dive pass 012

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / linked fertilizer-export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly observable in a primary/official/registry document or an exact-match negative check against such a source.
- `SOURCE_CLAIM` — claim made by an identified source and not independently adjudicated here.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — testable working theory.

Grades: `A` primary/official; `B` strong document-based secondary/registry mirror; `C` analytical lead; `D` weak/unverified.

## J1-A012-01 — Fert-Corporation: stable identifiers and registration timeline
Type: FACT / registry-derived + CACHE-VERSION CONFLICT
Grade: B+

Registry mirror Sheets.by, reproducing Belarus EGR/MNS data, identifies:
- company: ООО «Ферт-корпорэйшн» / Fert-Corporation;
- UNP: `193846088`;
- EGR registration: `26.02.2025`;
- MNS registration: `27.02.2025`;
- legal address: `Minsk, ul. Annaeva 69, isolated premises 17`;
- main activity: wholesale of other chemical products, OKED `46750`;
- public phone: `+375296687700`.

Source: https://sheets.by/unp/193846088

### Cache-version conflict / freshness handling
Two indexed snapshots of the same Sheets.by URL differ only in freshness: an older cached page states `status as of 26.12.2025: Active`, while a newer search snapshot states `status as of 26.04.2026: Active` and `updated 26.04.2026`. The newer snapshot is used as the best available status point, but it is still a secondary mirror and is not a current September-2026 official EGR extract. Direct access to the Belarus EGR page failed in this pass. Therefore the safe wording is: `Fert-Corporation was shown as Active as of 26.04.2026 in the newer registry-mirror snapshot`.

### Analytical value
This converts Fert-Corporation from a name-only investigative lead into a target with stable UNP, exact formation date, address, activity code and phone. The company was incorporated shortly after the December-2024 Polish sanctions against the earlier TST entities and before the spring/summer-2025 restructuring of the fertilizer-export chain described by BIC/KAS. Timing alone does not prove purpose or control.

### What this does NOT prove
- that Fert-Corporation remains active as of 02.09.2026;
- that Fert-Corporation exported any specific shipment;
- that it purchased from Grodno Azot;
- that Yuri Minich is currently the registered owner/director (the registry mirror page exposed in this pass does not display officers/participants);
- that the address is a production/warehouse site rather than an office;
- any relationship to other Annaeva 69 tenants solely from the shared building address.

### Next pivots
1. Direct EGR extract / historical registration package for UNP 193846088.
2. Founder/director history and charter capital.
3. Search exact phone `+375296687700` across contracts, ads, customs and corporate records.
4. Lease/title for isolated premises 17 at Annaeva 69.
5. Bank accounts, export license / special-exporter authorisation and customs declarations.

## J1-A012-02 — Yuri Minich forms a documented personnel/authority bridge among Fert-Corporation, TST and GrandGranit
Type: SOURCE_CLAIM
Grade: B

BIC's 15.07.2025 investigation states that:
- Fert-Corporation is owned and managed by `Yuri Minich`;
- Minich concurrently worked as a driver for TECHNOSPETSTRADING;
- he received salary from TECHNOSPETSTRADINGEXPORT in 2023;
- on `12.05.2025`, Nikita Ter-Minasov issued Minich a power of attorney to represent GrandGranit.

BIC article: https://investigatebel.org/ru/investigations/grodno-azot-sankcii-obhod-35-mln
Relevant embedded evidence files linked by the article:
- ownership/management exhibits: `/storage/page_blocks/July2025/311.jpg` and `/321.jpg`;
- power-of-attorney exhibit: `/storage/page_blocks/July2025/331.jpg`.

The web fetcher exposed the underlying image URLs but could not retrieve the image bytes in this run (`cache miss`), so the claims remain graded B rather than being upgraded from direct document inspection.

### INFERENCE / C
If the BIC exhibits are authentic as represented, Minich is not merely a nominally adjacent businessperson: the same individual would connect (1) Fert-Corporation ownership/management, (2) TST employment, (3) prior TSTExport payroll, and (4) formal authority to act for GrandGranit. This is a materially stronger network edge than shared address, nationality or publication adjacency.

### What this does NOT prove
- that Minich acted under the GrandGranit power of attorney in a specific transaction;
- that Armen Harutyunyan personally directed Minich;
- that Fert-Corporation and GrandGranit shared funds, bank accounts or shipments;
- any unlawful purpose.

### Next pivots
1. Recover/archive BIC image `331.jpg` and read issuer, scope, validity period and signature details.
2. Search GrandGranit contracts/customs filings signed by Minich after 12.05.2025.
3. Obtain Fert-Corporation founder/director extract and compare signatures/contact details.
4. Search TST/TSTExport HR/payroll references only in lawfully published material.

## J1-A012-03 — Current Polish national sanctions list: no exact Fert-Corporation/Minich identifier found
Type: FACT (negative exact-match check)
Grade: A for the scope of the check

Official current MSWiA sanctions-list page checked in this pass:
https://www.gov.pl/web/mswia/lista-osob-i-podmiotow-objetych-sankcjami

Exact-string checks returned no match for:
- `Fert` / `FERT`;
- `Minich`;
- `193846088`.

BIC had stated on 15.07.2025 that Fert-Corporation and GrandGranit were then able to deliver directly to Poland because they were not on sanctions lists. GrandGranit was subsequently placed on the Polish list on 06.08.2025, while this current exact-match check still does not identify Fert-Corporation or Minich.

Official GrandGranit notice for comparison:
https://www.gov.pl/web/kas/spolka-grandgranit-llc-z-wniosku-szefa-kas-zostala-wpisana-na-liste-sankcyjna

### What this does NOT prove
- that Fert-Corporation or Minich are unsanctioned in every jurisdiction;
- that no Polish entry exists under an unexpected alias/transliteration not searched here;
- that the company may lawfully handle any particular goods or transact with sanctioned counterparties;
- that a lack of entity-level listing eliminates transaction-level sanctions/customs restrictions.

### Next pivots
1. Check EU consolidated sanctions and other relevant jurisdictions by UNP/name/transliterations.
2. Monitor Polish MSWiA/KAS for a new application/decision against Fert-Corporation.
3. Search court docket for Fert-Corporation/Minich before any future public sanction notice.

## J1-A012-04 — Address/phone expansion: no corroborated second-level company edge yet
Type: FACT / NO-HIT
Grade: B

Searches on `+375296687700`, `193846088` and `Annaeva 69` did not produce a second entity sharing the exact Fert-Corporation phone or isolated premises 17. Other businesses appear at the broader building address Annaeva 69, but no additional independent basis connects them to Fert-Corporation, so no graph edges were created.

### Red Team rule
Do not connect companies solely because they occupy the same multi-tenant street address. A second basis is required: common phone/email/domain, owner/director, lease/landlord transaction, contract, bank details, shipment record or other operational evidence.

## Priority pivots from this pass
1. Direct Belarus EGR/history for UNP 193846088 and Yuri Minich.
2. Recover BIC `331.jpg` power of attorney and locate any instrument executed under it.
3. Search Fert-Corporation special-exporter authorisation, Grodno Azot contracts, invoices and customs declarations.
4. Search exact phone/UNP in CMR/CIM/SMGS/MRN and certificate repositories.
5. Maintain exact-match watch on Polish/EU sanctions registers.

No new reliable shipment-level MRN/CMR/CIM/SMGS, wagon number, French contact identity, Hungarian company identity or external payer was identified in this pass. No private relatives or ethnicity/nationality-based links were added.
