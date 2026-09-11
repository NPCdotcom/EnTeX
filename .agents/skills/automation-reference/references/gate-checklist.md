# Automation reference — gate checklist

**Role**: `automator` · **P5–P6** · Read-only.

## Required reads

1. `automations/AUTOMATION_INSTRUCTION.md`
2. `docs/LINEAR_AUTOMATION_POLICY.md`, `docs/LINEAR_PHASE_MAP.md`
3. `lifecycle-reference` — plan under `programs/` or `algorithms/`; `pdca_eligible: true`
4. `.agents/plans/<topic>.md`
5. Linked `related_design` path

## Gate checks

- [ ] plan exists
- [ ] plan `status: agreed`
- [ ] acceptance criteria explicit
- [ ] scope / out-of-scope explicit
- [ ] `scope_level` is `program` or `algorithm`
- [ ] upper H links in Scope hierarchy table
- [ ] `docs/project-state.yaml` `current_phase` ≥ P4（if exists）
- [ ] Cursor role + skill sequence known

## Verdict values

`automation_ok` | `needs_approval` | `blocked_no_agreed_plan` | `blocked_design_or_plan_gap`

Do not execute changes in this skill.
