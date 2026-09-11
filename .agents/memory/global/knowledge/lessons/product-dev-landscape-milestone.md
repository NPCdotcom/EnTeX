---
id: lesson-product-dev-landscape-milestone
kind: knowledge
topic: lesson
owner: kit
status: active
created: 2026-06-22
tags: [product-dev, landscape, cursor, aidlc, o-11, milestone]
sources:
  - learning/product-dev/notes/scans/landscape-extension-summary.md
  - learning/product-dev/notes/optimization/o-11-c08-kit-reflect.md
  - learning/product-dev/notes/research-cycle-log.md
  - docs/CURSOR_AGENT_TOOLING.md
promoted_at: 2026-06-22
---

# 教訓 — product-dev landscape 一段落（25 サイクル · o-11）

## Principle

**北極星**（AIDLC/AIDD キット最適化）の計画 landscape は **25 サイクルで一段落**。以降は四半期 changelog（c-11 型）か実プロジェクト検証が主。三層語彙を固定: **傘=AIDD** · **方法論主参照=AI-DLC（AWS）** · **実践=SDD+HITL**。

## Facts（2026-06-22 時点）

| トラック | 完了 |
|----------|------|
| C Cursor | 10/10（c-08〜10 拡張含む） |
| P Product | 7/7（p-07 continuous discovery） |
| A AIDLC | 8/8（a-08 Operations） |
| T Terminology | 6 |
| S Synthesis | 6 |
| O Optimization | 11（o-11 キット反映） |

## o-11 キット反映（確定知見）

| 領域 | 正本 |
|------|------|
| Plan 二重化 | `.agents/plans/`=工程契約 · `.cursor/plans/`=製品メモ |
| 併用ツール | Claude Code/Copilot 等はキット外 · Cursor 同期が正本 |
| Enterprise | regulated-checklist §5.5–5.6 · 料金は cursor.com 参照のみ |
| Discovery 運用 | `continuous-discovery-cadence.md`（任意） |
| Operations ループ | `feedback-to-inception.md` |
| landscape 調査 | Auto mode 優先（LANDSCAPE_RESEARCH_POLICY） |

## 境界（維持）

- Task/Subagent/Cloud/Automations **キット外**
- AI-DLC `.mdc` **丸コピー禁止**
- 週次インタビュー · 料金表 · 10万 LOC monorepo 実地は **スコープ外**

## Decisions

- 学習サンドボックス `learning/product-dev/` は調査正本 · キット `docs/` へは Track O + ユーザー Go
- TestProjectA = パイロット参照 repo

## Recall

product-dev 学習完了 · landscape 25 · o-11 · c-08-10 · 三層語彙 · キット境界
