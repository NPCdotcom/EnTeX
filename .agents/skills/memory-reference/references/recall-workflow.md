# Memory reference — recall workflow

Resolve paths: [`global-paths.md`](global-paths.md)

## Bootstrap contract（fail hard · do not soft-skip）

Before Phase 0, verify required paths exist under project memory root
(`.agents/memory/` or kit `memory/` when cwd is the kit):

| Path | Missing action |
|------|----------------|
| `state/nav.yaml` | **ERROR** `nav: missing` — stop Edit/conduct; copy `nav.yaml.example` then re-read |
| `index.yaml` | **ERROR** `index: missing` — copy `index.yaml.example` |
| `episodes/` | **ERROR** `episodes: missing` — `mkdir episodes`（bootstrap contract） |
| `audit/audit-log.md` | **ERROR** `audit-log: missing` — copy `audit-log.md.example` |

Report each ERROR in the recall report. Do not invent next_actions from chat when nav is missing.

## Phase 0 — Control Plane（最優先 · budget より前）

**Before** project index budget:

1. Read `.agents/memory/state/nav.yaml`（missing → **ERROR** above · do not continue as if OK）
2. Extract mandatory fields:
   - `session.intent`
   - `navigation.next_actions`（≤3）
   - `navigation.active_thread_id` · `active_plan`
   - `alignment.phase` · `scope_level` · `gate_status`
   - `pressure.reanchor_required` · `pre_compact_recommended`
3. If `active_thread_id` set → read that index entry **before** other threads
4. If `active_plan` set → read plan frontmatter（status, scope_level, criteria）

**Output Phase 0 block** in recall report（必須）。

## Phase A — Project index

**After** Phase 0 — apply **project read budget**:

| granularity | max every_turn |
|-------------|----------------|
| anchor | 5 |
| thread | 3 |
| episode (latest) | 2 |

## Phase B — Global index

**After** project tier — read global index:

| granularity | max every_turn |
|-------------|----------------|
| anchor | 2 |
| other | skip unless tags match current topic |

If global index missing → `global_index: missing`; continue.

## Phase C — Team canonical

1. `docs/project-state.yaml` — **Loop2 / reanchor / context-guard loop2 時は必読**
2. Loop1 標準: project-state は **nav.alignment 引用で足りる場合は skip 可**（正確性: 不一致1つでも read）
3. Linked team paths from project index（`recall: every_turn`）

## Priority merge

1. **nav.yaml**（Phase 0）
2. project index — `recall: every_turn`
3. global index（budget 内）
4. project-state（Loop2 / mismatch 時）
5. project episodes — `next_turn` + latest 2
6. knowledge — project first, then global
7. history — on_demand only

**Conflict**: same topic → **project > global > team summary**. **nav.next_actions** beats chat memory.

Then **memory-reason**（Loop1: mini · Loop2: full）。

index に無い Fact → 未記録。

## Output

[`assets/state/recall-report-template.md`](../assets/state/recall-report-template.md)

Do not write files.
