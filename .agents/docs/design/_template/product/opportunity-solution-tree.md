# Opportunity Solution Tree（OST · 軽量テンプレ）

**用途**: P0–P2 discovery · continuous discovery の **可視化スケルトン**。  
**正本配置**: `docs/design/product/opportunity-solution-tree.md`（任意 · 不確実性が高いとき）

> フル OST ツールの代替ではない。charter · 要求 · plan criteria への **橋渡し**（p-01 · p-05 · t-04）。

---

## Outcome（product outcome · 1 件）

| 項目 | 内容 |
|------|------|
| **Product outcome** | （顧客行動・感情の leading indicator · 1 文） |
| **Charter リンク** | `docs/design/product/charter.md` §成功指標 |
| **測定** | （どう知るか · 未設定なら「TBD」） |

---

## Opportunities（顧客の機会 · ≤5）

| ID | Opportunity（顧客の課題・ニーズ） | 証拠（インタビュー · データ · 仮説） | 優先 |
|----|-----------------------------------|--------------------------------------|------|
| O-1 | | | H / M / L |
| O-2 | | | |

---

## Solutions（解決案 · 各 Opportunity に 1–3）

| Opportunity | Solution 案 | キット接続 |
|-------------|-------------|------------|
| O-1 | | P3 design / H4 program |
| O-1 | | 別案 |

---

## Assumption tests（実験 · spike 候補）

| Solution | 仮説 | 最小実験（S0 / spike） | 結果 |
|----------|------|------------------------|------|
| | | | pending |

---

## キット接続

| OST 層 | キット |
|--------|--------|
| Outcome | charter · P6 `outcome-check-block` |
| Opportunity | P1 `要求.md` · verification-questions |
| Solution | P3 · H4/H5 plan |
| Experiment | S0 spike · P6 前プロト |

**順序**: OST（discovery）→ **RICE**（複数 unit 順序 · `rice-prioritization-block.md`）→ plan-record

**非採用**: 週次顧客インタビュー手順のキット化（プロジェクト運用）
