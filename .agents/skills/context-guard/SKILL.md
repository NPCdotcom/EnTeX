---
name: context-guard
description: Detect context pressure, nav mismatch, and summarize risk at the start of a turn. Use when starting every user message, especially long chats or after Cursor summarize.
---

# Context Guard

**Tier**: L1 · **Before** [`_chains/pm-turn.md`](../_chains/pm-turn.md)

Pre-empt summarize: pressure · reanchor · Loop2 flag — [PM_ROUTING.md](../../docs/PM_ROUTING.md) § context-guard

Checklist: [`references/guard-checklist.md`](references/guard-checklist.md) · hooks: [`.agents/hooks.json`](../../hooks.json)

**If Loop2 unclear → run Loop2.**
