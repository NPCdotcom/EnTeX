---
phys_doc_id: phys.topic.waves_oscillations
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [waves, oscillations, superposition, standing_waves, doppler]
phys_doc_regex_file: ^phys\-doc\-waves\-oscillations\.md$
---

<!-- PHYS_DOC_ID: phys.topic.waves_oscillations -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 波動 · 振動

**出典**: [波動（Wikipedia）](https://ja.wikipedia.org/wiki/波動) · [定在波（Wikipedia）](https://ja.wikipedia.org/wiki/定在波)

---

## 正弦波 · 位相

進行波（+x 方向）:

\[
y(x,t) = A \sin(kx - \omega t + \phi)
\]

| 記号 | 意味 | 関係 |
|------|------|------|
| \(A\) | 振幅 | — |
| \(k = 2\pi/\lambda\) | 波数 | 波長 \(\lambda\) |
| \(\omega = 2\pi f\) | 角振動数 | 周波数 \(f\) |
| \(v = \lambda f = \omega/k\) | 波の速度 | — |
| \(\phi\) | 初期位相 | 2 波の位相差 |

---

## 重ね合わせの原理

線形媒質では **独立な波は互いに干渉せず通り抜ける**（重ね合わせの原理）。合成波は各波の和:

\[
y_{\text{total}} = y_1 + y_2 + \cdots
\]

### 同振幅 · 同周波数

\(y_1 = A\sin(\omega t)\), \(y_2 = A\sin(\omega t + \Delta\phi)\):

\[
y_{\text{total}} = 2A\cos(\Delta\phi/2)\,\sin(\omega t + \Delta\phi/2)
\]

| 位相差 | 結果 |
|--------|------|
| \(\Delta\phi = 0, 2\pi n\) | **強め合い**（振幅 \(2A\)） |
| \(\Delta\phi = \pi, (2n+1)\pi\) | **打ち消し合い**（振幅 0） |

---

## 定在波

振幅等しい進行波 2 本が逆向きに重なる:

\[
y_1 = A\sin(kx - \omega t), \quad y_2 = A\sin(kx + \omega t)
\]

\[
y = 2A\sin(kx)\cos(\omega t)
\]

| 概念 | 条件 · 意味 |
|------|-------------|
| **節（node）** | \(\sin(kx)=0\) → 振幅常に 0 |
| **腹（antinode）** | \(|\sin(kx)|=1\) → 振幅最大 \(2A\) |
| **両端固定弦** | \(L = n\lambda/2\)（\(n=1,2,\ldots\)） |

---

## 音波 · ドップラー効果

### 音の速度

理想気体中の音速:

\[
v_{\text{sound}} \approx \sqrt{\gamma R T / M}
\]

\( \gamma \): 比熱比, \(R\): 気体定数, \(T\): 絶対温度, \(M\): モル質量

### ドップラー効果

観測周波数 \(f'\)（音源速度 \(v_s\)、観測者速度 \(v_o\)、音速 \(v\)、音源周波数 \(f\)）:

\[
f' = f \cdot \frac{v \pm v_o}{v \mp v_s}
\]

符号は「互いに近づく」場合に \(f' > f\) となるよう選ぶ。音源と観測者の相対運動により、観測される周波数が変化する。

| 状況 | 効果 |
|------|------|
| 互いに近づく | 周波数上昇（音は高く聞こえる） |
| 互いに遠ざかる | 周波数低下（音は低く聞こえる） |
