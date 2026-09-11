# Role & skill catalog — detailed table

## Every turn (PM)

| Timing | Skill |
|--------|-------|
| Start | **pm-turn-start** |
| Loop2 (conditional) | lifecycle-reference → nav-brief |
| Execute | **role-execute** |
| End | **pm-turn-end** |

Canonical chain: `skills/_chains/pm-turn.md`

## Libraries (cross-cutting)

| Lib | Used by |
|-----|---------|
| `lib-doc-frontmatter` | design-record · plan-record · doc-record |
| `lib-tdd-cycle` | implement-conduct |
| `lib-review-vmodel` | review-conduct |
| `lib-memory-io` | pm-turn-end · memory-flush · memory-record |

## Role → primary skills (Cursor IDE)

| Role | Primary skills (order) |
|------|------------------------|
| `router` | pm-turn-start internals · adaptive-lifecycle-plan · brownfield-reference · lifecycle-reference · landscape-research · terminology-research · cursor-tool-select |
| `spec_designer` | brownfield-reference · landscape-research · terminology-research · design-reference · design-deliberate · design-record · doc-record · lib-doc-frontmatter |
| `plan_slicer` | terminology-research · plan-reference · plan-record · design-reference · lib-doc-frontmatter |
| `builder` | implement-reference · implement-conduct · lib-tdd-cycle · implement-record · plan-reference · design-reference |
| `hotfixer` | patch-reference · patch-conduct · patch-record · plan-reference |
| `reviewer` | review-reference · review-conduct · lib-review-vmodel · review-record · lifecycle-reference |
| `evaluator` | evaluate-reference · plan-evaluate · project-evaluate · evaluate-record |
| `automator` | automation-reference · automation-run · automation-record · plan-reference |
| `kit_maintainer` | landscape-research · maintain-reference · maintain-scripts · maintain-adhoc · maintain-record · role-skill-catalog |

PM runs **`role-execute`** for role rows after `pm-turn-start`.

## Phase → Role → skills

| P | Role | Skills |
|---|------|--------|
| Every | PM / router | pm-turn-start → role-execute → pm-turn-end |
| P0–P3 | `spec_designer` | terminology-research → design-* · lib-doc-frontmatter |
| P4 | `plan_slicer` | terminology-research → plan-* · lib-doc-frontmatter |
| P5 | `builder` | implement-* · lib-tdd-cycle |
| P5+ | `hotfixer` | patch-* |
| P6 | `reviewer` / `evaluator` | review-* · lib-review-vmodel · evaluate-* |
| Kit | `kit_maintainer` | maintain-* |

## Phase → Rules (pointers only — no duplicate tables in rules)

| P | Rules |
|---|-------|
| Every | secretary-gate · no-subagents · kit-context-routing |
| P0–P3 | design-stewardship · docs-content · documentation-adr-glossary · project-lifecycle |
| P4 | planning · plans-content · project-lifecycle |
| P5 | implementation-stewardship · patch-stewardship · rules/local/*-implement |
| P6 | review-stewardship · evaluation-stewardship · rules/local/*-review |
| Cross | role-cross-skills · cursor-tooling-pm · cursor-tooling-stewards |
| Kit | maintenance-stewardship |
| Automation | automation-stewardship |

## Write boundaries

| Path | Writer |
|------|--------|
| `.agents/memory/**` | pm-turn-end / memory-record / memory-flush |
| `docs/requirements/` · `docs/design/` · `docs/adr/` · `docs/glossary/` | spec_designer |
| `docs/project-state.yaml` | PM |
| `.agents/plans/` | plan_slicer |
| Application source | builder · hotfixer |
| `docs/reviews/` | reviewer |
| `docs/evaluations/` | evaluator |
| `.agents/rules/` · `.agents/skills/` | kit_maintainer |

## Removed

See [`deprecated-aliases.md`](deprecated-aliases.md)
