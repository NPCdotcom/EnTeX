# Bootstrap — workflow steps

## 1. Project context（ユーザー確認）

Collect without writing into **kit source repo**.

## 2. Root AGENTS.md

Copy `.agents/AGENTS.md.template` → `AGENTS.md` · fill placeholders.

## 3. docs/ skeleton

See [`docs-skeleton.md`](docs-skeleton.md).

## 3b. `.agents/env/`（エージェント実行環境）

1. `.\env\bin\setup.ps1`（または `./env/bin/setup.sh`）— Python venv 作成
2. 検証: `python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills` → `OK: no layout issues`

正本: [`env/README.md`](../../env/README.md) · ポリシー: [`skills/_SCRIPT_POLICY.md`](../../skills/_SCRIPT_POLICY.md)

## 4. `.agents/memory/`（bootstrap 契約 · 欠落禁止）

**必須**（無い場合は作成してから続行。fail-soft 禁止）:

| Path | 用途 |
|------|------|
| `index.yaml` | from `index.yaml.example` |
| `state/nav.yaml` | from `nav.yaml.example`（kit workspace: `session.intent=kit-maintenance`） |
| `audit/audit-log.md` | from `audit-log.md.example` |
| `episodes/` | directory（README 可 · L1 書き先） |

1. `cp .agents/memory/index.yaml.example .agents/memory/index.yaml`
2. `cp .agents/memory/state/nav.yaml.example .agents/memory/state/nav.yaml`
3. `cp .agents/memory/audit/audit-log.md.example .agents/memory/audit/audit-log.md`
4. `mkdir` `episodes/`（空で可）
5. Ensure `.agents/hooks.json` + `.agents/hooks/*.py` exist
6. Run **`.agents/scripts/link-cursor.ps1`** → `.cursor/{rules,skills,hooks}` junction + `.cursor/hooks.json`
7. Ensure `knowledge/{alignment,lessons}/`, `state/`, `history/`, `traces/`, `audit/`, `evaluations/`, `rewards/`

## 5. `.agents/handoffs/`

Legacy README only — new briefs → `memory/episodes/`.

## 6. `.agents/plans/README.md`

Index table exists.

## 7. `rules/local/` lenses

From `AGENTS.md` stack docs.

## 7b. `learning/`（任意）

横断学習トピック: `cp -r learning/_template learning/<topic>` · 正本 [`docs/LEARNING_SANDBOX.md`](../../docs/LEARNING_SANDBOX.md)

## 8. Verify

- [ ] `.agents/memory/index.yaml` exists
- [ ] `.agents/memory/state/nav.yaml` exists（not leftover from another project）
- [ ] `.agents/memory/episodes/` directory exists
- [ ] `.agents/memory/audit/audit-log.md` exists
- [ ] `.agents/hooks.json` + `.agents/hooks/pre-compact.py` exist
- [ ] `.cursor/hooks.json` exists（link-cursor 後）
- [ ] No Hermes in `mcp.json`（`mcpServers: {}`）
- [ ] `env/python/.venv` exists（setup 後）
- [ ] `python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills` → ISSUES=0
- [ ] No subagent files

Apply via `maintain-record`.
