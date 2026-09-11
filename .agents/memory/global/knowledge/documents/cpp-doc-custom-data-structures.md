---
cpp_doc_id: cpp.topic.custom_ds
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [linked-list, hash, sorting]
cpp_doc_regex_file: ^cpp-doc-custom\-data\-structures\.md$
---

<!-- CPP_DOC_ID: cpp.topic.custom_ds -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ 自前データ構造とアルゴリズム

**出典**: 教科書的データ構造 · 計算量理論 — 実装で内部動作を体得した知識

---

## 1. 計算量の復習

| 記法 | 名称 | 典型 |
|------|------|------|
| $O(1)$ | 定数 | 配列インデックス |
| $O(\log n)$ | 対数 | 二分探索 |
| $O(n)$ | 線形 | 線形探索 |
| $O(n \log n)$ | 線形対数 | 効率ソート |
| $O(n^2)$ | 二次 | 二重ループ |
| $O(2^n)$ | 指数 | 部分集合列挙 |

---

## 2. 単方向連結リスト

```cpp
struct Node {
    int value;
    Node* next = nullptr;
};

class SinglyLinkedList {
public:
    void push_front(int v) {
        auto* node = new Node{v, head_};
        head_ = node;
    }
    ~SinglyLinkedList() { /* 全ノード delete */ }
private:
    Node* head_ = nullptr;
};
```

| 操作 | 計算量 |
|------|--------|
| 先頭挿入 | $O(1)$ |
| 末尾挿入（tail なし） | $O(n)$ |
| 探索 | $O(n)$ |
| 削除（値指定） | $O(n)$ |

**競プロでは** `vector` / `deque` が代替 — リストは理論理解用。

---

## 3. スタックとキュー

### スタック（LIFO）

```cpp
template<typename T>
class VectorStack {
    std::vector<T> data_;
public:
    void push(const T& v) { data_.push_back(v); }
    T pop() { T v = data_.back(); data_.pop_back(); return v; }
    bool empty() const { return data_.empty(); }
};
```

全操作 $O(1)$ 償却。

### キュー（FIFO）

`std::deque` または リングバッファ実装。先頭削除は `vector` では $O(n)$ — `deque` を使う。

---

## 4. ソートアルゴリズム

| アルゴリズム | 最悪 | 平均 | 安定 | 特徴 |
|--------------|------|------|------|------|
| バブルソート | $O(n^2)$ | $O(n^2)$ | はい | 教育用 |
| 選択ソート | $O(n^2)$ | $O(n^2)$ | いいえ | 交換回数少 |
| 挿入ソート | $O(n^2)$ | $O(n^2)$ | はい | ほぼソート済みで速い |
| マージソート | $O(n \log n)$ | $O(n \log n)$ | はい | 追加メモリ $O(n)$ |
| クイックソート | $O(n^2)$ | $O(n \log n)$ | いいえ | 実測最速のことが多い |
| `std::sort` | $O(n \log n)$ | $O(n \log n)$ | いいえ | Introsort |

**比較ソートの下界**: $\Omega(n \log n)$（決定木の葉 $n!$ 個）。

---

## 5. 探索

### 線形探索

```cpp
auto it = std::find(v.begin(), v.end(), key);  // O(n)
```

### 二分探索（ソート済み前提）

```cpp
auto it = std::lower_bound(v.begin(), v.end(), key);  // O(log n)
```

不変条件: `v[lo] <= key <= v[hi]` の区間を半分に狭める。

---

## 6. ハッシュテーブル

```cpp
// チェイン法
std::vector<std::list<std::pair<K,V>>> buckets_;

std::size_t hash(const K& key) const {
    return std::hash<K>{}(key) % buckets_.size();
}
```

| 操作 | 平均 | 最悪 |
|------|------|------|
| insert | $O(1)$ | $O(n)$ |
| find | $O(1)$ | $O(n)$ |
| erase | $O(1)$ | $O(n)$ |

負荷率 $\alpha = n/m$ を 0.7 以下に保つと再ハッシュで性能維持。  
実務では `std::unordered_map` を使う。

---

## 7. 平衡木（概念）

赤黒木 · AVL 木 — `std::map` / `std::set` の内部。  
insert/find/delete すべて $O(\log n)$ · 順序付き走査可能。

---

## 8. 自前実装 vs 標準ライブラリ

| 目的 | 推奨 |
|------|------|
| 学習 · 面接 | 自前実装で内部を理解 |
| 本番コード | `vector`, `unordered_map`, `sort` 等 |
| 競プロ | STL 優先 · UF/セグ木等 STL に無いもののみ自前 |
