---
chem_doc_id: chem.topic.physical_chemistry
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [thermodynamics, quantum, spectroscopy]
chem_doc_regex_file: ^chem\-doc\-physical\-chemistry\.md$
---

<!-- CHEM_DOC_ID: chem.topic.physical_chemistry -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 物理化学

物理化学は **熱力学 · 量子力学 · 統計力学 · 速度論 · 分光学** を統合し、分子レベルの原理から巨視的性質を説明する。

---

## 1. 熱力学

### 第 1 法則
ΔU = q + w（内部エネルギー = 熱 + 仕事）

定圧過程: ΔH = q_p（エンタルピー）

### 第 2 法則
孤立系のエントロピー ΔS ≥ 0。平衡では ΔG = 0。

### 平衡と温度依存
ΔG° = −RT ln K

van't Hoff: d(ln K)/dT = ΔH°/(RT²)

---

## 2. 量子化学（入口）

### 粒子箱
E_n = n²h²/(8mL²) — 零点エネルギー E₁ > 0

### 原子・分子軌道
AO の LCAO → 結合性/反結合性 MO（σ, π）

### 計算手法の階層
分子力学 → 半経験 → Hartree–Fock → 相関(MP2/CI/CC) / DFT

---

## 3. 統計力学（入口）

微視状態の統計的重みから巨視量（E, S, F, G）を導く。

F = −kT ln Z（Helmholtz 自由エネルギー、分配関数 Z）

---

## 4. 分光学

| 手法 | 励起 | 情報 |
|------|------|------|
| UV-Vis | 電子遷移 | 共役系 · 吸収波長 |
| IR | 振動 | 官能基 |
| NMR | 核スピン | 化学環境 |
| MS | イオン化 | m/z · 構造推定 |

**Beer–Lambert 法則**: A = ε l c（吸光度 = モル吸光係数 × 光路 × 濃度）

---

## 5. 計算化学との接続

ボーン–オッペンハイマー近似下、電子構造計算で得たポテンシャル面 V(r) を分子動力学や自由エネルギー計算の入力とする。
