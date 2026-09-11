## {ISO-8601} | {event_type} | {slug}

| Field | Value |
|-------|-------|
| **event_type** | `gate` · `lifecycle_plan` · `phase_change` · `question_approval` · `stage_complete` · `turn_summary` |
| **actor** | `user` · `router` · `builder` · … |
| **decision** | Go · Conditional Go · Recycle · Hold · Kill · Approve and Continue · — |
| **phase** | P0–P6 · S0 · S1 · — |
| **summary** | 1 行（80 字以内推奨） |
| **reason** | （任意）変更理由 · 規制向け free-text |

### Refs

- team: `docs/project-state.yaml`
- plan: `.agents/plans/...`
- trace: `.agents/memory/traces/YYYY-MM-DD-....md`
- questions: `docs/requirements/.../verification-questions.md`
- lifecycle: `lifecycle_plan.profile` / `skipped_phases`

### Detail（任意）

{補足 · 条件 · スキップしたステージ名}

---
