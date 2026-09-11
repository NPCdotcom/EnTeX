---
phys_doc_id: phys.topic.fusion_heating
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [tokamak, sparc, demo]
phys_doc_regex_file: ^phys\-doc\-fusion\-plasma\-heating\.md$
---

<!-- PHYS_DOC_ID: phys.topic.fusion_heating -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# 核融合プラズマ加熱

磁気閉じ込め核融合（MCF）における burning plasma 到達は、外部加熱から **α粒子自己加熱** への移行を意味する。トカマク型装置 SPARC · ITER · DEMO の設計・運転シナリオは、加熱 · 輸送 · ディバータ · 不純物排出の統合制御に基づく。

---

## 1. Burning plasma — SPARC

### 1.1 Q 値と運転点

SPARC（Compact High-Field Tokamak）は、HTS 磁石（B_T ~ 12.2 T）により小半径 · 高磁場 burning plasma を実現する。代表シナリオ:

| パラメータ | 値 |
|------------|-----|
| 融合ゲイン **Q** | **~30** |
| フラットトップ持続時間 | **~2100 s** |
| プラズマ電流 I_p | ~8.7 MA |
| 中心温度 T_i0 | ~12 keV |

Q = P_fusion / P_external は、DT 反応率 · confinement time · 加熱効率の積で決まる。

### 1.2 α 加熱 fraction

Burning plasma 条件では、He-4（α 粒子）のプラズマ内停止により **α 加熱** が支配的となる。SPARC DT シナリオでは、総加熱に対する α 加熱の寄与 fraction は **~0.99** に達し、外部 NBI · RF 加熱は点火補助 · プロファイル制御に移行する。

---

## 2. DEMO 炉シナリオ

### 2.1 設計目標

DEMO（Demonstration Power Plant）は ITER 後の net electricity 発電を目指す。代表設計パラメータ:

| 項目 | 目標 |
|------|------|
| **Q** | **> 75** |
| 平均 neutron wall loading | ~2 MW/m² |
| 容量因子 | ~50–75% |
| ヘリウム灰（He ash）濃度 | **< 0.8%** |

Q > 75 は、commercial viability に必要な余剰 fusion power を確保し、He ash 除去 · divertor 熱負荷 · トリチウム breeding の operational margin を与える。

### 2.2 Divertor — detached 運転

DEMO divertor は **detached** 状態（partial detachment → full detachment）で運転され、peak heat flux を **< 10 MW/m²** に抑制する。手法:

- デuterium · neon · nitrogen seeding
- divertor 磁場配置（Super-X · snowflake）
- 放射冷却 · 体積 recombination

Detached 運転と core confinement（H-mode）の両立が DEMO 設計の中核課題である。

### 2.3 He ash 排出

α 粒子 He ash の蓄積は fuel dilution により Q を低下させる。He ash 輸送は neoclassical + anomalous transport に依存し、**He ash exhaust fraction > 99%**（core He 濃度 < 0.8%）を steady-state で維持するには、ELM · 外部 perturbation による edge purge と divertor pumping の統合が必要である。

---

## 3. 定常運転 — q プロファイル制御

### 3.1 安全因子 q(r)

q プロファイルの形状は MHD 安定性 · 輸送 · 非帰化性 current drive に直結する。定常 tokamak では **non-inductive current fraction ~100%** を目指し、NBI · ECCD · LHCD により q_min > 1（または q_min ~ 2 最適化）を維持する。

### 3.2 制御手法

| 手法 | 作用 |
|------|------|
| ECCD | q プロファイル local 制御 |
| NBI | 中性ビーム current drive |
| LHCD | off-axis current |
| リアルタイム MSE · CES | q(r) 再構成フィードバック |

---

## 4. ELM pacing

### 4.1 ELM 問題

Type-I ELM（Edge Localized Mode）は H-mode edge pedestal の MHD 不安定性であり、瞬間 heat flux ~100 MW/m² を divertor に送る。DEMO では ELM サイズ ΔW_EL / W_ped を **< 1%** に抑制する必要がある。

### 4.2 Pacing 技術

| 手法 | 原理 |
|------|------|
| ペレット注入 pacing | edge pressure 周期 destabilization |
| 磁場 perturbation（RMP） | edge topology 制御 |
| 高頻 NBI / RF pulse | edge 駆動 |

ELM pacing により、自然 ELM 頻度（~1–10 Hz）を **~30–100 Hz** へ増加させ、個々 ELM エネルギーを分割する。He ash 排出 · impurity flush にも寄与する。

---

## 5. 加熱方式の比較

| 方式 | 周波数/エネルギー | 主用途 |
|------|-------------------|--------|
| NBI | ~100 keV–1 MeV | bulk 加熱 · current drive |
| ICRF | ~40–80 MHz | minority heating |
| ECRH/ECCD | ~100–200 GHz | 電子加熱 · q 制御 |
| LHCD | ~3–5 GHz | off-axis current |

Burning plasma では α 加熱が bulk を維持し、外部加熱は profile · MHD · ELM 制御に特化する。

---

## 6. 輸送と confinement scaling

H-mode confinement は ITER IPB98(y,2) scaling に基づくが、burning plasma では fast ion physics · α particle redistribution · TAE/EPM モードが confinement を修正する。Turbulence（ITG · TEM · ETG）と zonal flow の相互作用が temperature profile stiffness を決定する。

---

## 7. 記号（参照）

| 記号 | 意味 |
|------|-----|
| Q | 融合ゲイン P_fus / P_ext |
| τ_E | エネルギー閉じ込め時間 |
| q(r) | 安全因子 |
| f_α | α 加熱 fraction |
| ΔW_EL | ELM エネルギー損失 |

---

## 8. 関連トピック

- プラズマ物理学 · MHD 安定性
- 中性子学 · トリチウム breeding blanket
- 計算物理学（gyrokinetic · transport solvers）
