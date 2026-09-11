# Promotion graph — memory → docs

Agent **memory-reason** applies this every turn (after recall, before/after role-execute).

**Three scopes**: `global` · `project` · `team` — see `docs/MEMORY_ARCHITECTURE.md`

## Tiers by scope

```text
[project] episodes (1+ turns, raw)
    ↓ G1-G3 met, G4 pending
[project] knowledge/alignment/
    ↓ G4 + doc-record
[team] docs/glossary/<term>.md

[global] knowledge/lessons/     # cross-project · **trace 必須**
[global] knowledge/preferences/
[global] knowledge/philosophy/
    ↓ gate + cross-cutting, team-wide
[team] docs/adr/NNNN-slug.md

[project] knowledge/lessons/    # repo-only lesson
    ↓ affects design/plan
[team] docs/design/ or plan Risk section

Assumption (project episode)
    ↓ verified, project-specific
Fact → project alignment or design Facts
    ↓ verified, cross-project
Fact → global knowledge/lessons/
    ↓ rejected
Open → project thread, recall: next_turn

[team] docs/MEMORY_ARCHITECTURE.md  # kit truth — doc-record, not global file
```

## Scope choice (reason step)

| Signal | scope |
|--------|-------|
| Term tied to this repo / glossary candidate | project → team |
| Browser research usable in any repo | global |
| Landscape research report (scan+drill) | global `lessons/` · G3 URLs required |
| User preference / language / style | global |
| Phase, gate, blockers | team (+ project state snapshot) |
| Kit PDCA policy | team (docs/) |

**Conflict**: project alignment overrides global lesson on same term.

## Actions

| proposal | scope | next skill |
|----------|-------|------------|
| keep_memory | project or global | memory-flush → tier only（lesson は trace 必須） |
| promote_glossary | team | doc-record（spec_designer row） |
| promote_adr | team | doc-record |
| promote_design | team | design-record |
| wait_user | — | brief に確認項目 |
| archive | project or global | granularity: archive, recall: on_demand |

Do not promote without **memory-reason** row + criteria id (G1…).
