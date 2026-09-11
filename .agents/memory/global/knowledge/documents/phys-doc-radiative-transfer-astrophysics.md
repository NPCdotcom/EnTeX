---
phys_doc_id: phys.topic.radiative_transfer
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [rt, mcrt, fld, ali, vet, exoplanet]
phys_doc_regex_file: ^phys\-doc\-radiative\-transfer\-astrophysics\.md$
---

<!-- PHYS_DOC_ID: phys.topic.radiative_transfer -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 放射輸送 · 天体物理学

**出典**: [放射輸送方程式（Wikipedia）](https://en.wikipedia.org/wiki/Radiative_transfer) · [Radiation hydrodynamics](https://en.wikipedia.org/wiki/Radiation_hydrodynamics)

---

## 1. 放射輸送方程式（RTE）

周波数 \(\nu\)、方向 \(\mathbf{n}\)、位置 \(\mathbf{r}\) における **比強度** \(I_\nu(\mathbf{r},\mathbf{n})\) の変化:

\[
\frac{1}{c}\frac{\partial I_\nu}{\partial t} + \mathbf{n}\cdot\nabla I_\nu = -\kappa_\nu \rho I_\nu + j_\nu + \frac{\kappa_\nu \rho}{4\pi} B_\nu(T)
\]

| 記号 | 意味 |
|------|------|
| \(\kappa_\nu\) | 不透明度（質量あたり） |
| \(\rho\) | 質量密度 |
| \(j_\nu\) | 放射源項 |
| \(B_\nu(T)\) | Planck 関数 |

**定常 · 1D 平面平行**（光学深度 \(\tau_\nu\)）:

\[
\frac{dI_\nu}{d\tau_\nu} = -I_\nu + S_\nu, \quad S_\nu = \frac{j_\nu}{\kappa_\nu \rho} + B_\nu(T)
\]

\(S_\nu\): **ソース関数**。

### 1.1 Planck 関数

\[
B_\nu(T) = \frac{2h\nu^3}{c^2}\frac{1}{e^{h\nu/k_B T} - 1}
\]

### 1.2 光学深度 · Eddington 近似

\[
\tau_\nu = \int \kappa_\nu \rho\, ds
\]

Eddington 近似: \(J_\nu \approx B_\nu(T)\)（深い光学厚）。薄い場合は **表面温度–効果温度** 関係が重要。

---

## 2. モーメント方程式

\(I_\nu\) を角度積分して **0 次 · 1 次モーメント**:

\[
\frac{\partial J_\nu}{\partial t} + c\,\nabla\cdot\mathbf{F}_\nu = c\,\kappa_\nu \rho (S_\nu - J_\nu)
\]

\[
\frac{\partial \mathbf{F}_\nu}{\partial t} + c\nabla\cdot\mathbf{P}_\nu = -c\kappa_\nu \rho \mathbf{F}_\nu
\]

| 量 | 定義 |
|----|------|
| \(J_\nu = \oint I_\nu\, d\Omega / 4\pi\) | 平均強度 |
| \(\mathbf{F}_\nu = \oint I_\nu \mathbf{n}\, d\Omega\) | フラックス |
| \(\mathbf{P}_\nu\) | 放射圧テンソル |

**閉じ込め問題**: \(\mathbf{P}_\nu\) を \(J_\nu\) で閉じる関係（Eddington \(P = J/3\) など）が必要。

---

## 3. ALI · VET（多線 · 角度分解）

### 3.1 NLTE と ALI

**非局部熱平衡（NLTE）** では \(S_\nu \neq B_\nu(T)\)。**Accelerated Lambda Iteration (ALI)** は従来 Lambda iteration の収束遅延を改善する。

Lambda 更新:

\[
S_\nu^{(k+1)} = \frac{S_\nu^{\text{tot}} - \alpha_\nu J_\nu^{(k)}}{1 - \alpha_\nu \partial J_\nu / \partial S_\nu}
\]

\(\alpha_\nu\): **Lambda 因子**（局所 coupling）。ALI は \(\partial J/\partial S\) を近似的に含め **O(N)** で高速収束。

### 3.2 VET（Variable Eddington Tensor）

角度依存性を **Variable Eddington Tensor (VET)** \(\mathbf{f}_\nu = \mathbf{P}_\nu / J_\nu\) で表現:

\[
\nabla\cdot\mathbf{F}_\nu = -c\kappa_\nu \rho (J_\nu - S_\nu)
\]

\(\mathbf{f}_\nu\) は短特性法 · ray-by-ray で更新。恒星大気 · 降着円盤で標準。

| 手法 | 長所 | 短所 |
|------|------|------|
| Lambda iteration | 単純 | 収束遅い |
| ALI | 高速 NLTE | 実装複雑 |
| VET | 角度依存 | メモリ大 |

---

## 4. モンテカルロ放射輸送（MCRT）

確率的に光子（またはパケット）を追跡。**複雑幾何 · 散乱 · 偏光** に強い。

### 4.1 基本手順

1. ソースからパケット放出（周波数 · 方向サンプリング）
2. 自由行程 \(\tau = -\ln\xi\) まで移動
3. 吸収 · 散乱 · 再放出（\(S_\nu\) に従う）
4. 検出器 · 脱出で寄与を累積

### 4.2 分散 · ノイズ

分散 \(\propto 1/\sqrt{N_{\text{packets}}}\)。**重要性サンプリング · 偏り削減** で効率化。

| 用途 | 例 |
|------|-----|
| 星間ダスト | 銀河 SED |
| AGN トーラス | 赤外 SED |
| 超新星残骸 | 非平衡線 |

---

## 5. FLD（Flux-Limited Diffusion）— RHD 向け

**放射流体力学（RHD）** では RTE 全解は高コスト。**Flux-Limited Diffusion (FLD)** は拡散極限と自由流極限を滑らかに接続:

\[
\mathbf{F}_\nu = -\frac{c}{3\kappa_\nu \rho} \Lambda(\chi) \nabla J_\nu
\]

\(\chi = |\nabla J| / (\kappa \rho J)\): **光学的厚さパラメータ**、\(\Lambda(\chi)\): ** flux limiter**（例: Bruenn, Levermore–Pomraning）。

| \(\chi\) | 極限 |
|----------|------|
| \(\chi \ll 1\) | 拡散 \(\mathbf{F} \propto -\nabla J\) |
| \(\chi \gg 1\) | 自由流 \(\mathbf{F} \approx c J \mathbf{n}\) |

**灰色 FLD**（\(\int J_\nu d\nu\)）は超新星 · 恒星進化コード（例: FLASH, Vulcan）で標準。

---

## 6. 系外惑星大気 RT

透過 · 放射スペクトルから **大気組成 · 温度–圧力構造** を推定する。

### 6.1 透過スペクトル

恒星半径 \(R_\*\)、惑星半径 \(R_p\)、大気スケール高 \(H\):

\[
\frac{\Delta F}{F} \approx \left(\frac{R_p}{R_\*}\right)^2 e^{-(\tau_{\text{cloud}} + \tau_\lambda)}
\]

**Robin–Leiter · 指数モデル** で \(\tau_\lambda\)（分子吸収）を畳み込み。

### 6.2 放射スペクトル · リング

惑星からの **thermal emission**:

\[
F_\oplus(\lambda) = \pi \left(\frac{R_p}{d}\right)^2 B_\lambda(T_{\text{eff}}) \cdot \text{transmission}(\lambda)
\]

**相関マップ法（CRM）** · **cross-correlation spectroscopy** で CO\(_2\), H\(_2\)O 等を検出（JWST 時代）。

### 6.3 散乱 · 雲

| 効果 | モデル |
|------|--------|
| Rayleigh | \(\tau \propto \lambda^{-4}\) |
| Mie（雲） | 粒子サイズ分布 |
| ホットジュピター | 昼夜温度差 · 風 |

**retrieval** コード（PetitRADTRANS, Exo-REM, ARCiS）: ベイズ · MCMC で \(T-P\) profile, [X/H], C/O を推定。

---

## 7. 手法比較

| 手法 | 幾何 | NLTE | 計算コスト |
|------|------|------|------------|
| 短特性 + ALI/VET | 1D–2D | ○ | 中 |
| MCRT | 任意 3D | ○ | 高（並列可） |
| FLD | 3D RHD | △（灰色） | 低–中 |
| 系外惑星 retrieval | 1D 大気 | △ | 中（逆問題） |

---

## 8. 記号一覧

| 記号 | 意味 | SI |
|------|------|-----|
| \(I_\nu\) | 比強度 | W m⁻² sr⁻¹ Hz⁻¹ |
| \(\kappa_\nu\) | 不透明度 | m² kg⁻¹ |
| \(\tau_\nu\) | 光学深度 | 無次元 |
| \(J_\nu, \mathbf{F}_\nu\) | モーメント | — |
| \(B_\nu(T)\) | Planck 関数 | — |
