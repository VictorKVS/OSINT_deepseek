# Screening Factory schemas

- `screening-request.schema.json` — карточка задания и объекта;
- `screening-plan.schema.json` — профиль, waves, checks и human gates;
- `check-result.schema.json` — terminal semantics, observations and source attempts;
- `factory-run.schema.json` — результат партии;
- `source-registry.schema.json` — управляемый каталог официальных источников.

Schemas use JSON Schema Draft 2020-12. The Python runtime itself remains standard-library-only; schema validation can be added to a separate verification environment.
