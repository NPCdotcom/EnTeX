# Project lifecycle (phases · scope hierarchy · PDCA units)

**Canonical** for consumer projects. The kit holds generic definitions only. Product name and domain live in `AGENTS.md` and `docs/`.

## Three-layer model

| Layer | Name | Role |
|-------|------|------|
| **A** | Project phases **P0–P6** | Where conversation and artifacts are (requirements → design → plan → Do/Check) |
| **B** | Scope hierarchy **H0–H5** | What to fix first (higher = earlier) |
| **C** | PDCA units **S0–S1** | 1 plan = 1 cycle; **mainly at H4·H5** |

Layers are independent. Example: phase **P5 (Do)** while scope is **H5 (algorithm)**.

## A. Project phases (P0–P6)

Industry alignment: [ROLES_AND_GOVERNANCE.md](../.agents/docs/ROLES_AND_GOVERNANCE.md) (PM/PL/PO · Stage-Gate · V-model · Discovery/Delivery)

| ID | Name | Primary Cursor role | Main artifacts | Gate (next) |
|----|------|---------------------|----------------|-------------|
| **P0** | Product overview · boundaries | `spec_designer` | `docs/design/product/` charter | Purpose · non-goals · success metrics in short prose |
| **P1** | Requirements (stakeholder) | `spec_designer` | `docs/requirements/<slug>/要求.md` | Stakeholder needs listed |
| **P2** | Requirements (verifiable) | `spec_designer` | same folder `要件.md` | Verifiable acceptance; Open items not blockers |
| **P3** | Basic design (elements → frameworks) | `spec_designer` | `docs/design/{elements,systems,frameworks}/` | Upper H fixed; major IFs and constraints written |
| **P4** | Implementation plan | `plan_slicer` | `.agents/plans/programs/` or `algorithms/` | `related_design` · `scope_level` · user confirmation (below) |
| **P5** | PDCA Do | `builder` | source + plan PDCA log | Acceptance criteria met or split |
| **P6** | PDCA Check / Act | `reviewer` → plan/design | review / plan update | Act: shrink scope · split · phase rollback |

### P6 — Test levels (V-model)

In Japanese SI and V-model practice, left-side phases pair with right-side verification. The kit expresses this via **P6 review + plan criteria**.

| Level | Pairs with | Typical owner (industry) | Kit |
|-------|------------|------------------------|-----|
| **UAT** | P2 acceptance · requirements | User · PM | Final plan acceptance criteria check |
| **ST** | P3 basic design · system | QA · PL | `review-conduct` + design links |
| **IT** | P4 plan scope · IFs | Engineer · QA | Integration within plan scope |
| **UT** | P5 implementation | Engineer | P5 TDD; P6 coverage check |

**P6 four-layer gate (G10 · `review-conduct` required)**

Confirm explicitly per plan. Snippet: `docs/_template/plans/v-model-criteria-block.md`

| Layer | Review checks | If not met |
|-------|---------------|------------|
| **UT** | Unit test or manual rationale per AC | fail / conditional |
| **IT** | Integration · IFs within plan scope | same |
| **ST** | P3 design · non-functional alignment | same |
| **UAT** | P2 acceptance · requirement links | same |

**Traceability**: Each criterion links to `要件.md` or `docs/design/` (lightweight RTM).

### P6 — Outcome check (optional · post-ship)

Optional check beyond **output** (ship) for **outcome** (intended impact). Aligns with continuous discovery practice.

| Item | Content |
|------|---------|
| **When** | After plan acceptance criteria met · with `review-conduct` |
| **Who** | User (steering) · PM proposes evidence |
| **What** | **Product outcome** linked to P1/P2 (customer behavior · leading business indicator) as expected |
| **Required?** | **Optional** — skip for spikes · internal tools · plans with no outcome |
| **Record** | 1–3 lines in plan PDCA Act · Recycle or new plan if not met |

**Example outcomes**: "Export completion rate ≥ X%" · "Support tickets down by Y" — if unmeasurable, revise criterion in P2.

