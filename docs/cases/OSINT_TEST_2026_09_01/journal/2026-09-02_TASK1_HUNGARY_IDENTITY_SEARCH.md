# Task 1 — Hungarian intermediary identity search

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Status: ACTIVE / unresolved

## J1-H001 — Exact supplier identity search
Queries included:
- `"TST PL" Hungary urea supplier 2025`
- `"TST PL" węgierska spółka mocznik 2025 nazwa`
- `"Technospetstrading" Hungary company urea`
- `"Technospetstrading" Węgry mocznik`
- exact contract dates `10 stycznia 2025` and `21 lutego 2025` with TECHNOSPETSTRADING / external payer terms.

Primary result:
- Official Polish TST PL sanction decision confirms an unnamed Hungarian entity became the main supplier from February 2025.
- Belarus-origin fertilizer was customs-cleared in Latvia with Hungary as declared destination/movement country.
- Hungarian company had a urea contract directly with TECHNOSPETSTRADING LLC.
- Contract allowed an external payer.
- 2025-01-10 contract involved an unnamed Latvian entity with TST PL acting as payer despite not being a party.
- 2025-02-21 TECHNOSPETSTRADING signed a direct contract with the unnamed Hungarian entity.

Status: FOUND-A for the structure; `NO-HIT` for the exact Hungarian legal entity name in indexed public sources during this pass.

## J1-H002 — Red Team
Do not infer the Hungarian company from fertilizer-sector candidates without an identifier. Required discriminators:
- invoice/contract copy;
- VAT ID / company registration number;
- EORI;
- bank account / payer details;
- customs declaration;
- CMR/CIM consignee;
- shipment date/weight matching TST PL import data.

## Next pivots
1. Search leaks/investigative attachments for the 2025-02-21 contract.
2. Search Latvian customs/media datasets for consignee listed as Hungary.
3. Search Hungarian company registry using director/shareholder/address pivots recovered from any invoice.
4. Compare CN 3102 intra-EU movements Latvia→Hungary→Poland around shipment dates.
