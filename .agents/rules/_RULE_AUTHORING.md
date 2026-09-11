# Rule authoring

**Canonical content lives in `docs/`.** Rules are load triggers and pointers.

## AlwaysApply (L0)

- Max lines per [CONTEXT_TIERS.md](../docs/CONTEXT_TIERS.md): secretary-gate ≤25 · kit-context-routing ≤15 · no-subagents ≤10
- Minimal IF-THEN + links only — **no** duplicated procedure tables

## Conditional rules

- ≤20 lines + link to the owning doc
- No Role×Skill tables (those belong only in `full-catalog.md`)

## Forbidden

- Copying full PM loop into rules
- Keeping DEPRECATED stub files (delete; rely on git history)
- Conflicting gate tables vs `docs/PROJECT_LIFECYCLE.md`

Skill authoring: [`../skills/_SKILL_AUTHORING.md`](../skills/_SKILL_AUTHORING.md)
