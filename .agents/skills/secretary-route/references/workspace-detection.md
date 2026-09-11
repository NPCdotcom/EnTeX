# Workspace detection（G6 · AI-DLC Workspace Detection 相当）

**目的**: greenfield / brownfield / キット正本の誤作業を **ヒューリスティック**で判定し、**G1** `adaptive-lifecycle-plan` の入力とする。

**自動確定しない** — 判定は brief に 1 行書き、ユーザー **Go** で `lifecycle_plan` に記録。

## 判定シグナル

| # | 観測 | 推論 | `lifecycle_plan` 候補 |
|---|------|------|----------------------|
| 1 | `docs/project-state.yaml` 無し or `lifecycle_plan.profile` 空 | **初回入口** | `adaptive-lifecycle-plan` **必須** |
| 2 | ソース (`src/` `lib/` `app/` 等) あり · `docs/requirements/` 薄い | **brownfield** | `brownfield: true` · P1 前 `brownfield-reference` |
| 3 | `docs/` + charter あり · 新機能依頼 | **greenfield 追加** | profile `standard` · P0 skip 可 |
| 4 | ユーザー「工程」「スコープ変更」「緊急」 | **再計画** | `adaptive-lifecycle-plan` 再実行 |
| 5 | workspace = `~/.agents` のみ（利用先 repo なし） | **誤ルート** | 利用先へ `move_agent_to_root` 提案 |
| 6 | `lifecycle_plan` あり · phase と intent 整合 | **継続** | 再計画 **不要**（下表へ） |

## 読み取り順

1. `docs/project-state.yaml` · `lifecycle_plan`
2. Glob: `docs/requirements/**` · `docs/design/**` · ソース root
3. `nav.yaml` · `session.intent`
4. ユーザー発話（意図 · 緊急度）

## 出口（secretary-route）

| 判定 | 次スキル |
|------|----------|
| 初回 or 再計画 | **`adaptive-lifecycle-plan`** → ユーザー Go → 下表 |
| brownfield & RE 未完了 | **`brownfield-reference`**（P1 前） |
| 継続 | `routing-table.md` の通常行 · `lifecycle_plan.recommended_cursor_mode` を turn-brief へ |

## brownfield 簡易

`brownfield: true` 当てはまり例:

- 既存 `src/` または 100+ ファイルのコードベース
- `docs/project-state.yaml` の `lifecycle_plan.brownfield` が true
- ユーザー明示「既存コード」「リファクタ」

## 非採用

- 完全自動 phase 遷移（HITL 維持）
- AI-DLC Workspace Detection の丸コピー

**参照**: `adaptive-lifecycle-plan` · `c-07` · gap **G6** · **G1** 入口
