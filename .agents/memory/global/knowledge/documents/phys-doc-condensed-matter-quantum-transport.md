---
phys_doc_id: phys.topic.condensed_matter
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [condensed-matter, band-theory, kondo, topological, majorana]
phys_doc_regex_file: ^phys\-doc\-condensed\-matter\-quantum\-transport\.md$
---

<!-- PHYS_DOC_ID: phys.topic.condensed_matter -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 凝縮系 · 量子輸送

**出典**: [バンド理論（Wikipedia）](https://ja.wikipedia.org/wiki/バンド理論) · [トポロジカル絶縁体（Wikipedia）](https://ja.wikipedia.org/wiki/トポロジカル絶縁体)

---

## 1. バンド理論

固体中の電子は周期ポテンシャル \(V(\mathbf{r}+\mathbf{R})=V(\mathbf{r})\) 下で **ブロッホ定理** に従う:

\[
\psi_{n\mathbf{k}}(\mathbf{r}) = e^{i\mathbf{k}\cdot\mathbf{r}} u_{n\mathbf{k}}(\mathbf{r}), \quad u_{n\mathbf{k}}(\mathbf{r}+\mathbf{R}) = u_{n\mathbf{k}}(\mathbf{r})
\]

\(n\): バンド指数、\(\mathbf{k}\): 波数ベクトル。

### 1.1 エネルギーバンド

| 概念 | 内容 |
|------|------|
| 価電子帯 | 最高 occupied バンド |
| 伝導帯 | 最低 unoccupied バンド |
| バンドギャップ \(E_g\) | 絶縁体 · 半導体の分類 |
| フェルミ面 | \(E_F\) と等エネルギー面 |

**半金属 · 半導体 · 絶縁体**:

| 材料 | \(E_g\) | 電子密度（300 K） |
|------|---------|-------------------|
| 金属 | 0 | \(\sim 10^{28}\) m⁻³ |
| 半導体 | 0.1–4 eV | 本征 \(\sim 10^{16}\) m⁻³ |
| 絶縁体 | > 4 eV | 極小 |

### 1.2 有効質量

\[
\frac{1}{m^*} = \frac{1}{\hbar^2}\frac{\partial^2 E}{\partial k^2}
\]

バンド曲率から **有効質量 \(m^*\)** を定義。輸送現象（ドリフト · ホール効果）に現れる。

---

## 2. 量子輸送の基礎

### 2.1 ボルツマン方程式

分布関数 \(f(\mathbf{r},\mathbf{k},t)\) の時間発展:

\[
\frac{\partial f}{\partial t} + \mathbf{v}\cdot\nabla_{\mathbf{r}} f + \frac{e}{\hbar}(\mathbf{E}+\mathbf{v}\times\mathbf{B})\cdot\nabla_{\mathbf{k}} f = \left(\frac{\partial f}{\partial t}\right)_{\text{coll}}
\]

### 2.2 電気伝導率

Drude 模型（緩和時間 \(\tau\)）:

\[
\sigma = \frac{n e^2 \tau}{m^*}
\]

**Landauer–Büttiker 公式**（1 次元 conductor）:

\[
G = \frac{2e^2}{h} \sum_n T_n
\]

\(T_n\): 第 \(n\) チャンネルの透過率。量子化 conductance \(G_0 = 2e^2/h\)。

| 現象 | 特徴 |
|------|------|
| 整数 QHE | \( \sigma_{xy} = \nu e^2/h \)（\(\nu\) 整数） |
| Shubnikov–de Haas | 磁場振動（フェルミ面断面積） |
| 弱局在 | 2D 系の \(\ln T\) 抵抗 |

---

## 3. 近藤効果（Kondo Effect）

磁性不純物（スピン \(S=1/2\)）が金属中に埋め込まれると、低温で ** resistivity の \(\ln T\) 上昇** が観測される（Kondo 1964）。

### 3.1 ハミルトニアン

Anderson / Kondo 模型:

\[
H = \sum_{\mathbf{k}\sigma} \varepsilon_{\mathbf{k}} c_{\mathbf{k}\sigma}^\dagger c_{\mathbf{k}\sigma} + J \mathbf{S}\cdot\mathbf{s}(0)
\]

\(\mathbf{s}(0)\): 不純物位置の伝導電子スピン密度、\(J\): 反強磁性交換。

### 3.2 Kondo 温度

\[
k_B T_K \sim D \exp\left(-\frac{1}{J\rho(E_F)}\right)
\]

\(\rho(E_F)\): フェルミ準位状態密度、\(D\): バンド幅。

| \(T \gg T_K\) | \(T \ll T_K\) |
|---------------|---------------|
| 磁性モーメント自由 | スピン singlet 形成 |
| \(\Delta\rho \propto \ln T\) | Fermi 液体（重い準粒子） |

**Kondo 格子**（Ce, Yb 化合物）→ **重いフェルミオン** → 非従来超伝導 · 量子臨界点。

---

## 4. トポロジカル物質入門

### 4.1 トポロジカル不変量

バンド構造の **Chern 数** \(\mathcal{C}\) や **\(Z_2\) 指標** は adiabatic 変形で変わらない整数（または mod 2）。

**Chern insulator**（2D）:

\[
\sigma_{xy} = \mathcal{C}\,\frac{e^2}{h}
\]

境界に **手性エッジ状態**（バルク–境界対応）。

### 4.2 トポロジカル絶縁体（TI）

| 次元 | 代表 | 境界状態 |
|------|------|----------|
| 2D | HgTe QW | スピン Helical エッジ |
| 3D | Bi\(_2\)Se\(_3\) | ディラック表面 |

**\(Z_2\) 分類**: 時間反転対称性を保ちつつ \(\mathcal{C}=0\) でも非自明。

### 4.3 Weyl · Dirac 半金属

バルクに **Weyl / Dirac 点**（3D では対で現れる）。異常 Hall · chiral anomaly · 非reciprocal transport。

---

## 5. Majorana ゼロモード入門

### 5.1 Majorana フェルミオン

Majorana 演算子 \(\gamma = \gamma^\dagger\) は **自分自身の Hermite 共役**。1 つの Dirac フェルミオンは 2 つの Majorana に分解:

\[
\psi = \gamma_1 + i\gamma_2
\]

### 5.2 トポロジカル超伝導体

**p-wave 超伝導**（例: Kitaev chain 模型）:

\[
H = -t\sum_i (c_i^\dagger c_{i+1} + h.c.) - \mu\sum_i c_i^\dagger c_i + \Delta\sum_i (c_i c_{i+1} + h.c.)
\]

トポロジカル相（\(|\mu| < 2t\)）では端点に **Majorana ゼロエネルギー準位** \(\gamma_L, \gamma_R\)。

| 条件 | 結果 |
|------|------|
| \(\mu^2 < 4t^2\) | トポロジカル |
| Majorana ペア | 非 Abel 統計（braiding） |

### 5.3 実験系

| 系 | 実装 |
|----|------|
| 半導体ナノワイヤ + s-wave SC | Rashba + 磁場 → 有効 p-wave |
| トポロジカル Insulator + SC | 表面 Dirac → Majorana |
| vortex core | Fu–Kane 提案 |

**ゼロバイアス conductance peak** が Majorana のシグネチャ候補だが、通常 Andreev 準位との区別は困難（誤信号問題）。

---

## 6. 実験技法

| 手法 | 測定量 |
|------|--------|
| ARPES | バンド構造 \(E(\mathbf{k})\) |
| STM/STS | 表面状態 · ギャップ |
| 量子振動 | フェルミ面 |
| 輸送（lock-in） | \(\rho, \sigma_{xy}, S\) |

---

## 7. 記号一覧

| 記号 | 意味 |
|------|------|
| \(E_g\) | バンドギャップ |
| \(m^*\) | 有効質量 |
| \(T_K\) | Kondo 温度 |
| \(\mathcal{C}\) | Chern 数 |
| \(G_0 = 2e^2/h\) | 量子化 conductance |
