# Cursor tool inventory

## Quick checklist

- [ ] Web / screenshot → **cursor-ide-browser** available?
- [ ] Command / test / build → **Shell**?
- [ ] External service → plugin MCP descriptor exists?
- [ ] Show file/URL in IDE → **open_resource**?

## Built-in

| Tool | Use for |
|------|---------|
| Shell | git, npm, tests, scripts, dev servers |
| Read / Grep / Glob | files, search |
| SemanticSearch | codebase by meaning |
| Task | **禁止** — Subagent 不使用 |
| Await | poll background Shell |

## cursor-ide-browser

1. Confirm MCP server `cursor-ide-browser` in tool list
2. Plan: `browser_navigate` → `browser_take_screenshot`
3. Follow lock order in server INSTRUCTIONS

Do **not** default to "open your default browser".

## MCP discovery

1. List enabled MCP servers
2. Read `tools/<name>.json` schema per server
3. Invoke via **CallMcpTool**

## cursor-app-control

| Need | Tool |
|------|------|
| Reveal workspace file | open_resource |
| Focus terminal | open_resource |
| Automations UI | open_automation |
| Switch project root | move_agent_to_root |

See `.agents/docs/CURSOR_AGENT_TOOLING.md`.
