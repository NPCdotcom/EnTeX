---
name: action-evaluate
description: Score whether this turn advanced the goal and followed the plan. Use after finishing work or answering, before saving memory.
---

# Action Evaluate

**Tier**: L1 ﾂｷ **Chain**: [`_chains/pm-turn.md`](../_chains/pm-turn.md) ﾂｧevaluate

| Mode | When |
|------|------|
| **full** | execution ﾂｷ Loop2 ﾂｷ reanchor |
| **mini** | Loop1 read-only (Role 0) |
| **skip** | lightweight |

nav mismatch 竊・turn_reward 竕､ 0.5 ﾂｷ [PM_ROUTING.md](../../docs/PM_ROUTING.md) ﾂｧ evaluation

Rubric: [`references/rubric.md`](references/rubric.md) ﾂｷ deep evaluate: **evaluate-reference** (L2)

Canonical: [AGENT_EVALUATION.md](../../docs/AGENT_EVALUATION.md)
