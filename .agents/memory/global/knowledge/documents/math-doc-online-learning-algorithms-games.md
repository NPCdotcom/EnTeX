---
math_doc_id: math.topic.online_learning_games
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [omd, hedge, fp]
math_doc_regex_file: ^math-doc-online\-learning\-algorithms\-games\.md$
---

<!-- MATH_DOC_ID: math.topic.online_learning_games -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# ゲームにおけるオンライン学習

## 反復ゲームとオンライン学習

各ステップ t でプレイヤーは混合戦略を更新し、利得勾配または最良応答に基づく学習を行う。

## Hedge / FTRL

指数重み更新は外部後悔 O(√T) を保証するが、零和 bilinear ゲームの平均戦略の NE 収束は遅い場合がある。

## Optimistic Mirror Descent (OMD)

g_t^opt = 2g_t − g_{t−1}

零和では反復平均の NE 収束が Hedge より速い（条件付き O(1/T)）。

### Matching pennies（w_r=[3,1], w_c=[1,3], η=0.05）

| T | \|avg−NE\| Hedge | OMD |
|---|------------------|-----|
| 100 | 0.1605 | 0.1412 |
| 400 | 0.0551 | 0.0133 |

対称初期 (1,1) では両者とも即 NE。

## Fictitious Play（仮想プレイ）

各プレイヤーは相手の過去の混合戦略に対する最良応答を繰り返し、経験分布が NE に収束する（零和・協調で性質が異なる）。

協調ゲーム（Stag Hunt、3 人協調）では FP が Hedge より圧倒的に NE に近づく。

| 設定 | FP dist NE | Hedge dist NE |
|------|------------|---------------|
| Stag Hunt 対称 | 0.0000 | 1.0000 |
| 3 人協調 対称 | 0.0000 | 1.5000 |

## 零和での総合比較（定数 η）

| ゲーム | Hedge | OMD |
|--------|-------|-----|
| Matching Pennies T=800 | 0.0248 | 0.0080 |
| RPS 3×3 T=400 | 0.0390 | 0.0200 |

## OGDA / Extragradient

射影勾配降下法は simplex 上で周期軌道を示しうる。Extragradient は 2 段階評価で安定化するが、本検証の matching pennies では OMD が最良。

## ナッシュ均衡選択（協調）

| 介入 | 代表 dist to NE |
|------|-----------------|
| 対称初期分布 | Hedge ≈ 1.0 |
| バイアス付き初期分布 | ≈ 0.005 |
| 構造化バイアス | ≈ 0.06 |
| シグナル + バイアス | FP → 0.000 |

NE 選択は学習規則より初期条件とペイオフ構造が支配的。

## 学習率

η_t = η₀/√t の decay は零和で OMD 優位を失い、協調でも NE 距離を悪化させる。検証設定では定数 η を推奨。

## まとめ

零和 → OMD（定数 η）。協調 → FP。零和での OMD 優位は協調に移植できない。

## Global games と閾値

プレイヤーが私的信号 τ_i を受け、閾値ルールで行動を選ぶ協調モデル。**τ\*** 付近で均衡選択が鋭敏。C35 系の数値実験で Stag Hunt 型ペイオフの閾値挙動を確認。

## マトリクスゲーム拡張（μ パラメータ）

4 人 Stag Hunt 型で利得に μ を導入。**μ = −1** が臨界: 4+μ=3 で Hare 優位 · μ > −1 で FP は Stag へ収束しうる。NE 選択は学習則より **ペイオフ構造** が支配的。

## グラフ上の学習と basin

頂点ごとに FP / Hedge を走らせると、**λ₂**（Fiedler 値 · スペクトルギャップ）と **headroom** = 1 − 2|sym_init − 0.5| の積が basin 脱出指標。

| グラフ | λ₂ | lift×headroom |
|--------|-----|---------------|
| two-block | 低 | 中 |
| random 3-reg | 高 | 高 |
| path P₁₂ | 極低 | ~0 |

λ₂ 単独では不十分 — **headroom**（対称初期分布が未飽和か）と併用。expander はバイアスを洗い流し、path は init 固定に近い。

詳細: `math-doc-graph-theory-extremal-spectral.md` · `math-doc-functional-analysis.md`（拡散・Green 核）
