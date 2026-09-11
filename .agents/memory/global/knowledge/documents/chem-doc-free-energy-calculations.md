---
chem_doc_id: chem.topic.free_energy
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [fep, ti, bar, mbar]
chem_doc_regex_file: ^chem\-doc\-free\-energy\-calculations\.md$
---

<!-- CHEM_DOC_ID: chem.topic.free_energy -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 自由エネルギー計算

---

## 1. 熱力学量と分配関数

**Helmholtz 自由エネルギー**: F = −kT ln Z

**分配関数**: Z = ∫ exp(−U/kT) dq

凝縮相では G ≈ F。平衡定数:

K = exp(−ΔG/kT)

**重要**: 平均エネルギー ⟨E⟩ だけでは G は決まらない。**エントロピー（位相空間体積）** が G に含まれる。

---

## 2. Zwanzig FEP（自由エネルギー摂動）

状態 A から B へポテンシャルを一撃変更:

ΔG = −kT ln ⟨ exp(−ΔU/kT) ⟩_A

ΔU = U_B − U_A

| 条件 | 結果 |
|------|------|
| 良い重なり | 指数因子が安定 |
| 悪い重なり | 少数サンプル支配 → 大分散 |

---

## 3. 熱力学的積分（TI）

λ 結合ポテンシャル: U(λ) = (1−λ)U_A + λU_B

ΔG = ∫₀¹ ⟨dU/dλ⟩_λ dλ

段階的 λ 走査で重なりを改善。alchemical 変換（原子タイプの漸次変更）に使用。

---

## 4. BAR（Bennett Acceptance Ratio）

双方向サンプル（A と B 両方）を用いる自己無撞着方程式。2 状態間で FEP より頑健。

---

## 5. MBAR（Multistate Bennett Acceptance Ratio）

K 個の λ 状態を統合。全状態間の ΔG を同時推定。

---

## 6. 方法の選択指針

| 手法 | 適用 |
|------|------|
| FEP | 2 状態 · 良い重なり |
| TI | λ 連続 · alchemical |
| BAR | 2 状態 · 双方向 |
| MBAR | 多 λ 統合 |

実装: GROMACS, OpenMM, pymbar

---

## 7. 応用

結合自由エネルギー ΔG_bind · 酸化還元電位 · 相平衡 · 溶媒効果 · 触媒選択性

### 調和振動子の検証例
U = ½kx² で k のみ変更: 解析解 ΔG = (kT/2) ln(k_B/k_A)
