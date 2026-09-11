---
id: lesson-npcdotcom-landscape
kind: knowledge
topic: lesson
owner: NPCdotcom
status: active
created: 2026-06-18
tags: [cuda, vulkan, simulation, landscape]
---

# 教訓 — NPCdotcom 関連技術ランドスケープ（要約）

詳細正本は learning 層: `learning/npcdotcom/sources/landscape-dev-reference.md`

## 要点（2026-06-18 調査）

| 領域 | フック |
|------|--------|
| CUDA / 大規模 sim | Madrona（GPU batch ECS）、GPUDRIVE、NVIDIA Warp |
| CPU+GPU | 純オフロードより協調スケジューリングが進展 |
| Vulkan | Khronos エンジン教程、render graph、GPU-driven voxel（Aokana） |
| 最小 algorithm | DOD + Policy-Based + foundation 層分離 |
| 物理 ∥ 化学 | Noita、Mintage intent→resolver、データ駆動反応 |
| SoA | sim ホットパスでは GPU/CPU 双方で標準的 |

## 次に深掘りする候補

1. CUDA Graph / stream と決定性
2. Vulkan sync2 / render graph
3. Registry seal / hot-reload 方針
4. メタレジストリと tooling（エージェントが語彙を列挙）

## Related

- npcdotcom-philosophy
