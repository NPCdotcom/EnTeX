---
cpp_doc_id: cpp.topic.concurrency
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [threads, mutex, async]
cpp_doc_regex_file: ^cpp-doc-concurrency\.md$
---

<!-- CPP_DOC_ID: cpp.topic.concurrency -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ 並行プログラミング

**出典**: C++ `<thread>` 標準ライブラリ · Core Guidelines CP セクション · GSL

---

## 1. スレッドの基本

```cpp
#include <thread>

void worker() { /* ... */ }

std::thread t(worker);
t.join();   // 完了まで待つ — 必須
```

| 操作 | 意味 |
|------|------|
| `std::thread(f, args...)` | 新スレッドで `f` を実行 |
| `join()` | 終了を待ちリソース回収 |
| `joinable()` | join/detach 可能か |
| `detach()` | **非推奨** — 終了待ちなし · 寿命管理が困難 |

**join 忘れ** → デストラクタで `std::terminate`。

---

## 2. RAII スレッド（JoiningThread パターン）

```cpp
class JoiningThread {
public:
    template<typename F>
    explicit JoiningThread(F&& f) : t_{std::forward<F>(f)} {}
    ~JoiningThread() { if (t_.joinable()) t_.join(); }
    JoiningThread(const JoiningThread&) = delete;
    JoiningThread(JoiningThread&& other) noexcept : t_{std::move(other.t_)} {}
private:
    std::thread t_;
};
```

スコープ終了時に自動 join — 例外経路でも安全（CP.25）。

---

## 3. ミューテックス

```cpp
#include <mutex>

std::mutex m;
int counter = 0;

void increment() {
    std::lock_guard lock(m);  // C++17 CTAD
    ++counter;
}
```

| 型 | 用途 |
|----|------|
| `std::mutex` | 基本ロック |
| `std::recursive_mutex` | 同一スレッドから再入可 |
| `std::shared_mutex` | 読み書きロック（C++17） |
| `std::lock_guard` | RAII ロック（スコープ） |
| `std::unique_lock` | 手動 unlock · `condition_variable` 用 |
| `std::scoped_lock` | 複数 mutex をデッドロック回避（C++17） |

**データ競合**: 2 スレッドが同期なしに同じメモリへ一方が書き込む — UB。

---

## 4. 条件変数

```cpp
#include <condition_variable>

std::mutex m;
std::condition_variable cv;
bool ready = false;

void producer() {
    {
        std::lock_guard lock(m);
        ready = true;
    }
    cv.notify_one();
}

void consumer() {
    std::unique_lock lock(m);
    cv.wait(lock, []{ return ready; });
    // ready == true が保証される
}
```

`wait` は **spurious wakeup** あり — 述語付き `wait` を使う。

---

## 5. async と future

```cpp
#include <future>

auto fut = std::async(std::launch::async, []{
    return compute();
});
int result = fut.get();  // ブロックして結果取得
```

| 起動ポリシー | 動作 |
|--------------|------|
| `std::launch::async` | 新スレッド |
| `std::launch::deferred` | `get()` 時に同期実行 |

`std::promise` / `std::shared_future` で値を明示的に設定可能。

---

## 6. アトミック

```cpp
#include <atomic>

std::atomic<int> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);
```

ロックフリーな単一変数の読み書き。`memory_order` で同期の強さを制御。

---

## 7. 設計指針

| 指針 | 内容 |
|------|------|
| 共有データ最小化 | スレッドごとにローカルデータ |
| mutex とデータをセット | 生の共有変数を散らさない |
| デッドロック回避 | ロック順序の固定 · `scoped_lock` |
| detach 禁止 | join または RAII |
| 高レベル API | `async` · 並行アルゴリズム（C++17 `std::execution::par`） |

---

## 8. CMake でのスレッドリンク

```cmake
find_package(Threads REQUIRED)
target_link_libraries(app PRIVATE Threads::Threads)
```

MinGW では `-pthread` が付与される。
