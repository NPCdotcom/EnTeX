---
id: lesson-math-p0-p8-synthesis
kind: knowledge
topic: lesson
owner: learning/math
status: active
promoted: 2026-06-22
tags: [math, roadmap, p0-p8, foundations]
linked: [lesson-math-learning-complete]
---

# 教訓 — 数学 P0–P8 基礎ロードマップ

詳細正本: `learning/math/notes/wiki-roadmap.md`  
長期記憶: `math-learning-complete.md`

## 要点（2026-06-19 完走）

| 層 | フェーズ | 到達 |
|----|----------|------|
| A 共通基盤 | P0–P1 | 数学の地図 · 集合·論理·証明 |
| B 純粋数学 | P2–P5 | 量·解析·構造·空間（三分野） |
| C 横断応用 | P6–P8 | 離散·数値·統計·ゲーム入口 |

## フェーズ別フック

| P | キー概念 | ノート | 実験 |
|---|----------|------|------|
| 0 | 純粋/応用 · 構造·空間·変化 | `p0-overview.md` | — |
| 1 | 証明技法 · 集合演算 · 量化子 | `foundations-logic.md` | ド・モルガン |
| 2 | 数体系拡張 · 二次方程式 | `foundations-numbers.md` · `algebra.md` | 判別式 |
| 3 | 極限 · 微積 · ODE | `calculus.md` · `analysis.md` | Euler ODE |
| 4 | 行列 · 群 · 数論入口 | `linear-algebra.md` · `number-theory.md` | ガウス · mod-n 群 |
| 5 | 距離 · 角度 · 位相入口 | `geometry-topology.md` | 三角法 |
| 6 | 組合せ · グラフ · 確率 | `discrete-math.md` | BFS · モンテカルロ |
| 7 | 浮動小数 · 数値積分 · RK4 | `applied-mathematical-sciences.md` | 相消誤差 |
| 8 | 記述統計 · 検定 · 回帰 · NE | `probability-statistics.md` | 最小二乗 · Nash |

## 再発防止

1. 各フェーズで **完了条件**（wiki-roadmap）を満たしてから次へ
2. 未検証の主張は notes で Assumption と明記
3. 実験は **最小 Python**（NumPy 中心 · SymPy は代数で）

## Related

- lesson-math-learning-complete
- learning/math/notes/00-index.md
