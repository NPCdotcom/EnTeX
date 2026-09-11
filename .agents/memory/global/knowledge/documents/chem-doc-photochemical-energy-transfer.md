---
chem_doc_id: chem.topic.photochemical_et
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [forster, dexter, fret]
chem_doc_regex_file: ^chem\-doc\-photochemical\-energy\-transfer\.md$
---

<!-- CHEM_DOC_ID: chem.topic.photochemical_et -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 光化学的エネルギー移動

---

## 1. 励起状態とエネルギー移動

分子が光吸収で励起された後、**励起エネルギー** が別分子へ移る過程。光合成 · OLED · センサの基盤。

---

## 2. Förster 共鳴エネルギー移動（FRET）

**誘導双極子–双極子相互作用**（長距離）

k_F = (1/τ_D) (R₀/R)⁶

| 記号 | 意味 |
|------|------|
| τ_D | ドナー単独の蛍光寿命 |
| R₀ | Förster 半径（k_F = 1/τ_D となる距離） |
| R | ドナー–アクセプター間距離 |

R₀ はドナー蛍光とアクセプター吸収の **スペクトル重なり積分 J** に依存。

**距離依存**: R⁻⁶ — 6 nm 前後が典型的検出範囲

---

## 3. Dexter エネルギー移動

**電子交換** 機構（軌道重なり必須）

k_D ∝ J_overlap² exp(−2βR)

指数関数的に短距離（通常 < 1–2 nm）

---

## 4. 比較

| | Förster | Dexter |
|--|---------|--------|
| 距離 | R⁻⁶（中–長） | exp(−2βR)（短） |
| 機構 | 誘導双極子 | 電子交換 |
| スピン | 一重–一重 | 一重/三重可 |

---

## 5. スピン選択則

**スピン保存** — 三重–三重遷移は Förster では禁止（双極子結合がスピンを変えない）

三重–三重は **短距離 Dexter** 経路が支配的（TTA 等）

---

## 6. 距離域の実務

- R < R₀: Dexter と Förster が競合
- R ~ R₀–2R₀: FRET 効率が急変（センサに利用）
- R >> R₀: 移動効率急低下

---

## 7. 応用

光触媒の電荷分離 · 光合成アンテナ · OLED 発光層 · FRET バイオセンサ · 超分子自己組織化

**電荷移動（ET）** との区別 — Marcus 理論は電子移動（電荷移動）の速度論；Förster/Dexter は **励起エネルギー** の移動。
