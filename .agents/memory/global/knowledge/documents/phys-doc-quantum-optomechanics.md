---
phys_doc_id: phys.topic.optomechanics
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [cavity, matter-wave, maqro]
phys_doc_regex_file: ^phys\-doc\-quantum\-optomechanics\.md$
---

<!-- PHYS_DOC_ID: phys.topic.optomechanics -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 量子オプトメカニクス

量子オプトメカニクスは、光学共振器と機械振動子の radiation pressure 結合により、マクロscopic 物体の **量子状態制御 · 量子計測 · 重力量子実験** を可能にする。sideband resolved 領域 · 統一量子標準 · 大質量 matter-wave 干渉 · LIGO back-action cancellation · 集積フォトニクス · 宇宙空間デコヒーレンス試験（MAQRO）が現場の主要フロンティアである。

---

## 1. 空洞オプトメカニクス — sideband resolved

### 1.1 結合ハミルトニアン

単一モード cavity 場 a と機械モード b の相互作用:

H/ℏ = ω_c a†a + ω_m b†b + g₀ a†a (b + b†)

g₀ = (ω_c / L) x_zpf は vacuum optomechanical coupling rate。sideband parameter η = ω_m / κ（κ: cavity linewidth）により動作領域が分類される。

### 1.2 Sideband resolved 条件

**η > 1**（resolved sideband limit）では、赤側バンド（Stokes）と青側バンド（anti-Stokes）が分離され、冷却 · 量子 state transfer · single-phonon 操作が可能になる。現行最高性能実験では mechanical Q **> 5.5 × 10⁹** の unified quantum standards（統一量子標準）振動子が実現され、ground state cooling および phonon Fock state 準備に用いられる。

---

## 2. 統一量子標準

### 2.1 概念

異なる周波数 · 質量 · 材料の mechanical resonator を、共通の **quantum metrology standard** として較正する枠組み。統一量子標準は:

- 零点変位 x_zpf = √(ℏ / 2m_eff ω_m)
- 単一 phonon エネルギー ℏω_m
- 散逸率 Γ_m = ω_m / Q

を基準量とし、複数 lab 間の coupling g₀ · occupation number · decoherence rate を直接比較可能にする。

### 2.2 性能指標

| 指標 | 達成値 |
|------|--------|
| Mechanical Q | **> 5.5 × 10⁹** |
| n_th（有効熱 phonon 数） | < 0.1 |
| Position imprecision | x_zpf/√2 近傍 |

---

## 3. 大質量 matter-wave 干渉

### 3.1 可視性と質量スケーリング

光晶格 · マグネット制御による atom/optically levitated nanoparticle 干渉計では、de Broglie wavelength λ_dB = h/p と decoherence の競合が可視性 V を決定する。

| 質量 | 可視性 V | 条件 |
|------|----------|------|
| **~100 g**（gram-scale） | **~0.64** | T ~ μK, τ_coherence ~ ms |
| **~10 kg** | **~0.16** | confirmation experiment |

gram-scale（~100 g）物体の matter-wave interference は **V ~ 0.64** で観測され、量子–古典境界の mass scale を大幅に拡張する。**10 kg confirmation** 実験では、重力 · 内部 heating · blackbody radiation decoherence 下でも **V ~ 0.16** が予測され、macroscopic quantum superposition の存続を検証する。

### 3.2 Decoherence 機構

| 機構 | スケーリング |
|------|--------------|
| Collisional decoherence | ∝ pressure |
| Photons scattering | ∝ laser intensity |
| Internal emission | ∝ T⁴ |
| Gravity gradient | ∝ mass · Δg |

---

## 4. LIGO — radiation-pressure back-action 除去

### 4.1 量子ノイズ限界

Advanced LIGO の shot noise 限界近傍では、test mass mirror の **radiation pressure back-action** が displacement noise に寄与する。Feedforward · feedback による back-action subtraction 回路は、balanced homodyne 読み出しと結合し、SQL（Standard Quantum Limit）近傍の sensitivity を改善する。

### 4.2 実装

- 光圧 force の real-time 推定
- Digital filter による anti-correlation injection
- ~10 dB 級 back-action noise reduction（代表値）

これは cavity optomechanics の inverted 系として、GW 検出器を **macroscopic quantum sensor** として運用する例である。

---

## 5. 集積オプトメカニカルフォトニクス

### 5.1 524288-cell OM 配列

シリコンフォトニクス上の optomechanical crystal（OMC）配列は、**524288 cell**（2¹⁹）規模の並列 phonon モード制御を可能にする。各 cell は photonic · phononic bandgap により localized optical · mechanical mode を持ち、massively parallel quantum interface として機能する。

### 5.2 応用

| 応用 | 内容 |
|------|------|
| 量子情報 | phonon–photon transduction |
| センシング | 質量 · force array |
| シミュレーション | 多体 phonon dynamics |

---

## 6. MAQRO — 宇宙空間デコヒーレンス試験

### 6.1 ミッション

MAQRO（Macroscopic Quantum Resonators）は、LEO 宇宙空間で optically trapped dielectric particle（~10⁻¹⁴–10⁻¹² kg）の superposition を維持し、decoherence rate を地球環境と比較する。

### 6.2 コヒーレンス時間

代表目標: **T₂ > 22 s**（superposition coherence time）。宇宙空間の ultra-high vacuum · cryogenic · low EM 環境により、collisional · thermal decoherence が ~10³ 倍抑制される。

---

## 7. 理論枠組み

### 7.1 線形化と Langevin 方程式

δḃ + (iω_m + Γ_m/2) δb = −ig₀ α_s δa + √Γ_m n_th b_in

δȧ + (iω_c + κ/2) δa = −iG δb + √κ a_in

ここで G = g₀ α_s は linearized coupling。Input–output relation から homodyne spectrum S_θθ(ω) を導き、sideband cooling limit ⟨n⟩ → n_th κ/(4Ω)（Ω: 冷却 rate）を得る。

---

## 8. 記号（参照）

| 記号 | 意味 |
|------|-----|
| g₀ | vacuum optomechanical coupling |
| κ, Γ_m | optical · mechanical linewidth |
| x_zpf | 零点変位 |
| V | 干渉可視性 |
| T₂ | コヒーレンス時間 |
| Q | mechanical quality factor |

---

## 9. 関連トピック

- 量子力学（量子測定 · デコヒーレンス）
- 量子情報 · 計量（SQL · squeezed light）
- 重力波検出（LIGO · 量子ノイズ）
