---
math_doc_id: math.topic.complex_pde
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [pde, complex]
math_doc_regex_file: ^math-doc-complex\-analysis\-pde\.md$
---

<!-- MATH_DOC_ID: math.topic.complex_pde -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# 複素解析と偏微分方程式

## 複素解析の基礎

全純関数は Cauchy-Riemann 方程式を満たす。Cauchy 積分公式と留数定理が解析計算の核心。

## 楕円型：ラプラス方程式

Δu = 0 は定常平衡。Jacobi 反復などの緩和法で境界値問題を近似できる。

## 放物型：熱方程式

u_t = κ Δu。顕式差分は Δt ≤ C(Δx)² の安定性条件を要する。

## 双曲型：波動方程式

u_tt = c² Δu。d'Alembert 解により 1 次元では進行波の重ね合わせ。エネルギー E(t)=∫(u_t²+c²u_x²)dx は保存。

## 一階双曲系

u_t + A u_x = 0。風上差分が基本。Burgers 方程式は Rankine-Hugoniot で衝撃速度を決定する。

圧縮性 Euler 系の数値解法（HLLC · WENO · Sod ベンチマーク · 外部 Clawpack 検証）は `math-doc-numerical-hyperbolic-schemes.md` を参照。
