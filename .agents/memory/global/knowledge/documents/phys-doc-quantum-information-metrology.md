---
phys_doc_id: phys.topic.quantum_metrology
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [metrology, squeezing, caves, interferometry, atomic-clocks]
phys_doc_regex_file: ^phys\-doc\-quantum\-information\-metrology\.md$
---

<!-- PHYS_DOC_ID: phys.topic.quantum_metrology -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 量子情報 · 量子計量（Metrology）

**出典**: [Quantum metrology（Wikipedia）](https://en.wikipedia.org/wiki/Quantum_metrology) · [Caves 1981](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.23.1693)

---

## 1. 量子計量の枠組み

物理パラメータ \(\theta\) を **量子センサー** で推定する。\(N\) 個の量子リソース（光子 · 原子 · イオン）を用い、**量子 Cramér–Rao 下限（QCRB）** が精度の理論限界を与える。

### 1.1 古典限界

独立 \(N\) 回測定の標準誤差:

\[
\Delta\theta \geq \frac{1}{\sqrt{N}\,|\partial_\theta \langle O \rangle|}
\]

**ショットノイズ限界（SQL）**: \(\Delta\theta \propto N^{-1/2}\)。

---

## 2. Caves の量子限界

Caves (1981): **位相測定** において、単独モードの **真空位相ノイズ** が SQL を与える。

### 2.1 Mach–Zehnder 位相推定

入力 |0⟩\(_a\)|0⟩\(_b\) → 50:50 ビームスプリッター → 一方に位相 \(\theta\) → 再結合 → 光子数差 \( \hat{n} = \hat{n}_a - \hat{n}_b \) 測定。

**Heisenberg 限界（HL）**（エンタングル状態）:

\[
\Delta\theta \gtrsim \frac{1}{N}
\]

| 状態 | スケーリング |
|------|--------------|
| コヒーレント | \(N^{-1/2}\)（SQL） |
| NOON, 圧縮 | \(N^{-1}\)（HL に近い） |

### 2.2 QCRB

密度行列 \(\rho_\theta\) の **量子 Fisher 情報（QFI）** \(F_Q\):

\[
F_Q = \text{Tr}(\rho_\theta L^2), \quad \partial_\theta \rho_\theta = \frac{1}{2}(L\rho_\theta + \rho_\theta L)
\]

Cramér–Rao:

\[
(\Delta\theta)^2 \geq \frac{1}{m\, F_Q}
\]

\(m\): 繰り返し回数。**純粋状態** で \(F_Q = 4\,\text{Var}(\hat{h})\)（生成算符 \(\hat{h}\), \(\partial_\theta|\psi\rangle = i\hat{h}|\psi\rangle\)）。

---

## 3. 圧縮光（Squeezed Light）

**Heisenberg 不確定性**:

\[
\Delta X_1 \,\Delta X_2 \geq \frac{1}{4}
\]

（正規化 quadrature \( \hat{X}_1, \hat{X}_2 \)）。**圧縮** は一方の分散を \( \Delta X_1 < 1/2 \) に減らし、位相測定の SQL を突破。

### 3.1 圧縮パラメータ

\[
\hat{X}_1 = \frac{1}{2}(\hat{a} + \hat{a}^\dagger), \quad \hat{X}_2 = \frac{i}{2}(\hat{a}^\dagger - \hat{a})
\]

**圧縮度** \(r\): \(\hat{a}_\text{sq} = \cosh r\,\hat{a} - \sinh r\,\hat{a}^\dagger\)

| 量 | 意味 |
|----|------|
| \(r\) | 圧縮パラメータ |
| 10 dB 圧縮 | \(\Delta X_1 \sim 10^{-0.5}\) 倍 |
| LIGO | 信号周波数帯で squeezed vacuum 注入 |

### 3.2 位相感度

SQL を \(\Delta\theta_\text{SQL} = (N)^{-1/2}\) とすると、**圧縮因子 \(e^{-2r}\)** で:

\[
\Delta\theta \approx e^{-r}\, \Delta\theta_\text{SQL}
\]

---

## 4. 干渉計センシング

### 4.1 原子干渉計

**Ramsey–Bordé · Mach–Zehnder 型**: 原子波束包の位相差 \(\phi = k_\text{eff} \Delta\mathbf{v}\cdot\mathbf{T}\)（\(k_\text{eff}\): 二光子有効波数）。

**原子 Sagnac 干渉計** → 慣性センサ · 重力梯度。

| 系 | 感度 |
|----|------|
| 光 MZ | \(10^{-9}\)–\(10^{-12}\) rad/√Hz |
| 原子 MZ | \(10^{-11}\) rad/√Hz 級 |
| 原子レーザー gyro | ナビゲーション |

### 4.2 重力波検出器

LIGO: **Fabry–Perot + power recycling**、**4 km 腕**、**squeezed light** で shot noise を低減。

**strain 感度**:

\[
h \sim \frac{\Delta L}{L} \sim 10^{-23}/\sqrt{\text{Hz}}
\]

量子限界: **standard quantum limit** → **Heisenberg limit**（将来 ET, Cosmic Explorer）。

### 4.3 量子非破壊（QND）測定

繰り返し測定で **back-action evasion**（spin squeezing in atomic ensembles）→ \(F_Q \propto N^2\) に近づける。

---

## 5. 時計物理学（Clock Physics）

### 5.1 原子時計原理

**Rabi 周波数** \(\omega_0\) と local oscillator の **beat** をフィードバック。**Allan deviation**:

\[
\sigma_y(\tau) = \sqrt{\frac{1}{2(M-1)}\sum_{i=1}^{M-1}(\bar{y}_{i+1}-\bar{y}_i)^2}
\]

| 時計 | 不安定度 \(\sigma_y\) |
|------|----------------------|
| Cs マイクロ波 | \(10^{-15}\) @ 1 day |
| Sr 光学格子 | \(10^{-18}\)–\(10^{-19}\) |
| イオン \(^{27}\text{Al}^+\) | \(10^{-18}\) 級 |

### 5.2 量子限界と Dick 効果

** Dick 限界**: ローカル発振器ノイズが **dead time · 非同期サンプリング** で clock に coupling。

**量子 projection noise**:

\[
\sigma_y \propto \frac{1}{2\pi\nu_0 \sqrt{N\tau}}
\]

\(N\): 原子数、\(\tau\): 平均時間。**spin squeezing** で \(N \to N_\text{eff}\) 改善。

### 5.3 相対論 · 応用

| 応用 | 原理 |
|------|------|
| GPS · GNSS | 相対論補正 |
| 重力ポテンシャル測定 | 一般相対論的 redshift \(\Delta\nu/\nu = \Delta\Phi/c^2\) |
| 定数 drift 探索 | 比較測定 |
| 暗黒物質 |  ultralight field 結合 |

** optical clock network**（光学繊維リンク）で ** geodesy · fundamental physics**。

---

## 6. ベイズ · 実験設計

| 概念 | 内容 |
|------|------|
| QFI | 最適測定基底の理論指標 |
| Adaptive | 測定結果で次の \(\theta\) prior 更新 |
| Robust |  decoherence 下の bounds |

**Noisy metrology**: Markovian dephasing で HL → SQL へ **degradation**。

---

## 7. 記号一覧

| 記号 | 意味 |
|------|------|
| \(F_Q\) | 量子 Fisher 情報 |
| \(N\) | 量子リソース数 |
| \(r\) | 圧縮パラメータ |
| \(\sigma_y(\tau)\) | Allan deviation |
| \(\nu_0\) | 遷移周波数 |
