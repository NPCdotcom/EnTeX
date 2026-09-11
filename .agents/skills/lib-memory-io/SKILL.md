---
name: lib-memory-io
description: Contracts for writing nav.yaml, episodes, index, and audit-log. Use at turn end, after flush, or when repairing missing memory directories.
---

# Library — memory I/O

**Cross-cutting** · linked from pm-turn-end · memory-flush · memory-record

## Required paths

| Path | L1 | Notes |
|------|----|-------|
| `state/nav.yaml` | required | update `updated`, `next_actions`, pressure |
| `episodes/*.md` | required (non-lightweight) | one file per turn ok |
| `index.yaml` | touch | `updated` date |
| `audit/audit-log.md` | append on gate/preCompact | hook also appends |

## Missing → ERROR

Do not invent state. Copy from `*.example` then re-read. See memory-reference bootstrap contract.

Details: [`references/io-contract.md`](references/io-contract.md)
