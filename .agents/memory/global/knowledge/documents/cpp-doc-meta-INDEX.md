---
cpp_doc_id: cpp.meta.index
cpp_doc_topic: cpp
cpp_doc_kind: meta
cpp_doc_tags: [index, regex]
cpp_doc_regex_file: ^cpp-doc-meta-INDEX
---

<!-- CPP_DOC_ID: cpp.meta.index -->
<!-- CPP_DOC_KIND: meta -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ ドキュメント索引

`documents/` 直下のフラット配置。各ファイルは **単体完結** の C++ 知識文書（学習サイクル・フェーズ情報なし）。

## 正規表現

```text
全件:     ^cpp-doc-.*\.(md|yaml)$
トピック: ^cpp-doc-(?!meta-)[a-z0-9-]+\.md$
ID:       <!-- CPP_DOC_ID: ([\w.]+) -->
```

## 一覧（22 件）

### 言語 · 標準ライブラリ · 設計

- `cpp-doc-cpp-overview.md` — `cpp.topic.overview`
- `cpp-doc-language-fundamentals.md` — `cpp.topic.language_fundamentals`
- `cpp-doc-memory-ownership.md` — `cpp.topic.memory_ownership`
- `cpp-doc-classes-oop.md` — `cpp.topic.classes_oop`
- `cpp-doc-templates-exceptions-io.md` — `cpp.topic.templates_exceptions`
- `cpp-doc-stl.md` — `cpp.topic.stl`
- `cpp-doc-modern-cpp.md` — `cpp.topic.modern_cpp`
- `cpp-doc-build-tooling.md` — `cpp.topic.build_tooling`
- `cpp-doc-core-guidelines.md` — `cpp.topic.core_guidelines`

### システム · GPU · グラフィックス

- `cpp-doc-concurrency.md` — `cpp.topic.concurrency`
- `cpp-doc-networking-asio.md` — `cpp.topic.networking`
- `cpp-doc-gui-sdl.md` — `cpp.topic.gui_sdl`
- `cpp-doc-custom-data-structures.md` — `cpp.topic.custom_ds`
- `cpp-doc-cuda-programming.md` — `cpp.topic.cuda`
- `cpp-doc-vulkan-graphics.md` — `cpp.topic.vulkan`

### 競技プログラミング · アルゴリズム

- `cpp-doc-cp-complexity-search-greedy.md` — `cpp.topic.cp_complexity`
- `cpp-doc-cp-stl-union-find.md` — `cpp.topic.cp_stl_ds`
- `cpp-doc-cp-recursion-backtracking.md` — `cpp.topic.cp_search`
- `cpp-doc-cp-dynamic-programming.md` — `cpp.topic.cp_dp`
- `cpp-doc-cp-graph-algorithms.md` — `cpp.topic.cp_graphs`
- `cpp-doc-cp-range-queries.md` — `cpp.topic.cp_range_queries`
- `cpp-doc-cp-number-theory.md` — `cpp.topic.cp_number_theory`

- `cpp-doc-meta-REGISTRY.yaml`
