---
phys_doc_id: phys.topic.cosmic_rays
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [cosmic-rays, pevatron, gzk, fermi, shock-acceleration]
phys_doc_regex_file: ^phys\-doc\-cosmic\-rays\-acceleration\.md$
---

<!-- PHYS_DOC_ID: phys.topic.cosmic_rays -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 宇宙線 · 加速機構

**出典**: [宇宙線（Wikipedia）](https://ja.wikipedia.org/wiki/宇宙線) · [Hillas criterion](https://en.wikipedia.org/wiki/Hillas_criterion) · [GZK cutoff](https://en.wikipedia.org/wiki/Greisen%E2%80%93Zatsepin%E2%80%93Kuzmin_limit)

---

## 1. 宇宙線スペクトル

地球大気に降り注ぐ **高エネルギー粒子**（主に proton）。全方向から **等方的** に入射（磁場乱流による isotropization）。

### 1.1 エネルギー分布

\[
J(E) \propto E^{-\gamma}
\]

| 領域 | スペクトル指数 \(\gamma\) | 特徴 |
|------|---------------------------|------|
| knee 前 | \(\sim 2.7\) | 銀河系起源 |
| knee (\(\sim 3\times10^{15}\) eV) | 急峻化 | 銀河 accelerator 限界? |
| ankle (\(\sim 5\times10^{18}\) eV) | 平坦化 |  extragalactic 混入 |
| GZK | 抑制 | 宇宙マイクロ波背景との相互作用 |

---

## 2. Hillas 基準

粒子が **\(Ze\)** まで加速されるには、加速器の **サイズ \(L\)** と **磁場 \(B\)** が十分大きい必要がある（Hillas 1984）。

### 2.1 最大エネルギー（order-of-magnitude）

\[
E_{\max} \approx Ze\, B\, R
\]

\(R \sim L\): 磁場構造の曲率半径。** Hillas plot**: \(B\) vs \(L\) 上で \(E_{\max}\) 等高線。

| 源 | \(L\) | \(B\) | \(E_{\max}\)（概算） |
|----|-------|-------|---------------------|
| 超新星残骸（SNR） | \(\sim 10\) pc | \(\sim 10\,\mu\)G | PeV 級 |
| パルサー wind nebula | \(\sim 1\) ly | \(\sim 100\,\mu\)G | 100 TeV |
| AGN jet | kpc | mG | EeV?（議論） |
| 磁気乱流 | Mpc | nG | EeV（伝播） |

**PeVatron**: \(E_{\max} \gtrsim 1\) PeV の銀河系 accelerator。HESS · HAWC · LHAASO が **Galactic PeVatron** 候補（例: 銀心 · SNR）を報告。

---

## 3. 衝撃波加速

### 3.1 Fermi 第 1次（ショックドリフト）

粒子が **衝撃波面を往復** し、各 crossing で平均エネルギー gain \(\Delta E/E \sim u_s/c\)（\(u_s\): ショック速度）。

**Test particle** 限界では **指数スペクトル**:

\[
f(E) \propto E^{-\Gamma}, \quad \Gamma = \frac{r + 2}{r - 1 + \Delta}
\]

\(r = u_1/u_2\): 圧縮比（非 relativistic strong shock で \(r=4\) → \(\Gamma \approx 2\)）。

**臨界条件**: 粒子の **Larmor 半径** \(r_L = pc/(ZeB)\) が **ショック幅** \(\lesssim\) 乱流スケール。

### 3.2 Fermi 第 2次（確率的加速）

**乱磁場中の確率的散乱**（Fokker–Planck / diffusion）:

\[
\frac{\partial f}{\partial t} = \frac{\partial}{\partial p}\left[D_{pp}\frac{\partial f}{\partial p}\right] - \frac{\partial}{\partial p}\left[\dot{p}_\text{acc}\, f\right]
\]

**Bohm diffusion**: \(D \propto r_L v\)。平衡スペクトル \(f \propto p^{-s}\)（\(s \sim 4\)–5）。

| Fermi I | Fermi II |
|---------|----------|
| 衝撃波面 | 乱流 · 磁場揺らぎ |
| SNR, リング状構造 | 銀河盤 · halo |
| \(\Gamma \sim 2\) 自然 | より硬いスペクトルも |

### 3.3 非線形効果

**CR feedback**: 加速粒子圧力が **precursor** を形成 → **shock modification**、\(E_{\max}\) 増大 · スペクトル切断。

---

## 4. PeVatrons

### 4.1 銀河系 PeV 源

| 候補 | 証拠 |
|------|------|
| SNR（Tycho, Cas A 近傍） | TeV–PeV γ（Leptonic vs Hadronic 議論） |
| 銀心 | LHAASO PeV γ |
| OB association | 集団 wind · superbubble |
| パルサー周辺 | Leptonic cutoff vs hadronic |

**Hadronic モデル**: \(pp \to \pi^0 \to \gamma\)。**Leptonic**: IC 散乱。** \(\gamma\)–\(p\) 判別** は multi-messenger（中微子 IceCube）が鍵。

### 4.2 knee の起源

**銀河 CR accelerator の最大エネルギー** が knee に対応する説 vs **propagation break** 説。

---

## 5. GZK カットオフ

超高エネルギー宇宙線（UHECR, \(E > 10^{18}\) eV）が **宇宙マイクロ波背景（CMB）** 光子と相互作用:

\[
p + \gamma_{\text{CMB}} \to \Delta^+ \to p + \pi
\]

**Greisen–Zatsepin–Kuzmin (GZK) 限界**: proton の **可観測宇宙** が \(\sim 100\) Mpc に制限（\(E \gtrsim 6\times10^{19}\) eV）。

### 5.1 観測

| 実験 | 結果 |
|------|------|
| HiRes | GZK-like suppression |
| Auger | 北半球 · 組成 \(E\) 依存 |
| Telescope Array | 北天で hard spectrum 続く報告（地域差） |

**Photo-pion 損失**:

\[
\frac{dE}{dt} \approx -c \int n_\gamma \sigma(E_\gamma) E_\gamma \, dE_\gamma
\]

**Pair production**（\(e^+e^-\)）も electron に寄与。

### 5.2 組成

Auger: 高エネルギーで **heavy nuclei**  fraction 増加 → **iron photo-disintegration** も GZK 関連。**混合組成** モデルが propagation を複雑化。

---

## 6. 伝播 · 磁場

| エネルギー | ギリング | 伝播 |
|------------|----------|------|
| GeV–TeV | 小 | 銀河乱流拡散 |
| PeV | 中 | 銀河 halo |
| EeV | 大 | extragalactic · 局所源 |

**拡散係数** \(D(E) = D_0 (E/E_0)^\delta\)。**Anisotropy**（Auger, Telescope Array）から **近傍源** を探索。

---

## 7. 多メッセンジャー

| メッセンジャー | 情報 |
|----------------|------|
| γ 線（CTA, LHAASO） | 加速 site · hadronic |
| 中微子（IceCube） | hadronic CR 直接 |
| UHECR | 源 · 組成 · GZK |
| 電波 · X 線 | SNR shock · 磁場 |

---

## 8. 記号一覧

| 記号 | 意味 |
|------|------|
| \(E_{\max}\) | 最大加速エネルギー |
| \(r_L\) | Larmor 半径 |
| \(u_s\) | ショック速度 |
| \(\Gamma, \gamma\) | スペクトル指数 |
| \(D_{pp}\) | 運動量拡散係数 |
