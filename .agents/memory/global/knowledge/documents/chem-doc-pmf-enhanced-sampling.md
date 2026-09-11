---
chem_doc_id: chem.topic.pmf_sampling
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [umbrella, metadynamics, pmf]
chem_doc_regex_file: ^chem\-doc\-pmf\-enhanced\-sampling\.md$
---

<!-- CHEM_DOC_ID: chem.topic.pmf_sampling -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# ポテンシャル平均力と拡張サンプリング

---

## 1. 反応座標

分子の変換を記述する集合変数 **ξ**（例: 結合距離 · 二面角 · RMSD · 配位数）

---

## 2. ポテンシャル平均力（PMF）

W(ξ) = −kT ln p(ξ)

p(ξ): ξ の確率分布（正規化済み）

**活性化自由エネルギー**: ΔG‡ ≈ W(ξ‡) − W(ξ_react)

---

## 3. Umbrella サンプリング

バイアスポテンシャル: V_bias(ξ) = ½k(ξ − ξ₀)²

複数の窓 ξ₀ を重ね、WHAM 等で重み付け結合:

w = exp(V_bias/kT)

**窓設計**: 隣接窓で十分な重なり · k が強すぎるとサンプリング狭い

---

## 4. メタダイナミクス

履歴にバイアスを積み上げ:

V_bias(ξ, t) = Σᵢ w exp(−|ξ − ξ(tᵢ)|² / 2σ²)

**Well-tempered MetaD**: 効果的重み w_eff = w exp(−V_bias/(kTΔT))

平衡 PMF ≈ −V_bias（十分長時間後）

---

## 5. 手法比較

| 手法 | 特徴 |
|------|------|
| Umbrella | 窓を事前配置 · 1D に強い |
| MetaD | 探索的自動 · 高次元向き |
| SMD + Jarzynski | 非平衡仕事から ΔG |
| FEP/TI | 2 状態間 ΔG（ξ 不要な場合） |

---

## 6. 二重井戸モデル

U(ξ) = W(ξ² − 1)² — 井戸間障壁高さ W が ΔG‡ のオーダー

Umbrella 窓を障壁付近に配置しないと遷移状態をサンプリングできない。
