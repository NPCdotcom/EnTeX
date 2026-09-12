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

## Turn 3 (same day): P0 gate Go, P1 要求 written

- Reviewed progress against the 6 主要要素 (charter §8): `ir-schema` (type vocabulary) and `doc-package` (circle-monthly-report scaffold) have a base; `renderer` is untouched (only `version`/`doctor` in `src/entex/cli.py`); `form-ui`/`job-runner`/`data-import` are later roadmap steps.
- User decided **P0 gate = Go**, and confirmed **renderer-first** order (matches charter §11 step 1). Recorded in `docs/project-state.yaml` (`current_phase: P1`, `gate_status.current: passed`) and `.agents/memory/audit/audit-log.md` (`gate` entry, decision Go).
- Note: the workspace mount path changed mid-session (from a Windows path to `/workspace`); the gate-recording edits from the prior turn had landed on the old path and were not present in the actual repo, so they were redone here on `/workspace`.
- Wrote `docs/requirements/circle-monthly-report/要求.md` (P1) — grounded in charter §3/§5, `packages/circle-monthly-report/README.md`, and `schema.json`. Includes R1–R10 requirements list, agent recommendation (proceed with 案A: build renderer core now with provisional schema/layout, fix fields once the real report arrives), Facts/Assumptions carried over from ir-type-vocabulary.md.
- Linked from `docs/README.md`.

### Next

- User review of `要求.md` → promote to `要件.md` (P2, verifiable acceptance).
- Then P3 basic design for `renderer` (`docs/design/programs/renderer.md`, H4) → `plan-record` (P4) before any `implement-conduct`.

## Turn 4 (same day): P2 要件 written

- User said "次に進んでください" (proceed) — treated as continuation, not a new Stage-Gate decision (要件.md起票 only needs 要求.md to be reviewable, per PROJECT_LIFECYCLE.md gate table; no separate user Go required here).
- Wrote `docs/requirements/circle-monthly-report/要件.md` (P2): scope (in/out), FR1–FR8 (envelope check → type validation → derived-key rejection → expr evaluation → TeX escape → latexmk PDF → user-facing error mapping → CLI `entex render`), NFR1 (≤10s) / NFR2 (determinism), each with a concrete verification method tied to existing `examples/`. Agent recommendation: split renderer into `ir/loader.py` / `ir/derive.py` / `tex/escape.py` / `renderer.py` / `cli.py` (案2) rather than one monolithic module, to keep the doc-package-dependent vs. -independent boundary visible ahead of the 2nd doc-type judgment (charter §11 step 3).
- Open items carried to P3: how to split FR1–FR8 into plan-sized PDCA units, provisional `template.tex.j2` layout policy, FR7's latexmk→Japanese error mapping rules.
- Linked from `docs/README.md`. Recorded `phase_change` (P1→P2) in audit-log (not a new Stage-Gate; P0 Go remains the operative gate decision).

### Next

- P3 basic design: `docs/design/programs/renderer.md` (H4) — resolve the 3 Open items above, then `plan-record` (P4).
