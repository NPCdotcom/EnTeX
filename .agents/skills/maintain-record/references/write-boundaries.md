# Maintain record — write boundaries

**Role**: `kit_maintainer` · After `maintain-bootstrap` or `maintain-adhoc`.

| Path | Bootstrap | Ad hoc |
|------|:---------:|:------:|
| `.agents/agents/**` | ○ | ○ |
| `.agents/rules/**`（generic） | ○ | ○ |
| `.agents/rules/local/*.mdc` | ○ consumer | ○ consumer |
| `.agents/skills/**` | ○ | ○ |
| `.agents/README.md` | ○ | ○ |
| `.agents/plans/README.md`（index rows only） | ○ | ○ |
| `AGENTS.md`（repo root） | ○ | △ steward table one-line |
| `docs/**` skeleton README | ○ | ✗ |
| `docs/design/`, plan bodies, app source | ✗ | ✗ |

Do not write feature specs or application code here.
