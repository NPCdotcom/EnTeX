---
id: lesson-learning-complete-index
kind: knowledge
topic: lesson
owner: learning
status: active
created: 2026-06-22
promoted: 2026-06-22
tags: [learning, index, roadmap, cross-topic]
---

# 学習ワークスペース — 長期記憶マスター索引

**正本ルート**: `~/.agents/learning/`  
**索引**: `learning/index.yaml`  
**昇格日**: 2026-06-22

---

## Principle

全学習トピックの進捗・正本パス・global lessons は **本ファイルと各トピック長期記憶** に集約する。  
chat 履歴に依存せず、`learning/index.yaml` の `global_ids` から辿る。

---

## トピック一覧

| ID | 表示名 | 状態 | 長期記憶 ID | 正本パス |
|----|--------|------|-------------|----------|
| `npcdotcom` | NPCdotcom | promoted | `npcdotcom-philosophy` | `learning/npcdotcom/` + global philosophy |
| `chemistry` | 化学 | **roadmap_complete** | `lesson-chemistry-learning-complete` | `learning/chemistry/` |
| `math` | 数学 | **p9_cross_review_complete** | `lesson-math-learning-complete` | `learning/math/` |
| `physics` | 物理学 | **p9_in_progress** | `lesson-physics-learning-progress` | `learning/physics/` |
| `cpp` | C++ | **phases_1-6_complete** | `lesson-cpp-learning-progress` | `learning/cpp/` |
| `minecraft` | Minecraft | **engine_in_progress** | `lesson-minecraft-surface-to-deep-pattern` | `learning/minecraft/` |
| `product-dev` | プロダクト開発 | **roadmap_complete** | `lesson-product-dev-learning-complete` | `learning/product-dev/` |

---

## 完了 · 停止 · 継続

| トピック | 判定 |
|----------|------|
| chemistry | P0–P11 Cycle 36 計画分完走 · **停止** |
| math | P0–P8 + P9 Cycle 32 横断レビュー完走 · **停止** |
| product-dev | landscape 25 + o-11 反映 · **停止** |
| minecraft | S/D/X + ML 完走 · GL-MC-1 昇格 · **Phase E 継続中** |
| physics | P0–P8 完走 · P9 Cycle 112 まで · **継続可能** |
| cpp | LearnCpp/CG/MS Learn + フェーズ1–6 完走 · P6 Vulkan capstone 済 · **継続可能** |
| npcdotcom | philosophy 昇格済 · learning は参照層 |

---

## 昇格ファイル（global lessons）

```
~/.agents/memory/global/knowledge/lessons/
  learning-complete-index.md          ← 本ファイル
  chemistry-learning-complete.md
  chemistry-p11-synthesis.md        (archive)
  chemistry-p11-round4-synthesis.md   (archive)
  math-learning-complete.md
  math-learning-p9-cross-review.md  (archive 詳細)
  math-p9-synthesis.md                (archive)
  physics-learning-progress.md
  cpp-learning-progress.md
  product-dev-learning-complete.md
  minecraft-surface-to-deep-pattern.md
  secretary-as-mob-facilitator.md     (+ 7 product-dev patterns)
  npcdotcom-landscape-hooks.md
```

Philosophy/preferences: `knowledge/philosophy/` · `knowledge/preferences/`

---

## 再利用手順

1. `learning/index.yaml` でトピック ID と `global_ids` を確認
2. global `index.yaml` で lesson パスを解決
3. 詳細は `learning/<topic>/notes/00-index.md` へ

---

## Related

- `learning/index.yaml`
- `~/.agents/memory/global/index.yaml`
