---
id: 2026-09-12-ir-type-vocabulary
date: 2026-09-12
scope: project
tags: [ir-schema, design, H1, P0, monthly-report]
---

# Episode: scrutinize the IR type vocabulary (monthly report)

## Input

NPC proposed 11 IR types (`text` `rich_text` `month` `date` `integer` `money` `enum` `boolean` `object` `row_list` `list`) for the circle monthly report and asked for a review, saved as a file for Aster.

## Done

- `docs/design/elements/ir-type-vocabulary.md` (draft, H1). Kept all 11 names; tightened semantics.
- Linked from `schemas/README.md` and `docs/README.md`.
- Branch `5/npc/ir_type_vocabulary` (issue #5 assumed — no `gh` on this Windows host; rename if the number differs). Not committed.

## Key changes vs proposal

- `money`: signed integer (balance/carry-over can be negative); non-negativity is a field `minimum`, not the type.
- `rich_text`: fixed structure `{blocks:[paragraph|list]}`, no nesting, no inline markup. Markdown-subset string rejected as IR (would make renderer parse syntax); allowed only as form-ui/data-import input.
- `row_list` rows: scalars only; `max_items` because fixed layouts break on long tables (value lives in the doc-package).
- `list.items` ∈ {text, enum, date, integer}; `list<enum>` covers multi-select.
- `boolean` strictly 2-valued; 3-state → `enum`.
- `text`: single line, NFC normalize (determinism), no width normalization.
- Separated field attributes (required/label/default/derived/min/max/…) from types.
- Derived totals: recommend IR carries rows only; `derived` + small `expr` (sum + filter) evaluated in `src/entex/` without doc-type knowledge.
- Deferred: `time`, `number`, `year`, `url/email/phone`, `image` — re-judge at 2nd doc-type.
- `schema.json` format: recommend EnTeX compact form as source, JSON Schema generated; decision can wait until 2nd doc-type.

## Open

- Need the real Word monthly report to fix §6 fields (marked as the first Open item).
- Derived-value approach A vs B; `expr` grammar.
- Enum labels live in schema, not IR — API (step 2) must expose the schema too.
