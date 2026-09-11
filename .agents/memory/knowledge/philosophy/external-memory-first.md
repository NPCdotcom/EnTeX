---
id: kit-design-memory-first
kind: knowledge
topic: design-philosophy
status: active
created: 2026-06-17
tags: [memory, architecture, cursor]
---

# 外部記憶優先（IDE 正本）

## Principle

Cursor チャットの短期記憶は揮発する。**project index 最優先**、次 **global index**（`~/.agents/memory/global/`）、で外部ファイルを読み、ターン終端に **memory-flush** で掃き出す。

## Decisions

- Hermes Agent / MCP `hermes` は使用しない
- 三層: **global**（横断）· **project**（作業）· **team**（docs 正本）
- 優先: project index > global index > state = episodes > knowledge
- `docs/project-state.yaml` は team / state tier の canonical（project index からリンク）

## Related

- docs/MEMORY_ARCHITECTURE.md
- docs/CURSOR_ROLES.md
