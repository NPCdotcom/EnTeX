# Plans Index

**実装計画（P4+）** の正本。思案・仕様: `docs/design/`。要求・要件: `docs/requirements/`。

ライフサイクル: [docs/PROJECT_LIFECYCLE.md](../docs/PROJECT_LIFECYCLE.md)

## フォルダ（スコープ階層）

| フォルダ | scope_level | PDCA Do |
|----------|-------------|---------|
| `product/` | H0 | 通常しない（`pdca_eligible: false`） |
| `elements/` | H1 | 通常しない |
| `systems/` | H2 | 通常しない |
| `elements/` | H1 | 通常しない |
| `systems/` | H2 | 通常しない |
| `frameworks/` | H3 | S0 スパイクのみ |
| `programs/` | H4 | **主戦場** |
| `algorithms/` | H5 | **主戦場** |

**原則**: 1 plan = 1 PDCA サイクル（S0 or S1）。program / algorithm が主；それ以外はユーザー確認 + `pdca_eligible: false`。

## Actions

| Action | Skill / Agent |
|--------|----------------|
| Readiness | `plan-reference`, `lifecycle-reference` |
| Record | `plan-record` |
| Mid-plan evaluation | `plan-evaluate`, **`evaluator`** |
| Bundled | **`plan_slicer`** |

Template: [_template.md](_template.md)  
Example（中立・削除可）: [_example/](_example/)

## Plans

| Plan | scope_level | Status | Summary |
|------|-------------|--------|---------|
| *(add rows)* | | | |

Rules: `planning`, `plans-content`, `project-lifecycle`
