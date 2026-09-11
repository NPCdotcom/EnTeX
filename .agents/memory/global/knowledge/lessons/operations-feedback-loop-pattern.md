---
id: lesson-operations-feedback-loop
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, aidlc, operations, g4, feedback, a-08]
sources:
  - learning/product-dev/notes/scans/a-08-report.md
  - learning/product-dev/notes/scans/a-01-report.md
  - learning/product-dev/notes/optimization/o-08-remaining-gaps.md
  - docs/_template/operations/feedback-to-inception.md
promoted_at: 2026-06-22
---

# 教訓 — AI-DLC Operations フィードバックループ

## Principle

AI-DLC **Operations** のキット翻訳は **四テンプレセット** が実用上限: deploy · monitor · incident · **feedback→Inception**。後者（a-08）で G4 の残ギャップ（学習還流）を閉じる。P6=出荷判定、Operations=本番運用 — **分離維持**。

## Facts

- a-08: deploy/monitor/runbook（o-08）+ `feedback-to-inception.md`（新）
- ループ: P6 出荷 → 運用シグナル → feedback 記入 → **ユーザー Go** → lifecycle_plan / P1 巻き戻し
- audit-log イベント `operations_feedback` 推奨（regulated は p-06 change control と併用）
- Cloud Agent · Automations · WAF/RASP はキット外（a-07 · c-06）

## Decisions

- 配置: `docs/operations/<unit-slug>/`（P6 後 · profile でスキップ可）
- P3 `observability-hooks.md` から monitoring-slos へ昇格
- awslabs Operations 丸コピー禁止 — 写像表のみ README に記載

## Anti-patterns

- Operations 工程の常時強制
- フィードバックの自動 P1 巻き戻し（Gate なし）

## Recall

G4 · Operations · deploy · SLO · feedback-to-inception · a-08 · o-08
