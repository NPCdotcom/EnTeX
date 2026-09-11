---
name: pm-turn-start
description: Start every agent turn—read nav memory, detect context pressure, draft a short turn plan and pick roles. Use at the beginning of user messages, before coding or editing. Also when resuming after summarize or when unsure what to do next.
---

# PM turn start

**Role**: PM · **Chain**: [`_chains/pm-turn.md`](../_chains/pm-turn.md)

## Steps (in order — do not skip unless lightweight)

1. **context-guard** — pressure · Loop2 · reanchor · pre_compact ([`../context-guard/SKILL.md`](../context-guard/SKILL.md))
2. **memory-reference** — nav Phase 0 · bootstrap ERROR if missing ([`../memory-reference/SKILL.md`](../memory-reference/SKILL.md))
3. **memory-reason** — mini (Loop1) or full (Loop2) ([`../memory-reason/SKILL.md`](../memory-reason/SKILL.md))
4. **secretary-brief** — turn-brief; if Loop2, nav-brief first ([`../secretary-brief/SKILL.md`](../secretary-brief/SKILL.md))
5. **secretary-route** — Role rows ([`../secretary-route/SKILL.md`](../secretary-route/SKILL.md))

## Lightweight

Greeting-only: steps 1–2 minimal · one-line turn-brief · skip route Role 0 · skip pm-turn-end evaluate.

## Do not

Run `*-conduct` / Edit before this skill completes (except Re-anchor stop). Duplicate full loop text in chat.

**Canonical**: `docs/PM_ROUTING.md`
