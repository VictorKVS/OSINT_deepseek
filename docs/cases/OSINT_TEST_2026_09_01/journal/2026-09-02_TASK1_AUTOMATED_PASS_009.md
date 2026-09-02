# Task 1 — Automated deep-dive pass 009

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / linked fertilizer-export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly observable in a primary/registry/contract document.
- `SOURCE_CLAIM` — claim made by an identified source, not independently adjudicated here.
- `INFERENCE` — analytical conclusion derived from established facts.
- `HYPOTHESIS` — testable working theory.

Grades: `A` primary/official; `B` strong document-based secondary; `C` analytical lead; `D` weak/unverified.

## J1-A009-01 — Primary TST ↔ Astramar contract recovered
Type: FACT / SOURCE_CLAIM
Evidence: B+/A- for the visible contract copy; provenance is BIC publication rather than certified registry/court copy.

BIC publishes images of Specification No. 1 to Contract No. `10.01/25-UR-DAP`, dated `10.01.2025`, Minsk.

Visible terms:
- Seller: TECHNOSPETSTRADING LLC, reg. no. `193256472`.
- Buyer: `ASTRAMAR LIEPĀJA K.A.` SIA, VAT `LV42103016440`.
- Goods: urea grade A / carbamide prilled A, HS `3102101000`.
- Quantity: `22 t` (+/-10%).
- Price: `343 EUR/t`.
- Total: `7,546 EUR`.
- Terms: DAP `Brīvostas iela 21, Liepāja, LV-3405, Latvia`.
- Recipient address: `7 Bāriņu str., Liepāja, Latvia`.
- Packing: 1000 kg big-bags.
- Delivery by road under Incoterms 2010.
- Payment term: 100% within 60 calendar days from invoice / delivery terms as specified in the document.

Sources:
- https://investigatebel.org/ru/investigations/grodno-azot-sankcii-es-shema
- https://investigatebel.org/storage/page_blocks/June2025/593.jpg
- https://investigatebel.org/storage/page_blocks/June2025/601.jpg

What this does NOT prove:
- that payment was actually made;
- that this 22 t lot is the same cargo described in the Polish Hungary/procedure-42 chain;
- which truck/rail wagon carried it;
- whether the goods were physically relabelled/repacked;
- the final onward consignee after Liepāja.

Next pivots:
1. invoice issued under Contract `10.01/25-UR-DAP`;
2. CMR / vehicle registration / customs MRN;
3. warehouse receipt and weighing ticket at Brīvostas iela 21;
4. payment order / SWIFT details;
5. identify onward buyer and French contact mentioned by Astramar director.

## J1-A009-02 — Payment-routing identifiers in the contract
Type: FACT
Grade: B+ (contract image published by BIC).

The party-details page lists seller banking channels:
- JSC Priorbank, SWIFT `PJCBBY2X`;
- JSC BSB Bank, SWIFT `UNBSBY2X`.

Buyer banking channels listed:
- Citadele banka, SWIFT `PARXLV22`;
- Luminor Bank AS Latvian branch, SWIFT `RIKOLV2X`;
- correspondent bank Commerzbank Frankfurt/Main, SWIFT `COBADEFF`.

Source:
- https://investigatebel.org/storage/page_blocks/June2025/601.jpg

What this does NOT prove:
- which listed account/channel was actually used for this transaction;
- identity of an external payer;
- any sanctions breach by a bank.

Next pivot: search exact contract number + invoice + payment-order references and correlate with TST PL public IBANs already identified in prior passes.

## J1-A009-03 — Exact Liepāja physical node resolved: MOLS L, Brīvostas iela 21
Type: FACT
Grade: A/B (official Liepāja SEZ + Latvian corporate-registry aggregators).

The contract's final DAP destination `Brīvostas iela 21, Liepāja, LV-3405` matches the legal/operational address of LSEZ company `MOLS L` SIA, reg. no. `50003274861`, VAT `LV50003274861`, activity cargo handling / warehousing.

