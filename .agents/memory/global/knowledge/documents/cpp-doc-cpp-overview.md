---
cpp_doc_id: cpp.topic.overview
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [overview, standards, ecosystem]
cpp_doc_regex_file: ^cpp-doc-cpp\-overview\.md$
---

<!-- CPP_DOC_ID: cpp.topic.overview -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ 言語概観

**出典**: ISO C++ 委員会 · cppreference.com · Learn C++ · Microsoft Learn · C++ Core Guidelines

---

## 1. C++ とは

C++ は **静的型付け** · **コンパイル型** · **マルチパラダイム**（手続き · オブジェクト指向 · 汎用プログラミング）のシステムプログラミング言語。C の性能と低レベル制御に、抽象化 · 型安全 · 標準ライブラリを重ねた。

| 特性 | 内容 |
|------|------|
| 実行モデル | ソース → コンパイル → リンク → ネイティブバイナリ |
| 型システム | コンパイル時チェックが主 · テンプレートによる静的多態 |
| メモリ | スタック · ヒープ · 所有権をプログラマが明示（モダン C++ では RAII で自動化） |
| 標準 | ISO/IEC 14882 — C++11 以降 3 年周期で改訂 |

---

## 2. プログラムの骨格

```cpp
#include <iostream>

int main() {
    std::cout << "Hello\n";
    return 0;
}
```

| 要素 | 役割 |
|------|------|
| `#include` | プリプロセッサ — ヘッダを取り込む |
| `main()` | エントリポイント（必須） |
| `return 0` | 正常終了を OS に通知 |
| `std::` | 標準ライブラリ名前空間 |

**翻訳単位**: 各 `.cpp` は独立にコンパイルされ、オブジェクトファイルをリンカが結合する。宣言は `.h` / `.hpp` に分離するのが慣例。

---

## 3. 標準版の変遷

| 版 | 主な追加 | 実務上の位置づけ |
|----|----------|------------------|
| C++98/03 | STL 確立 | レガシー |
| **C++11** | `auto` · move · smart ptr · ラムダ · `constexpr` | モダン基盤 |
| C++14 | `make_unique` · generic lambda | 小改善 |
| **C++17** | `optional` · `string_view` · CTAD · `if constexpr` | 多くのプロジェクトの既定 |
| C++20 | concepts · modules · coroutines · ranges | 段階導入中 |
| C++23 | `print` · `expected` · `mdspan` 等 | 新機能参照 |

コンパイラ指定例:

```text
g++:   -std=c++17 -Wall -Wextra -pedantic
MSVC:  /std:c++17 /W4 /permissive-
```

---

## 4. 参照ドキュメントの使い分け

| リソース | 用途 |
|----------|------|
| [cppreference.com](https://en.cppreference.com/w/) | API · 言語仕様の de facto 標準参照（英語） |
| [cpprefjp](https://cpprefjp.github.io/) | 日本語リファレンス |
| [Learn C++](https://www.learncpp.com/) | 段階的チュートリアル |
| [Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) | 設計 · ベストプラクティス |
| [Microsoft Learn C++](https://learn.microsoft.com/en-us/cpp/) | MSVC · Windows ツールチェーン |
| WG21 ドラフト (N5046 等) | 仕様そのもの（必要な章のみ） |

---

## 5. コンパイラ実装

| 実装 | 標準ライブラリ | 典型環境 |
|------|----------------|----------|
| GCC | libstdc++ | Linux · MinGW |
| Clang | libc++ または libstdc++ | macOS · Linux · Windows |
| MSVC | Microsoft STL | Windows · Visual Studio |

同一 C++ 標準でも **ABI · ヘッダ配置 · 拡張** は実装依存。移植時は cppreference のコンパイラ対応表を確認する。

---

## 6. ビルドツールチェーン

```text
ソース (.cpp/.h)
    → プリプロセッサ (#include, #define)
    → コンパイラ (翻訳単位 → .o/.obj)
    → リンカ (ライブラリ結合 → 実行ファイル)
```

| ツール | 役割 |
|--------|------|
| **CMake** | クロスプラットフォームビルド記述 |
| **vcpkg** | C++ パッケージマネージャ（manifest モード） |
| **Google Test** | 単体テストフレームワーク |
| **GSL** | Guideline Support Library（境界チェック等） |

---

## 7. 学習領域の地図（知識の接続）

```text
言語基礎 → メモリ/所有権 → クラス/OOP → テンプレート/例外
    → STL → モダン C++ → Core Guidelines
    → 並行処理 · ネットワーク · GUI（応用）
    → CUDA（GPU 計算）· Vulkan（GPU グラフィックス）
    → 競技プログラミング（アルゴリズム · 計算量 · データ構造）
```

各領域は本レジストリの個別 `cpp-doc-*` ファイルに **単体完結** で記述する。
