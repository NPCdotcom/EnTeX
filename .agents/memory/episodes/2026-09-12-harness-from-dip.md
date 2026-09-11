---
id: 2026-09-12-harness-from-dip
date: 2026-09-12
scope: project
tags: [harness, git-workflow, ci, review, P0]
---

# Episode: port harness conventions from dip_distributed_llm

## Input

User asked to bring the working practices from `dip_distributed_llm` (agent harness, PR/commit prefixes) into EnTeX, add a `CLAUDE.md` that forwards to `AGENTS.md`, and keep only the parts that help build what the charter describes.

## Decisions (user, 2026-09-12)

- Branch flow: **`main` + PR**, no `develop` (dip used `develop`; two people and an early repo do not need the extra stage).
- Mechanical enforcement: register EnTeX in the PIR bash guard (`GUARDED_REPOS`) so protected-branch commits/pushes, branch-name shape and commit prefixes are rejected before they run.

## Done

- `CLAUDE.md` → forwards to `AGENTS.md` (same shape as dip).
- `AGENTS.md`: appended a Japanese project-operations half — doc index table, Git workflow (branch `issue/owner/slug`, commit `prefix:text` with no space), stop-and-ask rule for design invariants, context-loading cautions (TeX logs, PDFs, TeX Live tree), coding standards (escape before TeX, never surface TeX logs), test criteria, pre-PR local checks, CodeRabbit operation, harness map.
- `.github/workflows/ci.yml`: paths-filter → `lint-test` (ruff check / ruff format --check / pytest on 3.12+3.13) and `tex` (buildx with gha cache → `entex doctor`, `tex-smoke`, pytest incl. TeX).
- `.github/pull_request_template.md`: local-check boxes + charter §4/§6 invariant boxes.
- `.coderabbit.yaml`: ja-JP, ignores `out/`, PDFs, `.agents/`.
- `.claude/skills/docs-sync-check/SKILL.md`: EnTeX version — invariant drift, stack versions, doc-package layout, IR↔pydantic, command existence, cross-doc links, phase agreement.
- `.claude/settings.local.json`: allow `gh pr` / `gh issue` / `make`.
- README: layout rows for the new files + a short Contributing section for NPC.

## Verified

`ruff check .` clean · `ruff format --check .` clean (16 files) — CI's format gate will not fail on the current tree. CI workflow itself is unverified until the first PR.

## Lessons

- dip's CI was Bun-shaped; only the *structure* transfers (paths-filter + concurrency + per-area jobs). The expensive job here is TeX Live, so it is gated on TeX-relevant paths and cached via `type=gha`.
- CodeRabbit did not auto-review low-star repos in dip; the manual `@coderabbitai review` habit is part of the convention, not an accident.

## Open

- `docs/README.md` and `.agents/memory/index.yaml` contain mojibake from the kit bootstrap (UTF-8 read as CP932). Not fixed here — needs a decision on recovering vs rewriting the text.
- First PR will show whether the `tex` job's gha cache keeps the TeX Live build under a tolerable time.
