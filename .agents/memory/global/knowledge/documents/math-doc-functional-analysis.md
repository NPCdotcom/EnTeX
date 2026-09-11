---
math_doc_id: math.topic.functional_analysis
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [functional-analysis, lp-spaces, sobolev]
math_doc_regex_file: ^math-doc-functional\-analysis\.md$
---

<!-- MATH_DOC_ID: math.topic.functional_analysis -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# 関数解析

**MSC**: 46 · 47  
**前提**: `math-doc-measure-theory-lebesgue-integration.md` · `math-doc-linear-algebra.md`

---

## Banach 空間と Hilbert 空間

完備ノルム空間を **Banach 空間**、内積完備空間を **Hilbert 空間** という。L^p(Ω) は測度論的積分と結合した標準例。

## L^p 空間

| 空間 | ノルム | 完備性 |
|------|--------|--------|
| L^p(Ω, μ), 1≤p<∞ | ‖f‖_p = (∫|f|^p dμ)^{1/p} | Banach |
| L^∞ | ess sup | Banach |
| L^2 | 内積 ⟨f,g⟩ = ∫f ḡ dμ | Hilbert |

**Hölder**: 1/p + 1/q = 1 ⇒ |∫fg| ≤ ‖f‖_p ‖g‖_q  
**Minkowski**: ‖f+g‖_p ≤ ‖f‖_p + ‖g‖_p

L^p は p ∈ [1,∞) で完備（Riesz–Fischer）。C_c が L^p で稠密（p<∞）。

## 基本定理

- **Cauchy–Schwarz**: |⟨x,y⟩| ≤ ‖x‖‖y‖（Hilbert 空間）
- **Hahn–Banach**: 部分空間上の有界線形汎関数を全体へ延長（1 次形式の存在）
- **Riesz 表現**: Hilbert 上の連続線形汎関数は内積で表せる
- **Banach–Steinhaus · 開写像 · 閉グラフ**: 有界性と連続性の橋渡し

## Sobolev 空間 H^1（入口）

Ω ⊆ ℝ^n 開集合について:

H^1(Ω) = { u ∈ L^2(Ω) : ∂_i u ∈ L^2(Ω) 弱意味 }

弱導関数は分布論的定義。**Rellich–Kondrachov**: 有界領域で H^1 ↪ L^2 がコンパクト（境界条件付き版も重要）。

## コンパクト作用素

T: X → Y がコンパクト ⇔ 単位球の像が相对コンパクト。

- **Hilbert–Schmidt · トレース級**: L^2 核積分演算子の標準例
- **Green 核**: グラフ上ラプラシアンの擬逆は有限グラフで **コンパクト作用素**（スペクトル離散化）
- コンパクト自己共役作用素: スペクトル定理の無限次元版 · 固有値列が 0 に収束

## スペクトル半径と拡散

離散ラプラシアン L = D − A の最大固有値は 0 · 2 番目 λ₂ が mixing 時間スケールを規定。  
連続拡散 u_t = κΔu の半群 e^{κtΔ} とグラフ random walk は同一スペクトル構造の離散版。

**横断接続**: λ₂（グラフ）↔ basin 脱出（ゲーム学習）↔ 拡散モード（PDE）— `math-doc-graph-theory-extremal-spectral.md` · `math-doc-online-learning-algorithms-games.md`

---

## 推奨文献

Teschl, *Functional Analysis* · Evans, *Partial Differential Equations*（Sobolev 章）
