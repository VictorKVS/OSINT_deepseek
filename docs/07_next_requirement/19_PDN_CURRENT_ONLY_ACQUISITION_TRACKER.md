# PDN CURRENT_ONLY acquisition tracker

Status date: 2026-08-23

## Rule

The operational Knowledge Factory is built from currently effective legal texts plus already-published future-effective changes. Historical revisions are not a prerequisite for MVP. Point-in-time reconstruction is pulled only for a concrete incident, dispute, inspection or audit date.

Required acquisition record for every document:

`official source -> exact bytes -> SHA-256 -> verified identity -> legal status -> effective date -> CURRENT/FUTURE_EFFECTIVE -> structure -> requirements -> relations -> tracking`

## Wave 0 — already available locally

- [x] 152-ФЗ «О персональных данных» — local A0 proof available; current legal-reference revision: 26.07.2026.
- [x] ПП РФ № 1119 от 01.11.2012 — local A0 proof available.
- [x] Приказ ФСТЭК России № 21 от 18.02.2013 — local A0 proof available; current legal-reference revision: 14.05.2020.
- [x] Приказ ФСБ России № 378 от 10.07.2014 — local A0 proof available.

Wave 0 next action: run these four through the full document -> structure -> requirement -> relation conveyor using CURRENT_ONLY semantics.

## Wave 1 — operational PDn obligations

- [ ] ПП РФ № 687 от 15.09.2008 — non-automated PDn processing; current revision 18.01.2025; legal-reference validity through 01.09.2030.
- [ ] Приказ Роскомнадзора № 178 от 27.10.2022 — harm assessment; effective 01.03.2023; legal-reference validity through 01.03.2029.
- [ ] Приказ Роскомнадзора № 179 от 28.10.2022 — evidence of PDn destruction; effective 01.03.2023; legal-reference validity through 01.03.2029.
- [ ] Приказ Роскомнадзора № 180 от 28.10.2022 — operator notification forms.
- [ ] Приказ Роскомнадзора № 187 от 14.11.2022 — interaction for the PDn incident register; effective 01.03.2023.

## Wave 2 — current technical / public-sector context

- [ ] Приказ ФСТЭК России № 117 от 11.04.2025 — current protection requirements for state information systems and other systems of state bodies, state unitary enterprises and state institutions; effective 01.03.2026; replaced FSTEC order № 17 within its scope.
- [ ] Приказ ФСТЭК России № 137 от 08.05.2026 — FUTURE_EFFECTIVE change to № 117; main changes effective 01.09.2026, item 7 of appendix effective 01.03.2027.
- [ ] 149-ФЗ «Об информации, информационных технологиях и о защите информации» — current revision 26.06.2026; track published future-effective amendments separately.

## Wave 3 — conditional / domain-specific

- [ ] Приказ Роскомнадзора № 140 от 19.06.2025 — de-identification requirements and methods; effective 01.09.2025; use when de-identification is applicable.
- [ ] ПП РФ № 211 от 21.03.2012 — CONDITIONAL: operators that are state or municipal bodies; do not assign automatically to every state institution.
- [ ] 323-ФЗ «Об основах охраны здоровья граждан в Российской Федерации» — healthcare context; current legal-reference revision 04.08.2026; extract only operationally relevant provisions.

## Monitoring states

- `CURRENT` — used by agents and operational reports now.
- `FUTURE_EFFECTIVE` — published and verified, but not yet active; must trigger preparation and automatic status transition on the effective date.
- `CONDITIONAL` — applicable only if the organization/system/process satisfies a stated condition.
- `REPLACED` — excluded from operational requirements but retained as minimal audit evidence.
- `VERIFY_CURRENTNESS` — not allowed to feed operational legal claims until verified.

## Download queue

Order:

1. complete Wave 0 extraction;
2. acquire Wave 1 exact official bytes and hashes;
3. acquire FSTEC 117 and future amendment 137 before 01.09.2026;
4. add 149-ФЗ and healthcare/context documents;
5. expand the registry only from operational use-cases and explicit applicability.

## Deferred by design

- arbitrary 90-day historical backfill;
- full revision history for every act;
- historical obligation matrices;
- arbitrary-date legal reconstruction without a concrete case;
- parsing obsolete acts merely because they once existed.

Machine-readable source of truth: `config/pdn_current_only_registry.json`.
