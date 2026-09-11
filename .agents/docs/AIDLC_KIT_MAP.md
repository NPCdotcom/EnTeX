# AI-DLC ↔ kit map

**Status**: canonical (R-3 B3)  
**Vocabulary**: umbrella=AIDD · methodology=AI-DLC (AWS) · practice=SDD+HITL · **no awslabs copy-paste**

---

## Macro phases

| AI-DLC | Kit | Cursor |
|--------|-----|--------|
| **Inception** | P0–P3 · S0 | Ask → Plan |
| **Construction** | P4–P5 · H4/H5 unit | Plan → Agent |
| **Operations** | After P6 · `docs/operations/` optional | Debug · Agent |

---

## 13 stages ↔ kit

| # | AI-DLC stage | A/C | Kit | Skill / template |
|---|--------------|-----|-----|------------------|
| 1 | Workspace Detection | A | P0 · nav | secretary-route · workspace-detection |
| 2 | Reverse Engineering | C | Before P1 | brownfield-reference · RE templates |
| 3 | Requirements Analysis | A | P1–P2 | design-record · `requirements_depth` |
| 4 | User Stories | C | P1 optional | conditional-stages · design-record |
| 5 | **Workflow Planning** | A | lifecycle_plan | **adaptive-lifecycle-plan** |
| 6 | Application Design | C | P3 | design-deliberate/record |
| 7 | Units Generation | C | H4/H5 | plan-record · unit_scope |
| 8 | Functional Design | unit | P3 detail | design-record |
| 9 | NFR Req/Design | unit | P3 | design programs |
| 10 | Infrastructure Design | unit | P3 systems | `_template/infrastructure/` |
| 11 | Code Generation | A | P5 | implement-conduct |
| 12 | Build and Test | A | P5–P6 | review-conduct · v-model block |
| 13 | Operations | — | Optional | operations 4 templates · feedback-to-inception |

**A**=ALWAYS (skippable via profile) · **C**=CONDITIONAL · **unit**=H4/H5 loop

---

## Four cores (kit translation)

| Core | Kit |
|------|-----|
| Workflow Planning | adaptive-lifecycle-plan → `project-state.lifecycle_plan` |
| Question + Gate | verification-questions · Gate · Auto-review |
| State + audit | audit-log · traces · nav |
| Unit completion | 1 plan = 1 unit · plans-content |

---

## Out of kit scope

Task/Subagent · Cloud/Automations · awslabs `.mdc` copy · physical Mob room

**Phase detail**: [PROJECT_LIFECYCLE.md](./PROJECT_LIFECYCLE.md) · **Adaptive**: adaptive-lifecycle-plan skill
