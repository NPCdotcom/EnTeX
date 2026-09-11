---
phys_doc_id: phys.topic.pulsar_timing
phys_doc_topic: physics
phys_doc_kind: topic
phys_doc_tags: [pta, gwb, hellings-downs]
phys_doc_regex_file: ^phys\-doc\-pulsar\-timing\-arrays\.md$
---

<!-- PHYS_DOC_ID: phys.topic.pulsar_timing -->
<!-- PHYS_DOC_KIND: topic -->
<!-- PHYS_DOC_TOPIC: physics -->

# パルサー計時アレイ

パルサー計時アレイ（PTA）は、銀河内のミリ秒パルサー（MSP）を **銀河スケールの重力波検出器** として利用する。各 MSP の到着時刻系列から共通の赤色タイミング残差を抽出し、超低周波（nHz）重力波の存在を統計的に検出する。

---

## 1. ミリ秒パルサー as 時計

### 1.1 計時精度

MSP は 1 ms 以下の自転周期と 10⁻¹⁵–10⁻¹⁶ 程度の到着時刻安定度を持つ。長期間の位相接続により、**仮想時計** として機能する。タイミングモデルには、自転・軌道（Keplerian + post-Keplerian）、プロパゲーション（ISM · 太陽系 ephemeris）、観測所位置が含まれる。

### 1.2 残差と GWB 信号

タイミング残差 R_a(t) は、観測到着時刻とモデル予測の差である。GWB 存在下では、全パルサーに **共通の赤色成分** が重ね合わされる。個体のホワイトノイズ · 赤色ノイズ（spin noise, DM variations）を除去した後、交差相関解析が GWB 検出の主手段となる。

---

## 2. IPTA 共同データセット

### 2.1 規模

International Pulsar Timing Array（IPTA）は、EPTA · NANOGrav · PPTA · InPTA 等の地域 PTA を統合する。第 3 世代共同データリリース（DR3 相当）では:

| 項目 | 値 |
|------|-----|
| 対象 MSP 数 | **~200 個** |
| 最長ベースライン | **~46 年** |
| 観測バンド | ラジオ（~0.3–3 GHz 中心） |

複数観測所 · 複数受信機系の系統差を **ベイズ共同フィッティング** で吸収する。

### 2.2 データ処理パイプライン

1. TOA（Time of Arrival）抽出 — PRESTO / Tempo2 / PINT
2. タイミングモデル更新 — 軌道 · DM · ジャンプ
3. 残差のホワイトニング · 赤色ノイズモデル化
4. 交差相関 · ベイズ GWB 推論

---

## 3. Hellings–Downs 相関

### 3.1 角相関関数

等方 GWB 下、パルサー a, b の天空角分離 γ に対する交差相関の期待値:

Γ(γ) = (1/2) − (3/4)(1 − cos γ) ln[(1 − cos γ)/2]

この **Hellings–Downs（HD）曲線** は、トランサーバーサル波に特有であり、観測された角相関が HD 予測と一致することは GWB 起源の強い証拠となる。

### 3.2 GWB 振幅

IPTA 共同解析では、HD 相関を仮定した GWB 特性振幅が **A_GWB ~ 10⁻¹⁵** オーダー（h²Ω_GW 正規化）で検出される。スペクトル指数 γ_GW（通常 Ω_GW(f) ∝ f^γ_GW）も推定され、astrophysical（γ ≈ 2/3）と cosmological 起源の判別に用いられる。

---

## 4. 個別 SMBHB 源 — Simon 解析

NANOGrav 15 年データに対する **Simon et al. 型ベイズ解析** では、Hellings–Downs 背景に加え、**個別超大質量 BH 二重（SMBHB）** 源の寄与を明示的にモデル化する。最も有意な候補源に対し、背景モデルとの比較で **~14.5 σ** の個別源有意度が報告される。

| パラメータ | 典型推定 |
|------------|----------|
| 天空位置 | 赤経 · 赤緯 posterior |
| チープ周波数 f | nHz 帯 |
| チープ率 df/dt | LISA 帯への extrapolation |
| 距離 · 質量 | chirp mass · luminosity distance |

個別源モデルは GWB 振幅推定と trade-off するため、階層的 prior（源数密度 · 質量関数）で degeneracy を管理する。

---

## 5. 異方性 — 多極解析

### 5.1 天空マップ

GWB が完全等方でない場合、タイミング残差の天空分布は **球面調和関数** で展開される。IPTA DR3 解析では、異方性の有意な多極成分が **l ~ 11** 付近まで検出され、局所的超クラスター方向 · 銀河大規模構造との関連が議論される。

### 5.2 物理的解釈

| 成分 | 起源候補 |
|------|----------|
| 単極 (l=0) | 観測系統 · 太陽系 ephemeris |
| 低次多極 | 近傍 SMBHB · 宇宙弦 |
| 高次多極 (l~11) | 複数源の重ね合わせ · 構造形成 |

---

## 6. SKA-PTA と天空定位

Square Kilometre Array（SKA）Phase 1 稼働後の PTA（SKA-PTA）は、~1000 以上の MSP と μsec 級計時を目標とする。シミュレーションに基づく GWB 源定位性能では、単一 SMBHB 源の **天空定位 ~0.12 deg²**（90% 信頼領域）が達成可能とされる。これは LISA · 地上 GW との triangulation と EM follow-up（AGN  variability）を可能にする。

---

## 7. PTA–LISA チープ

### 7.1 周波数接続

PTA が nHz 帯で観測する SMBHB の inspiral 信号は、years–decades スケールで周波数を増大させ、LISA 帯（mHz）へ移行する。**Joint SNR** は PTA 位相 + LISA 振幅 + チープ率の共同制約により、単独帯域を大幅に上回る。

### 7.2 科学出力

- 合体時刻予報（months–years 精度 → days 精度へ改善）
- 空間位置 · 距離 · chirp mass の degeneracy 解消
- GWB スペクトルと個別源の分離

---

## 8. 前景 · 系統効果

| 効果 | 対策 |
|------|------|
| 太陽系 ephemeris 誤差 | JPL DE440/441 · ベイズ ephemeris |
| ISM DM 変動 | DM–frequency 分離 · 複数周波数 |
| 観測所クロック | 共通 clock · 原子時計リンク |
| 個体 spin noise | 個体赤色ノイズパラメータ化 |

---

## 9. 記号（参照）

| 記号 | 意味 |
|------|-----|
| R_a(t) | パルサー a のタイミング残差 |
| Γ(γ) | Hellings–Downs 相関 |
| A_GWB | GWB 振幅 |
| γ_GW | スペクトル指数 |
| f, ḟ | チープ周波数 · チープ率 |

---

## 10. 関連トピック

- 重力波天文学（LVK · SGWB · マルチバンド SNR）
- 超大質量 BH 二重の形成 · 硬い X 線ローブ
- 一般相対性理論（PTA レスポンス関数 D^a(θ, φ)）
