---
phys_doc_id: phys.topic.exoplanet_atmospheres
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [ariel, jwst, hwo]
phys_doc_regex_file: ^phys\-doc\-exoplanet\-atmospheres\.md$
---

<!-- PHYS_DOC_ID: phys.topic.exoplanet_atmospheres -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 系外惑星大気

系外惑星大気物理学は、トランジット · 直接成像 · 分光から大気組成 · 温度構造 · 雲 · 化学反応を推定する。Ariel 均質サーベイ · JWST 高精度分光 · 将来の Habitable Worlds Observatory（HWO）が、統計的 · 個別的 · バイオシグネチャ探索の三層構造を形成する。

---

## 1. Ariel — 均質サーベイ

### 1.1 ミッション概要

Ariel（Atmospheric Remote-sensing Infrared Exoplanet Large-survey）は、0.5–7.8 μm 分光で **~1000 個** の系外惑星大気を系統調査する ESA M4 ミッションである。均質（homogeneous）解析パイプラインにより、全対象に同一 retrieval フレームワークを適用する。

### 1.2 規模と検出率

| 項目 | 値 |
|------|-----|
| 対象惑星数 | **~3400**（candidate pool 含む） |
| 大気検出 fraction | **~0.78** |
| 主要分子 | H₂O, CO, CO₂, CH₄, NH₃, HCN |

~3400 惑星の parent sample から、SNR 閾値 · ステラー contamination · 雲 opacity 条件を満たす **~78%** で大気特征（spectral features）が検出されると予測される。残り ~22% は雲・霾 dominated または低 SNR により「flat spectrum」と分類される。

### 1.3 科学出力

- 組成–質量–温度（CMT）diagram の population 構造
- 金属量 · C/O ratio の分布
- 熱木星 vs サブネプチューン vs super-Earth の分類

---

## 2. JWST — 岩石系惑星大気

### 2.1 シナジー観測

JWST（NIRSpec · NIRCam · MIRI）による transit · eclipse spectroscopy は、M-dwarf 周回の岩石系惑星（R < 2 R⊕）大気に感度を持つ。Ariel 設計 inputs と JWST Cycle 1–3 データの **synergy** により、岩石系大気検出 **~128 件** が累積される規模に達する。

### 2.2 ベイズ retrieval と systematics

大気 retrieval は forward model（1D/3D radiative transfer + chemistry）と nested sampling を組み合わせる。**Bayesian retrieval systematics** として以下を明示的にモデル化する:

| 系统 | 処理 |
|------|------|
| ステラー heterogeneity | spot · faculae contamination |
| インストルメント drift | wavelength calibration · flat field |
| 相関ノイズ | red noise · GP モデル |
| 事前分布 sensitivity | log vs linear abundances |

Posterior 間の **Bayesian model averaging** により、分子存在の Bayes factor · 組成 uncertainty が報告される。

---

## 3. HWO — バイオシグネチャ探索

### 3.1 ミッション能力

Habitable Worlds Observatory（HWO, NASA Habitable Worlds 概念）は、UV–IR 直接成像 · 分光で **~25 pc 以内の HZ 惑星** を調査する。第 4 運用年（year-4 ops）時点の代表予測:

| 項目 | 値 |
|------|-----|
| **O₂ 確認 target 数** | **~4** |
| 観測モード | coronagraph · starshade |
| 波長 | 0.2–1.8 μm（UV–NIR） |

O₂（および O₄ dimer）検出は、rocky planet 大気における photochemical equilibrium から **false positive** リスクを伴う。

### 3.2 光化学 false positive 率

Abiotic O₂ 生成経路（CO₂ photolysis + H escape, H₂O photolysis on M-dwarf planets）を population synthesis で評価すると、HWO year-4 確認 target に対する **photochemical false positive rate ~0.035**（3.5%）と推定される。判別には **O₂ + O₃ + CH₄ co-detection** · surface feature · seasonal variability が必要である。

---

## 4. 分光診断

### 4.1 主要バンド

| バンド | 分子 · 物理 |
|--------|-------------|
| 1.4, 1.9 μm | H₂O |
| 2.3, 4.3 μm | CO, CO₂ |
| 3.3 μm | CH₄ |
| 0.2–0.3 μm | O₃, SO₂（UV） |

### 4.2 雲 · 霾

KCl · Na₂S · silicate cloud の condensate により、スペクトル feature が平坦化する。retrieval では cloud deck pressure · particle size distribution · grey vs wavelength-dependent opacity をパラメータ化する。

---

## 5. 温度–圧力構造

Transit transmission probes 上層大気（~mbar–0.1 bar）。Eclipse emission probes より深い層（~0.01–1 bar）。TP profile inversion により thermal inversion（TiO/VO · S-rich photochemistry）を検出する。

---

## 6. 記号（参照）

| 記号 | 意味 |
|------|-----|
| R_p, R⊕ | 惑星半径 |
| H | スケールハイト |
| χ²_red | retrieval goodness-of-fit |
| C/O | 炭素酸素比 |
| HZ | Habitable Zone |

---

## 7. 関連トピック

- 放射輸送 · 大気物理学
- 恒星物理学（M-dwarf activity · UV flux）
- ベイズ統計 · nested sampling（MultiNest · dynesty）
