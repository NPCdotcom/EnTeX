---
phys_doc_id: phys.topic.neutron_stars
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [neutron-star, eos, urca, gw, hyperon, quark]
phys_doc_regex_file: ^phys\-doc\-astrophysics\-neutron\-stars\.md$
---

<!-- PHYS_DOC_ID: phys.topic.neutron_stars -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 中性子星天体物理学

**出典**: [中性子星（Wikipedia）](https://ja.wikipedia.org/wiki/中性子星) · [Tolman–Oppenheimer–Volkoff equation](https://en.wikipedia.org/wiki/Tolman%E2%80%93Oppenheimer%E2%80%93Volkoff_equation)

---

## 1. 中性子星（NS）構造

重力崩壊後に残る **\(M \sim 1.4\,M_\odot\), \(R \sim 10\)–12 km** のコンパクト星。中心密度 \(\rho_c \sim 10^{17}\)–\(10^{18}\) kg/m³。

### 1.1 TOV 方程式

球対称 · 一般相対論的静平衡:

\[
\frac{dP}{dr} = -\frac{G (\varepsilon + P)(m + 4\pi r^3 P/c^2)}{r(r - 2Gm/c^2)}
\]

\[
\frac{dm}{dr} = 4\pi r^2 \varepsilon / c^2
\]

\(P\): 圧力、\(\varepsilon\): エネルギー密度、\(m(r)\):  enclosed mass。

| 領域 | 内容 |
|------|------|
| 地殻 | 原子核 + 電子 |
| 外核 | 超流動 neutron + proton + electron |
| 内核 | 不明（EOS 依存） |

---

## 2. 状態方程式（EOS）

\(P = P(\varepsilon)\) または \(P(n)\) が **質量–半径関係** \(M(R)\) と **最大質量** \(M_{\max}\) を決定する。

### 2.1 ソフト vs 硬

| EOS | \(M_{\max}\) | \(R(M=1.4M_\odot)\) |
|-----|--------------|---------------------|
| ソフト | 低（\(\lesssim 2 M_\odot\)） | 大 |
| 硬 | 高 | 小 |

**GW170817** の tidal deformability \(\Lambda\) が \(R\) を拘束（\(R \sim 13\) km 付近）。

### 2.2 微視模型

| 模型 | 内容 |
|------|------|
| APR, SLy | 核力 + 3-body |
| DBHF | Dirac–Brueckner–Hartree–Fock |
| パラメトリック | piecewise polytrope |

---

## 3. 冷却

新生 NS は **\(T \sim 10^{11}\) K** から **Urca 過程 · 中間子放出 · 超流動性** により冷却。

### 3.1 Urca 過程

**迅速 Urca**（\(\beta\) 平衡で lepton 番号変化）:

\[
n \to p + e^- + \bar\nu_e, \quad p + e^- \to n + \nu_e
\]

**direct Urca** 条件: フェルミ面が proton, electron, neutron で **同時に重なる**（高 \(\rho\) で proton fraction \(x_p\) 増加時）。

冷却率:

\[
\frac{dU}{dt} \propto T^6 \quad (\text{direct Urca})
\]

| 過程 | 温度依存 | 効率 |
|------|----------|------|
| direct Urca | \(T^6\) | 非常に高 |
| modified Urca | \(T^8\) | 中 |
| 中間子 Urca | \(T^6\)–\(T^8\) | 高（許容時） |
| 超流動ギャップ | 抑制 | 低温で急減 |

### 3.2 観測

**Chandra · NICER** の表面温度 \(T_s\)–年齢関係が **superfluid gap · fast cooling 源（Cas A 等）** を示唆。

---

## 4. 合体 · 重力波信号

### 4.1 BNS 合体

**バイナリ中性子星（BNS）** 合体は **kilonova**（r-process 元素）+ **短時間 γ 線バースト** + **GW** を産む。

**GW170817**（2017）: \(M_{\text{tot}} \approx 2.74 M_\odot\)、**潮汐効果** が inspiral 位相の位相に imprints。

### 4.2 潮汐 deformability

Quadrupole tidal deformability:

\[
\Lambda = \frac{2}{3} k_2 \left(\frac{R}{GM/c^2}\right)^5
\]

\(k_2\): Love number。** \(\Lambda_1, \Lambda_2\) ** から EOS 族を絞る。

| 信号 | 周波数帯 | 情報 |
|------|----------|------|
| inspiral | 数十–数千 Hz | \(M, \Lambda\) |
| merger | kHz | 不安定性 · EOS |
| post-merger | kHz | 超巨大核 · quark? |

### 4.3 残留天体

合体後 **超巨大中性子星** または **ブラックホール** 即座形成。\(M_{\text{rem}} \gtrsim M_{\max}\) で BH。

---

## 5. ハイパロン · クォーク物質の示唆

核密度を超えると **新自由度** が開く可能性。

### 5.1 ハイパロン（Hyperons）

\(\Lambda, \Sigma, \Xi\) 等が **閾値密度** \(n_H\) 以上で現れる。

| 効果 | 結果 |
|------|------|
| 追加圧力 | EOS ソフト化 |
| \(M_{\max}\) 低下 | 2 \(M_\odot\) pulsar との緊張 |
| 超流動ハイパロン | 冷却 · GW への影響 |

**Pulsar PSR J0740+6620** (\(\sim 2.08 M_\odot\)) は **硬い EOS · hyperon 抑制**（hyperon puzzle）を議論させる。

### 5.2 クォーク物質

**Quark–hadron transition**（1 次 or crossover）:

| 相 | 内容 |
|----|------|
|  hadronic | n, p, \(\pi\), hyperons |
| 2SC / CFL | 色超伝導 quark |

**Quark star** 仮説: 全体または core が **free quark**。表面で hadronic shell。**第三 family**  compact star。

観測的ヒント（議論中）:

| 現象 | 解釈 |
|------|------|
| post-merger GW 持続 | 柔らかい core · quark |
| NICER \(R\) | 中程度硬さ |
| GW190425 | 重 BNS? |

---

## 6. 観測プローブ

| 手段 | 物理量 |
|------|--------|
| 電波パルサー | \(M\)（Shapiro delay） |
| NICER | \(R(M)\)（pulse profile） |
| LIGO–Virgo–KAGRA | \(\Lambda\), \(M_{\max}\) |
| X-ray timing | \(T_s\), 超流動 |
| 重力レンズ | 孤立 NS |

---

## 7. 記号一覧

| 記号 | 意味 |
|------|------|
| \(M_\odot\) | 太陽質量 |
| \(\varepsilon, P\) | エネルギー密度 · 圧力 |
| \(\Lambda\) | 潮汐 deformability |
| \(k_2\) | 2 次 Love number |
| \(x_p\) | proton fraction |
