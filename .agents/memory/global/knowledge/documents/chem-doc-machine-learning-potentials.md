---
chem_doc_id: chem.topic.ml_potentials
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [nnp, active-learning]
chem_doc_regex_file: ^chem\-doc\-machine\-learning\-potentials\.md$
---

<!-- CHEM_DOC_ID: chem.topic.ml_potentials -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 機械学習ポテンシャル

---

## 1. 位置づけ

| 手法 | 精度 | 速度 | 汎用性 |
|------|------|------|--------|
| DFT/ab initio | 高 | 低 | 広い |
| 古典力場 | 低–中 | 高 | パラメータ依存 |
| ML ポテンシャル | 中–高 | 中–高 | 学習データ範囲内 |

---

## 2. 学習問題

入力: 原子配置 R（回転並進不変な記述子）

出力: エネルギー E(R), 力 F_i = −∂E/∂R_i

**力の一致学習** — 自動微分でエネルギーと力を一貫

---

## 3. アーキテクチャ

| 型 | 特徴 |
|----|------|
| Behler–Parrinello | 対称関数 + ニューラルネット |
| SchNet, PaiNN | 連続フィルタ畳み込み |
| NequIP, MACE | E(3) 等変性 · 高データ効率 |

---

## 4. Δ-学習

E_total = E_forcefield + E_ML^Δ

既存力場の系統誤差を NN で補正。

---

## 5. 精度指標

RMSE(E), RMSE(F) — 力の誤差が MD 安定性に直結

外挿（学習域外の構造）では発散リスク

---

## 6. 能動学習

1. 初期データでモデル学習
2. MD/サンプリングで不確実性の高い構造を **query**
3. DFT でラベル付け → 再学習

**注意**: 平衡構造のみのデータでは遷移状態 · 障壁付近が欠落 → query 設計が重要

---

## 7. パイプライン

DFT 教師データ → ML ポテンシャル → 大規模 MD → PMF / ΔG 計算
