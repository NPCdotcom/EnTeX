---
name: cursor-capabilities-reference
description: List available Cursor tools (browser, Shell, MCP, open_resource) before claiming something is unavailable. Use when verifying URLs, screenshots, or terminals.
---

# Cursor Capabilities Reference

**Role**: `router` / PM · **毎ターン** · Read-only

Run **before** telling the user to use an external browser or saying a capability is missing.

## Inventory

[`references/tool-inventory.md`](references/tool-inventory.md)

## Report

[`assets/capabilities-report-template.md`](assets/capabilities-report-template.md)

## Do not

Skip when user asked for agent-driven verification; assume plugins from memory.

Pair with `cursor-tool-select` every turn.
