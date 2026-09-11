---
phys_doc_id: phys.topic.lattice_qcd
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [lattice-qcd, gauge-theory, monte-carlo, hadron-masses]
phys_doc_regex_file: ^phys\-doc\-lattice\-qcd\-gauge\-theory\.md$
---

<!-- PHYS_DOC_ID: phys.topic.lattice_qcd -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 格子 QCD · ゲージ理論

**出典**: [格子 QCD（Wikipedia）](https://ja.wikipedia.org/wiki/格子QCD) · [Lüscher formula](https://en.wikipedia.org/wiki/L%C3%BCscher%27s_formula)

---

## 1. QCD の格子定式化

量子色力学（QCD）の経路積分:

\[
Z = \int \mathcal{D}A_\mu\,\mathcal{D}\bar\psi\,\mathcal{D}\psi\; e^{-S_G[A] - S_F[\bar\psi,\psi,A]}
\]

**格子**上でゲージ場 \(U_\mu(x) \in \text{SU}(3)\)（リンク変数）とフェルミオン \(\psi(x)\) を定義し、連続極限 \(a \to 0\) で物理量を取る。\(a\): 格子間隔。

### 1.1 Wilson 作用

\[
S_G = \frac{\beta}{3}\sum_P \text{Re}\,\text{Tr}\left[1 - U_P\right], \quad \beta = \frac{6}{g^2}
\]

\(U_P\): プレイクett（plaquette）周回積。**Wilson ループ** \(\text{Tr}\, W(C)\) はゲージ不変。

| 量 | 格子上 |
|----|--------|
| クォーク confinement | 面積則 \(\langle W\rangle \sim e^{-\sigma A}\) |
| 漸近的自由 | \(g(\mu) \to 0\)（短距離） |

---

## 2. ゲージ理論の基礎

### 2.1 ゲージ対称性

局所 SU(3) 変換 \(\psi \to G(x)\psi\)、\(A_\mu \to G A_\mu G^{-1} + \frac{i}{g}(\partial_\mu G)G^{-1}\) でラグランジアン不変。

**Field strength**（連続）:

\[
F_{\mu\nu}^a = \partial_\mu A_\nu^a - \partial_\nu A_\mu^a + g f^{abc} A_\mu^b A_\nu^c
\]

### 2.2 ループ変数

| ループ | 物理 |
|--------|------|
| プレイクett | 作用の最小単位 |
| \(1\times 1\) Wilson loop | 静的重クォークポテンシャル \(V(R)\) |
| Polyakov loop |  deconfinement 順序パラメータ |

---

## 3. モンテカルロ法

配位 \(\{U,\psi\}\) を **Boltzmann 重み** \(e^{-S}\) に従いサンプリング。

### 3.1 Hybrid Monte Carlo (HMC)

分子動力学 + Metropolis で **詳細釣り合い** を保ちつつ、リンク · フェルミオンを同時更新。フェルミオン行列 \(M^\dagger M\) の逆行列（または force）が必要 → **ランダム推定子**。

### 3.2 更新 algorithm

| 手法 | 用途 |
|------|------|
| Metropolis | 単純だが autocorrelation 長 |
| HMC | 標準（高精度） |
| RHMC | 有理近似で複数味 |

**autocorrelation time** \(\tau_{\text{int}}\): 独立配位に必要な MC ステップ数。物理量の **統計誤差** \(\propto \sqrt{(1+2\tau_{\text{int}})/N}\)。

---

## 4. フェルミオン作用

Wilson フェルミオンは **カイラル対称性を明示的に破る**（\(m_{\text{phys}} \propto 1/a\) の additive mass）。**カイラル fermion** が現代標準。

| 作用 | カイラル対称性 | 備考 |
|------|----------------|------|
| Wilson | 破る | 実装容易 |
| Staggered | 部分的（4 taste） | 軽い quark |
| Domain wall / Overlap | 保つ（exact） | 高コスト |
| Wilson twisted mass | 破る（O(a) 改善） | tmLQCD |

**Staggered** では rooted staggered で taste 簡約。**Möbius domain-wall** は overlap の近似。

フェルミオン行列:

\[
S_F = \bar\psi M[U] \psi, \quad M = \gamma_\mu D_\mu + m
\]

---

## 5. Lüscher 有限体積公式

有限体積 \(L^3\) 内の **2 粒子エネルギー** \(E_n(L)\) から散乱振幅 · 束縛状態質量を抽出。

### 5.1 2 粒子質量

2 粒子の rest frame で **量子化条件**（s-wave 近似）:

\[
p \cot \delta(p) = \frac{1}{L}\sum_{n} \frac{2}{z_n^2 - (pL/2\pi)^2}
\]

\(\delta(p)\): 位相偏移、\(z_n\): 特殊関数零点。 \(E = \sqrt{m_1^2+p^2}+\sqrt{m_2^2+p^2}\) と \(\delta\) が結びつく。

### 5.2 束縛状態 · 共振

\(E_0(L) < m_1 + m_2\) なら bound state。**Lüscher** 拡張で inelastic · 多チャンネルも扱う（Rummukainen–Gottlieb 等）。

| 応用 | 例 |
|------|-----|
| \(\pi\pi\) scattering | \(f_0(500)\), \(\rho\) |
| \(K\pi\) | \(\kappa\) |
| 核力 | HAL QCD（2–3 バリオン） |

---

## 6. ハドロン質量 · 物理量

### 6.1 クォーク質量

格子上の **bare quark mass** \(m_q(a)\) を tune し、**PCAC** や ** Ward identity** で renormalized \(m_q(\mu)\) を得る。

### 6.2 代表計算量

| 量 | 格子 QCD 出力 |
|----|---------------|
| \(m_N, m_\pi, m_K\) | スペクトル |
| \(f_\pi, f_K\) | 弱い崩壊定数 |
| \(\alpha_s(m_Z)\) | Schrödinger functional |
| \(g_A\) | nucleon matrix element |

**continuum extrapolation**: \(a \to 0\) で \(O(a^n)\) 外挿。**Chiral extrapolation**（\(m_q \to m_{\text{phys}}\)）は PT で補正。

### 6.3 典型結果（概念）

\[
\frac{m_N}{m_\rho} \approx 1.22 \quad (\text{実験}), \quad f_\pi \approx 130\,\text{MeV}
\]

 lattice–experiment 一致は **Standard Model** の QCD セクター検証。

---

## 7. 計算資源 · 精度

| 世代 | 特徴 |
|------|------|
| \(N_f=2+1+1\) HISQ | 物理 up, down, strange, charm |
| \(a \sim 0.03\)–0.06 fm | continuum limit |
| \(L \gtrsim 4\) fm | 有限体積修正 |

**FLAG**（Flavour Lattice Averaging Group）が average 値を公開。

---

## 8. 記号一覧

| 記号 | 意味 |
|------|------|
| \(a\) | 格子間隔 |
| \(\beta = 6/g^2\) | ゲージ結合 |
| \(U_\mu(x)\) | SU(3) リンク |
| \(\delta(p)\) | 散乱位相 |
| \(L\) | 有限体積辺長 |
