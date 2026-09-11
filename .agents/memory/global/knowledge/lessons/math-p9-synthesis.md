---
id: lesson-math-p9-synthesis
kind: knowledge
topic: lesson
owner: learning/math
status: active
promoted: 2026-06-22
tags: [math, roadmap, numerical-toy, p9, hyperbolic, game-theory]
linked: [lesson-math-learning-complete, lesson-math-p9-early-synthesis, lesson-math-learning-p9-cross-review]
---

# 教訓 — 数学 P9 第 2–3 期（Cycle 11–32）

詳細正本: `learning/math/notes/p9-cycle32-cross-review.md`  
長期記憶: `math-learning-complete.md`  
前提: `math-p9-early-synthesis.md`（C01–10）

## 要点（2026-06-22 · 並行 track C11–31 + 横断レビュー C32）

| 領域 | フック |
|------|--------|
| ロードマップ | MSC2020 下位分野から 1–2 本 · P0–P8 完走後の反復深化 |
| 並行 track | C11–31: 毎サイクル 双曲系 Euler + ゲーム学習 |
| 双曲結論 | 1st HLLC + scalar WENO のみ有効 · 自前系高次は未達 |
| ゲーム結論 | 零和 OMD · 協調 FP · NE 選択 = init/構造 |
| 横断軸 | 問題構造に合わせた手法選択が汎用高次/no-regret を上回る |

## 双曲 track（C11–30）

| ベンチマーク | 勝者 | L1 rho（代表） |
|--------------|------|----------------|
| Sod | 1st HLLC | ~0.012 |
| Sod | scalar WENO-Z | （系では未使用） |
| エントロピー波 | scalar WENO-Z | ~0.005 |
| エントロピー波 | 1st HLLC | ~0.010 |

**失敗パターン**: 原始変数 WENO 系 · conserved PP · Char WENO 周期波爆発

## ゲーム track（C11–31）

| 構造 | 最良 | 典型失敗 |
|------|------|----------|
| 零和 MP / RPS | OMD（定数 eta） | eta decay で優位喪失 |
| Stag Hunt / 協調 | FP | Hedge NE 未到達 |
| 3 人協調 | FP | init 依存 |

**NE 選択介入**: バイアス init（C20）· 構造化バイアス（C25）· シグナル+バイアス（C28）で FP 完全収束

## 数値 toy の再発防止

1. **厳密解 1 点** — Toro Sod · エントロピー波厳密解で sanity
2. **スカラーと系を分離** — decoupled WENO 成功 != 系パイプライン成功
3. **算法×構造マトリクス** — 零和手法を協調に流用しない
4. **init を実験変数に** — 協調 NE 距離は动力学より init が支配
5. **命名・索引** — `p9-cycleNN-<slug>.md` + `experiments/p9_cycleNN/`

## 次に深掘りする候補（Cycle 33+ · 未計画）

1. MSC 別分野選定（ユーザー指示）
2. Clawpack/PyClaw conda 導入（双曲 gold ref）
3. global games 完全モデル（私的シグナル + 事前）

## Related

- lesson-math-learning-complete（正本）
- lesson-math-p9-early-synthesis（C01–10）
- lesson-math-learning-p9-cross-review（横断詳細）
