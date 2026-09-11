# Design deliberation — workflow detail

Decide **what to build** at the current **H level**（`lifecycle-reference`）. P4 planning → **plan_slicer**.

## Steps

0. **Research** — 探索型（options・方針・比較）→ **`landscape-research`**（広→狭 WebSearch）→ landscape report  
   **用語** → **`terminology-research`**（狭く深い · alignment 表）— 両方必要なら landscape 先
1. `lifecycle-reference` + `design-reference` — which H is unfixed?
2. **Goal** — one sentence tied to parent H
3. **Options** — 2–4 with pros/cons（**おすすめ 1** を明示）
4. **Recommendation** + assumptions
5. **Open questions** for the user
6. Draft `>` block for user 殴り書き
7. Next: `design-record` — **not** plan until P3 + user confirm for program/algorithm

## Artifact

`docs/design/<topic>.deliberation.md` — [docs/design/_deliberation-template.md](../../../../docs/design/_deliberation-template.md)

## Do not

- Write `.agents/plans/` or application code
- Set `status: agreed` without user confirmation
