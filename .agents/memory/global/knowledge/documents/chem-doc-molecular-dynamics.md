---
chem_doc_id: chem.topic.molecular_dynamics
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [md, force-fields, msd]
chem_doc_regex_file: ^chem\-doc\-molecular\-dynamics\.md$
---

<!-- CHEM_DOC_ID: chem.topic.molecular_dynamics -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 分子動力学

---

## 1. MD の基本原理

ニュートン運動方程式を数値積分し、原子の軌道 r(t) を追跡。平衡物性は時間平均で得る。

`	ext
初期条件 (r, v) → F = −∇V(r) → 積分 → 熱浴/圧力制御 → 観測量の平均
`

---

## 2. 積分法

**Verlet / leap-frog** — 位置と速度を交互更新。エネルギー保存に優れる（微小時間刻み Δt ~ 1–2 fs）。

---

## 3. 力場

U = 結合伸縮 + 角度弯曲 + 二面角 + LJ 非結合 + 静電

| 力場 | 用途 |
|------|------|
| UFF | 汎用 |
| AMBER, CHARMM | 生体分子 |
| OPLS | 有機液体 |

---

## 4. アンサンブル

| 記号 | 制御 |
|------|------|
| NVE | 粒子数 · 体積 · エネルギー（微正準） |
| NVT | 温度一定（ノーズ–フーバー等） |
| NPT | 温度 · 圧力一定 |

**周期境界条件（PBC）** — 無限系の近似

---

## 5. 輸送係数

**平均二乗変位 MSD**:

MSD(t) = ⟨|r(t) − r(0)|²⟩

3 次元長時間極限: MSD = 6Dt

**Stokes–Einstein**: D = kT / (6πηr)

---

## 6. 動径分布 g(r)

粒子間距離の確率分布 — 液体構造の特徴。

---

## 7. 量子化学との接続

ab initio / DFT で V(r) を計算 → 力 F = −∇V → MD。ボーン–オッペンハイマー下では核は古典粒子として扱う。
