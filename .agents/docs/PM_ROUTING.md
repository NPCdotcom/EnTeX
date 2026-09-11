# PM routing — dual loops · control plane · pressure

**Canonical**: this file · **Index**: [MANDATORY_PROCEDURES.md](./MANDATORY_PROCEDURES.md) · **Tiers**: [CONTEXT_TIERS.md](./CONTEXT_TIERS.md)

Related: [MEMORY_ARCHITECTURE.md](./MEMORY_ARCHITECTURE.md) · [AGENT_EVALUATION.md](./AGENT_EVALUATION.md)

---

## Enforcement legend

| Label | Meaning |
|-------|---------|
| **hook** | Cursor hook / script — deterministic |
| **script** | `env/bin/agents-run.py` or kit script |
| **llm-soft** | Agent must follow; if skipped, next turn repairs via nav/episode gap (fallback) |

---

## Design principles

| Principle | Meaning |
|-----------|---------|
| **Separation** | Per-turn rhythm ≠ phase P/H/gate decisions |
| **Control plane** | Next actions live in **files** — do not trust chat |
| **Accuracy** | If Loop2 unclear → **run Loop2** |
| **Pre-empt compress** | Before Cursor summarize: L2 flush + nav update + new chat |
| **Minimal turn** | Standard turn = **3 skills** (+ Loop2 conditional) |

---

## Control plane (two files)

| File | Layer | Update | Holds | Enforcement |
|------|-------|--------|-------|-------------|
| **`docs/project-state.yaml`** | team | gate · phase | P/H/gate/blockers | llm-soft |
| **`.agents/memory/state/nav.yaml`** | project | **every turn** | intent, next_actions, pressure | llm-soft (+ **hook** on preCompact) |

`nav.alignment.*` syncs with `project-state` in **Loop2** only (Loop1: **quote**).

---

## Loop 1 — minimal operating rhythm

**Canonical chain**: [`skills/_chains/pm-turn.md`](../skills/_chains/pm-turn.md)

```
pm-turn-start
  = context-guard + memory-reference(nav) + memory-reason(mini)
    + secretary-brief(turn) + secretary-route
→ [Loop2?] lifecycle-reference + nav-brief
→ role-execute
→ pm-turn-end
  = action-evaluate(staged) + [full→critique] + memory-flush + memory-record
→ reply + short operational trace
```

**L1 required writes** (non-lightweight): `nav.yaml` + **one** `episodes/*` + `index.yaml` touch.
traces / evaluations / rewards: only on full evaluate, `turn_reward<0.6`, or pre_compact (**llm-soft** fallback: note gap in episode).

**Exclude from turn-brief**: lifecycle re-classify · exploration (→ Loop2).

---

## Loop 2 — project navigation (conditional)

**Triggers** (any · if unclear still run): context-guard loop2/reanchor · user P/H/plan/gate · nav≠project-state · before `*-record` / implement-conduct · research on record path · Re-anchor.

```
lifecycle-reference → nav-brief → [research if needed] → turn-brief reflects nav-brief
```

**Re-anchor**: Stop Edit/conduct → read nav + project-state + active thread/plan only → one-line chat vs file delta → L2 flush.

---

## context-guard · hooks

| pressure | Terminal flush |
|----------|----------------|
| low | L1 |
| medium | L1 + nav |
| high | L2 recommended |
| pre_compact | **L2 required** + new chat |

| Hook | File | Enforcement |
|------|------|-------------|
| **preCompact** | [hooks/pre-compact.py](../hooks/pre-compact.py) | **hook** — sets pressure + audit-log |
| **stop** | [hooks/stop-reanchor.py](../hooks/stop-reanchor.py) | **hook** — Re-anchor followup (max 3) |

---

## Staged evaluation

| Turn type | evaluate | critique |
|-----------|----------|----------|
| Lightweight | skip | skip |
| Loop1 read-only | mini | skip |
| Loop1 execute / Loop2 / reanchor | full | full |

---

## Bootstrap contract

```bash
cp .agents/memory/state/nav.yaml.example .agents/memory/state/nav.yaml
cp .agents/memory/audit/audit-log.md.example .agents/memory/audit/audit-log.md
mkdir .agents/memory/episodes
cp docs/project-state.template.yaml docs/project-state.yaml
```

Missing nav / episodes / audit-log → **ERROR** (memory-reference) — do not soft-skip. Kit workspace: `session.intent=kit-maintenance`.
