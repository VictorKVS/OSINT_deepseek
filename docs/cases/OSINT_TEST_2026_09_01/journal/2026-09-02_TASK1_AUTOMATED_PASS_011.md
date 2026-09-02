# Task 1 — Automated deep-dive pass 011

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: Armen Seryozhaevich Harutyunyan / TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / linked fertilizer-export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly observable in a primary/official/registry/court document.
- `SOURCE_CLAIM` — claim made by an identified source, not independently adjudicated here.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — testable working theory.

Grades: `A` primary/official; `B` strong document-based secondary/self-published operational evidence; `C` analytical lead; `D` weak/unverified.

## J1-A011-01 — Armen Harutyunyan: WSA procedurally rejected the sanctions complaint
Type: FACT
Grade: A

Court source: WSA Warszawa / NSA judgments database mirror.
Case: `V SA/Wa 3613/25`
Order date: `30.01.2026`
Subject: complaint against the MSWiA decision on entry to the sanctions list, decision `DPP-WTPZ.0272.112.2025.BS(2)`.
Result shown by the court database: `odrzucenie skargi` / complaint rejected.
Source: https://www.orzeczenia-nsa.pl/postanowienie/v-sa-wa-3613-25/odrzucenie_skargi/23e2c06.html

### Red Team / what this does NOT prove
Polish `odrzucenie skargi` is a procedural rejection and must not be rewritten as `oddalenie skargi` (dismissal on the merits). This order does not, by itself, mean that the WSA judicially confirmed the factual allegations in the sanctions decision. The currently indexed record does not expose the reason for the procedural rejection, finality or a later NSA remedy.

### Next pivots
1. Full text / uzasadnienie of `V SA/Wa 3613/25`.
2. Prawomocność/finality marker.
3. Any zażalenie / NSA follow-up.

## J1-A011-02 — TST PL: WSA procedurally rejected the sanctions complaint
Type: FACT
Grade: A

Court source: WSA Warszawa / NSA judgments database mirror.
Case: `V SA/Wa 3682/25`
Order date: `10.03.2026`
Subject: complaint against MSWiA decision `DPP-WTPZ.0272.113.2025.BS(2)` concerning TST PL.
Result shown by the court database: `odrzucenie skargi`.
Source: https://www.orzeczenia-nsa.pl/postanowienie/v-sa-wa-3682-25/odrzucenie_skargi/19126b5.html

### Red Team / what this does NOT prove
This is procedural rejection, not a merits judgment on KAS/MSWiA factual findings. The reason for rejection and any later appeal/finality are not established in this pass.

### Next pivots
1. Full reasoning and finality status.
2. Search NSA/zażalenie by case number and decision number.

## J1-A011-03 — GrandGranit self-published exact production-facility address; direct conflict with Polish sanction status
Type: SOURCE_CLAIM + CONFLICT
Grade: B for the company self-description; A for the contradictory Polish sanction record

GrandGranit's current corporate website identifies the same entity by `UNP 191768505` and states that it leased a `1,441 m²` production facility at:
`Minsk Region, Dzerzhinsky District, Fanipol Rural Council, 37-4, near Fanipol`.
It says the facility is used for UAN/AUS32 production and that full-scale production began on `May 14` (the page does not explicitly state the year in that sentence).
Source: https://grandgranit.net/homeeng/

The same live page states: `Our company is not subject to sanctions and does not cooperate with any sanctioned entities.`

Official Polish KAS/MSWiA material states that GrandGranit LLC was entered on the Polish national sanctions list by decision of `06.08.2025`; the KAS publication is dated `07.08.2025`.
Official source: https://www.gov.pl/web/kas/spolka-grandgranit-llc-z-wniosku-szefa-kas-zostala-wpisana-na-liste-sankcyjna

### Analytical value
The website likely identifies the previously unresolved `small warehouse/production hall near Minsk` physical pivot with a concrete site address. This is a high-value target for property/lease, equipment, transport and satellite/photo verification.

The sanctions statement on the current website is in direct conflict with the official Polish record and must be preserved as a dated contradiction rather than normalized away.

### What this does NOT prove
- that the Fanipol 37-4 facility is definitively the exact hall described by KAS; that requires a lease/property document or another independent identifier;
- that the facility produced the 1,300 t imported to Poland;
- that it is technically capable of industrial-scale urea production;
- when the website text was first published or last edited;
- whether the website's `not subject to sanctions` wording is intended to refer only to a jurisdiction other than Poland.

### Next pivots
1. Property/lease records for Fanipol Rural Council `37-4`.
2. Owner/lessor and other tenants at the site.
3. Site plan, photographs, satellite imagery, permits and equipment list.
4. Web-archive/version history to date the sanctions disclaimer.
5. Match the address against KAS's underlying lease evidence.

