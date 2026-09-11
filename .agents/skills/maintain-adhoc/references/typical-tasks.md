| New role mapping | Update `docs/CURSOR_ROLES.md`, `role-skill-catalog` |
| New memory skill | `assets/{index,state,episodes}/` + `memory/index.yaml` |
| PM routing sync | `rg context-guard docs/PM_ROUTING.md` · secretary-reference に lifecycle 毎ターン無し |
| Hermes residue | `rg -i hermes` → Cursor role へ（禁止文脈除く · deprecated-aliases 除く） |
| Skill layout audit | `python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills` |
| Script inventory | `python env/bin/agents-run.py maintain-scripts inventory skills` |
| Script review | `python env/bin/agents-run.py maintain-scripts review` |
| Script dedupe report | `python env/bin/agents-run.py maintain-scripts dedupe-report` |
| Agent env setup | `.\env\bin\setup.ps1` or `./env/bin/setup.sh` |
| Hooks bootstrap | `hooks.json` + `hooks/pre-compact.py` + `nav.yaml.example` |
