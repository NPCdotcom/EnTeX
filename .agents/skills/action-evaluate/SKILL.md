---
name: action-evaluate
description: Score whether this turn advanced the goal and followed the plan. Use after finishing work or answering, before saving memory.
---

# Action Evaluate

**Tier**: L1 · **Chain**: [`_chains/pm-turn.md`](../_chains/pm-turn.md) §evaluate

| Mode | When |
|------|------|
| **full** | execution · Loop2 · reanchor |
| **mini** | Loop1 read-only (Role 0) |
| **skip** | lightweight |

nav mismatch → turn_reward ≤ 0.5 · [PM_ROUTING.md](../../docs/PM_ROUTING.md) § evaluation

Rubric: [`references/rubric.md`](references/rubric.md) · deep evaluate: **evaluate-reference** (L2)

Canonical: [AGENT_EVALUATION.md](../../docs/AGENT_EVALUATION.md)