Official Liepāja SEZ board material states that MOLS L received development rights at Brīvostas iela 21 for:
- a hopper-wagon unloading pit on Liepāja port railway siding 19 at berth 60;
- scales at berth 61;
- rights through 31.12.2028 for these projects/operations.

Sources:
- https://www.liepaja.lv/liepajas-sez-valdes-sedes-lemumi/
- https://company.lursoft.lv/mols-l/50003274861

Analytical value:
This upgrades the Astramar route from a generic 'Liepāja port' hypothesis to a precise physical delivery address with documented bulk/rail handling infrastructure.

What this does NOT prove:
- that MOLS L itself was contractual carrier, customs declarant or owner of the goods;
- that the TST cargo used berth 60 or 61 specifically;
- that the goods arrived by rail rather than truck (the recovered specification says road delivery);
- that MOLS L changed labels, certificates or packaging.

Next pivot: MOLS L warehouse/terminal records, truck gate records, scales/weighbridge tickets, berth logs, customs declarations and storage agreements for Jan–Mar 2025.

## J1-A009-04 — Corporate bridge: MOLS L is a shareholder of Astramar Liepāja
Type: FACT
Grade: B+ (current Latvian company-information page reproducing shareholder registry data).

Firmas.lv lists `MOLS L` SIA (reg. no. `50003274861`, Brīvostas iela 21) as a `4%` shareholder of `ASTRAMAR LIEPĀJA K.A.` SIA, with shareholding event dates 22.12.2015 / 07.01.2016.

Source:
- https://www.firmas.lv/en/companies/astramar-liepaja-k-a/42103016440

INFERENCE / C:
The delivery address was therefore not an arbitrary unrelated warehouse address: the terminal operator at Brīvostas iela 21 has an ownership relationship with the buyer Astramar. This materially strengthens the physical/corporate coherence of the route.

What this does NOT prove:
- control by MOLS L over Astramar (4% is minority ownership);
- that MOLS L handled this particular 22 t shipment;
- shared management, bank accounts or beneficial ownership beyond the shown shareholding.

Next pivot: Astramar shareholder history/annual report, agreements between Astramar and MOLS L, storage/stevedoring invoices for Contract `10.01/25-UR-DAP`.

## J1-A009-05 — Provenance-document anomaly: Fox Chemical identifiers do not match the named company
Type: FACT + SOURCE_CLAIM
Grade: A/B for identifier mismatch; B for BIC's assessment of 'signs of falsification'.

BIC publishes two upstream documents used in the Turkmenistan/Kazakhstan origin narrative:
1. Invoice `RB2024-05`, 02.05.2024: seller `TOO FOX CHEMICAL`, buyer/consignee `Novaya biotekhnologicheskaya kompaniya LLC`, reg. no. `193578207`, Belarus; DAP Zhabinka; quantity `30,863.00`; price `253 USD`; total `7,808,399 USD`.
2. Invoice `KZ2024-3`, 02.05.2024: seller Turkmen `Marikarbamid`, buyer/consignee `Fox Chemical LLP`; document shows `NIP 140540003892` and address Karaganda region, Temirtau, Bayseitova 4/1, apt. 52.

Kazakhstan open records identify the actual `FOX Chemical` as BIN `211240001655`, registered in Almaty, Kuldzhinskiy tract 2, with director Shakir Ildarovich Nazirov. Conversely, BIN `140540003892` belongs to unrelated LLP `ALTYN TAÝ`, with the same Temirtau/Bayseitova 4/1 apt.52 address shown on the purported Fox invoice.

Sources:
- https://investigatebel.org/storage/page_blocks/June2025/572.jpg
- https://investigatebel.org/storage/page_blocks/June2025/582.jpg
- https://xn--80aa7aoihk4d.xn--e1anb.xn--80ao21a/ru/registry/show_supplier/550660
- https://safedeal.kz/counterparties/kz/company/96414

BIC separately states that the Turkmen/Kazakh papers supplied to Latvian buyers showed signs of falsification and that the Kazakhstan certificate referred to grade B while TST supplied grade A to Latvia.

