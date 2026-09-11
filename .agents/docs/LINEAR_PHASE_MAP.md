# Linear 状態 ↔ ライフサイクル（P / H）対応

正本の工程定義: [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md)  
Automation ポリシー: [LINEAR_AUTOMATION_POLICY.md](./LINEAR_AUTOMATION_POLICY.md)

## Linear issue 状態 → 工程 P

| Linear 状態 | 工程 P | 主 Cursor role | 典型成果物 |
|-------------|--------|----------------|------------|
| `design-draft` | P0–P1 | `spec_designer` | charter / `要求.md` draft |
| `design-ready` | P2–P3 | `spec_designer` | `要件.md` agreed；`docs/design/` H1–H3 |
| `plan-draft` | P4 | `plan_slicer` | `.agents/plans/programs\|algorithms/*.md` draft |
| `plan-agreed` | P4 完了 → P5 入口 | `plan_slicer` → `builder` | plan `status: agreed` |
| `do-running` | P5 | `builder` | ソース + plan Do log |
| `check-running` | P6 | `reviewer` | review / criteria 検証 |
| `done` | P6 完了 | — | 次トピックへ（**P1–P3 巻き戻し可**） |
| `blocked` | 任意 | `evaluator` / PM | Open questions・ゲート block |

## Linear ↔ スコープ H（issue ラベル推奨）

Linear の label または issue タイトル接頭辞で揃える:

| Label / 接頭辞 | H | plan フォルダ |
|----------------|---|---------------|
| `h0-product` | H0 | `plans/product/` |
| `h1-element` | H1 | `plans/elements/` |
| `h2-system` | H2 | `plans/systems/` |
| `h3-framework` | H3 | `plans/frameworks/` |
| `h4-program` | H4 | `plans/programs/` |
| `h5-algorithm` | H5 | `plans/algorithms/` |

**Automation が動く plan**: `h4-program` または `h5-algorithm` + `pdca_eligible: true` のみ。

## `project-state.yaml` との同期（手動または PM）

Automation / 秘書 brief 前に揃える:

```yaml
current_phase: P4
linear_issue_state: plan-draft   # optional
scope_focus:
  level: H5
  path: docs/design/programs/foo.md
```

## 巻き戻し例

| 状況 | Linear | P 工程 |
|------|--------|--------|
| Do 完了後に新要求 | 新 issue `design-draft` | P1 |
| 設計矛盾 | `design-ready` に戻す | P3 |
| plan 分割 | 親 `done`、子 `plan-draft` | P4 |

## Instruction への追記（Automation 用）

`automations/AUTOMATION_INSTRUCTION.md` の実行ペイロードに任意で含める:

- `lifecycle_phase: P5`
- `scope_level: program | algorithm`
- `plan_path: .agents/plans/algorithms/...`
