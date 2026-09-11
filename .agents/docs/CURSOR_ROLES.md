# Cursor Roles (logical roles — in-IDE execution)

**Execution**: PM runs **`role-execute`** for role skill columns.  
**Every turn**: `pm-turn-start` → `role-execute` → `pm-turn-end` — [`_chains/pm-turn.md`](../skills/_chains/pm-turn.md)  
**Canonical**: `docs/PM_ROUTING.md` · catalog: `skills/role-skill-catalog/references/full-catalog.md`  
**No Hermes · No Subagent.**

| Role | Duty | Primary skills |
|------|------|----------------|
| `router` | Entry · brief · route | inside pm-turn-start · adaptive-lifecycle-plan when needed |
| `spec_designer` | P0–P3 | landscape/terminology · design-* · lib-doc-frontmatter |
| `plan_slicer` | P4 | plan-* · lib-doc-frontmatter |
| `builder` | P5 | implement-* · lib-tdd-cycle |
| `hotfixer` | P5+ | patch-* |
| `reviewer` | P6 | review-* · lib-review-vmodel |
| `evaluator` | P6 | evaluate-* |
| `automator` | Automation | automation-* |
| `kit_maintainer` | Kit | maintain-* |

Memory: `docs/MEMORY_ARCHITECTURE.md`
