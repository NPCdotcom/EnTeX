---
math_doc_id: math.meta.index
math_doc_topic: math
math_doc_kind: meta
math_doc_tags: [index, regex]
math_doc_regex_file: ^math-doc-meta-INDEX
---

<!-- MATH_DOC_ID: math.meta.index -->
<!-- MATH_DOC_KIND: meta -->
<!-- MATH_DOC_TOPIC: math -->

# 数学ドキュメント索引

`documents/` 直下のフラット配置。各ファイルは **単体完結** の数学文書（学習フェーズ・サイクル番号は本文に埋め込まない）。

**再編纂**: 2026-06-19 — P9 深化（48 サイクル）· 論理数学 L01–L23 · Clawpack 外部検証を反映。

## 正規表現

```text
全件:     ^math-doc-.*\.(md|yaml)$
トピック: ^math-doc-(?!meta-)[a-z0-9-]+\.md$
ID:       <!-- MATH_DOC_ID: ([\w.]+) -->
```

## 一覧（22 件）

### 全体像 · 基礎

- `math-doc-mathematics-overview.md` — `math.topic.overview`
- `math-doc-foundations-logic-proofs.md` — `math.topic.foundations_logic`（P1 入口）
- `math-doc-mathematical-logic-advanced.md` — `math.topic.mathematical_logic`（MSC 03 体系）

### 代数学 · 解析 · 幾何

- `math-doc-number-systems-elementary-algebra.md` — `math.topic.numbers_algebra`
- `math-doc-calculus-differential-equations.md` — `math.topic.calculus_ode`
- `math-doc-analysis-series.md` — `math.topic.analysis_series`
- `math-doc-linear-algebra.md` — `math.topic.linear_algebra`
- `math-doc-abstract-algebra.md` — `math.topic.abstract_algebra`
- `math-doc-number-theory-cryptography.md` — `math.topic.crypto`
- `math-doc-geometry-topology.md` — `math.topic.geometry_topology`
- `math-doc-complex-analysis-pde.md` — `math.topic.complex_pde`

### 離散 · 確率 · 数値

- `math-doc-discrete-mathematics.md` — `math.topic.discrete`
- `math-doc-probability-statistics.md` — `math.topic.probability_statistics`
- `math-doc-numerical-analysis.md` — `math.topic.numerical_analysis`

### P9 深化（検証済み）

- `math-doc-measure-theory-lebesgue-integration.md` — `math.topic.measure_theory`
- `math-doc-graph-theory-extremal-spectral.md` — `math.topic.graph_theory`
- `math-doc-functional-analysis.md` — `math.topic.functional_analysis`
- `math-doc-spectral-theory-operators.md` — `math.topic.spectral_theory`
- `math-doc-game-theory-nash-minimax.md` — `math.topic.game_theory`
- `math-doc-computational-complexity-ppad.md` — `math.topic.ppad`
- `math-doc-numerical-hyperbolic-schemes.md` — `math.topic.hyperbolic_numerical`
- `math-doc-online-learning-algorithms-games.md` — `math.topic.online_learning_games`

### メタ

- `math-doc-meta-REGISTRY.yaml`

## 読み方（推奨）

```text
overview → 関心分野の topic doc
基礎     → foundations_logic → mathematical_logic（論理を深める場合）
P9 横断  → hyperbolic_numerical + online_learning_games + graph_theory + functional_analysis
         → overview § P9 横断表
```
