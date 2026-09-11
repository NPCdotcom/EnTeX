---
name: adaptive-lifecycle-plan
description: Recommend which project phases to run, what to skip, and Cursor mode from a new or changed goal. Use at project start or when scope jumps; wait for user Go before advancing.
---

# Adaptive Lifecycle Plan

**Role**: `router` · `spec_designer`（入口）· PM orchestration  
**参照**: `docs/PROJECT_LIFECYCLE.md` · `docs/project-state.template.yaml` · `t-01` AI-DLC 主参照

## When

- 新規プロジェクト / チャット入口（P0 相当）
- brownfield 初回 · 重大 scope 変更 · ユーザー「工程を決めて」
- `secretary-route` が固定 P ルートに迷ったとき

## Workflow

[`references/workflow.md`](references/workflow.md) · **G8**: [`references/conditional-stages.md`](references/conditional-stages.md)

## Output

[`assets/lifecycle-plan-output-template.md`](assets/lifecycle-plan-output-template.md)

## Question file（P1–P2）

[`assets/question-file-template.md`](assets/question-file-template.md) · 正本テンプレ: `docs/requirements/_template/verification-questions.md`

## Do not

- ユーザー Go なしに `current_phase` や plan を進める
- 全 P0–P6 を常に順送り（profile でスキップを明示）
- チャットだけで構造化質問を完結（ファイル優先 · s-05）