**AI-era note**: Faster delivery (Cursor Agent) increases ship-without-outcome risk. DORA 2024 stresses **small batches + verification** — this check is one compensating control.

### Discovery / Delivery (overlapping phases)

Discovery (reduce uncertainty) and Delivery (build) may **run in parallel** (Atlassian, Mind the Product).

- **High uncertainty** → `S0` spike (P0–P3) first; **`implement-conduct` forbidden**
- **Low uncertainty** → P4–P6 Delivery
- Agile: short **H4/H5** cycles through P1–P6
- **OST (optional · o-10)**: High uncertainty P0–P2 → `docs/design/_template/product/opportunity-solution-tree.md` → `docs/design/product/opportunity-solution-tree.md`. Multiple unit candidates: **RICE block** (`docs/_template/plans/rice-prioritization-block.md`) after discovery
- **Weekly discovery (optional · p-07)**: `docs/design/_template/product/continuous-discovery-cadence.md` — project ops · not kit-mandatory

### Continuity and rollback

- After **P5+**, may return to **P1·P2·P3** for new needs · spec change · design revision.
- On rollback: update `current_phase` in `docs/project-state.yaml`; router brief gets **rollback reason** in one line.
- **Do not cling to one implementation**: if a plan stalls → **split** (same `scope_level`) or **`status: superseded`** + new plan.

## B. Scope hierarchy (H0–H5) — fix higher first

| ID | Name | Design path | Plan path | PDCA Do |
|----|------|-------------|-----------|---------|
| **H0** | Product overview · features | `docs/design/product/` | `.agents/plans/product/` (optional · eval) | Usually no |
| **H1** | Element overview · features | `docs/design/elements/` | `.agents/plans/elements/` | Usually no |
| **H2** | System overview · features | `docs/design/systems/` | `.agents/plans/systems/` | Usually no |
| **H3** | Frameworks · libraries | `docs/design/frameworks/` | `.agents/plans/frameworks/` | S0 spike only |
| **H4** | Program (module · component) | `docs/design/programs/` | `.agents/plans/programs/` | **Primary PDCA** |
| **H5** | Algorithm | `docs/design/programs/` or `algorithms/` section | `.agents/plans/algorithms/` | **Primary PDCA** |

**Rule**: Do not start **H(n+1)** `plan-record` / `implement-conduct` before **H(n)** is fixed (exception: user-approved S0 spike).

**Agent assist**: At each H, offer **2–4 options · 1 recommendation · tradeoffs**. Final decision: user (PM confirms). User thinking in `>` blockquotes; refinement loop (below).

## C. PDCA units (S0–S1)

| ID | Name | Use | Acceptance criteria guide |
|----|------|-----|---------------------------|
| **S0** | Spike · research | Remove uncertainty; up to H3 | ≤2; minimal code |
| **S1** | Standard PDCA | **H4·H5** program / algorithm | ≤5; one definition of done |

1 plan file = 1 S* cycle. If too large → **split** (separate files in folder).

## Thinking refinement (`>` blockquotes)

Markdown **leading `>`** = scratch · thinking memo area.

- Agent: draft · options · recommendation in normal paragraphs; **awaiting user** in `>` placeholders or empty headings.
- User: edit freely inside `>`.
- Next turn: `design-record` / `plan-record` / requirements update promotes `>` into body.

## Gate table (router · PM · user)

**Gate Keeper is the user (steering)**. PM assembles evidence and **proposes** decision. Vocabulary: **Go / Conditional Go / Recycle / Hold / Kill** ([ROLES_AND_GOVERNANCE.md](../.agents/docs/ROLES_AND_GOVERNANCE.md)).

