---
math_doc_id: math.topic.mathematical_logic
math_doc_topic: math
math_doc_kind: topic
math_doc_tags: [logic, incompleteness, set-theory, computability, model-theory]
math_doc_regex_file: ^math-doc-mathematical\-logic\-advanced\.md$
---

<!-- MATH_DOC_ID: math.topic.mathematical_logic -->
<!-- MATH_DOC_KIND: topic -->
<!-- MATH_DOC_TOPIC: math -->

# 数理論理学（形式体系と基礎）

**MSC**: 03（Mathematical logic and foundations）  
**前提**: `math-doc-foundations-logic-proofs.md`（素朴集合論 · 証明技法 · 記号）  
**接続**: `math-doc-computational-complexity-ppad.md` · `math-doc-number-theory-cryptography.md`

---

## 1. 形式言語と推論

### 命題論理

- **構文**: 原子公式 · ¬ ∧ ∨ → · 括弧による well-formed 公式
- **意味論**: 真理表 · 充足 · トートロジー（恒真）· 矛盾
- **推論**: 自然演繹 NJ またはヒルベルト系 · **健全性** ⊢ φ ⇒ ⊨ φ
- **正規形**: CNF/DNF · 解決法（resolution）による refutation

### 一階述語論理

| 概念 | 内容 |
|------|------|
| 項 | 定数 · 変数 · 関数記号の合成 |
| 公式 | 原子 P(t₁,…,tₙ) · 論理結合子 · ∀x · ∃x |
| 構造 𝔐 | 領域 · 定数・関数・関係の解釈 |
| 充足 | 𝔐 ⊨ φ（構造が公式を真にする） |

**ゲーデル完全性定理**: 有限の意味で ⊨ φ ⟺ ⊢ φ。  
**コンパクト性定理**: 任意の公式集合 Γ が有限部分ごとに充足可能なら Γ 自体が充足可能。  
**Löwenheim–Skolem**: 無限モデルを持つ countable 言語の理論は可算無限モデルも持つ（非標準算術の動機）。

---

## 2. 公理的集合論（ZFC）

### ZFC 公理（要約）

空集合 · 対 · 和集合 · 冪集合 · 無限 · 置換 · 正則性 · 選択（AC）。

ラッセルのパラドックスは「集合の集合」ではなく **限定された公理体系** で回避する。

### 順序数と基数

- 順序数: 推移的集合 · ω = {0,1,2,…} · 超限帰納
- 基数 ℵ₀, 2^ℵ₀: 連続体仮説（CH）は ZFC から独立（Cohen forcing）
- **選択公理（AC）** の等价形: ツォル補題 · 整列定理 · 各種選択原理

---

## 3. 計算可能性

### チューリング機械とチャーチ–テーリング

部分再帰関数 = チューリング可算 = λ 可算（等価な計算モデル）。

### 停止問題と帰着

HALT = {(M,w) : M(w) 停止} は **判定不能**。  
任意の判定不能問題へ **多対一帰着** で帰着可能。

### 算術階層（Post）

| 階層 | 定義（概略） |
|------|-------------|
| Σ⁰_n | ∃…∃Π⁰_{n−1} 形の算術公式で定義される集合 |
| Π⁰_n | 補集合 |
| Δ⁰_n | Σ⁰_n ∩ Π⁰_n |

**Post 定理**: Σ⁰_n と Π⁰_n は n ≥ 1 で異なる（完全性の階層的分離）。

### Turing 度

a ≤_T b: a が b のオラクルで計算可能。  
**0′** = HALT の度 · **ジャンプ演算子** · r.e. 集合 ↔ 再帰可算列挙可能度。

**Priority argument**: 要求（requirements）を優先度付きで同時に満たす構成法（度論・r.e. 度の標準技法）。

---

## 4. 不完全性と証明論

### ゲーデル第一・第二不完全性定理

十分強い再帰的公理化算術 T（例: PA）について:

- **G1**: T が ω-整合なら「Con(T)」に相当する文は T で証明不能
- **G2**: T が整合なら Con(T) は T で証明不能

**算術化**: 証明 · 公式 · 充足を自然数上の関係として符号化 · **対角化補題** · Prov_T(x)。

### 証明論

- **Gentzen**: PA に対するカット除去 · 証明論的順序数 ε₀ 以上
- **Goodstein 定理**: PA では証明不能だが ZFC では証明可能（具体的不完全性）
- **Paris–Harrington**: 組合せ的に自然な PA 独立命題

---

## 5. モデル理論

### 初等等価と型

- 𝔐 ≡ 𝔑: 同じ一階文を真にする（初等等価）
- **型**: 変数の一貫な性質の集合 · omitting types · 初等埋め込み

### 安定性（入口）

完全理論 T が **κ-安定** ⇔ |S(A)| ≤ κ  for |A| ≤ κ（型の数に上界）。  
**Morley ランク**: 定義可能集合の次元のような不変量 · ω-安定 ⟹ カテゴリカル（同基数モデルは同型）。

### ブール代数（代数的論理学）

Lindenbaum–Tarski 代数: トートロジー同値類による商 · Stone 対偶性（位相空間との対応）。

---

## 6. 記述集合論・大基数・決定性

### 記述集合論（Borel 階層）

ℝ 上の Borel 集合 · 射影集合（解析 · coanalytic · Π¹₁ 等）。  
**Suslin 問題** · 決定性仮説との接続。

### Forcing（Cohen）

部分順序 (P, ≤) と **generic フィルタ** G によりモデル V[G] を構成。  
CH の独立性: 可算閉包条件付き forcing で 2^ℵ₀ = ℵ₂ を実現。

### 大基数

不可達 · Mahlo · 弱コンパクト · 可測基数等 — ZFC の整合性より強い存在仮定。  
**forcing ↔ 大基数**: 射影決定性 · 大基数の存在が決定性原理と等価（サーベイレベル）。

### 決定性（Gale–Stewart ゲーム）

2 プレイヤーが整数の有限列を交互に選び、勝利集合 W ⊆ ω^ω で勝敗決定。  
**Martin 1975**: Borel 勝利集合のゲームは **決定的**（ZFC）。  
**AD**（全集合決定的）: AC と両立しない · 大基数と射影決定性の関係。

---

## 7. 知識の階層（統合）

```text
証明技法（P1）
  → 形式論理・ZFC（L1–L3）
    → 計算可能性・不完全性（L4–L5）
      → モデル理論（L6）
        → 深化: 安定性 · 度 · forcing · 決定性（L14–L23）
```

| 問い | 参照節 |
|------|--------|
| 真 ⇔ 証明可能？ | §1 完全性 · §4 G1/G2 |
| 何が計算可能？ | §3 TM · HALT |
| 集合論の限界？ | §2 ZFC · §6 forcing |
| NE は計算可能？ | `math-doc-computational-complexity-ppad` |

---

## 8. 推奨文献

| 文献 | 用途 |
|------|------|
| Enderton, *A Mathematical Introduction to Logic* | §1 |
| Jech / Kunen | §2 · §6 forcing |
| Sipser, *Introduction to the Theory of Computation* | §3 |
| Smith, *An Introduction to Gödel's Theorems* | §4 |
| Marker, *Model Theory* | §5 |
| SEP（Stanford Encyclopedia of Philosophy）各論理項目 | 全体補助 |
