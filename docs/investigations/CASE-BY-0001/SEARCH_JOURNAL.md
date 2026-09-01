# CASE-BY-0001 — Search Journal

**Task:** identify and assess the company associated with `Republic of Belarus, Minsk, Naklonnaya St., 28`.  
**Approved output:** activity, risk factors, revenue model, connected persons and organizations.  
**Current disposition:** `CLOSED` at preliminary management-decision scope.  
**Public journal:** redacted; raw captures remain outside the public repository.

## Final status by requirement

| Requirement | Result | Grade | Summary |
|---|---:|---:|---|
| Identify the object | `PASS` | A/B | Two key interrelated legal entities were resolved; the supplied UIN/UNP `193648909` identifies the export entity. |
| Determine activity | `PASS` | A/B | Observable role: wholesale/export trade in chemical products and nitrogen fertilizers. |
| Determine risk factors | `PASS` | A | Direct Polish national sanctions exposure; elevated AML, banking, logistics, counterparty, UBO and reputational risk. |
| Determine revenue model | `PASS/PARTIAL` | B | Most probable model: wholesale/export margin and commercial support of cross-border deliveries; exact P&L structure unavailable. |
| Identify connected persons/entities | `PASS/PARTIAL` | A–C | Core cross-border network identified; full ownership history and several employment links remain incomplete. |
| Special-threat screening | `NO_HIT` | — | No substantiated public-source finding of terrorism, extremism, narcotics trafficking or unlawful arms trafficking in the checked corpus. |

## Search log

| Entry | Result | Action / query | Source class | Result summary | Next pivot / disposition |
|---|---:|---|---|---|---|
| BY-0001 | `PASS` | Address search across map, registry, company-catalog and government-document results | mixed | Address exists and is used by more than one legal entity. | Do not equate address with a single company. |
| BY-0002 | `PASS` | Resolve `193648909` | Belarus registry aggregator + Polish official documents | `TECHNOSPETSTRADINGEXPORT LLC / ООО «ТехноспецтрейдингЭкспорт»`; registered 2022-09-27; wholesale chemical-products profile. | Main subject selected. |
| BY-0003 | `PASS` | Resolve `193256472` | supplied registration document + company site + Polish official documents | `TECHNOSPETSTRADING LLC / ООО «Техноспецтрейдинг»`; registered 2019-05-20. | Treat as primary connected company, not the same entity. |
| BY-0004 | `PASS` | Compare public functions of the two entities | company site + registration data | Main company presents broader trade/production profile; Export entity performs export/wholesale function. | Separate declared from observed activity. |
| BY-0005 | `PASS/PARTIAL` | Review `ТУ BY 193256472.002-2022` | supplied corporate technical document | Confirms technical documentation and named management/engineering roles on document date. | Does not prove a separate full-cycle plant. |
| BY-0006 | `PASS` | Polish sanctions and trade-flow review | KAS / MSWiA official publications | Polish authorities link the network to fertilizer supplies and list relevant companies/persons under Polish national sanctions. | Attribute conclusions to the issuing authority. |
| BY-0007 | `PASS` | Resolve core person `Armen Seryozhaevich Harutyunyan` | official Polish material + Armenian government publication + Lithuanian registry aggregator | Identity and cross-jurisdiction corporate roles materially supported. | Full ownership graph still requires primary registries. |
| BY-0008 | `PARTIAL` | Resolve Ruzanna Khachatryan, Dmitry Goshko, N. V. Dashuk, Sergey Pilets, Petr Pasikov | official decision, technical document, investigative media | Roles range from formal ownership/representation to management and claimed employment links. | Keep exact relation type and source grade. |
| BY-0009 | `PASS` | Search exact company names and identifiers in public sanctions sources | Polish official sources | Direct Polish national sanctions exposure confirmed. | Do not automatically describe as EU-wide listing. |
| BY-0010 | `PARTIAL` | Review Russia-linked corporate and court trail | commercial Russian registry aggregators + published court text | Russian corporate link through ООО «МСК» is highly probable; court appearance as third party does not establish wrongdoing. | Primary EGRUL extract required for final grade A. |
| BY-0011 | `REJECTED` | Hypothesis: “one address = one company” | Red Team | Rejected because two separate registration identifiers and dates exist. | Permanent methodological correction. |
| BY-0012 | `REJECTED` | Hypothesis: “technical specifications = proof of own industrial plant” | Red Team | Rejected; specifications prove documentation, not ownership/location/capacity of production. | Require plant, equipment, permits and supply evidence. |
| BY-0013 | `REJECTED` | Hypothesis: “Polish sanctions = automatic EU listing” | Red Team | Rejected; national and EU legal regimes must be separated. | Check each jurisdiction and transaction separately. |
| BY-0014 | `NO_HIT` | Special-threat searches in checked public/official corpus | public/official | No substantiated terrorism, extremism, narcotics or unlawful arms-trafficking connection found. | Reopen only on concrete new indicator. |

## Core public sources

- Polish KAS: `https://www.gov.pl/web/kas/spolka-tst-pl-oraz-jej-beneficjent-rzeczywisty-harutyunyan-armen-seryozhaevich-z-wniosku-szefa-kas-zostala-wpisana-na-liste-sankcyjna`
- Polish MSWiA sanctions decisions: `https://www.gov.pl/web/mswia/decyzje-ministra-swia-w-sprawie-wpisu-na-liste-sankcyjna`
- Company website: `https://technospetstrading.com`
- Export entity registry aggregator: `https://checko.ru/by/company/193648909/registration`
- Belarusian Investigative Center material: `https://belarusfiles.org/ru/investigations/how-belarusian-fertilizer-company-get-banned-nitrogen-into-europe-through-straw-companies`
- Armenian Prime Minister official publication: `https://www.primeminister.am/en/press-release/item/2018/11/20/Nikol-Pashinyan-meeting/`

## Closure note

The case is sufficient for a preliminary management decision and enhanced due diligence recommendation. It is not sufficient for criminal-law qualification, complete beneficial-ownership determination, audited revenue allocation or definitive industrial-production verification.
