# Book → Knowledge pipeline

## Purpose

Use books already present in the user's lawful/private library as source material for the Knowledge Analyst without turning the public GitHub repository into a distribution point for copyrighted books or full translations.

## Storage boundary

### Private corpus storage

May contain, subject to the user's rights/licence:

- original PDF/EPUB/DOCX bytes;
- SHA-256 and file metadata;
- extracted full text;
- full aligned translation;
- page/block/paragraph mappings;
- source images/figures where needed for analysis.

The private corpus is an evidence store. It is not a public knowledge publication.

### Public repository

May contain:

- source metadata and bibliographic identifiers;
- hashes and stable opaque source/span IDs;
- parser/translator/analyser code;
- schemas and regression fixtures using synthetic text;
- derived knowledge objects that do not reproduce the book;
- concepts, definitions in paraphrased form where appropriate, patterns, principles, trade-offs, decision criteria, failure modes and relations;
- citations/references back to private span IDs;
- review/audit status.

A full book, reconstructable text dump or full translation is not a required GitHub artifact.

## Production stages

```text
B0  SOURCE_REGISTERED
    ↓
B1  ORIGINAL_BYTES_VERIFIED
    source bytes + SHA-256
    ↓
B2  TEXT_EXTRACTED
    layout/order provenance retained
    ↓
B3  TRANSLATION_ALIGNED
    source unit ↔ translated unit
    ↓
B4  SEMANTIC_STRUCTURE
    part/chapter/section/paragraph/list/figure/table
    ↓
B5  KNOWLEDGE_CANDIDATES
    term/concept/definition/claim/principle/pattern/trade-off/
    criterion/failure-mode/example/relation
    ↓
B6  CROSS_SOURCE_REVIEW
    compare with other books, specifications, documentation, experiments
    ↓
B7  KB_PUBLISHED
    reviewed reusable knowledge only
```

## Translation contract

Translation is not allowed to replace the original evidence.

Every translation unit keeps:

- `unit_id`;
- source character range or page/block locator;
- source text hash;
- original language text in the private corpus;
- translated text in the private corpus;
- translation method/model/version where available;
- review status.

If an architectural claim is disputed, the analyst must be able to return to the original wording.

## Semantic decomposition

The first decomposition layer preserves document structure:

```text
Book
 ├─ Part
 │  └─ Chapter
 │     └─ Section
 │        ├─ Paragraph
 │        ├─ List
 │        ├─ Figure
 │        ├─ Table
 │        └─ Example
```

The analyst then derives a knowledge layer:

```text
Source span
 ├─ TERM_CANDIDATE
 ├─ CONCEPT_CANDIDATE
 ├─ DEFINITION_CANDIDATE
 ├─ CLAIM_CANDIDATE
 ├─ PRINCIPLE_CANDIDATE
 ├─ PATTERN_CANDIDATE
 ├─ TRADEOFF_CANDIDATE
 ├─ DECISION_CRITERION_CANDIDATE
 ├─ FAILURE_MODE_CANDIDATE
 ├─ EXAMPLE_CANDIDATE
 └─ RELATION_CANDIDATE
```

All candidates start as `NEEDS_REVIEW`.

## Analyst responsibilities

The book analyst does more than summarisation. It must answer:

1. What concepts does the author introduce?
2. Which concepts are definitions versus explanations/examples?
3. Which statements are principles, heuristics or empirical claims?
4. What architectural decision is being discussed?
5. What forces/constraints drive the decision?
6. What alternatives are compared?
7. What trade-offs and consequences are stated?
8. In what context does the recommendation apply?
9. What failure modes or anti-patterns are described?
10. Which claims need confirmation from another source?
11. Which terms collide with terminology used by other authors?
12. Which knowledge object is reusable by an architect agent?

## Cross-book professor stage

A single book never becomes the truth layer by itself. The professor stage compares candidate knowledge across sources and can mark relations such as:

- `SUPPORTS`;
- `CONTRADICTS`;
- `REFINES`;
- `SPECIALIZES`;
- `GENERALIZES`;
- `USES_DIFFERENT_DEFINITION`;
- `ALTERNATIVE_TO`;
- `APPLIES_WHEN`;
- `FAILS_WHEN`;
- `SUPERSEDED_BY`.

Every relation requires evidence references.

## Pilot

`BOOK-PILOT-ARCH-001` is registered for **Software Architecture: The Hard Parts**.

The pilot remains `AWAITING_SOURCE_BYTES` until a lawful/private source copy is available to the corpus pipeline. No external public mirror is treated as evidence of redistribution rights.
