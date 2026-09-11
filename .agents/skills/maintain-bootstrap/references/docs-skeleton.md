# Bootstrap — docs/ skeleton

Create if missing:

```
docs/
├── README.md
├── PROJECT_LIFECYCLE.md
├── project-state.yaml
├── requirements/README.md
├── requirements/_template/
├── design/README.md
├── design/product/
├── design/elements/
├── design/systems/
├── design/frameworks/
├── design/programs/
├── adr/
├── glossary/
├── reviews/          # optional
└── evaluations/      # optional
```

## Copy from kit（汎用のみ — 製品名を埋めない）

- `.agents/docs/PROJECT_LIFECYCLE.md`, `FIRST_PROJECT_START.md`
- `.agents/docs/LINEAR_PHASE_MAP.md`（Linear 利用時）
- `.agents/docs/CONSUMER_DOCS_README.template.md` → `docs/README.md`
- `.agents/docs/project-state.template.yaml` → `docs/project-state.yaml`（`current_phase: P0`）
- `.agents/memory/state/nav.yaml.example` → `.agents/memory/state/nav.yaml`
- `.agents/memory/audit/audit-log.md.example` → `.agents/memory/audit/audit-log.md`
- Create `.agents/memory/episodes/`（required L1 write target）
- Kit `hooks.json` + `hooks/*.py` → project `.agents/`（bootstrap）

## Optional samples（ユーザー要望時のみ）

- `.agents/docs/_example/design/product/charter.md` → `docs/design/product/charter.md`（example prose を置換）
- `.agents/docs/_example/requirements/sample-capability/` → `docs/requirements/<user-slug>/`（**never** leave `sample-capability` in production）
- Do **not** copy `_example/` as-is unless user wants reference copy

## Also ensure

- `.agents/env/bin/setup.ps1`（agent venv）· `python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills`
- `.agents/plans/{product,elements,systems,frameworks,programs,algorithms}/`
- `docs/requirements/_template/`, empty `docs/design/{product,elements,systems,frameworks,programs}/`
- Point user to `.agents/docs/FIRST_PROJECT_START.md`

Minimal README pointers only — no game/product spec bodies unless user supplies for `docs/design/`.
