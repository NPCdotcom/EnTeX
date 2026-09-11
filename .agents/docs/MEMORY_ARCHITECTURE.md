# MEMORY_ARCHITECTURE.md 正本 — 長期記憶（三層）

**方針**: Cursor チャットは信用しない。**context-guard → Recall → Reason → Act → Evaluate → Critique → Flush → Refine → Record**。

ルーティング: **`docs/PM_ROUTING.md`** · Control Plane: **nav.yaml** + **project-state.yaml**

評価正本: `docs/AGENT_EVALUATION.md`

## 三層モデル

| 層 | scope | 物理パス | Git | 用途 |
|----|-------|----------|-----|------|
| **Learning** | `learning` | `learning/` · `.agents/learning/` | 一部 | **検証前**調査・実験・教材（→ lessons へ昇格） |
| **Global** | `global` | `%USERPROFILE%\.agents\memory\global\`（Unix: `~/.agents/memory/global/`） | 外 | 横断知識・好み・汎用教訓 |
| **Project** | `project` | `{workspace}/.agents/memory/` | 外 | episode / thread / 作業 state / プロジェクト alignment |
| **Team** | `team` | `{workspace}/docs/` · `.agents/plans/` | **正本** | project-state, glossary, adr, design, plans |

**衝突時**: **project > global > team 要約**（同一トピックはプロジェクト側を優先）。

**Learning 層**: team/global/project の正本ではない。詳細は **`docs/LEARNING_SANDBOX.md`**。

## Git

- **`.agents/memory/`**（project）と **`~/.agents/memory/global/`** は commit しない
- 昇格後の正本のみ `docs/` / `.agents/plans/` を commit
- キット設計思想の正本は **`docs/MEMORY_ARCHITECTURE.md`**（team 層）

## 優先順位（Recall）

```
0. .agents/memory/state/nav.yaml     Control Plane · every_turn Phase 0
1. project index.yaml (+ shards/)     anchor / thread / archive
2. global index.yaml                  anchor（budget 内）
3. docs/project-state.yaml            team canonical（Loop2 / mismatch）
4. project episodes
5. knowledge — project 優先、次 global
6. history — on_demand
7. docs/plans 正本（index / nav.active_plan から）
```

## Control Plane

| ファイル | scope | 用途 |
|----------|-------|------|
| **`state/nav.yaml`** | project | session_intent · next_actions · pressure · alignment mirror |
| **`docs/project-state.yaml`** | team | P/H · gate · active_pdca · blockers |

**next_actions** の正本は **nav.yaml**（brief は引用）。Loop1 では P/H を nav から読む · Loop2 で project-state と同期。

## Global 層

```
~/.agents/memory/global/
├── index.yaml
├── index/shards/          # 50+ entries 時
└── knowledge/
    ├── philosophy/        # ユーザー横断の判断原則
    ├── lessons/           # 技術調査・汎用教訓（プロジェクト非依存）
    └── preferences/       # コーディング/運用の好み
