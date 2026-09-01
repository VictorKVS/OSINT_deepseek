# Search Journal Template

**Case ID:** `CASE-...`  
**Subject:**  
**Tasking authority / basis:**  
**Approved scope:**  
**Access class:** `PUBLIC | PUBLIC_WITH_PERSONAL_DATA | AUTHORIZED_INTERNAL | RESTRICTED`  
**Opened:**  
**Current status:** `PENDING | IN_PROGRESS | REVIEW | CLOSED`

## Workstream status

| Stream | Scope | Status | Result summary | Blocking condition | Next action |
|---|---|---:|---|---|---|
| 1 | Primary data | `PENDING` |  |  |  |
| 2 | Relations and graph | `PENDING` |  |  |  |
| 3 | Off-source attribution | `PENDING` |  |  |  |
| 4 | Risk and abuse | `PENDING` |  |  |  |
| 5 | Red Team and source control | `PENDING` |  |  |  |

## Journal entries

| Entry ID | Recorded at UTC | Stream | Query / action | Source / tool | Result mark | Result summary | Evidence grade | Entities / relations created | Rejected alternatives | Next pivot | Access class |
|---|---|---:|---|---|---:|---|---:|---|---|---|---|
| `...` | `YYYY-MM-DDThh:mm:ssZ` | `1` |  |  | `PENDING` |  |  |  |  |  | `PUBLIC` |

## Required disposition language

- `PASS` — verified result;
- `PARTIAL` — useful but incomplete result;
- `NO_HIT` — no relevant result in named sources at recorded time;
- `REJECTED` — false/irrelevant/unsupported lead;
- `BLOCKED` — collection prevented by a recorded constraint;
- `PENDING` — not yet executed;
- `REVIEW` — requires analyst/Red Team decision;
- `CLOSED` — scope formally closed.

## Source note

For each material source record:

```yaml
source_id: SRC-...
url: https://...
title: ...
publisher: ...
source_type: official_government | court | blockchain_explorer | company | registry | media | forum | social | code | archive | other
affiliation: ...
bias_or_interest: ...
accessed_at_utc: ...
published_at: ...
reliability_grade: A | B | C | D
what_it_supports:
  - ...
what_it_does_not_support:
  - ...
capture_sha256: ...
capture_location: restricted://...
access_class: PUBLIC | PUBLIC_WITH_PERSONAL_DATA | AUTHORIZED_INTERNAL | RESTRICTED
```

## Closure gate

A case may be marked `CLOSED` only when:

- every task question has an explicit answer or recorded data gap;
- all material findings cite a source;
- entity resolution and false-positive checks are documented;
- facts, source claims, inferences and hypotheses are separated;
- high-impact conclusions have passed Red Team review;
- unresolved mandatory actions are listed;
- the decision-maker report states its legal and evidentiary limits.
