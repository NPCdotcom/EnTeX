# Mandatory procedures — index

**Canonical loop**: [PM_ROUTING.md](./PM_ROUTING.md)  
**Tiers**: [CONTEXT_TIERS.md](./CONTEXT_TIERS.md) · **Gate**: `rules/secretary-gate.mdc`

Priority: `secretary-gate` → `PM_ROUTING` → this index → `MEMORY_ARCHITECTURE` → `AGENT_EVALUATION`

---

## Enforcement

| Procedure | Enforcement | Fallback if skipped |
|-----------|-------------|---------------------|
| preCompact pressure | **hook** | — |
| nav Phase 0 read | **llm-soft** | ERROR + repair from example |
| L1 episode + nav update | **llm-soft** | next turn notes gap; do not invent state |
| Role×Skill table | catalog only | — |

---

## Control plane (required)

| File | Every turn |
|------|------------|
| `.agents/memory/state/nav.yaml` | Phase 0 read · terminal update |
| `.agents/memory/episodes/` | L1 write (non-lightweight) |
| `docs/project-state.yaml` | Loop2 · recall Phase C |

---

## Turn type → procedure

| Type | Condition | Procedure |
|------|-----------|-----------|
| **Standard** | Default | `_chains/pm-turn.md` · pm-turn-start → role-execute → pm-turn-end |
| **Lightweight** | Greeting only · Role 0 · no record | minimal start · skip end evaluate · L0/nav touch |
| **Re-anchor** | mismatch · compact | PM_ROUTING § re-anchor |
| **pre_compact** | pressure=pre_compact | L2 required · new chat |

**Loop2**: if unclear → **run**.

---

## L1 chain (standard)

1. `pm-turn-start`
2. `[Loop2]` lifecycle-reference → nav-brief
3. `role-execute`
4. `pm-turn-end`

Canonical: [skills/_chains/pm-turn.md](../skills/_chains/pm-turn.md)

---

## Evaluate matrix

| Turn | evaluate | critique |
|------|----------|----------|
| Lightweight | skip | skip |
| Loop1 read-only | mini | skip |
| Loop1 execute / Loop2 | full | full (if full evaluate) |

---

## Always forbidden

Hermes · Subagent · memory without index · conduct while gate=block · P/H re-inference in Loop1 · soft-skip missing nav/episodes

---

## Catalog

[skills/role-skill-catalog/references/full-catalog.md](../skills/role-skill-catalog/references/full-catalog.md)
