---
name: pm-turn-end
description: End every agent turn—score the turn, flush chat into episode/nav memory, update next_actions. Use before the final user reply after work finishes. Also after failed tools or when context pressure is high.
---

# PM turn end

**Role**: PM · **Chain**: [`_chains/pm-turn.md`](../_chains/pm-turn.md) · **IO contract**: [`../lib-memory-io/SKILL.md`](../lib-memory-io/SKILL.md)

## Steps

1. **action-evaluate** — full | mini | skip ([`../action-evaluate/SKILL.md`](../action-evaluate/SKILL.md))
2. **memory-critique** — only if full evaluate ([`../memory-critique/SKILL.md`](../memory-critique/SKILL.md))
3. **memory-flush** — L1 default; L2 if pre_compact / low reward ([`../memory-flush/SKILL.md`](../memory-flush/SKILL.md))
4. **memory-record** — **nav.yaml REQUIRED** + episode + index ([`../memory-record/SKILL.md`](../memory-record/SKILL.md))
5. **memory-refine** — conditional only

## L1 required writes

| Path | Required |
|------|----------|
| `.agents/memory/state/nav.yaml` | yes — `updated`, `next_actions`, pressure clear if done |
| `.agents/memory/episodes/YYYY-MM-DD-*.md` | yes (non-lightweight) |
| `.agents/memory/index.yaml` | touch `updated` |

## Do not

Skip nav update on standard turns. Write traces/evaluations on every turn (L2 only).

**Canonical**: `docs/PM_ROUTING.md` · `docs/MEMORY_ARCHITECTURE.md`
