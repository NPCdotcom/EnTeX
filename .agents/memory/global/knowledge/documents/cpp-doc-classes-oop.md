---
cpp_doc_id: cpp.topic.classes_oop
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [classes, inheritance, polymorphism]
cpp_doc_regex_file: ^cpp-doc-classes\-oop\.md$
---

<!-- CPP_DOC_ID: cpp.topic.classes_oop -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ クラス · オブジェクト指向

**出典**: Learn C++ Ch13–16, 21–25 · C++ Core Guidelines C セクション

---

## 1. クラスの基本

```cpp
class Point {
public:
    Point(double x, double y) : x_{x}, y_{y} {}  // コンストラクタ

    double distance() const { return std::hypot(x_, y_); }

private:
    double x_{};
    double y_{};
};
```

| 概念 | 説明 |
|------|------|
| **カプセル化** | `public` / `protected` / `private` でアクセス制御 |
| **不変条件 (invariant)** | コンストラクタで確立 · メンバ関数で維持 |
| **`const` メンバ関数** | オブジェクトを変更しない — const オブジェクトから呼べる |
| **`this`** | 自身へのポインタ — メソッドチェーン等 |

---

## 2. 特殊メンバ関数

| 関数 | 役割 |
|------|------|
| デフォルトコンストラクタ | 引数なし構築 |
| コピーコンストラクタ | 同型からコピー構築 |
| ムーブコンストラクタ | 右辺値からリソース移動 |
| コピー代入演算子 | 既存オブジェクトへコピー |
| ムーブ代入演算子 | 既存オブジェクトへ移動 |
| デストラクタ | リソース解放 |

```cpp
class Widget {
public:
    Widget() = default;
    ~Widget() = default;
    Widget(const Widget&) = default;
    Widget& operator=(const Widget&) = default;
    Widget(Widget&&) noexcept = default;
    Widget& operator=(Widget&&) noexcept = default;
};
```

**Rule of Zero**: メンバが適切に定義されていれば、上記をすべて `= default` に委ねる。

---

## 3. 演算子オーバーロード

```cpp
class Fraction {
public:
    Fraction(int num, int den) : num_{num}, den_{den} {}

    Fraction operator+(const Fraction& other) const {
        return {num_ * other.den_ + other.num_ * den_, den_ * other.den_};
    }

    friend std::ostream& operator<<(std::ostream& os, const Fraction& f) {
        return os << f.num_ << '/' << f.den_;
    }

private:
    int num_, den_;
};
```

よくオーバーロードする演算子: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `<<`, `>>`, `[]`, `()`, `->`.

---

## 4. 継承

```cpp
class Animal {
public:
    virtual ~Animal() = default;           // 多態の基底は virtual dtor
    virtual void speak() const = 0;      // 純粋仮想 = 抽象クラス
};

class Dog : public Animal {
public:
    void speak() const override { std::cout << "woof\n"; }
};
```

| 継承 | 意味 |
|------|------|
| `public` | is-a 関係 · 最も一般的 |
| `protected` | 派生クラスのみ public 的にアクセス |
| `private` | 実装継承（has-a の実装手段） |

**構築順**: 基底 → メンバ → 派生本体。  
**破棄順**: 逆順。

---

## 5. 多態（動的束縛）

```cpp
std::unique_ptr<Animal> pet = std::make_unique<Dog>();
pet->speak();  // 実行時に Dog::speak が呼ばれる
```

| キーワード | 用途 |
|------------|------|
| `virtual` | オーバーライド可能 |
| `override` | 派生で明示（タイポ検出） |
| `final` | これ以上オーバーライド不可 |

**vtable**: コンパイラが仮想関数テーブルを生成。ポインタ/参照経由でのみ多態が働く。

---

## 6. コンポジション vs 継承

| 関係 | 手段 | 例 |
|------|------|-----|
| **has-a** | メンバ変数（コンポジション） | `Car` が `Engine` を持つ |
| **is-a** | `public` 継承 | `Dog` は `Animal` |

継承は **インターフェースの共有** に限定し、実装の再利用はコンポジションを優先（Guidelines C.120）。

---

## 7. 静的メンバ

```cpp
class Counter {
public:
  static int count() { return s_count; }
  Counter() { ++s_count; }
private:
  static inline int s_count = 0;
};
```

クラス全体で共有されるデータ · ユーティリティ関数。

---

## 8. フレンド

```cpp
class Matrix;
class Vector {
    friend Matrix;  // Matrix が Vector の private にアクセス可
};
```

密結合の表現 — 乱用しない。

---

## 9. 設計チェックリスト

| 項目 | 推奨 |
|------|------|
| 不変条件 | コンストラクタで確立 |
| 多態の基底 | `virtual ~Base() = default` |
| コピー/ムーブ | Rule of Zero を第一選択 |
| データメンバ | `private` · アクセサは必要最小限 |
| 出力 | ストリーム演算子または `to_string` 風メソッド |
