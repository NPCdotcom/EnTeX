---
id: trace-2026-06-22-math-full-promotion
kind: trace
scope: global
created: 2026-06-22
promoted_to:
  - lesson-math-learning-complete
  - lesson-math-p0-p8-synthesis
  - lesson-math-p9-early-synthesis
  - lesson-math-p9-synthesis
  - lesson-math-learning-p9-cross-review
---

# Trace — 数学学習ロードマップ全体の長期記憶昇格

## Cognitive

- **Intent**: ユーザー指示「全てを長期記憶に挙げて」— P0–P9 数学学習プロジェクト全体を global lessons へ昇格
- **Scope**: global `knowledge/lessons/`（chemistry-learning-complete 5 件構成を踏襲）
- **Prior**: 2026-06-22 に P9 横断レビューのみ部分昇格済み → 本 trace で全体統合

## Operational

| Artifact | Action |
|----------|--------|
| math-learning-complete.md | 新規 anchor（P0–P9 正本） |
| math-p0-p8-synthesis.md | 新規 archive |
| math-p9-early-synthesis.md | 新規 archive（C01–10） |
| math-p9-synthesis.md | 更新（C11–32 · complete へリンク） |
| math-learning-p9-cross-review.md | archive 化（詳細横断レビュー） |
| global/index.yaml | 5 件 math lessons 登録 |
| learning/index.yaml | math → roadmap_complete |
| manifest.yaml | roadmap_complete + global_lessons 5 件 |

## Verifiable checks

- P0–P8: wiki-roadmap 進捗表すべて「完了」
- P9: p9-deepening-roadmap C01–32 すべて「完了」
- 実験: 42 dirs · 128 .py files
- 横断再現: `p9_cross_review.py` exit 0（前回確認済み）
- ノート: 79 .md in notes/

## Contextual recall

- Pattern: lesson-chemistry-learning-complete + 3 archives
- User state: Cycle 32 完了後 **指示待ち**（Cycle 33 未着手を Decision に記録）
