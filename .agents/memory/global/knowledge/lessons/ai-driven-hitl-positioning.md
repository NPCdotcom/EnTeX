---
id: lesson-ai-driven-hitl-positioning
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, aidlc, hitl, governance, positioning]
sources:
  - learning/product-dev/notes/scans/a-04-report.md
  - learning/product-dev/notes/scans/a-05-report.md
  - learning/product-dev/notes/glossary-alignment.md
promoted_at: 2026-06-22
---

# 教訓 — AI-driven + HITL の立ち位置

## Principle

マーケ・ドキュメントでは **「AI-driven（人間 Gate）」** を一貫使用する。AWS AI-DLC 正本: assisted / autonomous 単独は不十分 — **AI が計画・質問・実行提案 · 人間が検証・承認**。

## Facts

- 三層語彙: 傘 AIDD · 方法論 AI-DLC · 実践 SDD+HITL（t-01）
- キット: secretary + Gate = driven · Cursor Agent = 実行層（autonomous 能力はポリシーで拘束）
- Human-on-the-loop（監視のみ）は標準非採用 — HITL（出力単位レビュー）が主モード
- ~10 回/ bolt の承認は AI-DLC 仕様 · profile で緩和（a-05）

## Decisions

- Cloud / Task 完全自律はキット外オプション（CURSOR_SUBAGENT_POLICY）
- audit-log + gate_status で監査可能性を確保（o-01 核3）

## Related

- lesson-secretary-mob-facilitator
- docs/ROLES_AND_GOVERNANCE.md
