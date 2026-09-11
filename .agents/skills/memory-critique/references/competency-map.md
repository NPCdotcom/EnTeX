# MemoryAgentBench → memory-critique

| Competency | Critique signal | fail 例 |
|------------|-----------------|---------|
| **Accurate retrieval** | IsRel + cited ids ∈ recall | 幻覚 memory id |
| **Test-time learning** | episode→lesson に trace 証拠 | 同失敗の繰り返し |
| **Long-range understanding** | thread + project-state 一貫 | phase と action 不一致 |
| **Selective forgetting** | IsStale · archive 未処理 | 古い alignment 優先 |

`competency_gaps` に fail した能力 id を記録 → memory-refine / memory-reason へ。