What this does NOT prove:
- a final judicial finding of document forgery;
- who created or altered the documents;
- that every TST shipment used the same provenance pack;
- that the 30,863 t upstream document corresponds to the 22 t Astramar contract.

Next pivot:
- authenticate the CT-1 certificate number with Kazakhstan issuer/customs;
- verify invoice numbers with Fox Chemical / named bank records if public;
- compare quantities, dates and contract references across certificate, invoices and Latvian customs entries;
- locate the exact provenance documents Astramar received.

## J1-A009-06 — BIC bank-form copy directly shows 99% Grodno Azot raw-material share
Type: FACT about the published document / SOURCE_CLAIM about authenticity
Grade: B+.

BIC publishes a copy of a financial-activity form dated `30.09.2024` for TECHNOSPETSTRADING listing:
- PILOT Tasit Koltuklari San. Ve Tic. A.S. — seats — 1%;
- OAO `GrodnoAzot` — raw materials for fertilizer production — 99%.

Source:
- https://investigatebel.org/storage/page_blocks/June2025/61.png

This upgrades the prior pass from an article-only assertion to an archived visible document copy, but it is still not a certified bank extract.

What this does NOT prove:
- exact purchase volumes/values;
- authenticity certified by VTB/another bank;
- that 99% continued after the form date.

Next pivot: source bank/form metadata, accompanying statements, supplier invoices and Grodno Azot contracts.

## J1-A009-07 — Broader post-Poland route environment: new loading stations and double-proxy model
Type: SOURCE_CLAIM
Grade: B.

BIC's full Russian-language investigation states that in 2025 shipping papers no longer name Auls as origin; loading points are shown as `Brest`, `Baranovichi`, `Motykaly`, and `Zhabinka`. It describes a double-proxy model: special exporters obtain product from Grodno Azot while new Belarus entities act as shippers into Latvia. BIC names `Lesohimik`, `BelAmiks`, and `Brestvneshtrans` in the broader network, and reports at least 278 fertilizer railcars entering Latvia in the studied period.

Source:
- https://investigatebel.org/ru/investigations/grodno-azot-sankcii-es-shema

RED TEAM:
These companies/stations are part of the broader Grodno Azot route environment. No direct evidence in this pass connects Lesohimik/BelAmiks/Brestvneshtrans to the recovered TST→Astramar 22 t lot. Do not create direct graph edges without shipment-level documents.

## Potential conflict to resolve — 10.01.2025 Latvian contract vs Polish 'external payer' account
Prior official Polish material describes a 10.01.2025 Latvian contract where TST PL acted as payer despite not being a contract party, with goods moving toward a Hungarian company. The recovered BIC contract is also dated 10.01.2025 and is numbered `10.01/25-UR-DAP`, between TECHNOSPETSTRADING and Astramar, for DAP Liepāja.

Status: HYPOTHESIS / CONFLICT TO TEST, grade C.

Do NOT assume they are the same contract until the Polish decision's contract number/Latvian counterparty/payment order is matched. If they are the same document, the external-payer field could directly reveal TST PL's role in the Astramar transaction. If not, 10 January 2025 had multiple Latvian contracts.

Next pivot: obtain the payment order referenced by Astramar/LSM, contract number quoted in KAS annexes, and SWIFT/payment data.

## Highest-priority next pivots
1. Payment order for Contract `10.01/25-UR-DAP` and actual payer.
2. CMR/MRN for the 22 t TST→Astramar shipment.
3. MOLS L weighbridge/warehouse/terminal record at Brīvostas iela 21.
4. Identify French contact who asked Viesturs Andersons to facilitate shipment.
5. Compare the Jan 10 Astramar contract against Polish KAS description of the Jan 10 Latvian contract with TST PL as payer.
6. Authenticate Fox Chemical/Marikarbamid provenance documents through Kazakhstan/Turkmen registry/certificate channels.
7. Preserve primary images in case evidence store if repository policy permits.
