# Terminology & web research policy（用語・Web 調査）

要求・要件・設計・計画（**P0–P4**）では **用語の食い違い** が手戻りの主因。  
本キットでは **WebSearch + browser MCP** を省略しない。

**探索型**（方針・アーキテクチャ・「調査して」）は **`landscape-research`**（広→狭）。  
正本: [`LANDSCAPE_RESEARCH_POLICY.md`](LANDSCAPE_RESEARCH_POLICY.md)

**構造化質問**（AI-DLC question-driven）: P1–P2 で曖昧点が残る場合、`docs/requirements/<slug>/verification-questions.md`（テンプレ: `docs/requirements/_template/verification-questions.md` · skill `adaptive-lifecycle-plan`）を起票し **チャットではなくファイル**で `[Answer]:` を記入 → Gate 後に record へ。

## 2 系統

| 系統 | Skill | 用途 |
|------|-------|------|
| 用語 | `terminology-research` | 定義 · alignment · record 前 gate |
| 探索 | `landscape-research` | scan → drill → 設計根拠 · deliberate 前 |

## 必須

| 工程 | Role | 調査 |
|------|------|------|
| P0–P3 | `spec_designer` | Skill **`terminology-research`**（Cursor: WebSearch + browser） |
| P4 | `plan_slicer` | 同上（criteria・DoD・スコープ語） |
| 毎回 | `router` | P0–P4 用語 → terminology-research · 探索型 → landscape-research |

## Gate

- `design-record` / `plan-record` **前** に Terminology alignment ブロックが無い → **block**
- P1–P2 で要件が曖昧なまま → **verification-questions.md** を起票（未回答なら **block**）
- ソース無しの「一般論」だけ → **Recycle**（調査やり直し）

## Requirements depth（adaptive-lifecycle-plan 連携）

| depth | いつ | terminology の厚み |
|-------|------|-------------------|
| **minimal** | profile `spike` / hotfix | 受入条件・核心用語のみ |
| **standard** | profile `standard`（デフォルト） | 3–8 用語 · alignment 表 |
| **comprehensive** | profile `full` | 上記 + トレーサビリティ語彙 · `docs/requirements/_template/traceability-table.md` |

正本フィールド: `docs/project-state.yaml` → `lifecycle_plan.requirements_depth`（skill `adaptive-lifecycle-plan` が設定）。

## Skill / Rule

- Skill: `terminology-research` → **`memory-reason`**（alignment / glossary G1–G5）
- Skill: `landscape-research` → **`memory-reason`**（lessons / G3 URL）
- Rule: `design-stewardship`, `planning`, `cursor-tool-select`
- Router: `secretary-route`, `secretary-brief`

## PM

brief の Cursor 補助を **実行してから** または **role 実行と並行** で record へ進む。  
運用証跡に `用語調査: WebSearch+browser | done/skipped` を 1 行含めてよい。
