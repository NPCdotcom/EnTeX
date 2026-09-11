---
cpp_doc_id: cpp.topic.templates_exceptions
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [templates, exceptions, iostream]
cpp_doc_regex_file: ^cpp-doc-templates\-exceptions\-io\.md$
---

<!-- CPP_DOC_ID: cpp.topic.templates_exceptions -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ テンプレート · 例外 · 入出力

**出典**: Learn C++ Ch11, 20, 26–28 · Core Guidelines E/T セクション

---

## 1. 関数テンプレート

```cpp
template<typename T>
T maximum(T a, T b) {
    return (a < b) ? b : a;
}

// 明示的特殊化
template<>
const char* maximum<const char*>(const char* a, const char* b) {
    return std::strcmp(a, b) < 0 ? b : a;
}
```

コンパイラが呼び出し時の型から **実装を生成**（コード生成 = 静的ポリモーフィズム）。

---

## 2. クラステンプレート

```cpp
template<typename T, std::size_t N>
class StaticArray {
public:
    T& operator[](std::size_t i) { return data_[i]; }
    std::size_t size() const { return N; }
private:
    T data_[N]{};
};

StaticArray<int, 10> arr;
```

`std::vector<T>` · `std::array<T,N>` · `std::optional<T>` 等が代表例。

---

## 3. テンプレート引数の種類

| 種類 | 例 |
|------|-----|
| 型引数 | `template<typename T>` |
| 非型引数 | `template<int N>` · `template<auto V>` (C++17) |
| テンプレートテンプレート | `template<template<typename> class C>` |
| 可変引数 | `template<typename... Args>` |

```cpp
template<typename... Args>
void log(Args&&... args) {
    (std::cout << ... << args);  // C++17 fold expression
}
```

---

## 4. SFINAE と concepts（概要）

**SFINAE**: 置換失敗はエラーにしない — オーバーロード解決でテンプレートを除外。

**C++20 concepts**:

```cpp
template<std::integral T>
T add(T a, T b) { return a + b; }
```

制約をシグネチャに明示し、エラーメッセージを改善。

---

## 2. 例外処理

### 2.1 基本構文

```cpp
double safe_divide(double a, double b) {
    if (b == 0.0) throw std::invalid_argument("division by zero");
    return a / b;
}

try {
    auto r = safe_divide(1, 0);
} catch (const std::invalid_argument& e) {
    std::cerr << e.what() << '\n';
} catch (...) {
    std::cerr << "unknown error\n";
}
```

### 2.2 例外の設計指針

| 指針 | 内容 |
|------|------|
| 専用型 | `std::runtime_error` 派生を問題ごとに |
| noexcept | 例外を投げない関数に付与 |
| RAII | スタック巻き戻しで自動解放 |
| 契約違反 | `assert` / `std::terminate`（回復不能） |

```cpp
void foo() noexcept;  // 例外を投げない契約
```

**デストラクタは通常 noexcept** — 例外中のデストラクタ例外は `std::terminate`。

### 2.3 標準例外階層

```text
std::exception
 ├── std::logic_error (invalid_argument, out_of_range, ...)
 └── std::runtime_error (overflow_error, ...)
```

---

## 3. 入出力ストリーム

### 3.1 標準ストリーム

```cpp
#include <iostream>
#include <iomanip>

int x = 42;
std::cout << std::setw(5) << std::setfill('0') << x << '\n';
std::cin >> x;
```

| ストリーム | 用途 |
|------------|------|
| `std::cin` | 標準入力 |
| `std::cout` | 標準出力 |
| `std::cerr` | 標準エラー（バッファリングなし） |
| `std::clog` | ログ（バッファリングあり） |

### 3.2 文字列ストリーム

```cpp
#include <sstream>

std::ostringstream oss;
oss << "value=" << 42;
std::string s = oss.str();

std::istringstream iss("1 2 3");
int a, b, c;
iss >> a >> b >> c;
```

### 3.3 ファイル I/O

```cpp
#include <fstream>

std::ifstream in("data.txt");
std::ofstream out("out.txt", std::ios::app);
std::string line;
while (std::getline(in, line)) {
    out << line << '\n';
}
```

**RAII**: ストリームはデストラクタで自動クローズ。

### 3.4 書式（C++20 `<format>`）

```cpp
#include <format>
std::string msg = std::format("x={} y={}", 1, 2);
```

C++17 以前は `stringstream` またはサードパーティ（fmt 等）。

---

## 4. ファイルシステム（C++17）

```cpp
#include <filesystem>
namespace fs = std::filesystem;

if (fs::exists("path/to/file")) {
    auto size = fs::file_size("path/to/file");
}
for (const auto& entry : fs::directory_iterator(".")) {
    // ...
}
```
