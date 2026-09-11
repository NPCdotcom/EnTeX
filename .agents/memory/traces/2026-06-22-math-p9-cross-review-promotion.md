---
id: trace-2026-06-22-math-p9-cross-review-promotion
kind: trace
scope: global
created: 2026-06-22
promoted_to: [lesson-math-learning-p9-cross-review, lesson-math-p9-synthesis]
---

# Trace — 数学 P9 横断レビュー長期記憶昇格

## Cognitive

- **Intent**: ユーザー指示「いったんこれを長期記憶へ昇華」— P9 Cycle 32 横断レビュー完了状態を chat 非依存の global lessons へ昇格
- **Scope**: global `knowledge/lessons/`（chemistry-learning-complete パターン踏襲）
- **Promotion criteria**: G1 検証済み実験再現済み · G2 正本ノート存在 · G3 sources 明示 · G4 ユーザー明示昇格指示

## Operational

| Step | Result |
|------|--------|
| `p9_cross_review.py` Unicode 修正 | exit 0（2026-06-22 再実行） |
| 索引更新 00-index / p9-roadmap / wiki-roadmap | 完了 · 待機状態 |
| global lesson 2 件作成 | math-learning-p9-cross-review · math-p9-synthesis |
| global/index.yaml 更新 | lesson-math-learning-p9-cross-review 追加 |
| learning/index.yaml 更新 | math status + global_ids |
| manifest.yaml 更新 | p9_cross_review_complete |

## Verifiable checks

- Cross-review script: `experiments/p9_cycle32/p9_cross_review.py` exit 0
- Canonical note: `notes/p9-cycle32-cross-review.md` checklist all [x]
- Experiment dirs: 32 (`p9_cycle01` … `p9_cycle32`)

## Contextual recall

- Prior pattern: `lesson-chemistry-learning-complete` (2026-06-20)
- User constraint: Cycle 32 完了後待機 — Cycle 33 未着手を Decision に記録
