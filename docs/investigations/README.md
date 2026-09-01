# OSINT Search Journals

> Status: **PUBLIC / REDACTED / AUDITABLE**
>
> Scope: public-source investigation logs only. Raw captures, restricted material, unnecessary personal data and non-public client information must not be committed to this public repository.

## Purpose

This directory is the versioned search journal for official OSINT cases. It records what was searched, where it was searched, what result was obtained, what was rejected, and what the next investigative pivot is.

The journal is not a narrative report and does not establish criminal liability. It preserves the research process and prevents silent replacement of facts, claims, inferences and hypotheses.

## Mandatory result marks

| Mark | Meaning |
|---|---|
| `PASS` | Result independently verified or supported by a primary/official source. |
| `PARTIAL` | Material result obtained, but the required collection or verification is incomplete. |
| `NO_HIT` | No relevant result was found in the explicitly named sources at the recorded time. |
| `REJECTED` | False lead, entity mismatch, duplicate, irrelevant result or unsupported inference. |
| `PENDING` | Planned but not yet executed. |
| `BLOCKED` | Execution could not be completed because of access, API, tooling or legal constraints. |
| `REVIEW` | Result requires analyst or Red Team review before use. |
| `CLOSED` | Case or workstream closed at the currently approved scope. |

`NO_HIT` never means that the fact does not exist. It means only that the recorded searches did not produce a relevant result.

## Evidence grades

- `A` — primary/official evidence or several independent high-quality sources;
- `B` — strong secondary evidence or several consistent signals;
- `C` — analytical hypothesis; alternatives remain;
- `D` — discovery lead requiring validation.

## Mandatory journal fields

Every material journal entry should contain:

```text
entry_id
recorded_at_utc
case_id
workstream
query_or_action
source_or_tool
result_mark
result_summary
evidence_grade
entities_or_relations_created
rejected_alternatives
next_pivot
access_class
analyst_note
```

## Relation-first rule

An investigation must not stop at the literal wording of the task. Each relevant person, organization, wallet, address, domain, transaction, contract, court case, document or account is evaluated as a possible pivot.

However, a connection is included only with an explicit type and support level:

```text
OWNS / CONTROLS / DIRECTS / REPRESENTS / EMPLOYED_BY
TRANSACTED_WITH / FUNDED / RECEIVED_FROM / SENT_TO
LOCATED_AT / MENTIONED_IN / SANCTIONED_BY
CLAIMED_BY_SOURCE / CONFIRMED_BY / CONTRADICTED_BY
```

A shared counterparty, address, telephone, transaction or source mention does not automatically prove common ownership, criminal association or coordinated activity.

## Case directories

- [`MASTER_SEARCH_JOURNAL.md`](MASTER_SEARCH_JOURNAL.md) — consolidated status of all active cases;
- [`CASE-BY-0001/SEARCH_JOURNAL.md`](CASE-BY-0001/SEARCH_JOURNAL.md) — company/address task;
- [`CASE-BTC-0001/SEARCH_JOURNAL.md`](CASE-BTC-0001/SEARCH_JOURNAL.md) — Bitcoin address task;
- [`CASE-TRON-0001/SEARCH_JOURNAL.md`](CASE-TRON-0001/SEARCH_JOURNAL.md) — TRON address task.

## Public repository rule

The public journal may contain public URLs, public blockchain addresses, public company identifiers, redacted conclusions, source metadata and hashes. It must not contain raw leaked datasets, private communications, credentials, unnecessary residential details, private keys, seed phrases, authentication tokens or uncontrolled allegations.
