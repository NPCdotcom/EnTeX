---
phys_doc_id: phys.topic.electromagnetism
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [electromagnetism, coulomb, gauss, circuits, maxwell]
phys_doc_regex_file: ^phys\-doc\-electromagnetism\.md$
---

<!-- PHYS_DOC_ID: phys.topic.electromagnetism -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 電磁気学

**出典**: [電磁気学（Wikipedia）](https://ja.wikipedia.org/wiki/電磁気学) · [マクスウェルの方程式（Wikipedia）](https://ja.wikipedia.org/wiki/マクスウェルの方程式)

---

## クーロン法則 · 電場 · 電位

### クーロン力

点電荷 \(q_1, q_2\) 間（真空、距離 \(r\)）:

\[
F = k_e \frac{|q_1 q_2|}{r^2}, \quad k_e = \frac{1}{4\pi\varepsilon_0} \approx 8.99\times 10^9\ \text{N·m}^2/\text{C}^2
\]

同性なら反発、異性なら引力。

### 電場

\[
\mathbf{E} = \frac{\mathbf{F}}{q_{\text{test}}}, \quad E = k_e \frac{|Q|}{r^2}\ \text{（点電荷）}
\]

**重ね合わせ**: \(\mathbf{E}_{\text{total}} = \sum \mathbf{E}_i\)

### 電位 · 電位差

\[
V = k_e \frac{Q}{r}, \quad \Delta V = -\int \mathbf{E}\cdot d\mathbf{l}
\]

---

## ガウス法則 · コンデンサ

### ガウス法則

\[
\oint \mathbf{E}\cdot d\mathbf{A} = \frac{Q_{\text{enc}}}{\varepsilon_0}
\]

対称性がある場合、電場を簡単に求められる（球対称 · 円柱 · 無限平面）。

### コンデンサ

平行板（面積 \(A\)、間隔 \(d\)）:

\[
C = \varepsilon_0 \frac{A}{d}, \quad Q = CV, \quad U = \tfrac{1}{2}CV^2
\]

| 接続 | 合成容量 |
|------|----------|
| 直列 | \(1/C = 1/C_1 + 1/C_2\) |
| 並列 | \(C = C_1 + C_2\) |

---

## 電流 · 磁場 · アンペール法則

### 電流

\[
I = \frac{dQ}{dt}, \quad \mathbf{J} = \rho \mathbf{v}\ \text{（電流密度）}
\]

**オーム法則**: \(V = IR\)

### ビオ・サバール · 直線電流

無限長直線電流 \(I\) から距離 \(r\) の磁場:

\[
B = \frac{\mu_0 I}{2\pi r}
\]

### アンペールの法則（静磁）

\[
\oint \mathbf{B}\cdot d\mathbf{l} = \mu_0 I_{\text{enc}}
\]

---

## ファラデー法則 · インダクタンス · 回路

### ファラデーの電磁誘導法則

\[
\mathcal{E} = -\frac{d\Phi_B}{dt}, \quad \Phi_B = \int \mathbf{B}\cdot d\mathbf{A}
\]

### インダクタンス

\[
V_L = -L\frac{dI}{dt}, \quad U_L = \tfrac{1}{2}LI^2
\]

### RC 回路（放電）

\(R\) と \(C\) 直列、初期電圧 \(V_0\):

\[
V(t) = V_0 e^{-t/RC}, \quad \tau = RC
\]

時定数 \(\tau\) は電圧が初期値の \(1/e\) に減衰するまでの時間を表す。

---

## Maxwell 方程式

真空における微分形:

| 名称 | 微分形 | 物理的内容 |
|------|--------|------------|
| **ガウス（E）** | \(\nabla\cdot\mathbf{E} = \rho/\varepsilon_0\) | 電荷が E の源 |
| **ガウス（B）** | \(\nabla\cdot\mathbf{B} = 0\) | 磁気単極子なし |
| **ファラデー** | \(\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t\) | 変動 B が E を誘導 |
| **アンペール・マクスウェル** | \(\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\partial\mathbf{E}/\partial t\) | 電流 · 変動 E が B を誘導 |

積分形は各法則の \(\oint\) / \(\iint\) 表現（ガウス · ストークス定理で対応）。Maxwell 方程式は電磁波の存在を予言し、光が電磁波であることを示す。