## J1-A011-04 — Official GrandGranit volume: 1,300 t from June 2025 + contractual AzotSpetstrans transport at Grodno Azot
Type: SOURCE_CLAIM
Grade: A (official MSWiA/KAS decisions as to the authority's findings)

Official GrandGranit decision states that imports into Poland began in `June 2025`, declaring urea/ammonium-nitrate mixture in a volume of `1,300 tonnes`.
Source: https://www.gov.pl/attachment/9165f701-2b73-427c-b395-1ac305c0218e

Official TST PL decision states that GrandGranit:
- had direct contracts with Grodno Azot for equipment lease and raw-material supply;
- had a contract with `AzotSpetstrans` (described as a Grodno Azot subsidiary) for transport services on Grodno Azot plant territory;
- used Grodno Azot infrastructure;
- had goods imported to Poland dispatched from Grodno.
Source: https://www.gov.pl/attachment/24038b12-876c-4991-8b93-5d7ea1e716ea

### Supporting operational rail evidence
A 2026 procurement record names `Transport Unitary Enterprise AzotSpetstrans` as customer for capital overhaul/modernization of locomotive `ТЭМ2У-9183`, demonstrating maintained shunting-rail assets. Secondary procurement source: https://zakupki.kontur.ru/SNG4979708

This strengthens the physical rail pivot but is not shipment-level proof.

### INFERENCE / C
The combination `GrandGranit contract → AzotSpetstrans transport inside Grodno Azot → 1,300 t June-2025 import → dispatch from Grodno` gives a sharply bounded cargo-tracing target. Instead of searching the entire 2025 flow, reconstruct the June 2025 1,300 t as a finite set of declarations / train consignments and match weight, dates, wagon/cistern identifiers and consignee.

### What this does NOT prove
- exact number of customs declarations or trains;
- wagon numbers;
- that every tonne was produced by Grodno Azot as a judicially adjudicated fact (the underlying producer conclusion is the administrative authority's finding);
- that the cited locomotive hauled any GrandGranit consignment.

### Next pivots
1. June 2025 declarations totaling ~1,300 t.
2. GrandGranit↔AzotSpetstrans contract number/date.
3. Plant shunting lists, dispatch records and station/Auls records.
4. SMGS/CIM, wagon/cistern numbers, exact Polish consignee and unloading point.

## J1-A011-05 — GrandGranit publishes quality-certificate templates exposing shipment-level schema
Type: FACT / SOURCE_CLAIM
Grade: B

The current GrandGranit website exposes one-page `SAMPLE` quality-certificate templates for UAN-32, UAN-34, UAM+M and AUS32. They identify GrandGranit LLC, UNP `191768505`, and technical-standard identifiers including:
- `TU/TS BY 191768505.003-2025` — UAN-32;
- `TU/TS BY 191768505.002-2025` — UAN-34.

The templates contain shipment fields for `Contract`, `Invoice`, `Cisterns` or `Wagons`, `Date of manufacture`, `Lot`, mode of transport/packaging and net weight. In the published documents these shipment identifiers are blank because the files are explicitly marked `ОБРАЗЕЦ / SAMPLE`.

Sources:
- https://grandgranit.net/wp-content/uploads/2025/05/%D0%9F%D0%B0%D1%81%D0%BF%D0%BE%D1%80%D1%82-%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%B0-%D0%9A%D0%90%D0%A1-32_%D0%BA%D0%BE%D1%80%D1%80.-%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%B5%D1%86_watermark.pdf
- https://grandgranit.net/wp-content/uploads/2025/05/%D0%9F%D0%B0%D1%81%D0%BF%D0%BE%D1%80%D1%82-%D0%BA%D0%B0%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%B0-%D0%9A%D0%90%D0%A1-34_%D0%BA%D0%BE%D1%80%D1%80.-%D0%BE%D0%B1%D1%80%D0%B0%D0%B7%D0%B5%D1%86_watermark.pdf
- https://grandgranit.net/wp-content/uploads/2025/07/%D0%A1.%D0%9A-%D0%BD%D0%B0-AUS32_%D0%BA%D0%BE%D1%80%D1%80.-1_watermark.pdf

### Analytical value
These templates provide exact field names and document layout to use when searching leaked/indexed shipment certificates and comparing them to customs/rail records. They are a new schema-level pivot for cargo fingerprinting.

### What this does NOT prove
- any actual shipment, lot, wagon, cistern, invoice or consignee;
- authenticity of a future filled certificate merely because it matches the template.

### Next pivot
Search by exact standard IDs + file-name patterns + `GrandGranit` + lot/invoice/wagon fields, then cross-match any filled certificate against June-2025 1,300 t customs/rail records.

## Searches with no reliable new hit
No reliable public hit in this pass identified:
- the unnamed French contact behind the Astramar request;
- the unnamed Hungarian company and external payer;
- shipment-level MRN/CMR/CIM/SMGS for the Astramar 22 t lot;
- new material Sergei Teterin involvement in the fertilizer-export chain;
- a confirmed NSA follow-up/finality record for the two newly found WSA procedural orders.

No entity was linked solely by surname, nationality/ethnicity, shared address without corroboration, or adjacency in a publication.
