---
cpp_doc_id: cpp.topic.language_fundamentals
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [syntax, types, control-flow]
cpp_doc_regex_file: ^cpp-doc-language\-fundamentals\.md$
---

<!-- CPP_DOC_ID: cpp.topic.language_fundamentals -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ 言語基礎

**出典**: Learn C++ Ch1–11 · cppreference 言語セクション

---

## 1. 文 · 関数 · 名前空間

| 用語 | 定義 |
|------|------|
| **文 (statement)** | 実行される命令。多くは `;` で終わる |
| **関数** | 文の集合。呼び出しで制御が移る |
| **識別子** | 変数 · 関数 · 型の名前 |
| **名前空間** | 名前の衝突を避けるスコープ（`std` が標準ライブラリ） |

```cpp
namespace app {
    int compute(int x) { return x * 2; }
}
```

---

## 2. 型システム

### 2.1 基本型

| カテゴリ | 型 | 典型サイズ（実装依存） |
|----------|-----|------------------------|
| 整数 | `bool`, `char`, `short`, `int`, `long`, `long long` | 1–8 バイト |
| 浮動小数 | `float`, `double`, `long double` | 4–16 バイト |
| 文字 | `char`, `wchar_t`, `char8_t`, `char16_t`, `char32_t` | — |
| void | `void` | 戻り値なし / 汎用ポインタの基底 |

`sizeof(T)` でバイト数を取得。**固定幅型**: `<cstdint>` の `int32_t` 等。

### 2.2 型修飾子

| 修飾子 | 効果 |
|--------|------|
| `const` | 変更不可 |
| `volatile` | 最適化抑制（ハードウェア等） |
| `signed` / `unsigned` | 符号付き/なし整数 |

### 2.3 初期化

```cpp
int a = 5;      // コピー初期化
int b(5);       // 直接初期化
int c{5};       // リスト初期化（推奨 — 窄い変換を防ぐ）
int d{};        // 値初期化 → 0
```

**未初期化変数は UB（未定義動作）** — 常に初期化する。

---

## 3. 演算子と式

| 優先度（高→低） | 演算子例 |
|-----------------|----------|
| 単項 | `!`, `~`, `++`, `--`, `*`, `&` |
| 乗除 | `*`, `/`, `%` |
| 加減 | `+`, `-` |
| 比較 | `<`, `>`, `<=`, `>=`, `==`, `!=` |
| 論理 | `&&`, `\|\|` |
| 代入 | `=`, `+=`, `-=` 等 |

**整数除算**は切り捨て。`%` は剰余。

---

## 4. 制御フロー

### 4.1 条件分岐

```cpp
if (condition) {
    // ...
} else if (other) {
    // ...
} else {
    // ...
}

// C++17
if (auto it = find(v, x); it != end(v)) { /* it 使用 */ }

switch (value) {
    case 1: /* fallthrough 注意 */ break;
    default: break;
}
```

### 4.2 ループ

```cpp
for (int i = 0; i < n; ++i) { /* ... */ }

for (auto& elem : container) { /* range-for */ }

while (cond) { /* ... */ }
do { /* ... */ } while (cond);
```

`break` でループ脱出 · `continue` で次イテレーションへ。

---

## 5. 関数

```cpp
int add(int a, int b) { return a + b; }           // 値渡し
void scale(int& x) { x *= 2; }                    // 参照渡し（変更可）
void print(const std::string& s) { /* 読み取り */ } // const 参照（大オブジェクト）

// デフォルト引数
void log(const std::string& msg, int level = 0);

// オーバーロード — 引数の型/数で解決
int abs(int x);
double abs(double x);

// 関数テンプレート
template<typename T>
T max(T a, T b) { return (a < b) ? b : a; }
```

| 渡し方 | コピー | nullptr 可 | 変更 |
|--------|--------|------------|------|
| 値 | あり | — | コピー側のみ |
| 参照 `T&` | なし | 不可 | 元を変更 |
| const 参照 | なし | 不可 | 読み取り専用 |
| ポインタ `T*` | なし | 可 | 間接変更 |

---

## 6. スコープと生存期間

| スコープ | 例 | 生存期間 |
|----------|-----|----------|
| ブロック | `{ int x; }` | ブロック終了で破棄 |
| 関数パラメータ | 呼び出し中 | 呼び出し中 |
| 静的（関数内） | `static int c;` | プログラム全体 |
| 名前空間 | ファイルスコープ変数 | プログラム全体 |
| クラスメンバ | メンバ変数 | オブジェクトと同じ |

**シャドウイング**: 内側スコープの同名が外側を隠す — 避ける。

---

## 7. コンパイル時定数

```cpp
constexpr int square(int x) { return x * x; }  // C++11+
const int limit = 100;                          // 実行時 const も可

// C++17
if constexpr (std::is_integral_v<T>) {
    // T が整数型のときのみコンパイルされる分支
}
```

`consteval`（C++20）: 必ずコンパイル時に評価される関数。

---

## 8. 列挙型

```cpp
enum class Color { Red, Green, Blue };  // スコープ付き（推奨）
Color c = Color::Red;
// 暗黙の整数変換なし
```

---

## 9. よくある落とし穴

| 問題 | 対策 |
|------|------|
| 未初期化変数 | `{}` 初期化を徹底 |
| 符号付き/なし混在 | 明示キャスト · 同型に揃える |
| `=` と `==` の取り違え | コンパイラ警告を有効化 |
| 浮動小数の `==` | イプシロン比較 |
| 整数オーバーフロー | より広い型 · 事前チェック |

---

## 10. 入出力の最小例

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name;
    std::cout << "Name: ";
    std::cin >> name;
    std::cout << "Hello, " << name << '\n';
}
```

`std::endl` はフラッシュ付き — 通常は `'\n'` で十分。詳細はテンプレート・I/O 文書を参照。
