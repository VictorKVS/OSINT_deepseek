# Task 1 — Automated deep-dive pass 005

Date: 2026-09-02
Case: OSINT_TEST_2026_09_01
Object: TECHNOSPETSTRADING / TECHNOSPETSTRADINGEXPORT / related fertilizer export network
Status: ACTIVE

## Evidence labels
- `FACT` — directly stated in a primary/official/public record.
- `SOURCE_CLAIM` — statement by a source that has not yet been independently reproduced from the underlying primary record.
- `INFERENCE` — analytical conclusion from established facts.
- `HYPOTHESIS` — proposition requiring evidence.

## Evidence grades
- `A` — primary/official record.
- `B` — strong secondary / registry-derived / documented corporate source.
- `C` — analytical lead or incomplete attribution.
- `D` — weak/unverified lead; not usable in conclusions.

---

## J1-A005-01 — IMPORTANT RED TEAM correction: Astramar ↔ Piemare ownership/service relation appears historical, not current ownership

### FACT / A
Official Liepāja municipal / Liepāja SEZ materials state that in summer 2021 SIA `Norplast` acquired the shares of LSEZ AS `Piemare` and the company was renamed `Norplast Piemare`.

Official/public sources:
- Liepāja municipality, 2021-12-09: https://www.liepaja.lv/darbu-liepajas-sez-teritorija-uzsak-pirmais-uznemums-ar-norvegijas-kapitalu-norplast-piemare-lsez-as/
- Liepāja SEZ, 2025-01-17: https://liepaja-sez.lv/en/home/the-new-lsez-as-norplast-piemare-plant-has-started-manufacturing

The 2025 SEZ publication describes LSEZ AS `Norplast Piemare` as an Entec Group company. Other current 2024/2025 sources describe its owner as SIA `Entec Norplast` / Norwegian Entec group.

Evidence grade: `A` for the 2021 acquisition/rename and current Entec-group control as stated by official Liepāja public bodies.

### CONFLICT / stale-source warning
LAFF's currently accessible Astramar member page still states that `Astramar Liepāja K.A.` is a co-owner of the holding group involving LSEZ AS `Piemare` and `Krasts invests`:
- https://laff.lv/lv/astramar-liepaja-k-a-sia

Astramar's own website also continues to describe stevedoring services via LSEZ `PIEMARE` AS at Liepāja berths 64, 65, 73, 74, 75 and 76:
- https://www.astramarliepaja.lv/

Because official sources establish that Piemare's shares were acquired by Norplast in 2021 and the company was renamed, the LAFF co-owner language and Astramar's `PIEMARE` service description should be treated as potentially historical/stale unless a current contract or current corporate extract proves otherwise.

### RED TEAM correction to earlier analysis
A 2025 TECHNOSPETSTRADING ↔ Astramar contract does **not** by itself justify a graph edge from the TST cargo to the former Piemare terminal/berths. The Astramar–TST relationship is a B-level source claim from LSM with a direct comment by Astramar's director; the exact 2025 stevedore, terminal and berth remain unresolved.

### What this does NOT prove
- that Astramar stopped using those berths/services after 2021;
- that Norplast Piemare handled or did not handle the TST cargo;
- that the TST cargo was physically stored/handled at berths 64/65/73–76;
- any misconduct by Astramar, Piemare/Norplast Piemare or Entec.

### Next pivot
- 2025 port-call/berth logs for the relevant Astramar-arranged cargo;
- current Astramar stevedoring contracts/subcontractors;
- current operator/lease rights for berths 64/65/73–76;
- cargo manifest, wagon-to-ship transfer act, vessel IMO, consignee and port of discharge;
- identify the French contact described by Viesturs Andersons.

---

## J1-A005-02 — Latvia corridor: exact stop dates and September confirmation

### FACT / SOURCE_CLAIM / B+
LSM / De facto reported on 2025-08-24, citing Latvian Customs/VID and other official data, that:
- the last Belarus-origin urea cargo released by Latvian customs was on `2025-06-29`;
- the last urea-solution cargo was released on `2025-07-10`;
- in August 2025 these fertilizer categories did not transit Latvia;
- several July cargoes were subject to enhanced checks for possible sanctions-circumvention indicators;
- four refusal-to-open-criminal-proceeding decisions were appealed by Customs with FIU cooperation and were under prosecutor review;
- 6.1 thousand tonnes imported by four Latvian companies were under customs supervision in free zones/customs warehouses in Riga and Liepāja, intended for Estonia, Poland and Germany;
- one named company was `RIN Cargo`.

Source:
- https://www.lsm.lv/raksts/zinas/ekonomika/24.08.2025-baltkrievu-karbamids-latvija-muitas-policija-lietas-neierosina-par-spiti-sankciju-apiesanas-pazimem.a611523/

