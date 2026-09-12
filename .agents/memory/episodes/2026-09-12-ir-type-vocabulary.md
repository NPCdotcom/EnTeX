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

## Turn 2 (same day): A decided, package scaffolded

- Aster agreed on **A** (derived values computed at generation time). Doc §4 now records the decision, a structured JSON `expr` (sum/where, count, add/sub, nesting), and "derived key in input → reject".
- Added §6.1 envelope `{doc_type, schema_version, content}`; unknown keys rejected; schema lives in `schemas/ir/` side.
- `packages/circle-monthly-report/`: `schema.json` (案1 compact form, provisional; uses all 11 types + attributes), `examples/valid/` ×6 (typical, minimal, deficit, max-rows, fiscal-year-start, tex-special-chars), `examples/invalid/` ×6, README with expected errors and derived totals.
- Verified with a throwaway checker (deleted): all valid pass; invalid ones fail exactly as documented (06 → 6 content errors when envelope is ignored).

## Open

- Need the real Word monthly report to fix schema fields (first Open item).
- `schema_version` bump policy; `expr` vocabulary sufficiency — confirm against real form.
- Enum labels live in schema, not IR — API (step 2) must expose the schema too.
