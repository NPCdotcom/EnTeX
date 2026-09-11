# Automation record — fields

**Role**: `automator` · **P5–P6** · After `automation-run`.

## Record fields

| Field | Value |
|-------|-------|
| timestamp | ISO or YYYY-MM-DD |
| linear_project | if used |
| linear_issue_id | if used |
| plan_path | |
| plan_status | |
| related_design | |
| role | e.g. builder |
| skills_used | comma list |
| criteria_touched | |
| result | done / blocked / needs_approval |
| next_action | |

## Storage

- Default: chat summary（[`assets/run-log-template.md`](../assets/run-log-template.md)）
- Optional file: only when user requests persistence

## Rules

Factual only; separate facts / assumptions / speculation; never mask missing approvals.

Do not change plan status by assumption or mark criteria done without evidence.
