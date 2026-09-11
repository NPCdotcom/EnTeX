# L1 chain — PM turn (canonical)

**Tier**: L1 · **Language**: English  
**Only every-turn chain** — replaces memory-turn + secretary-turn.

`
pm-turn-start
→ [Loop2?] lifecycle-reference → secretary-brief (nav-brief)
→ role-execute
→ pm-turn-end
→ reply + short operational trace
`

**pm-turn-start** internals: context-guard → memory-reference → memory-reason(mini) → secretary-brief(turn) → secretary-route  

**pm-turn-end** internals: action-evaluate → [full] memory-critique → memory-flush → memory-record (nav REQUIRED) → [conditional] memory-refine  

**L1 writes**: nav.yaml + one episode + index touch.  
**L2 writes**: traces/evaluations when full evaluate / turn_reward<0.6 / pre_compact.

**Canonical**: [PM_ROUTING.md](../../docs/PM_ROUTING.md) · [MEMORY_ARCHITECTURE.md](../../docs/MEMORY_ARCHITECTURE.md) · [CONTEXT_TIERS.md](../../docs/CONTEXT_TIERS.md)
