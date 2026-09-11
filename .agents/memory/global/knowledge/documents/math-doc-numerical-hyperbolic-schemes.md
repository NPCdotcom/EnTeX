---
math_doc_id: math.topic.hyperbolic_numerical
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [hyperbolic, weno, hllc]
math_doc_regex_file: ^math-doc-numerical\-hyperbolic\-schemes\.md$
---

<!-- MATH_DOC_ID: math.topic.hyperbolic_numerical -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# 双曲型保存則の数値解法

## 双曲型保存則

圧縮性 Euler 方程式は質量・運動量・エネルギーを保存する双曲系。弱解では Rankine-Hugoniot 条件とエントロピー条件が衝撃速度を決定する。

風上差分、Lax-Friedrichs（数値粘性大）、Lax-Wendroff（2 次だが Gibbs 振動）、TVD リミター（minmod, van Leer）がスカラー移流の段階的発展。

## Riemann 解法器と Sod 問題

**HLLC** は接触不連続を扱う Riemann 解法器。**1 次 HLLC** は Sod ショック管の内部参照解として grid 収束が確認されている。

### Sod（nx=200, t=0.2, Toro 厳密解, L1 in rho）

| 方式 | L1 rho | vs 1st |
|------|--------|--------|
| 1st HLLC | 0.012092 | 1.00 |
| MUSCL-HLLC | 0.021041 | 1.74× |
| primitive PP WENO-Z | 0.045317 | 3.75× |
| conserved PP WENO-Z | 0.066531 | 5.50× |

### エントロピー波（nx=100, t=0.5）

| 方式 | L1 rho |
|------|--------|
| scalar WENO-Z（decoupled） | 0.005282 |
| 1st HLLC | 0.009986 |
| primitive PP WENO-Z | 0.157337 |

### Grid 収束（1st HLLC, Sod）

| nx | L1 rho |
|----|--------|
| 50 | 0.0289 |
| 100 | 0.0193 |
| 200 | 0.0121 |
| 400 | 0.0076 |

約 1.6 倍の grid 細分化ごとに誤差減少（1 次収束に近い）。

## WENO-Z と系結合

スカラー移流 u_t+u_x=0、周期 [0,1]、u(x,0)=1+0.2 sin(2πx)、厳密解 u(x,t)=1+0.2 sin(2π(x−t))。

WENO-Z の L1≈0.0053 は 1 次 upwind 0.0073 より約 28% 良い。しかし同じ再構成を Euler 系に結合（原始 PP、conserved PP、特性変数）しても Sod / エントロピー波で 1st HLLC を下回れない。

**結論**：ボトルネックは WENO 重みではなく系結合パイプライン。スカラー decouple のみ高次が有効。1st HLLC は自前実装の信頼できるベンチマーク。

## 外部ソルバ（Clawpack）

| 環境 | 結果 |
|------|------|
| Windows pip / conda-forge | 不可（Fortran ビルド · win-64 なし） |
| WSL Ubuntu + conda-forge 5.9 | **利用可**（`clawpack.riemann` の euler_hllc_1D / euler_hll_1D） |

Godunov フラックス: F_hat = F(q_r) − apdq（classic 規約）。

### Sod 外部比較（t=0.2, nx=200, Toro 厳密解）

| ソルバ | L1 rho |
|--------|--------|
| 自前 1st HLLC（Toro） | 0.012092 |
| clawpack HLLC | 0.011627 |
| clawpack HLL | 0.012270 |

clawpack HLLC は Einfeldt 速度の別実装（Toro HLLC と面フラックスは一致しない）だが、L1 は同オーダー — **外部クロスチェック成立**。PyClaw は conda 解決不可だが riemann モジュールで Sod 比較に十分。

### スカラー WENO-Z 拡張（nx≤1600）

t=0.5 · 周期境界 · 参照 L1≈0.0053（nx=100）。nx 200→400 で ratio≈2（高次 decay）。nx=800 付近は周期境界の数値ノイズに注意。
