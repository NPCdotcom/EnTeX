---
phys_doc_id: phys.topic.cosmological_observations
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [desi, lsst, bao, cmb-s4]
phys_doc_regex_file: ^phys\-doc\-cosmological\-observations\.md$
---

<!-- PHYS_DOC_ID: phys.topic.cosmological_observations -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 宇宙論観測

現代宇宙論は、大規模サーベイ（分光 · 写真 · CMB · 弱重力レンズ）の **統計的整合** により、宇宙の幾何 · 組成 · 成長 · 初期条件を精密に制約する。Stage V 世代では DESI + LSST 共同解析が dark energy · 成長率 · neutrino 質量の同時推定の中核となる。

---

## 1. DESI + LSST 共同宇宙論（Stage V）

### 1.1 データ統合

| サーベイ | 手法 | 主要プローブ |
|----------|------|--------------|
| **DESI** | 分光 BAO · RSD | H(z), D_A(z), fσ₈(z) |
| **LSST (Rubin)** | 弱重力レンズ · クラスター | S₈, Ω_m, 成長 |
| **CMB-S4** | 温度 · 偏光 | r, Σm_ν, n_s |

Stage V 共同フィットでは、photometric redshift calibration · intrinsic alignment · baryonic feedback を **共通 systematics モデル** で扱う。

### 1.2 主要パラメータ制約

CPL（Chevallier–Polarski–Linder）dark energy パラメータ化 w(a) = w₀ + w_a(1−a) 下の Stage V 合同解析代表値:

| パラメータ | 代表制約 | 意味 |
|------------|----------|------|
| **S₈** | **~0.764** | σ₈ · (Ω_m/0.3)^0.5 — WL 成長 |
| **w_a** | **~0.016** | dark energy 時間変化 |
| w₀ | ~−1.03 | 現 epoch の状態方程式 |

S₈ tension（Planck CMB vs 低 redshift WL）は Stage V 統計量で **~2–3 σ** レベルまで縮小または再配置される。w_a の精密化は dynamical dark energy vs ΛCDM の判別力を決定する。

---

## 2. BAO — post-mission と legacy

### 2.1 DESI 5 年 mission

DESI は ~1400 万 galaxy · QSO の分光 redshift を取得し、z = 0.1–1.1（LRG/ELG）および z = 2–4（QSO Ly-α forest）で BAO スケールを測定する。Mission 完了後の **post-mission 解析** では、全 sky coverage · 最終 selection function · 1% 級 systematics 監査を経て、comoving angular diameter distance D_A(z) と Hubble parameter H(z) を **0.3–0.5%** 精度で推定する。

### 2.2 Legacy extended — z > 3.8

Ly-α BAO および high-z QSO サンプルの **legacy extended** 解析は z > 3.8 領域まで BAO 信号を拡張する。高 redshift BAO は pre-recombination 以降の幾何に対する独立プローブであり、early dark energy · extra relativistic species · primordial non-Gaussianity の間接制約に寄与する。

### 2.3 BAO スケール

comoving BAO スケール s = r_d / D_V(z)（または angular + radial 分解）の測定は、sound horizon r_d ~ 147 Mpc の絶対キャリブレーションに依存する。DESI 内部 consistency check（cross-correlation · mock challenge）で r_d 系統を ~0.2% に抑える。

---

## 3. RSD — 成長率 fσ₈

### 3.1 赤方偏移空間歪み

galaxy clustering の anisotropy から **成長率 fσ₈(z) = σ₈(z) · Ω_m(z)^0.55** を抽出する。DESI RSD 解析では z-bin ごとに fσ₈ を測定し、modified gravity · massive neutrino · dark energy モデルと比較する。

### 3.2 精度

Stage V 合同解析における fσ₈(z) の bin-averaged 精度は **~0.6%** に達する。これは Planck ΛCDM 予測との比較で、成長抑制（neutrino · w ≠ −1）の検出感度を決定する。

---

## 4. Rubin LSST — 弱重力レンズ archive

### 4.1 データ規模

LSST 10 年 survey（~18,000 deg², ugrizy）から、~10⁹ galaxy の shape 測定と photometric redshift が **Rubin LSST Science Archive** として公開される。弱重力レンズ（WL）cosmic shear 2-point · 3-point 統計が S₈ · Ω_m · intrinsic alignment amplitude を制約する。

### 4.2 系统論

| 系统 | 対策 |
|------|------|
| PSF 補正 | per-visit metrology · self-calibration |
| photo-z bias | DESI 分光 cross-match · clustering redshifts |
| baryonic feedback | hydrodynamical simulation priors |
| IA | TATT / NLA モデル · joint fit |

---

## 5. CMB-S4 — post-EoM 制約

### 5.1 観測仕様

CMB Stage-4（CMB-S4）は ~500,000 検出器 · ~400,000 deg²（南半球中心）の CMB 温度 · E-mode · B-mode 偏光観測を行う。**End of Mission（EoM）** 解析では、大気 · 前景 · レンズing delensing 後の B-mode スペクトルから:

| パラメータ | post-EoM 目標 |
|------------|---------------|
| **r**（テンソル–スカラー比） | σ(r) ~ 0.001 |
| **Σm_ν** | σ(Σm_ν) ~ 0.015 eV |

### 5.2 統合宇宙論

CMB-S4 + DESI BAO + LSST WL の合同フィットは、**絶対スケール（r_d, θ_*）** と **成長（fσ₈, S₈）** を同時拘束し、neutrino mass hierarchy · w₀w_a · ΔN_eff の degeneracy を解消する。

---

## 6. CPL dark energy モデル

w(a) = w₀ + w_a(1 − a)

| 限界 | 意味 |
|------|------|
| w_a → 0 | cosmological constant |
| w₀ = −1, w_a ≠ 0 | 時間依存 dark energy |
| w < −1 | phantom（量子不安定性に注意） |

DESI BAO + SNIa + CMB distance priors で (w₀, w_a) の confidence contour を描き、ΛCDM からの逸脱を **~2 σ** レベルで探索する。

---

## 7. 記号（参照）

| 記号 | 意味 |
|------|------|
| S₈ | σ₈(Ω_m/0.3)^0.5 |
| fσ₈ | 線形成長率 × 振幅 |
| r_d | sound horizon at drag epoch |
| r | インフレーション tensor-to-scalar ratio |
| Σm_ν | 3 種 neutrino 質量の和 |

---

## 8. 関連トピック

- 一般相対性理論（FLRW · 摂動成長方程式）
- CMB 物理学（Sachs–Wolfe · レンズing · delensing）
- 統計力学 · ベイズ推論（MCMC · emcee · Cobaya）
