# ADR-001 — Context tiering and language split

**Status**: accepted (R-3 B1 · 2026-06-22)  
**Context**: Track R refresh after product-dev learning (25 cycles)

## Decision

1. **Four load tiers** L0–L3 documented in `docs/CONTEXT_TIERS.md`.
2. **Single loop canonical**: `docs/PM_ROUTING.md` — other docs link only.
3. **L0 rules in English** — `secretary-gate`, `kit-context-routing`, `no-subagents`.
4. **Two-layer language**: machine canon English · project templates Japanese (`LANGUAGE_POLICY.md`).
5. **Remove** `rules/project-leadership.mdc` — absorbed into gate + `PM_ROUTING` + `CURSOR_ROLES`.
6. **Role×Skill canonical**: `skills/role-skill-catalog/references/full-catalog.md` only.
7. **L1 chains**: `skills/_chains/memory-turn.md`, `secretary-turn.md`.

## Consequences

- Lower duplicate policy text in always-loaded context.
- `SKILLS_RULES_BY_PHASE.md` → redirect stub.
- Existing JP procedural docs translated incrementally on touch.

## References

- `learning/product-dev/notes/refresh/r-01` through `r-05`
