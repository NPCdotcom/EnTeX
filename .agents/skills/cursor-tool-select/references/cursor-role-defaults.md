# Role — Cursor 補助デフォルト

| Role | **Cursor mode**（G11） | よく付ける Cursor 補助 |
|------|------------------------|------------------------|
| `router` | Ask→Plan | P0–P4 → **WebSearch+browser 必須**；memory-reference 先 |
| `spec_designer` | Ask→Plan | **WebSearch 必須** + browser；Read/Grep |
| `plan_slicer` | Plan | **WebSearch 必須** + browser（criteria・DoD）；Read |
| `reviewer` | Agent（失敗時 Debug） | Shell + UI 時 browser MCP |
| `builder` | Agent | Shell + UI 受け入れ時 browser |
| `hotfixer` | Agent | Shell；UI 再現時 browser |
| `automator` | Agent | Shell + 検証 URL 時 browser |
| `evaluator` | Ask | Read + git/Shell；用語争点 WebSearch |
| `kit_maintainer` | Plan→Agent | Read/Write `.agents/` · `env/bin/agents-run.py` |

`lifecycle_plan.recommended_cursor_mode` があれば上表より優先。Router は **mode 列** + **Cursor 補助** + **memory-flush** を brief に含める。