BIC subsequently reported on 2025-10-30 that Latvia's State Revenue Service (VID) confirmed no shipments under CN `310210` and `31028000` in **August and September 2025**.

Source:
- https://investigatebel.org/en/news/grodno-azot-sanctions-eu-block-belarus-fertilizers

Evidence grade: `B+` for the LSM account based on named Latvian authorities; `B` for the BIC report of VID's later confirmation until the direct VID statement is archived.

### Analytical value
The Latvia route shows a measurable operational discontinuity after enhanced customs scrutiny: the broad Belarus-origin urea/UAN corridor that was material in H1/H1–July 2025 is reported as absent in August and September. This is a useful change-point for searching subsequent displacement to other EU entry points/routes.

### What this does NOT prove
- that all earlier Latvia cargoes belonged to TECHNOSPETSTRADING;
- that the stoppage was caused solely by one investigation or one company;
- that a criminal sanctions-evasion offence was established;
- what route replaced Latvia after July 2025.

### Next pivot
- Eurostat monthly CN 310210 / 310280 flows by EU entry state before/after July 2025;
- identify alternative post-July entry corridors and new importers;
- prosecutor outcome for the four Latvian cases;
- direct VID monthly customs data / statements.

---

## J1-A005-03 — AS Garantstroy operational evidence beyond registry code/address

### SOURCE_CLAIM / B
A Kontur-Fokus generated company-profile PDF for OAO `Minsk Tractor Works` reproduces a Belarus economic-court/order entry dated `2020-02-20`, case/order `983-19Пп/2020`, amount `68.95 BYN`, claimant OAO `Минский Тракторный Завод` (UNP 100316761), debtor ООО `АС Гарантстрой` (UNP 192237039), with the note that the debtor partially admitted the debt.

Source:
- https://kontur-f.ru/wp-content/uploads/%D0%9E%D0%90%D0%9E_%D0%9C%D0%A2%D0%97-by_100316761-2020-10-20.pdf

Evidence grade: `B` until the original Belarus court record is retrieved.

### SOURCE_CLAIM / B-C
ImportGenius' customs-derived dataset for Ukrainian importer TOV `Белагроснаб` lists ООО `АС Гарантстрой` among five trading partners across the importer dataset (2007-01-02 to 2020-01-28).

Source:
- https://www.importgenius.cn/ukraine/importers/%D1%82%D0%BE%D0%B2-%D0%B1%D0%B5%D0%BB%D0%B0%D0%B3%D1%80%D0%BE%D1%81%D0%BD%D0%B0%D0%B1

Evidence grade: `B-C` because this is a commercial customs-data aggregator and row-level AS Garantstroy shipment details were not recovered in the open view.

### INFERENCE
These two independent secondary signals strengthen the proposition that AS Garantstroy's agricultural-machinery wholesale profile was operational rather than merely a registry code. That makes it more relevant as a historical predecessor/neighbor at Naklonnaya 28, but still does not prove ownership or business continuity into TECHNOSPETSTRADING.

Evidence grade: `C` for continuity inference.

### Critical limitations
- The 68.95 BYN court amount is very small and cannot support a claim of a major MTZ commercial relationship.
- The visible ImportGenius sample row names Bobruiskagromash, not AS Garantstroy; do not attribute that shipment to AS Garantstroy.
- No direct personnel/ownership/bank-account overlap between AS Garantstroy and TST was established in this pass.

### Next pivot
- original Belarus court entry for 983-19Пп/2020;
- row-level customs records where AS Garantstroy is named supplier;
- invoices/contracts with MTZ / Belagrosnab;
- founders/directors/POAs and bank details by year;
- compare customers/suppliers with later TST counterparties.

---

## J1-A005-04 — Hungary / Latvian contract identities / French contact

Repeated exact-date, contract-language and route searches still did not yield a reliable public identity for:
- Latvian counterparty in the 2025-01-10 contract;
- Hungarian counterparty in the 2025-02-21 contract;
- external payer;
- French acquaintance/contact who asked Astramar director Viesturs Andersons to assist the cargo.

Status: `NO-HIT`.

No candidate company/person has been promoted into the graph without a contract, VAT/EORI, invoice, manifest, customs declaration or other identifying evidence.

---

## Updated priority queue

1. Correct Astramar physical-route reconstruction after the 2021 Piemare ownership change: current terminal/stevedore, berth, vessel, consignee, French contact.
2. Direct VID confirmation and prosecutor outcome for the four July 2025 Latvian cargo cases.
3. Identify displacement route after Latvia's Aug–Sep 2025 stop using Eurostat/CN time series and customs/company pivots.
4. Original court record 983-19Пп/2020 and row-level AS Garantstroy customs records.
5. Latvian contract party (2025-01-10), Hungarian company (2025-02-21), external payer.
6. CMR/CIM/SMGS, wagon numbers, batch/quality certificates and cargo fingerprints linking individual TST/TSTExport/GrandGranit shipments.
