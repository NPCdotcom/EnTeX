# Skill authoring

Canonical: [role-skill-catalog](./role-skill-catalog/SKILL.md) · [MEMORY_ARCHITECTURE.md](../docs/MEMORY_ARCHITECTURE.md) · [CONTEXT_TIERS.md](../docs/CONTEXT_TIERS.md)

## description (Discovery-first)

Write for **when the user would need this**, not pipeline jargon.

| Include | Avoid in description |
|---------|----------------------|
| What it does | `P5`, `Loop2`, `after X`, `L1 chain step N` |
| Concrete situations / user phrasing | Role-only jargon without context |

Pipeline position belongs in the **body**, not description.

Example: `Implement the agreed plan with TDD and minimal diffs. Use when coding features or fixes inside plan scope.`

## SKILL.md body

**Role** · **Phase** · Read/Write · links to `lib-*` for shared knowledge · keep under 120 lines.

## Memory skills

- Read: via `pm-turn-start` / `memory-reference`
- Write: via `pm-turn-end` / `lib-memory-io`
- assets: `assets/index|state|episodes/` when memory-touching

## Forbidden

- Hermes / Subagent
- Index-less memory files
- Ad-hoc scripts mid-turn → [`_SCRIPT_POLICY.md`](./_SCRIPT_POLICY.md)

## Scripts

| Item | Rule |
|------|------|
| Path | `skills/<name>/scripts/<stem>.py` |
| Run | `python env/bin/agents-run.py <name> <stem> [args]` |

## Audit

```powershell
python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills
```

Rules authoring: [`../rules/_RULE_AUTHORING.md`](../rules/_RULE_AUTHORING.md)
