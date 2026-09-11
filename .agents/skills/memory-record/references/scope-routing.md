# Memory record — scope routing

Used by **memory-record** after **memory-flush** + **memory-reason** report.

## Decision table

| Content | scope | Target path | Index file |
|---------|-------|-------------|------------|
| Turn trace | project | `.agents/memory/traces/` | project `index.yaml` |
| Turn evaluation | project | `.agents/memory/evaluations/` | project `index.yaml` |
| Rewards rollup | project | `.agents/memory/rewards/rollup.yaml` | optional index link |
| Turn log, Assumptions, Open | project | `.agents/memory/episodes/` | project `index.yaml` |
| Active plan / topic | project | thread entry | project `index.yaml` |
| Project term alignment | project | `.agents/memory/knowledge/alignment/` | project `index.yaml` |
| Repo-specific lesson | project | `.agents/memory/knowledge/lessons/` | project `index.yaml` |
| Cross-project tech research | global | `~/.agents/memory/global/knowledge/lessons/` | global `index.yaml` |
| Landscape research report | project or global | `.agents/memory/evaluations/` + optional `lessons/` | project `index.yaml` |
| User coding / comm preferences | global | `~/.agents/memory/global/knowledge/preferences/` | global `index.yaml` |
| User-wide design principle | global | `~/.agents/memory/global/knowledge/philosophy/` | global `index.yaml` |
| Phase / gate / blockers | team | `docs/project-state.yaml` | project index links team path |
| Gate · lifecycle · phase audit | project | `.agents/memory/audit/audit-log.md` | project `index.yaml` · `tier: audit` |
| Confirmed glossary term | team | `docs/glossary/` | doc-record |
| Kit architecture truth | team | `docs/*.md` | doc-record |
| Learning scratch (unverified) | learning | `learning/<topic>/notes/` · `experiments/` | optional `learning/index.yaml` — **not** lessons until promoted |

## Learning layer

Writes under `learning/**` during learning turns (**rule `learning-sandbox`**).  
**memory-record** does not treat learning notes as lessons. Promotion: trace + critique → `lessons/` or `doc-record`.

## memory-reason signals

Reason report column **scope** must be set for each flush row:

```yaml
scope: project | global | team
path: ...
action: create | update | link_only
```

## Dual index update

When writing global knowledge:

1. Write file under global root
2. Update **global** `index.yaml`
3. Optional: add project index `linked:` entry pointing to global id (read-only pointer, no duplicate body)

When writing project episode:

1. Update **project** index only
2. Do **not** mirror to global

## project_id on global entries

Set when lesson is tied to one repo but stored globally for personal reuse:

```yaml
project_id: "github.com/org/repo"
```

Recall: still global `on_demand`; project index may link it when `project_id` matches current repo.
