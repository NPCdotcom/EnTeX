---
math_doc_id: math.topic.graph_theory
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [graphs, spectral]
math_doc_regex_file: ^math-doc-graph\-theory\-extremal\-spectral\.md$
---

<!-- MATH_DOC_ID: math.topic.graph_theory -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# グラフ理論

## グラフの基本

グラフ G=(V,E)。次数、経路、木（n 頂点なら n−1 辺）、完全グラフ K_n。

## 極値グラフ理論

**Turán 定理**：K_r を部分グラフに含まないグラフの辺数最大は Turán グラフ（完全 r-部グラフ）で達成される。

**Ramsey 数** R(3)=6：6 頂点以上の完全グラフは必ず三角形単色モノクローム部分を持つ。

平面グラフは K₅ と K_{3,3} をマイナーとして禁止する（Kuratowski）。

## ラプラシアンと Modularity

グラフ ラプラシアン L = D − A（次数行列 − 隣接行列）。

Modularity（Newman）:

Q = (1/2m) Σ_{ij} [A_{ij} − k_i k_j/(2m)] δ(c_i,c_j)

modularity 行列 B_{ij} = A_{ij} − k_i k_j/(2m) は各行和 0。最大固有値 β₁ の固有ベクトル u₁ の符号で 2 分割するスペクトル法が標準的。

### 数値例（2×K₃ + 橋）

自然な 2 クラスタ分割で Q≈0.265。橋だけで 2 分割すると Q≈0.117 と低下し、クラスタ内密度の優位を modularity が捉えることを確認。

スペクトル分割の Q≈0.266 は貪欲 modularity 最適化と一致。

## F-分解

グラフ G の辺を、部分グラフ F に同型なコピーでちょうど一度ずつ被覆する分解。

- **分数 F-分解**：各辺 e で Σ_{F'∋e} ω(F')=1
- Haxell–Rödl：分数分解 ⇒ 近似分解（未使用辺 o(n²) のみ）
- δ*_{K₃} ≤ (7+√21)/14 ≈ 0.827
- Wilson (1976)：大きな K_n が F-可分割なら F-分解可能

absorber 技法により、近似分解の残り部分を吸収して厳密分解へ拡張するのが現代の標準パイプライン。

## スペクトルギャップと Fiedler ベクトル

グラフ ラプラシアン L の固有値 0 = λ₁ ≤ λ₂ ≤ … ≤ λ_n。

- **λ₂**（Fiedler 値）: 連結性の強さ · mixing 時間 ~ 1/λ₂
- **Fiedler ベクトル** u₂: 符号分割による 2 コミュニティ検出（スペクトル clustering）

### 数値例

| グラフ | λ₂（概算） | 意味 |
|--------|-----------|------|
| path P_n | O(1/n²) | 弱 mixing · init 固定 |
| expander / random d-reg | Ω(1) | 強 mixing |
| two-block + 橋 | 中程度 | コミュニティ間弱結合 |

## ゲーム学習との接続

頂点ごとに Fictitious Play を走らせたとき、**basin 脱出**（対称初期分布から NE へ）の指標:

**lift × headroom** — headroom = 1 − 2|p_init − 0.5|（対称 init の未飽和度）

λ₂ と headroom の相関は正だが **λ₂ 単独では不十分**（path は λ₂ 極小でも headroom 依存）。  
expander 型グラフはバイアス付き init を洗い流しやすい。

Modularity スペクトル法（§ ラプラシアンと Modularity）と Fiedler 分割は同一スペクトル思想の応用。

詳細: `math-doc-online-learning-algorithms-games.md` · `math-doc-functional-analysis.md`
