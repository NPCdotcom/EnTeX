# Automation run — workflow and stop conditions

**Role**: `automator` · **P5–P6**

**Prerequisite**: `automation-reference` verdict = `automation_ok`.

## Workflow

1. Confirm metadata: plan path, `status: agreed`, design path, target role + skills
2. Execute via **`role-execute`** / agreed skill order（PM が Cursor 内で実行）
3. Map work to acceptance criteria IDs or bullets
4. Scope drift → stop → `needs_approval`

## Stop conditions

- plan status not `agreed`
- missing criterion for requested action
- design conflict unresolved
- repeated failure without new evidence

## Do not

Execute from draft plan; widen scope automatically; skip approval for scope-affecting actions
