# Memory reason — checklist

**When**:
- after **memory-reference** + **context-guard**（Loop1: **mini** · Loop2/reanchor: **full**）
- again after **action-evaluate** + **memory-critique**（full evaluate 時のみ）

Paths: [`../../memory-reference/references/global-paths.md`](../../memory-reference/references/global-paths.md)

## Loop1 mini（標準）

1. Verify **nav.yaml** Phase 0 fields vs recall report
2. List **this turn** new/changed Facts/Decisions/Assumptions/Open（chat + turn-brief）
3. Assign **scope** per item
4. Propose **flush** L1 · L2 if context-guard `pre_compact` / high pressure
5. Propose **nav updates**（next_actions, session_intent, alignment sync）
6. **Do not** re-derive P/H from chat alone

## Loop2 / reanchor full

1. All mini steps
2. Merge **nav-brief** + **project-state** deltas
3. Run **promotion-graph** + glossary criteria if term-related
4. Ingest evaluate/critique scores
5. Propose flush L2 if record/gate/alignment/turn_reward<0.6
6. Propose role-execute additions（doc-record, …）

## Pass to memory-record

nav.yaml updates are **mandatory** every standard turn（see [`../../memory-record/assets/state/nav-write-template.yaml`](../../memory-record/assets/state/nav-write-template.yaml)）

## Limits

- ≤3 **next_actions**
- ≤3 new project thread entries per turn
- Merge into existing thread when same plan slug

## Do not

- Loop1 full reason when mini suffices（except pre_compact）
- Promote to docs without criteria
- L2 lesson when critique confabulation high
