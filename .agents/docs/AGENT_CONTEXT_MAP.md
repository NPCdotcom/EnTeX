# Agent context map

**Subagents forbidden** · **Hermes forbidden** · Memory: nav + index tiers

Canonical: [CONTEXT_TIERS.md](./CONTEXT_TIERS.md) · [PM_ROUTING.md](./PM_ROUTING.md) · [LANGUAGE_POLICY.md](./LANGUAGE_POLICY.md)

---

## Control plane

| File | Purpose |
|------|---------|
| `.agents/memory/state/nav.yaml` | session_intent · next_actions · pressure · **every turn** |
| `docs/project-state.yaml` | P/H · gate · active_pdca (Loop2) |
| `.agents/hooks.json` | preCompact · stop reanchor |

---

## Load tiers (summary)

| Tier | What |
|------|------|
| **L0** | 3 always rules + AGENTS entry |
| **L1** | `_chains/pm-turn` · `pm-turn-start` · `pm-turn-end` |
| **L2** | Phase skills · stewardship rules |
| **L3** | PM_ROUTING · LIFECYCLE · MEMORY_ARCHITECTURE · CURSOR_* |

Full spec: [CONTEXT_TIERS.md](./CONTEXT_TIERS.md)

---

## Learning sandbox

| Path | Use |
|------|-----|
| `learning/<topic>/` | Cross-project research (not kit canon) |

Rule: `learning-sandbox.mdc` · exclude `learning/**` from default index

---

## Role × skill catalog

**Only canonical table**: [full-catalog.md](../skills/role-skill-catalog/references/full-catalog.md)

Research policies: [LANDSCAPE_RESEARCH_POLICY.md](./LANDSCAPE_RESEARCH_POLICY.md) · [TERMINOLOGY_RESEARCH_POLICY.md](./TERMINOLOGY_RESEARCH_POLICY.md)
