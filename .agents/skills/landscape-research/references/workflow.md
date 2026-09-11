# Landscape research — workflow

Policy: `docs/LANDSCAPE_RESEARCH_POLICY.md`

## Phase 0 — Frame

1. ユーザー問いを **1 文** に固定
2. **5–7 独立軸** に分解（例: memory / reward / trace / goal eval / memory quality / tooling）
3. 各軸に **scan 用キーワード** 1 行（[`scan-queries.md`](scan-queries.md)）
4. 既知正本を Read（`docs/` · global memory）— 重複調査を避ける

## Phase 1 — Scan（広く浅く · 並列）

- **WebSearch: 軸の数だけ並列**（最低 4 · 推奨 5–7）
- 各結果: タイトル · URL · 1–2 文要約 · **tags**（論文/ブログ/公式/ survey）
- **禁止**: この段階で「だから X を実装」と書く
- 出力: [`../assets/outputs/scan-map-template.md`](../assets/outputs/scan-map-template.md)

目安: 1 軸あたり top 2–3 ヒットをメモすれば足りる（深読みしない）。

## Phase 2 — Cluster

1. **重複** — 同一論文・同一概念を 1 行に
2. **対立** — A vs B（例: RLHF vs RLVR）
3. **空白** — scan で見えなかった角
4. **Hooks** — 第2波で深掘りする **2–4 点**（名前付き: 論文名 · フレームワーク名）

ユーザー関心・brief の P/H に合わせて hooks を選ぶ。

## Phase 3 — Drill（狭く深く）

- hooks **各 1–2 追加クエリ**（合計 ≤ 8 追加）
- 必要なら **browser MCP** 1–2 ページ（論文 abstract · 公式 doc）
- 各 hook: 主張 · 根拠 · キットへの含意 · 反証リスク
- 出力: [`../assets/outputs/drill-summary-template.md`](../assets/outputs/drill-summary-template.md)

## Phase 4 — Map

キットへの写像（表形式）:

| 調査結果 | 写先 |
|----------|------|
| 学習モード（未検証） | `learning/<topic>/notes/` |
| durable 横断知見 | global `lessons/` |
| repo 固有 | project `lessons/` |
| 方針・gate | `docs/` · deliberate |
| 新 skill / rule | `kit_maintainer` 行 |
| 用語が残る | → **terminology-research** へ委譲 |

## Phase 5 — Critique

- 反証 · confabulation リスク · 「未検証 Assumption」
- 第1波で見逃した bias（最初の軸に偏っていないか）

## Phase 6 — Record

1. [`../assets/outputs/landscape-report-template.md`](../assets/outputs/landscape-report-template.md) 完成
2. **memory-reason** — scope · lesson 昇格 · flush L2 提案
3. 運用証跡: `調査: landscape-research | scan:N drill:M`

## Cursor tools

```
Frame → parallel WebSearch (Phase 1)
→ Cluster (chat/reason, no new tools)
→ WebSearch (+ optional browser) (Phase 3)
→ memory-reason → memory-flush/record
```

## Do not

- Scan 前に drill（偏り）
- terminology 定義を landscape で完結
- drill 無しで landscape report 完了宣言
