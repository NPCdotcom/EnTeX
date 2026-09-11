---
cpp_doc_id: cpp.topic.build_tooling
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [cmake, vcpkg, gtest]
cpp_doc_regex_file: ^cpp-doc-build\-tooling\.md$
---

<!-- CPP_DOC_ID: cpp.topic.build_tooling -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ ビルド · ツールチェーン

**出典**: Microsoft Learn · CMake 公式 · vcpkg · Google Test

---

## 1. 翻訳モデル

```text
.cpp + .h
  → プリプロセッサ (#include, #define, #if)
  → コンパイラ (各 .cpp → .o / .obj)
  → リンカ (ライブラリ + オブジェクト → 実行ファイル)
```

| 成果物 | 説明 |
|--------|------|
| オブジェクトファイル | 1 翻訳単位の機械語 |
| 静的ライブラリ `.a` / `.lib` | オブジェクトのアーカイブ |
| 動的ライブラリ `.so` / `.dll` | 実行時ロード |
| 実行ファイル | `main` を含む |

---

## 2. 手動ビルド（最小）

```powershell
g++ -std=c++17 -Wall -Wextra -pedantic -c foo.cpp -o foo.o
g++ -std=c++17 foo.o bar.o -o app
```

静的ライブラリ:

```powershell
ar rcs libadd.a add.o
g++ main.cpp -L. -ladd -o main
```

---

## 3. CMake

### 3.1 最小プロジェクト

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(myapp main.cpp foo.cpp)
target_compile_options(myapp PRIVATE -Wall -Wextra -pedantic)
```

### 3.2 ビルド手順

```powershell
cmake --preset mingw-release    # または -B build -G Ninja
cmake --build build
ctest --test-dir build
```

### 3.3 よく使うコマンド

| コマンド | 用途 |
|----------|------|
| `add_library` | 静的/共有ライブラリ |
| `target_link_libraries` | リンク依存 |
| `target_include_directories` | インクルードパス |
| `find_package` | 外部パッケージ検出 |
| `FetchContent` | リポジトリから取得 |
| `add_subdirectory` | サブプロジェクト |

### 3.4 Presets（CMake 3.19+）

`CMakePresets.json` で generator · ビルドタイプ · コンパイラフラグを共有可能。

---

## 4. vcpkg

manifest モード (`vcpkg.json`):

```json
{
  "dependencies": ["fmt", "gtest"]
}
```

```cmake
# CMakeLists.txt
find_package(fmt CONFIG REQUIRED)
target_link_libraries(myapp PRIVATE fmt::fmt)
```

```powershell
cmake -B build -DCMAKE_TOOLCHAIN_FILE=[vcpkg root]/scripts/buildsystems/vcpkg.cmake
```

| 概念 | 説明 |
|------|------|
| manifest | プロジェクト直下の `vcpkg.json` |
| triplet | `x64-windows`, `x64-mingw-dynamic` 等 |
| バイナリキャッシュ | ビルド済みパッケージの再利用 |

---

## 5. Google Test

```cpp
#include <gtest/gtest.h>

TEST(MathTest, Add) {
    EXPECT_EQ(2 + 2, 4);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

CMake:

```cmake
find_package(GTest CONFIG REQUIRED)
add_executable(tests test_main.cpp)
target_link_libraries(tests PRIVATE GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(tests)
```

| マクロ | 用途 |
|--------|------|
| `EXPECT_EQ` | 等価（失敗しても続行） |
| `ASSERT_EQ` | 等価（失敗で停止） |
| `EXPECT_THROW` | 例外検証 |

---

## 6. GSL（Guideline Support Library）

Microsoft 提供の Core Guidelines 支援ライブラリ。

| 型/関数 | 用途 |
|---------|------|
| `gsl::span<T>` | 非所有連続範囲 |
| `gsl::not_null<T*>` | null 非許容ポインタ |
| `gsl::finally` | スコープ終了時の後処理 |
| `Expects` / `Ensures` | 契約チェック |

---

## 7. コンパイラフラグ（推奨）

| フラグ | 効果 |
|--------|------|
| `-Wall -Wextra -Wpedantic` | 警告最大化 |
| `-Werror` | 警告をエラーに（CI 向け） |
| `-g` | デバッグ情報 |
| `-O2` / `-O3` | 最適化 |
| `-fsanitize=address` | AddressSanitizer（デバッグ） |

---

## 8. 静的解析 · フォーマット

| ツール | 用途 |
|--------|------|
| clang-tidy | 静的解析 · Guidelines チェック |
| clang-format | コード整形 |
| Compiler Explorer | 生成アセンブリの比較 |
