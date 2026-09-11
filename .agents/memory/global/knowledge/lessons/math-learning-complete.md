---
id: lesson-math-learning-complete
kind: knowledge
topic: lesson
owner: learning/math
status: active
created: 2026-06-22
promoted: 2026-06-22
tags: [math, learning, roadmap, p0-p9, complete]
sources:
  - learning/math/notes/wiki-roadmap.md
  - learning/math/notes/p9-cycle32-cross-review.md
linked: [lesson-math-learning-p9-cross-review, lesson-math-p9-synthesis, lesson-learning-complete-index, math-doc-meta-index]
---

# 数学学習ロードマップ — 長期記憶（正本）

**正本パス**: `~/.agents/learning/math/`  
**エージェント用ドキュメント**: `~/.agents/memory/global/knowledge/documents/math-doc-meta-INDEX.md`（47 件 · フラット · `math-doc-*`）  
**詳細（P9 横断）**: `math-learning-p9-cross-review.md`  
**状態**: P0–P8 完走 · P9 Cycle 32 横断レビュー完了 · **ユーザー指示待ち**

---

## Facts

| 項目 | 値 |
|------|-----|
| 基礎層 | P0–P8 完了（Wikipedia / MSC2020 ベース） |
| P9 深化 | Cycle 01–31（双曲系 + ゲーム学習 並行 track）+ Cycle 32 横断レビュー |
| 総括 | Cycle 30（双曲）· 31（ゲーム）· 32（横断） |
| P9 実験 | `experiments/p9_cycle01/` … `p9_cycle32/` |
| 索引 | `notes/00-index.md` · global `documents/math-doc-meta-INDEX.md` |
| ドキュメント | `~/.agents/memory/global/knowledge/documents/`（47 件 · regex `^math-doc-`） |
| manifest | `status: p9_cross_review_complete` |

## 横断レビュー確定事項（要約）

- **双曲**: 1st HLLC を内部ベンチマーク · scalar WENO-Z が厳密解で最良
- **ゲーム**: Cycle 31 で coordination / tracks 総括
- 再現: `experiments/p9_cycle32/p9_cross_review.py`

## 次候補（未計画）

第 5 ラウンド選定 · Clawpack 外部 gold · ユーザー指示待ち
