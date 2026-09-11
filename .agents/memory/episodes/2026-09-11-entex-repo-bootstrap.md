---
id: 2026-09-11-entex-repo-bootstrap
date: 2026-09-11
scope: project
tags: [bootstrap, github, wsl]
---

# Episode: EnTeX repo bootstrap

## Summary

Connected local `Documents/GitHub/EnTeX` to `NPCdotcom/EnTeX` on `main`. Bootstrapped shared docs/schemas/design plus tracked `.agents` kit. Removed user-global memory leak from initial copy.

## Outcomes

- Remote: `git@github.com:NPCdotcom/EnTeX.git` tracking `origin/main`
- Members documented: NPC (`NPCdotcom`), Aster (`astel_isk`)
- `.gitignore` excludes secrets/generated only — AI kit assets tracked
- Cursor junctions via `link-cursor.ps1`

## Next

1. Invite `astel_isk` as collaborator
2. P0 charter under `docs/design/product/`
3. WSL Ubuntu toolchain confirmation
