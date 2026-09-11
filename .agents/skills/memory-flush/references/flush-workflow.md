# Memory flush — chat to files

**When**: ターン終端。**L1 標準** — **memory-reason** の `proposed flush level` + **scope** に従う。

Paths: [`../../memory-reference/references/global-paths.md`](../../memory-reference/references/global-paths.md)  
Routing: [`../../memory-record/references/scope-routing.md`](../../memory-record/references/scope-routing.md)

## Levels

| Level | 動作 |
|-------|------|
| **L1** | project episode + **traces/** + **evaluations/**（action-evaluate/critique 出力） |
| **L2** | L1 + knowledge/state + history + memory-refine トリガ |
| **L0** | index `updated` のみ（例外） |

L2 追加条件: turn_reward<0.6 · confabulation_risk:high · alignment · gate · *-record · Facts≥2 · **context-guard pre_compact/high**

## nav.yaml（毎ターン）

memory-record が **必ず** `.agents/memory/state/nav.yaml` を更新（L0 軽量除く · 最低 `updated` + turn_estimate）。

pre_compact: **L2 必須** + nav 全フィールド + episode + trace/eval。

## Scope routing（L2 knowledge）

| 内容 | scope |
|------|-------|
| ターン作業・Open | project → episodes |
| trace / eval | project → traces/ · evaluations/ |
| プロジェクト用語 | project → knowledge/alignment |
| 横断教訓 | global → lessons（**trace 必須**） |
| gate / phase | team → project-state |

**Episodes · traces は append-only**。global に thread/episodes 禁止。

## Workflow

1. Input: memory-reason report + action-evaluate + memory-critique
2. Write evaluations YAML + trace MD → **memory-record**
3. Facts/Decisions → reason 指定 path
4. Assumptions/Open → episodes + thread
5. memory-refine if L2 or refine_needed

## Do not

- reason 無し glossary 昇格
- trace/critique 無し L2 lesson
- traces 上書き
- 推測を Fact 化
