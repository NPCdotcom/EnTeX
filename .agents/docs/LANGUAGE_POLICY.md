# Language policy

**Status**: canonical (R-3 B1 · 2026-06-22)  
**Principle**: **Two-layer language** — machine canon = English · human deliverables = Japanese

---

## Summary

| Surface | Language | Rationale |
|---------|----------|-----------|
| **Machine canon** (L0–L2) | **English** | Instruction-following · terse IF-THEN · Cursor ecosystem |
| **Human deliverables** (project templates) | **Japanese** (default) | User reads/writes requirements · charter |
| **User ↔ agent chat** | **Japanese** | User preference |
| **Identifiers** | **English** | `spec_designer`, `secretary-gate`, paths |
| **Learning / refresh notes** | **Japanese** | `learning/` design memory |
| **Global lessons** | **English** | Cross-session recall |

**Anti-pattern**: Duplicate JP+EN copies of the same procedural doc.

---

## By tier

See [CONTEXT_TIERS.md](./CONTEXT_TIERS.md) § language.

| Tier | Language |
|------|----------|
| L0–L2 | English |
| L3 procedural docs | English |
| L3 kit README (human) | Japanese OK |
| `_template/` user fields | Japanese |
| Project `docs/requirements/` etc. | Japanese default |

---

## Agent behavior

- User messages: **Japanese**
- Replies to user: **Japanese**
- Kit canon reads: **English**
- Code · commits · identifiers: **English** unless project dictates otherwise