| Action | Min phase | Min scope fixed | Other |
|--------|-----------|-----------------|-------|
| New `要件.md` | P1 started | H0 overview exists | **terminology-research done** (req terms) |
| `docs/design/*` basic design | P2 done target | Parent H agreed or deliberate done | **terminology-research done**; agent recommendation recorded |
| `plan-record` | P3 equivalent | **H4/H5 parent** (program design) linkable in `docs/design/` | **User confirmation** (PM); **terminology-research done** |
| `implement-conduct` | P4 | plan `status: agreed`; `scope_level: program \| algorithm` | `plan-reference` readiness |
| `plan-record` (H0–H2) | — | Roadmap · evaluation | **PDCA Do forbidden** (frontmatter `pdca_eligible: false`) |

## Incomplete Do recovery

1. **Plan split** — move unmet criteria to new plan.
2. **`evaluator`** — `plan-evaluate` → at_risk / blocked.
3. **Act** — `status: superseded`, feedback to design (P3 rollback OK).
4. **`hotfixer`** — local fix after completion only (not full PDCA redo).

## Related files

| File | Use |
|------|-----|
| `docs/project-state.yaml` | Current phase · focus H · **gate_status** · allowed actions (from `project-state.template.yaml`) |
| `docs/_example/` | Neutral sample (in kit · deletable) |
| `docs/FIRST_PROJECT_START.md` | First project bootstrap |
| `docs/requirements/<slug>/` | Requirements P1–P2 |
| `docs/design/**` | P0–P3 design |
| `.agents/plans/{programs,algorithms}/**` | P4–P6 main arena |

Skill: `lifecycle-reference` · **`adaptive-lifecycle-plan`** (entry · Workflow Planning equivalent). Rule: `project-lifecycle.mdc`.

### Adaptive lifecycle (`adaptive-lifecycle-plan`)

From intent · brownfield · complexity, recommend **which P0–P6 / S0–S1** to run; after user **Go**, record in `docs/project-state.yaml` → `lifecycle_plan`. Kit translation of AI-DLC Workflow Planning. 13-stage map: [**AIDLC_KIT_MAP.md**](../.agents/docs/AIDLC_KIT_MAP.md) · procedure: skill `adaptive-lifecycle-plan`.

### Brownfield reverse engineering (Reverse Engineering equivalent)

When `lifecycle_plan.brownfield: true`, before P1 use skill **`brownfield-reference`** to inventory existing code. Templates: `docs/design/_template/reverse-engineering/` → consumer `docs/design/reverse-engineering/`. After user **Go** → P1. Industry research outside code → `landscape-research` (role separation · o-05).

### Infrastructure Design (IaC · G9 equivalent)

For cloud / IaC projects at P3 create **`docs/design/systems/<slug>/`** and fill 6 templates from `docs/design/_template/infrastructure/` (topology · iac-structure · networking · environments · observability-hooks · iac-verification). Kit translation of AI-DLC Infrastructure Design — record via `design-deliberate` / `design-record`. CI verification in consumer `.github/workflows/` (e.g. `iac-checkov.example.yml` · a-07).

### Operations (deploy · monitor · G4 equivalent · optional)

After P6 gate, for units needing ship/ops copy **`docs/_template/operations/`** to **`docs/operations/<unit-slug>/`** (deploy-checklist · runbook-skeleton · monitoring-slos · **feedback-to-inception**). Promote from P3 `observability-hooks.md`. Ops findings **roll back to Inception** (a-08 · `feedback-to-inception.md`) — after user Go to P1/P3. Kit translation of AI-DLC Operations — **phase not mandatory** (skippable by profile). Cloud Background Agent is out of kit per `CURSOR_SUBAGENT_POLICY.md`.

### Audit log (audit · AI-DLC audit.md equivalent)

Append-only record of gate decisions · phase transitions · lifecycle Go · question-file approvals in `.agents/memory/audit/audit-log.md`. Skill `memory-record` · `references/audit-view.md`.

## Linear integration (optional)

[LINEAR_PHASE_MAP.md](../.agents/docs/LINEAR_PHASE_MAP.md) — issue state vs P/H mapping. Align via `linear_sync` in `docs/project-state.yaml`.
