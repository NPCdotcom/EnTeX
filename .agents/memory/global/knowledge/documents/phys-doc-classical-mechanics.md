---
phys_doc_id: phys.topic.classical_mechanics
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [mechanics, newton, energy, momentum, rotation]
phys_doc_regex_file: ^phys\-doc\-classical\-mechanics\.md$
---

<!-- PHYS_DOC_ID: phys.topic.classical_mechanics -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 古典力学

**出典**: [力学（Wikipedia）](https://ja.wikipedia.org/wiki/力学) · [ニュートンの運動の法則（Wikipedia）](https://ja.wikipedia.org/wiki/ニュートンの運動の法則)

---

## ニュートンの運動 3 法則

| 法則 | 内容 | 記号 |
|------|------|------|
| **第 1 法則（慣性）** | 外力が働かない物体は静止または等速直線運動を続ける | — |
| **第 2 法則** | 加速度は力に比例し、質量に反比例する | **F = ma** |
| **第 3 法則（作用反作用）** | 2 物体間の力は大きさ等しく向き反対 | **F₁₂ = −F₂₁** |

**自由体図（FBD）**: 物体に働く力をすべて矢印で描き、第 2 法則を成分分解して適用する。

---

## 1 次元 · 2 次元運動

### 基本量

| 量 | 記号 | SI 単位 |
|----|------|---------|
| 位置 | **r** | m |
| 速度 | **v** = d**r**/dt | m/s |
| 加速度 | **a** = d**v**/dt | m/s² |

1 次元では `x, v, a` の符号が向きを表す。

### 等加速度運動（1D）

\[
v = v_0 + at, \quad x = x_0 + v_0 t + \tfrac{1}{2} a t^2
\]

### 放物運動（2D、重力のみ）

初速度 \(v_0\)、仰角 \(\theta\)、重力加速度 \(g\)（下向き正とする場合 \(a_y = -g\)）:

\[
x(t) = v_0 \cos\theta \cdot t, \quad y(t) = v_0 \sin\theta \cdot t - \tfrac{1}{2} g t^2
\]

**射程**（同一高度から発射）:

\[
R = \frac{v_0^2 \sin 2\theta}{g}
\]

**最大高度**:

\[
H = \frac{v_0^2 \sin^2\theta}{2g}
\]

---

## 仕事 · エネルギー · 保存則

### 仕事

\[
W = \int \mathbf{F} \cdot d\mathbf{r}
\]

定数力 · 直線変位: \(W = F s \cos\phi\)（\(\phi\) は力と変位のなす角）

### 運動エネルギー · 位置エネルギー

\[
K = \tfrac{1}{2} m v^2, \quad U_g = m g h \quad \text{（重力）}
\]

### 保存則

| 保存量 | 条件 |
|--------|------|
| **力学的エネルギー** \(E = K + U\) | 保存力のみ（非保存力の仕事 = 0） |
| **運動量** \(\mathbf{p} = m\mathbf{v}\) | 外力の合力 = 0 |
| **角運動量** \(\mathbf{L} = \mathbf{r} \times \mathbf{p}\) | 外トルクの合力 = 0 |

**仕事-エネルギー定理**: 保存力に対する仕事 = 位置エネルギーの減少 = 運動エネルギーの増加。

---

## 角運動量 · トルク · 剛体回転

### トルク

\[
\boldsymbol{\tau} = \mathbf{r} \times \mathbf{F}, \quad |\tau| = r F \sin\phi
\]

### 角運動量 · 回転の第 2 法則

\[
\boldsymbol{\tau} = \frac{d\mathbf{L}}{dt}, \quad L = I \omega \quad \text{（定軸回転）}
\]

| 量 | 記号 | 単位 |
|----|------|------|
| 慣性モーメント | \(I\) | kg·m² |
| 角速度 | \(\omega\) | rad/s |
| 回転運動エネルギー | \(K_{\text{rot}} = \tfrac{1}{2} I \omega^2\) | J |

**慣性モーメントの例**:

| 形状 | 回転軸 | \(I\) |
|------|--------|-------|
| 細棒 | 一端固定 | \(\tfrac{1}{3} m L^2\) |
| 円板 | 中心軸 | \(\tfrac{1}{2} m R^2\) |

---

## 単振動 · 減衰振動

### ばね振子（理想）

\(F = -k x\) より \(m \ddot{x} + k x = 0\)、角振動数 \(\omega = \sqrt{k/m}\):

\[
x(t) = A \cos(\omega t + \phi)
\]

| 量 | 式 |
|----|-----|
| 周期 | \(T = 2\pi/\omega = 2\pi\sqrt{m/k}\) |
| 最大速度 | \(v_{\max} = A\omega\) |
| 総エネルギー | \(E = \tfrac{1}{2} k A^2\)（保存） |

### 減衰振動

\(m \ddot{x} + b \dot{x} + k x = 0\)。減衰比 \(\zeta = b/(2\sqrt{mk})\):

| 条件 | 振動の様相 |
|------|------------|
| \(\zeta < 1\) | 減衰振動（振幅が指数減衰） |
| \(\zeta = 1\) | 臨界減衰 |
| \(\zeta > 1\) | 過減衰 |
