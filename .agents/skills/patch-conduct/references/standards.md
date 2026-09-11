# Patch conduct standards（汎用・小規模）

Stack detail: **AGENTS.md**, **rules/local/**.

## Minimal diff

- Fix the reported symptom first; no adjacent cleanup
- One logical cause per patch batch
- Reuse project utilities; no parallel one-off helpers unless ≤5 lines

## Quality

- Fail loudly at the boundary you touch
- Match surrounding naming and types
- English identifiers unless AGENTS.md says otherwise

## Architecture

- Do not move simulation boundaries or add new ticks/commands
- If fix needs a boundary change → **spec_designer**, not patch

## Handoff

| Situation | Role |
|-----------|------|
| Fix ok, user wants merge confidence | reviewer |
| Same area breaks again | evaluator or plan_slicer |
| Fix needs new criterion | plan_slicer |
