# Context tiers (L0–L3)

**Status**: canonical  
**Related**: [PM_ROUTING.md](./PM_ROUTING.md) · [LANGUAGE_POLICY.md](./LANGUAGE_POLICY.md)

Load only what the turn requires. **One deep doc per turn** at L3.

---

## Tier definitions

| Tier | Name | When loaded | Budget |
|------|------|-------------|--------|
| **L0** | Always | Every Cursor session | ≤50 lines (3 rules + AGENTS entry) |
| **L1** | Turn | Every user message | **1** chain (`pm-turn`) + ≤2 skill files |
| **L2** | Phase | Role run · Loop2 · glob rules | One skill + one reference |
| **L3** | Deep | Design · audit · research | One doc per turn |

### Language (P7)

| Tier | Language |
|------|----------|
| L0–L2 | **English** |
| L3 procedural | **English** |
| Project templates | **Japanese** |
| User chat | **Japanese** |

---

## L0 — Always

| File | Max lines |
|------|-----------|
| `rules/secretary-gate.mdc` | 25 |
| `rules/kit-context-routing.mdc` | 15 |
| `rules/no-subagents.mdc` | 10 |
| Project `AGENTS.md` entry | 35 |

**Not in L0**: full loop text · role tables · memory details. Rules = pointers + minimal IF-THEN only.

---

## L1 — Every turn

**Canonical chain**: `skills/_chains/pm-turn.md` (only)

| Turn type | Allowed reads |
|-------------|---------------|
| Lightweight | pm-turn-start (minimal) |
| Standard | pm-turn.md · pm-turn-start · pm-turn-end |
| Loop2 | + lifecycle-reference · nav-brief |
| Re-anchor | lifecycle-reference · nav-brief only (no conduct) |

`evaluate-reference` is **L2**, not L1.

---

## L2 — Conditional

| Trigger | Read |
|---------|------|
| P0–P3 design | design-stewardship · design-* · lib-doc-frontmatter |
| P4 plan | planning · plan-* · lib-doc-frontmatter |
| P5 implement | implementation-stewardship · implement-* · lib-tdd-cycle |
| P6 review | review-* · lib-review-vmodel · evaluate-reference |
| Adaptive first run | adaptive-lifecycle-plan |
| Brownfield | brownfield-reference |
| Research | landscape/terminology + policy |
| `docs/**` edit | docs-content |
| `plans/**` edit | plans-content |

Conditional rules: ≤20 lines + link to `docs/`.

---

## L3 — On demand

| Doc | When |
|-----|------|
| [PM_ROUTING.md](./PM_ROUTING.md) | Loop detail · pressure |
| [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md) | Phase · gate |
| [MEMORY_ARCHITECTURE.md](./MEMORY_ARCHITECTURE.md) | Promotion · flush |
| [CURSOR_AGENT_TOOLING.md](./CURSOR_AGENT_TOOLING.md) | Tools · modes |

---

## Pressure

| pressure | Allowed |
|----------|---------|
| low | L0 + L1 standard |
| medium | L0 + L1 + nav re-read |
| high / pre_compact | L0 + L1 minimal + L2 lifecycle only |

---

## learning/

Exclude `learning/**` from default codebase index. Touch only via `learning-sandbox` rule.
