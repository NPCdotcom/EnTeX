# Landscape research — scan query patterns

**Phase 1**: 1 axis = 1 query · **broad** · 年号入れ可（2024 2025 2026）

## 軸の切り方（Frame）

| 軸タイプ | 例 |
|----------|-----|
| 問題域 | `{topic} LLM agent challenges survey` |
| 機構 | `{topic} architecture memory evaluation` |
| 比較 | `{A} vs {B} agent design` |
| ベンチマーク | `{topic} benchmark arxiv` |
| 実装 | `{topic} best practices IDE cursor` |
| リスク | `{topic} failure mode confabulation agent` |
| 運用 | `{topic} production governance` |

## クエリ型

```
# 広域 survey
{topic} survey OR benchmark OR framework 2024 2025

# Named approach（第2波の hook 候補探し）
{topic} Reflexion OR Self-RAG OR "agent memory"

# 実務
{topic} implementation lessons learned
```

## 並列数

| 問いの規模 | Scan 並列 |
|------------|-----------|
| 小（1 決定） | 4 |
| 中（設計章） | 5–6 |
| 大（キット方針） | 6–7 |

## Drill クエリ（Phase 3）

```
"{PaperOrFrameworkName}" {key mechanism}
site:arxiv.org OR site:github.com  # 任意
```

Drill は **Cluster で選んだ 2–4 hooks のみ**。

## 禁止

- 第1波で `{用語} 定義` のみ（→ terminology-research）
- 同一クエリの使い回し（軸が被る）
