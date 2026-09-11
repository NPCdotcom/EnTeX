# Memory I/O contract

- Kit workspace: `session.intent` must stay `kit-maintenance` (no foreign project leftovers).
- L2 (traces/evaluations): only full evaluate / turn_reward&lt;0.6 / pre_compact.
- Enforcement: writes are **llm-soft**; preCompact audit line is **hook**.
