# Linear Automation Policy (Generic)

## Goal

Operate Linear-backed automation safely with clear approval boundaries:
only execute work that belongs to an **agreed plan cycle**.

## Channel Strategy

Use a hybrid channel model.

- Global operations channel: cross-project incidents, policy updates, runtime health
- Per-project run channel: execution logs and routine progress
- Per-project approval channel: approvals, exceptions, scope change decisions

Recommendation:

- `#auto-ops-global`
- `#auto-<project>-run`
- `#auto-<project>-approval`

One-channel-only is acceptable only for very small projects with low concurrency.

## Issue State Model (Linear)

Core states（工程 P・スコープ H との対応: [LINEAR_PHASE_MAP.md](./LINEAR_PHASE_MAP.md)）:

1. `design-draft` — P0–P1
2. `design-ready` — P2–P3
3. `plan-draft` — P4
4. `plan-agreed` — P4 done → P5 entry
5. `do-running` — P5（plan under `programs/` or `algorithms/`, `pdca_eligible: true`）
6. `check-running` — P6
7. `done` or `blocked` — may roll back to P1–P3 for next work

Automation may move issues only within:

- `plan-agreed -> do-running -> check-running -> done/blocked`

## Approval Rules

- Required before automation run:
  - linked plan with `status: agreed`
  - clear acceptance criteria
  - no unresolved scope ambiguity
- Required during run:
  - any scope expansion request
  - unresolved design contradiction
  - repeated failures on same action

## Instruction Contract for Linear-triggered Automation

Each run instruction must include:

- `linear_project`
- `linear_issue_id`
- `plan_path`
- `plan_status=agreed`
- `scope_level=program|algorithm`
- `lifecycle_phase=P5`（推奨）
- `related_design`
- `steward + skills`
- `stop_conditions`

## Agent Model

Default runtime model for delegated execution:

- `Composer 2.5 fast`

Model changes require explicit policy update and approval in the project approval channel.

## Auditing

For each run, post:

- steward/skills invoked
- criteria touched
- files/artifacts changed
- verification summary
- next state transition proposal

## Do Not

- Run from draft plans
- Hide approvals in free-text comments
- Collapse approval and execution into a single unreviewable action
