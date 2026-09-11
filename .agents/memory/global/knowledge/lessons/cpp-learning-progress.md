---
id: lesson-cpp-learning-progress
kind: knowledge
topic: lesson
owner: learning/cpp
status: active
created: 2026-06-22
promoted: 2026-06-22
tags: [cpp, learning, learncpp, cuda, vulkan, complete-phases]
sources:
  - learning/cpp/notes/00-index.md
  - learning/cpp/notes/phase1-complete.md
  - learning/cpp/notes/phase3-complete.md
linked: [lesson-learning-complete-index]
---

# C++ 学習ロードマップ — 長期記憶（正本）

**正本パス**: `~/.agents/learning/cpp/`  
**状態**: LearnCpp + CG + MS Learn 完走 · **フェーズ1–6 完走** · 拡張は任意

---

## Facts

| 項目 | 値 |
|------|-----|
| LearnCpp | Ch0–28 + 付録 A–C **読了** |
| Core Guidelines | CG-1–4 **完走** |
| MS Learn | MS-0–5（vcpkg 含む）**完走** |
| フェーズ1 | Capstone GradeBook CLI v8 |
| フェーズ2 | A データ構造 · B STL · C スレッド · D ネット · E GUI **完走** |
| フェーズ3 | CUDA P3-0–8 + capstone gpu_stats **完走** |
| フェーズ4 | CUDA 深掘り P4-0–2 **完走** |
| フェーズ5 | 応用 P5-0–2 **完走** |
| フェーズ6 | Vulkan P6-0–9 + capstone **完走** |
| 索引 | `notes/00-index.md` · `notes/mslearn-roadmap.md` · `notes/phase2-roadmap.md` |
| manifest | `status: phases_1-6_complete` |

## 実験レイアウト

```text
experiments/
  chNN_learncpp/   LearnCpp 章ごと
  p2_*/            フェーズ2 モジュール
  p3_cuda/         CUDA + capstone
  p6_vulkan/       Vulkan
  capstone/        GradeBook CLI
```

## 教訓

- RAII · スマートポインタ · move を実験で確認してから本番へ
- CMake + vcpkg は MS-4/5 で固定
- CUDA: ホスト/デバイス分離 · stream は P4 深掘り

## 次候補（任意）

新 Capstone · Rust 相互運用 · 本番プロジェクトへの適用 — ユーザー指示待ち
