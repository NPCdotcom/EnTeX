# Deprecated aliases（削除済み）

## Kit Hardening Mega (2026-07)

| Old | Replacement |
|-----|-------------|
| `_chains/memory-turn.md` | `_chains/pm-turn.md` |
| `_chains/secretary-turn.md` | `_chains/pm-turn.md` |
| Per-turn discovery of many memory/secretary skills | `pm-turn-start` · `pm-turn-end` |
| Duplicated frontmatter/TDD/V-model text in `*-record`/`*-conduct` | `lib-doc-frontmatter` · `lib-tdd-cycle` · `lib-review-vmodel` · `lib-memory-io` |
| `docs/SKILLS_RULES_BY_PHASE.md` | `full-catalog.md` |
| `rules/cursor-agent-tooling.mdc` | `cursor-tooling-pm` / `cursor-tooling-stewards` |

## Hermes 全面撤去（2026-06）

| 旧 | 代替 |
|----|------|
| Hermes Agent / `hermes -z` | Cursor IDE + `role-execute` |
| MCP server `hermes` | `memory-reference` + `.agents/memory/` |
| `hermes-role-execute` | `role-execute` |
| `hermes-*` bundle YAML | `role-skill-catalog/references/full-catalog.md` |
| `docs/HERMES_*.md` | `docs/CURSOR_ROLES.md`, `docs/MEMORY_ARCHITECTURE.md` |
| `hermes.router` 等 | `router`, `spec_designer`, …（`hermes.` 接頭辞なし） |

## 旧 Subagent 時代

| 旧 skill | 代替 |
|----------|------|
| steward-skill-catalog | role-skill-catalog |
| pm-delegation-launch | role-execute |

## 検証

```bash
rg -i 'hermes' .agents docs --glob '!**/deprecated-aliases.md'
python env/bin/agents-run.py maintain-adhoc audit-skill-layout .agents/skills
```

ヒットは **バグ** として除去する（意図的な deprecated 表を除く）。
