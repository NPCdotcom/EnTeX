---
id: lesson-adaptive-lifecycle-plan-pattern
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, aidlc, lifecycle, workflow-planning, adaptive]
sources:
  - learning/product-dev/notes/synthesis/gap-analysis.md
  - learning/product-dev/notes/optimization/o-01-adaptive-lifecycle-draft.md
promoted_at: 2026-06-22
---

# 教訓 — adaptive-lifecycle-plan パターン

## Principle

AI-DLC Workflow Planning のキット翻訳は **新しい always rule ではなく skill** で実装する。意図・brownfield・複雑度から **実行する P0–P6 集合** を推薦し、ユーザー Go 後に `project-state.lifecycle_plan` へ記録する。

## Facts

- 最大ギャップ G1 の解消策（s-01）
- profiles: hotfix · spike · standard · full · doc_only
- Plan モードで計画提示 · secretary-route 入口で発火
- awslabs `.mdc` 丸コピーは二重オーケスト — **禁止**

## Decisions

- skipped_phases / skipped_stages を明示 · 全 P 順送りしない
- unit_scope を lifecycle 出力に含め H4/H5 完走と接続

## Open

- o-03 パイロットで体感速度を検証（H-02）

## Related

- lesson-secretary-mob-facilitator
- skill `adaptive-lifecycle-plan`
