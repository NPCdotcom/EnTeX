---
cpp_doc_id: cpp.topic.modern_cpp
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [cpp11, cpp17, cpp20]
cpp_doc_regex_file: ^cpp-doc-modern\-cpp\.md$
---

<!-- CPP_DOC_ID: cpp.topic.modern_cpp -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# モダン C++（C++11–23）

**出典**: Learn C++ 付録 B/F · Microsoft Learn Modern C++ · Core Guidelines

---

## 1. C++11 — モダン基盤

| 機能 | 構文例 | 用途 |
|------|--------|------|
| `auto` | `auto x = 42;` | 型推論 |
| `nullptr` | `int* p = nullptr;` | null ポインタ |
| Range-for | `for (auto& x : v)` | コンテナ走査 |
| ラムダ | `[&](int x){ return x+1; }` | 無名関数オブジェクト |
| ムーブ | `std::move(x)` | 右辺値参照 |
| Smart ptr | `unique_ptr`, `shared_ptr` | RAII 所有権 |
| `enum class` | `enum class C { Red };` | スコープ列挙 |
| `override`/`final` | `void f() override;` | 仮想関数の明示 |
| `constexpr` | `constexpr int N = 10;` | コンパイル時定数 |
| `noexcept` | `void f() noexcept;` | 例外非送出 |
| 均一初期化 | `vector<int> v{1,2,3};` | `{}` 初期化 |
| `static_assert` | `static_assert(sizeof(int)==4);` | コンパイル時検査 |

---

## 2. C++14

| 機能 | 例 |
|------|-----|
| `make_unique` | `auto p = make_unique<Foo>();` |
| Generic lambda | `[](auto a, auto b){ return a+b; }` |
| Relaxed constexpr | constexpr 関数内にループ可 |
| 桁区切り | `int n = 1'000'000;` |
| `std::exchange` | 移動 + 旧値を既定に |

---

## 3. C++17（多くのプロジェクトの既定）

| 機能 | 例 | 用途 |
|------|-----|------|
| **CTAD** | `pair p{1, 2.0};` | テンプレート引数推論 |
| **`optional`** | `optional<int> o;` | 値の有無 |
| **`string_view`** | `void f(string_view s);` | 非所有文字列 |
| **`if constexpr`** | コンパイル時分岐 | SFINAE 簡素化 |
| Structured binding | `auto [a,b] = pair;` | 分解代入 |
| `filesystem` | `fs::exists(path)` | ファイルシステム |
| `inline` 変数 | `inline constexpr int N=10;` | ヘッダ内定義 |
| Nested namespace | `namespace a::b {}` | 名前空間短縮 |
| `std::gcd`/`lcm` | `<numeric>` | 整数演算 |

---

## 4. C++20（段階導入）

| 機能 | 概要 |
|------|------|
| **Concepts** | テンプレート制約 `template<integral T>` |
| **Modules** | `import std;` — コンパイル時間短縮 |
| **Coroutines** | `co_await` / `co_yield` |
| **Ranges** | `views::filter`, `views::transform` |
| **`span<T>`** | 非所有連続範囲 |
| **`<=>`** | 宇宙船演算子 · 自動比較生成 |
| **`format`** | 型安全フォーマット |
| **`consteval`** | 必ずコンパイル時評価 |
| **`jthread`** | 協調的キャンセル付きスレッド |

---

## 5. C++23（参照）

`print` / `println` · `expected<T,E>` · `mdspan` · `flat_map`/`flat_set` · `generator`（coroutine）等。

---

## 6. 実践チェックリスト

### メモリ · 所有権

- 動的配列 → `vector` · 単一所有 → `unique_ptr`
- 生 `new`/`delete` を避ける
- 共有は `shared_ptr` + `make_shared`（本当に必要なとき）
- C 配列を使わない

### 型 · 初期化

- `auto` で冗長な型名を省略（意図は明確に）
- `{}` 初期化を優先
- 常に初期化 · null は `nullptr`
- 列挙は `enum class`

### 関数 · 式

- range-for を優先
- 小さな述語はラムダ
- in: 小→値 · 大→`const&` · out→戻り値
- `std::move` は必要時のみ
- キャストは named cast · 最小限

### クラス · エラー

- 不変条件は ctor で確立
- Rule of Zero/Five
- 多態の基底は virtual dtor
- エラーは専用例外型

---

## 7. MSVC 固有の注意

| 項目 | 内容 |
|------|------|
| `/std:c++17` | 言語標準指定 |
| `/Zc:__cplusplus` | `__cplusplus` マクロを正しい値に |
| `/permissive-` | 非標準拡張を抑制 |
| `/MD` vs `/MT` | DLL CRT vs 静的 CRT — 混在禁止 |

MinGW は libstdc++ — MSVC の CRT 表と 1:1 非対応。
