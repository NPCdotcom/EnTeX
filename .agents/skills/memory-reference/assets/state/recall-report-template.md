## Memory recall

### Phase 0 — Control Plane (nav.yaml)
- nav_read: yes | missing | bootstrapped
- session_intent: ""
- next_actions: []
- active_thread_id: ""
- active_plan: ""
- alignment: { phase, scope_level, gate_status }
- pressure: { level, reanchor_required, pre_compact_recommended }

### Project layer
- project_index_read: yes | missing
- state_ids: []
- episode_ids: []
- knowledge_ids: []
- project_state_read: yes | skipped | mismatch

### Global layer
- global_index_read: yes | missing
- global_anchor_ids: []

### Merge
- conflicts_resolved: []
- gaps: []
- nav_vs_chat: aligned | mismatch | unknown
- block_recall: yes | no
