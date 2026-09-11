# AGENT_EVALUATION.md 正本 — 行動・記憶・報酬

**方針**: 長期記憶を **行動の根拠** として評価する。Actor（実行）と Evaluator（採点）を分離。

関連: `docs/MEMORY_ARCHITECTURE.md` · `docs/CURSOR_ROLES.md`

## 三層評価

| 層 | 何を測る | 主 Skill | 出力先 |
|----|----------|----------|--------|
| **Task** | ゴール達成・gate | action-evaluate | `evaluations/` |
| **Trajectory** | brief vs 実行・手順遵守 | action-evaluate | `traces/` + `evaluations/` |
| **Memory** | recall 根拠・矛盾・陳腐化 | memory-critique | `evaluations/` |

**P6 中期評価**（plan drift / プロジェクト監査）は別系統: `evaluate-reference` → `plan-evaluate` / `project-evaluate`（`evaluator` role）。

## 調査と評価

| 系統 | Skill | 評価への接続 |
|------|-------|--------------|
| 探索 Web 調査 | **`landscape-research`** | scan map + drill → landscape report → `process_compliance` · global lesson |
| 用語調査 | **`terminology-research`** | alignment → `memory_grounding` · glossary G1–G5 |

探索型で **第1波のみ**（drill 無し）→ `process_compliance ≤ 0.5`。正本: `docs/LANDSCAPE_RESEARCH_POLICY.md`

## 標準 PM ループ（evaluate 段階化）

**正本**: `docs/PM_ROUTING.md` · `skills/_chains/pm-turn.md`

```
0. pm-turn-start
1. [Loop2] nav-brief
2. role-execute
3. pm-turn-end — action-evaluate full|mini|skip → [full] critique → flush → record(nav)
```

**evaluations/ 書き込み**: full evaluate または turn_reward&lt;0.6 または pre_compact 時のみ（L1 では episode に要約で足りる）。

## Turn reward（報酬スキーマ）

毎ターン `evaluations/` に 0.0–1.0 の部分スコア + 合成:

| フィールド | 意味 | 主な根拠 |
|------------|------|----------|
| `task_progress` | ゴールへの寄与 | project-state, brief, ユーザー意図 |
| `process_compliance` | 手順遵守 | secretary-gate 順, Loop1/2, scope, P/H |
| `nav_alignment` | nav 整合 | next_actions · session_intent vs 実行（**mini evaluate**） |
| `memory_grounding` | 記憶の根拠 | memory-critique IsRel/IsSup |
| `verifiable_pass` | 客観検証 | lint/test/git（あれば） |

```yaml
turn_reward: 0.0–1.0   # 加重平均（デフォルト重み: 0.35/0.25/0.25/0.15）
verifiable_checks: []
critique_summary: ""
```

**L2 トリガー追加**: `turn_reward < 0.6` · memory-critique `confabulation_risk: high` · `*-record` 後

## Memory critique（Self-RAG 型）

| チェック | 意味 | fail 時 |
|----------|------|---------|
| **IsRel** | recall した memory が今ターンに relevant | gap 記録、再 recall 提案 |
| **IsSup** | 行動・発言が memory / docs で supported | Assumption へ降格、lesson 昇格禁止 |
| **IsUse** | ターン全体が brief / gate に有用 | action-evaluate と共有 |
| **IsStale** | supersedes 未処理・古い thread | memory-refine で archive 提案 |
| **IsConflict** | project vs global vs team 矛盾 | project 優先、global を archive |

## Trace 記録（AgentTrace 型）

`traces/YYYY-MM-DD-{slug}.md` — **append-only**、1 ターン 1 ファイル可:

| Surface | 内容 |
|---------|------|
| cognitive | plan, reason 要約, 選択理由 |
| operational | tools, files, 成否 |
| contextual | recall ids, docs 参照 |

**lesson 昇格の証拠**は trace または verifiable_checks を必須（confabulation 防止）。

## memory-refine（ReMem 型）

**When**: L2 · turn_reward < 0.6 · IsStale/IsConflict · 50+ index entries

| 操作 | 効果 |
|------|------|
| archive thread | granularity → archive, recall → on_demand |
| supersedes | 古い alignment を新 id にリンク |
| reject_lesson | 証拠なし lesson 候補を却下 |
| prune_index | shard 整理提案 |

書込: **memory-record** 経由のみ。

## スキル分担（既存との境界）

| Skill | タイミング | 境界 |
|-------|------------|------|
| **action-evaluate** | 毎ターン | brief / 単ターン trajectory |
| **memory-critique** | 毎ターン | recall と action の grounding |
| **memory-refine** | 条件付き | index / thread 整理 |
| plan-evaluate | P6 · evaluator | `.agents/plans` ドリフト |
| project-evaluate | P6 · evaluator | プロジェクト全体 |
| review-conduct | P6 · reviewer | コード vs plan/design |

## 研究対応（参考）

| 概念 | 本キット |
|------|----------|
| Reflexion | evaluations の verbal critique → episodes |
| ReMem Refine | memory-refine |
| Self-RAG | memory-critique IsRel/IsSup/IsUse |
| AgentTrace | traces/ 3 surface |
| MemoryAgentBench | memory-critique 4 能力マップ |
| Agent-as-a-Judge | action-evaluate trajectory vs goal |

## 禁止

- critique なしで Assumption → Fact / lesson 昇格
- trace なしで L2 lesson 書込
- Actor が memory-critique をスキップして pass 自己宣言
- 報酬だけ上書きして episode 証拠を消す
