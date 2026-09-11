---
name: maintain-adhoc
description: Update kit skills, rules, or catalogs for process changes. Use when the agent kit itself needs an incremental fix.
---

# Maintain Ad hoc

**Role**: `kit_maintainer` · **Prerequisite**: `maintain-reference`.

## Tasks

[`references/typical-tasks.md`](references/typical-tasks.md)

## Audit

| Stem | 用途 |
|------|------|
| `audit-skill-layout` | skill フォルダ構造 · 46 件 · PM 必須 skill |
| `migrate-hermes-to-cursor-roles` | legacy（deprecated · 削除予定） |

```powershell
python env/bin/agents-run.py maintain-adhoc audit-skill-layout skills
```

スクリプト資産の inventory/review: **`maintain-scripts`**

Apply via **maintain-record**.
