---
math_doc_id: math.topic.measure_theory
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [measure, lebesgue]
math_doc_regex_file: ^math-doc-measure\-theory\-lebesgue\-integration\.md$
---

<!-- MATH_DOC_ID: math.topic.measure_theory -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# 測度論とルベーグ積分

## 動機

リーマン積分と点wise 極限では次が厳密に扱えない。

- 連続確率で「ランダムな実数がちょうど 1 になる」確率 0 の意味
- 関数列の極限と積分の交換条件
- 広い関数クラス上の積分

ルベーグ測度とルベーグ積分が標準的解答である。

## 可測空間と測度

| 概念 | 定義 |
|------|------|
| σ-代数 ℱ | ∅∈ℱ、補集合閉、可算和閉 |
| 測度 μ | μ(∅)=0、互いに素な可算族で可算加法性 |
| Borel 代数 | 開集合から生成される最小 σ-代数 |
| 可測関数 | f⁻¹(B)∈ℱ（B は Borel 集合） |

ルベーグ測度 m は平行移動不変で m([0,1])=1。正則・平行移動不変・単位立方体=1 な測度は一意（Theorem 6.20 型の結果）。

## 積分の構成

非負の単関数から積分を定義し、一般の可測関数は正部・負部に分解する。リーマン可積分関数はルベーグ可積分で積分値は一致する。

Jordan 測度では [0,1]∩ℚ は不可測だが、ルベーグ測度では可算集合の測度は 0 なので m(ℚ∩[0,1])=0。

## 三大収束定理

| 定理 | 仮定 | 結論 |
|------|------|------|
| 単調収束（MCT） | 0≤f₁≤f₂≤…, f_n→f | ∫f_n→∫f |
| Fatou | f_n≥0 可測 | ∫(liminf f_n) ≤ liminf ∫f_n |
| 優収束（DCT） | f_n→f, \|f_n\|≤g, ∫g<∞ | ∫f_n→∫f |

### 反例：スパイク列

f_n = n·χ_{[0,1/n]} なら ∫f_n=1 だが点wise 極限の積分は 0。Fatou の不等式が strict になる典型例。

### 数値検証

- MCT 例：f_n(x)=min(n,x) on [0,1] → ∫f_n→∫x=1/2
- DCT 例：f_n=sin(nx)/n, |f_n|≤1 → ∫f_n→0（n=1000 で ≈0）

## Riesz 表現

正の線形汎関数 I: C_c(X)→ℝ はある測度 μ で ∫f dμ = I(f) と表せる（null 集合を除き一意）。これが Jordan/Lebesgue 構成の抽象骨格。

## Fubini の注意

∫₀¹∫₀¹ (y²−x²)/(x²+y²)² dxdy = π/4 だが積分順序を入れ替えると −π/4 になる例があり、可積分性・可測性の仮定なしに Fubini は使えない。

## L^p 空間（接続）

ルベーグ積分から L^p ノルムを定義。L^2 は Hilbert 空間 · L^p 完備性は関数解析の出発点。詳細は `math-doc-functional-analysis.md`。