```

**書いてよい**: ブラウザ調査の durable 要約、個人 preferences、複数 repo で再利用する lessons。

**書いてはいけない**: プロジェクト進行、thread、プロジェクト固有 alignment、秘密情報。

初回: `skills/memory-reference/assets/global/index.yaml.example` をコピー。

## Project 層

```
.agents/memory/
├── index.yaml
├── state/
│   └── nav.yaml           # Control Plane · 毎ターン更新
├── episodes/
├── traces/              # append-only · cognitive/operational/contextual
├── audit/               # append-only · audit-log.md（AI-DLC audit.md 相当）
├── evaluations/         # turn scores + critique reports
├── rewards/             # rollup.yaml 累積報酬
├── knowledge/
│   ├── alignment/
│   └── lessons/
└── history/
```

`philosophy/` · `preferences/` は **project には通常作らない**（global へ）。

## Knowledge taxonomy（scope 付き）

| 種別 | scope | パス |
|------|-------|------|
| ターン trace | project | `.agents/memory/traces/` |
| 監査ログ（gate · lifecycle） | project | `.agents/memory/audit/audit-log.md` |
| ターン評価 | project | `.agents/memory/evaluations/` |
| 累積報酬 | project | `.agents/memory/rewards/rollup.yaml` |
| 設計思想（キット共通） | team | `docs/MEMORY_ARCHITECTURE.md` 等 |
| 学習・実験（検証前） | learning | `learning/<topic>/` · `.agents/learning/` |
| 設計思想（ユーザー横断） | global | `global/knowledge/philosophy/` |
| 用語 alignment | project | `.agents/memory/knowledge/alignment/` |
| 汎用教訓 | global | `global/knowledge/lessons/` |
| プロジェクト教訓 | project | `.agents/memory/knowledge/lessons/` |
| 好み | global | `global/knowledge/preferences/` |

**昇格正本**: `docs/glossary/` · `docs/adr/` · `docs/design/` · plans

## Index 粒度と read budget

| 層 | granularity | every_turn 上限 |
|----|-------------|-----------------|
| project | anchor | ≤ 5 |
| project | thread | ≤ 3 |
| project | episode (latest) | ≤ 2 |
| global | anchor | ≤ 2 |
| global | その他 | on_demand |

`summary` ≤ 80 文字。50 entries 超 → `index/shards/*.yaml`

### エントリ 필드

```yaml
id:
scope: global | project | team
tier: index | state | episodes | knowledge | history | traces | audit | evaluations | rewards
granularity: anchor | thread | archive
path:                    # scope に応じた絶対/相対パス
summary:
tags: []
recall: every_turn | next_turn | on_demand
linked: []
supersedes: null
project_id: null         # global index の project 向けエントリのみ（任意）
```

**project_id**（global 側）: git remote URL または workspace フォルダ名。特定プロジェクト向け global メモ用（稀）。

## 毎ターン（PM）

**正本**: `docs/PM_ROUTING.md` · chain: `skills/_chains/pm-turn.md`

| 順 | Skill | Enforcement |
|----|-------|-------------|
| 0–1 | **pm-turn-start**（内包: context-guard → memory-reference → memory-reason → turn-brief → route） | llm-soft |
| 2 | [Loop2] lifecycle → **nav-brief** | llm-soft |
| 3 | role-execute | llm-soft |
| 4 | **pm-turn-end**（evaluate → [critique] → flush → record） | llm-soft |
| 5 | 応答 + 短縮運用証跡 | llm-soft |

preCompact pressure / audit-log 追記: **hook**

## Flush レベル

| Level | 条件 | 動作 | Enforcement |
|-------|------|------|-------------|
| **L1**（標準） | 非軽量ターン | **nav + episode 1 + index touch** のみ | llm-soft |
| **L2** | pre_compact · turn_reward&lt;0.6 · full evaluate · `*-record` 後 · confabulation high | + traces/evaluations/knowledge 等 | llm-soft（skip → episode に gap 記載） |
| **L0** | 挨拶のみ / 記録不要明示 | index `updated` または nav touch | llm-soft |

### Flush ルーティング（scope）

| 内容 | scope | 先 |
|------|-------|-----|
| ターン trace | project | `traces/` |
| ターン評価・critique | project | `evaluations/` |
| 累積報酬 | project | `rewards/rollup.yaml` |
| ターン作業ログ | project | `episodes/` |
| thread 更新 | project | project `index.yaml` |
| プロジェクト用語 alignment | project | `knowledge/alignment/` |
| プロジェクト固有教訓 | project | `knowledge/lessons/` |
| 学習メモ（未検証） | learning | `learning/<topic>/notes/`（昇格前） |
| 横断技術調査・汎用教訓 | global | `global/knowledge/lessons/` |
| ユーザー好み | global | `global/knowledge/preferences/` |
| gate / phase delta | team + project | `docs/project-state.yaml` + project state snapshot |
| 確定用語・ADR | team | `docs/glossary/` 等（doc-record 経由） |

## Reason → 昇格

Skill **`memory-reason`** が promotion graph に従い scope を判定し glossary / adr / design 昇格を **Agent 側で先に提案**。

正本: skill `memory-reason/references/promotion-graph.md`

## Role 実行

**role-execute** — Cursor 内 skill 列。Hermes 禁止。

関連: `docs/CURSOR_ROLES.md` · `docs/TERMINOLOGY_RESEARCH_POLICY.md` · `docs/AGENT_EVALUATION.md` · `docs/LEARNING_SANDBOX.md` · `skills/memory-reference/references/global-paths.md`
