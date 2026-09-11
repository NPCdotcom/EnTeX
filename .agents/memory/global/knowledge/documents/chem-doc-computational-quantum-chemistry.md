---
chem_doc_id: chem.topic.computational_quantum
chem_doc_topic: chemistry
chem_doc_kind: topic
chem_doc_tags: [dft, hartree-fock, scf]
chem_doc_regex_file: ^chem\-doc\-computational\-quantum\-chemistry\.md$
---

<!-- CHEM_DOC_ID: chem.topic.computational_quantum -->
<!-- CHEM_DOC_KIND: topic -->
<!-- CHEM_DOC_TOPIC: chemistry -->

# 計算化学と量子化学

---

## 1. 計算の階層

`	ext
古典力学（力場）
  → 半経験（AM1, PM6）
  → ab initio: Hartree–Fock → 相関（MP2, CI, CC）
  → DFT（密度汎関数）
`

**ボーン–オッペンハイマー近似** — 核は固定、電子のみ量子力学で扱う。

---

## 2. 基底関数

| 系列 | 特徴 |
|------|------|
| STO-nG | 最小基底 |
| 6-31G(d,p) | 標準分割価 |
| cc-pVTZ | 相関整合 |

精度 ↑ = 計算コスト ↑

---

## 3. Hartree–Fock と SCF

**Roothaan 方程式**: F C = S C ε

密度行列: P = C_occ C^T

**SCF 循環**: 初期 P → F(P) 構築 → 対角化 → 新 P → 収束まで反復

---

## 4. 密度汎関数理論（DFT）

Hohenberg–Kohn: 基底状態エネルギーは電子密度 ρ(r) の汎関数

Kohn–Sham 方程式: 有効1電子ハミルトニアン + 交換相関汎関数 E_xc[ρ]

| 汎関数 | タイプ |
|--------|--------|
| LDA | 局所密度 |
| PBE, BLYP | GGA |
| B3LYP | ハイブリッド |

---

## 5. 用途

- 分子構造最適化 · 振動解析（IR）
- 遷移状態（TS）探索 · IRC
- 固体（周期境界条件、VASP 等）
- 励起状態（TD-DFT）

---

## 6. 分子力学との接続

力場 U = U_bond + U_angle + U_torsion + U_LJ + U_elec

量子計算で得たパラメータや Δ-学習で補正 → 大規模 MD へ
