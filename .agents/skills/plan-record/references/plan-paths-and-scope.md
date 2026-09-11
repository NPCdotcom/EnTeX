# Plan paths and scope_level

## Folder by scope_level

| scope_level | Path | pdca_eligible |
|-------------|------|---------------|
| `program` | `.agents/plans/programs/<slug>.md` | `true`（Do 対象） |
| `algorithm` | `.agents/plans/algorithms/<slug>.md` | `true` |
| H0–H2 roadmap | `.agents/plans/product/` · `elements/` · `systems/` | usually `false` |
| `framework` roadmap | `.agents/plans/frameworks/<slug>.md` | usually `false` |

## Frontmatter（必須）

- `scope_level`: `program` or `algorithm` for implement Do
- `pdca_eligible`: `true` for S1 Do plans
- `related_design`, `related_requirements`, `parent_hierarchy`
- `status`: `draft` until user confirms; `agreed` for large Do

## Template source

Copy from [plans/_template.md](../../../plans/_template.md). Fill **Scope hierarchy** + **Goal**（上位 H への 1 行リンク）。

## Index

Update [.agents/plans/README.md](../../../plans/README.md) — one row per new plan.

## Agent recommendations

Add **Agent recommendations** + `>` **ユーザー思考** section for user iteration.
