# Memory critique — checklist

**Input**: memory-reference report · action-evaluate scores · 今ターン chat/brief

## Self-RAG 型（必須）

| ID | Check | pass 条件 |
|----|-------|-----------|
| **IsRel** | recall 項目が今ターン topic に relevant | 無関係 anchor ≤1 または on_demand のみ |
| **IsSup** | 出力・action が memory/docs で supported | 未支持 claim = Assumption |
| **IsUse** | recall が brief 達成に寄与 | action-evaluate task_progress と整合 |
| **IsStale** | 古い thread/alignment が active のまま | supersedes または archive 提案 |
| **IsConflict** | project / global / team 矛盾 | project 優先 · conflict 行を列挙 |
| **IsNav** | 実行が nav.next_actions / session.intent と一致 | mismatch → refine_needed · Loop2 推奨 |

## Confabulation ガード

| Signal | 判定 |
|--------|------|
| 失敗後に原因未検証で lesson 候補 | `confabulation_risk: high` |
| binary pass/fail のみで reflection | `feedback_granularity: low` |
| trace / verifiable 無しで Fact | **reject write** |

## Output fields

- `memory_grounding` — 0.0–1.0（action-evaluate へ反映）
- `confabulation_risk`: low | medium | high
- `competency_gaps`: [] — MemoryAgentBench 4 能力
- `refine_needed`: yes | no

## Do not

- Actor が critique をスキップ
- high confabulation で L2 lesson 昇格
