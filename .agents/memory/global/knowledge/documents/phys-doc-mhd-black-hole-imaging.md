---
phys_doc_id: phys.topic.mhd_eht
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [eht, ngEHT, grmhd]
phys_doc_regex_file: ^phys\-doc\-mhd\-black\-hole\-imaging\.md$
---

<!-- PHYS_DOC_ID: phys.topic.mhd_eht -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# MHD ブラックホール撮像

イベントホライズン・テレスコープ（EHT）および次世代 EHT（ngEHT）は、very-long-baseline interferometry（VLBI）により M87* · Sgr A* 等の SMBH シャドウと accretion flow を **μas 解像度** で直接撮像する。GRMHD シミュレーションと観測データのベイズ比較が、磁場構造 · 降着モード · 放射機構を制約する。

---

## 1. ngEHT — 次世代アレイ

### 1.1 構成と性能

| 項目 | EHT 2017 | ngEHT（持続アレイ） |
|------|----------|---------------------|
| ステーション数 | ~8 | **~40** |
| 角解像度 | ~20 μas | **~1.1 μas** |
| 観測モード | キャンペーン型 | **持続（sustained）** |
| 偏光 | 時間平均 | **sub-hour 偏光ムービー** |

~40 ステーションの地球–宇宙 VLBI（space-ground）含む構成により、(u, v) カバレッジが大幅に改善され、シャドウリング · リング直径 · 偏光構造の temporal variability が解決される。

### 1.2 科学目標

- シャドウサイズ · 形状の精密比較（GR テスト）
- 偏光ベクトル（EVPA）の時間変動 → 磁場 topology
- 近傍 SMBH 質量 · スピン · 降着率の joint inference

---

## 2. EVPA 再構成

### 2.1 電気ベクトル位置角

偏光輝度 Stokes (Q, U) から EVPA（Electric Vector Position Angle）ψ = (1/2) arctan(U/Q) を導く。ngEHT の full-polarization 再構成では、EVPA 精度 **~0.004°** が達成され、磁場の azimuthal wrap · spiral · リング上の ordered field を直接可視化する。

### 2.2 系統論

| 効果 | 対策 |
|------|------|
| バンド間 depolarization | multi-frequency joint imaging |
| Faraday rotation | RM synthesis · 周波数依存 EVPA |
| キャリブレーション | self-cal · closure phase/quaternion |

---

## 3. キネティック EHT

### 3.1 GRMHD + PIC ハイブリッド

標準 GRMHD は流体近似であり、非熱電子分布 · シンクロトロン · 逆コンプトンを簡略化する。**キネティック EHT** は GRMHD 背景場に粒子-in-cell（PIC）または Vlasov 求解を結合し、first-principles 放射スペクトルを生成する。

### 3.2 比較ライブラリ

公開 GRMHD+PIC 比較ライブラリは、複数コード（BHAC · KHARMA · H-AMR · grPIC 等）の cross-validation を提供する:

| 比較項目 | 内容 |
|----------|------|
| リング直径 | ~40–45 μas（M87*） |
| 偏光 fraction | ~5–15% |
| スペクトル index | mm–submm SED |
| variability | light curve PSD |

---

## 4. MAD と tearing 不安定性

### 4.1 MAD（Magnetically Arrested Disk）

磁場フラックスが降着を抑制する MAD 状態は、EHT 観測と整合する高効率ジェット放出を説明する。MAD–SANE（Standard and Normal Evolution）遷移はブラックホールスピン · 降着率 · 初期磁場に依存する。

### 4.2 Tearing 不安定性

磁場リコネクションに伴う **tearing mode** 不安定性は、薄い accretion disk 内で plasmoid 形成 · 加熱 · 非熱電子加速を駆動する。GRMHD シミュレーションでは、 tearing により **BZ（Blandford–Znajek）フレア** 的な時間的輝度変動が誘発され、EHT 観測された NIR · submm flare と対応する。

---

## 5. 磁気変動と BZ フレア

### 5.1 観測

M87* · Sgr A* ともに、EHT · ALMA · GRAVITY 連携で **日–時間スケール** の flux variability が観測される。偏光 fraction · EVPA swing は磁場 reconfiguration イベントと同期する。

### 5.2 モデル

| モデル | 特徴 |
|--------|------|
| Hot spot | 軌道コンポーネント |
| Magnetic flux eruption | MAD tearing |
| BZ jet power 変動 | P_BZ ∝ B² · Ω_H² |

BZ 抽出 power の変動は、jet 基底 · リング偏光の **sub-hour** 変動として ngEHT に検出可能である。

---

## 6. 画像再構成パイプライン

1. 可視度データ V_ijk — 各 baseline · 時間 · 周波数
2. Regularized maximum likelihood（SMILI · eht-imaging）
3. Closure quantities による systematics チェック
4. GRMHD 画像ライブラリとの Bayesian model selection
5. パラメータ posterior（spin a_*, i, M_BH, ρ, B）

---

## 7. 記号（参照）

| 記号 | 意味 |
|------|-----|
| θ_g | 重力半径に対応する角スケール |
| EVPA ψ | 偏光電場方向 |
| RM | Faraday rotation measure |
| MAD / SANE | 降着磁場状態 |
| P_BZ | Blandford–Znajek jet power |

---

## 8. 関連トピック

- 一般相対性理論（Kerr メトリック · 測地線 · シャドウ）
- プラズマ MHD（理想 MHD · リコネクション）
- 数値相対論 · GRMHD（HARM · BHAC）
