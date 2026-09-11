---
cpp_doc_id: cpp.topic.memory_ownership
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [pointers, raii, smart-pointers]
cpp_doc_regex_file: ^cpp-doc-memory\-ownership\.md$
---

<!-- CPP_DOC_ID: cpp.topic.memory_ownership -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ メモリ · 所有権 · RAII

**出典**: Learn C++ Ch12–13, 17, 19, 22 · C++ Core Guidelines R/I セクション

---

## 1. メモリモデル

| 領域 | 割当 | 解放 | 速度 | サイズ制限 |
|------|------|------|------|------------|
| **スタック** | 自動（スコープ入り） | スコープ抜け | 速い | 小（KB 級） |
| **ヒープ** | `new` / `make_*` | `delete` / スマートポインタ | 遅い | 大（RAM 制限まで） |
| **静的** | プログラム開始時 | 終了時 | — | 固定 |

**RAII（Resource Acquisition Is Initialization）**: リソースの取得をコンストラクタ、解放をデストラクタに結びつける。スコープ終了で自動解放。

---

## 2. ポインタと参照

### 2.1 アドレス演算子

```cpp
int x = 42;
int* px = &x;    // px は x のアドレスを保持
int& rx = x;     // rx は x の別名（参照）
*px = 10;        // 間接参照で x を変更
```

| | ポインタ `T*` | 参照 `T&` |
|---|---------------|-----------|
| null 可 | はい | いいえ（必ず有効オブジェクト） |
| 再代入 | 別アドレスへ可 | 不可 |
| 間接参照 | `*p` 必要 | 直接使用 |

### 2.2 nullptr

```cpp
int* p = nullptr;  // C++11 — NULL マクロより推奨
if (p) { /* 非 null */ }
```

### 2.3 ポインタ算術

```cpp
int arr[] = {1, 2, 3};
int* p = arr;       // 配列名は先頭要素へのポインタに decay
*(p + 1) == arr[1]; // true
```

配列境界外アクセスは **UB**。

---

## 3. 動的メモリ（生ポインタ）

```cpp
int* raw = new int(42);
delete raw;           // 配列は delete[]
```

| 問題 | 説明 |
|------|------|
| メモリリーク | `delete` 忘れ |
| 二重解放 | 同じポインタを二度 `delete` |
| ダングリング | 解放後のポインタを使用 |

**モダン C++ の方針**: 生 `new`/`delete` はスマートポインタとコンテナに置き換える（Guidelines R.11）。

---

## 4. スマートポインタ

### 4.1 unique_ptr — 単一所有

```cpp
#include <memory>

auto p = std::make_unique<int>(42);
// コピー不可 · move のみ
auto q = std::move(p);  // p は null に
```

配列版: `std::make_unique<int[]>(n)`（C++14 以降の慣例）。

### 4.2 shared_ptr — 共有所有

```cpp
auto sp1 = std::make_shared<int>(42);
auto sp2 = sp1;  // 参照カウント +1
// 最後の shared_ptr 破棄時に delete
```

**循環参照**: `weak_ptr` で打破。

### 4.3 所有権の移譲

```cpp
void consume(std::unique_ptr<Foo> p);  // 所有権を受け取る

auto f = std::make_unique<Foo>();
consume(std::move(f));
```

---

## 5. ムーブセマンティクス

```cpp
std::vector<int> a = {1, 2, 3};
std::vector<int> b = std::move(a);  // a のリソースを b に移動
// a は有効だが未指定状態 — 再代入のみ安全
```

| | コピー | ムーブ |
|---|--------|--------|
| コスト | 深いコピー | ポインタの付け替え |
| 元オブジェクト | 不変 | リソースを奪われる |
| トリガ | 左辺値 | `std::move` した右辺値 |

**Rule of Five**: デストラクタ · コピーコンストラクタ · コピー代入 · ムーブコンストラクタ · ムーブ代入のいずれかを定義するなら、残りも検討する。

**Rule of Zero**: 特殊メンバを一切定義せず、メンバのデフォルトに委ねる（推奨）。

---

## 6. 配列と vector

| 方式 | 用途 |
|------|------|
| `std::array<T,N>` | 固定長 · スタック |
| `std::vector<T>` | 動的長 · **デフォルトの連続コンテナ** |
| C 配列 `T[N]` | レガシー · 新規コードでは避ける |

```cpp
std::vector<int> v = {1, 2, 3};
v.push_back(4);
v.size(); v[0]; v.at(0);  // at は境界チェック
```

---

## 7. optional と値の有無

```cpp
#include <optional>

std::optional<int> parse(const std::string& s) {
    // パース成功時のみ値を持つ
    if (/* ok */) return 42;
    return std::nullopt;
}

if (auto v = parse("42")) {
    std::cout << *v;
}
```

ポインタの代替として「値があるかもしれない」を型安全に表現。

---

## 8. 所有権設計の指針

| 状況 | 推奨 |
|------|------|
| 単一所有者 | `unique_ptr` または値型 |
| 共有が必要 | `shared_ptr`（本当に必要なときのみ） |
| 観察のみ（所有しない） | 参照 · 生ポインタ（寿命が保証される場合） |
| 動的配列 | `vector<T>` |
| 出力パラメータ | **戻り値**（Guidelines F.20） |

```cpp
// 悪い: 出力引数
void get_value(int& out);

// 良い: 戻り値
std::optional<int> get_value();
```

---

## 9. 寿命とダングリング

```cpp
// 危険: ローカルへの参照を返す
const std::string& bad() {
    std::string s = "temp";
    return s;  // UB — s は破棄済み
}

// 安全: 値を返す（RVO/NRVO でコピー省略）
std::string good() {
    return "temp";
}
```

`string_view` は **非所有** — 元文字列の寿命が `view` より長いことを保証する。
