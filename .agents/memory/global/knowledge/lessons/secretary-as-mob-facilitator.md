---
id: lesson-secretary-mob-facilitator
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, aidlc, secretary, mob, orchestration]
sources:
  - learning/product-dev/notes/synthesis/s-03-secretary-mob.md
  - learning/product-dev/notes/scans/a-02-report.md
promoted_at: 2026-06-22
---

# 教訓 — secretary を Mob ファシリテータとして扱う

## Principle

AI-DLC の Mob Elaboration は **複数人同室** ではなく、1-user キットでは **secretary-route + role-execute + Gate Keeper** に翻訳する。Mob/Bolt 語は正本に入れず、既存語彙（unit · plan · gate）で足りる。

## Facts

- secretary = いつどの role/skill を直列実行するかの正本（c-02）
- ユーザー = 全ステークホルダー席の圧縮（Go / Recycle）
- paralleldrive multi-agent orchestrator は no-subagents と衝突 — **非採用**（a-03）

## Decisions

- 単一 PM オーケストを維持 · Task/Explore サブエージェントはキット外
- role-execute で専門家発言を直列化（spec_designer → builder → reviewer）

## Related

- lesson-adaptive-lifecycle-plan-pattern
- lesson-ai-driven-hitl-positioning
