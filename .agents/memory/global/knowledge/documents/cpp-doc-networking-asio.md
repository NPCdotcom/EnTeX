---
cpp_doc_id: cpp.topic.networking
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [asio, tcp, sockets]
cpp_doc_regex_file: ^cpp-doc-networking\-asio\.md$
---

<!-- CPP_DOC_ID: cpp.topic.networking -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ ネットワークプログラミング（Boost.Asio）

**出典**: Boost.Asio ドキュメント · POSIX/Berkeley ソケットモデル

---

## 1. ネットワークの基本概念

| 用語 | 意味 |
|------|------|
| **IP アドレス** | ホストの論理アドレス（IPv4: 32bit · IPv6: 128bit） |
| **ポート** | ホスト内の通信エンドポイント（0–65535） |
| **ソケット** | ネットワーク通信の OS 抽象 |
| **TCP** | 接続型 · 信頼性 · 順序保証 |
| **UDP** | 非接続 · 高速 · 信頼性なし |

```text
クライアント                    サーバ
  socket()                       socket()
  connect(ip, port)    ←→    bind(port)
                              listen()
  send/recv            ←→    accept() → 新ソケット
                              send/recv
  close()                      close()
```

---

## 2. Boost.Asio の骨格

```cpp
#include <boost/asio.hpp>
namespace net = boost::asio;

net::io_context io;
net::ip::tcp::socket socket(io);
```

| 型 | 役割 |
|----|------|
| `io_context` | 非同期 I/O のイベントループ |
| `ip::tcp::socket` | TCP ソケット |
| `ip::tcp::acceptor` | 接続受付 |
| `ip::tcp::resolver` | ホスト名解決 |
| `streambuf` / `buffer` | 読み書きバッファ |

---

## 3. TCP エコーサーバ（同期）

```cpp
net::io_context io;
net::ip::tcp::acceptor acceptor(io, {net::ip::tcp::v4(), 8080});

for (;;) {
    net::ip::tcp::socket socket(io);
    acceptor.accept(socket);
    char buf[1024];
    std::size_t n = socket.read_some(net::buffer(buf));
    net::write(socket, net::buffer(buf, n));  // echo
}
```

---

## 4. TCP クライアント

```cpp
net::io_context io;
net::ip::tcp::resolver resolver(io);
auto endpoints = resolver.resolve("127.0.0.1", "8080");

net::ip::tcp::socket socket(io);
net::connect(socket, endpoints);
net::write(socket, net::buffer("hello"));
```

---

## 5. 非同期モデル

```cpp
void on_read(const boost::system::error_code& ec, std::size_t n) {
    if (!ec) { /* 処理 */ }
}

socket.async_read_some(net::buffer(buf), on_read);
io.run();  // イベントループ
```

| パターン | 説明 |
|----------|------|
| 同期 | ブロック — シンプル |
| 非同期 | コールバック / coroutine（C++20） |
| `io_context::run()` | 完了ハンドラをディスパッチ |

---

## 6. エラー処理

Asio は **エラーコード** モデル（例外を投げない API が多い）:

```cpp
boost::system::error_code ec;
socket.read_some(net::buffer(buf), ec);
if (ec) { /* エラー処理 */ }
```

---

## 7. プロトコル設計の要点

| 項目 | 推奨 |
|------|------|
| メッセージ境界 | 長さプレフィックス or 区切り文字 |
| バイト順 | ネットワークバイトオーダ（big-endian） |
| 部分読み | `read_some` は全バイトを保証しない — ループ |
| 接続切断 | `error::eof` を処理 |
| タイムアウト | `deadline_timer` 等 |

---

## 8. ビルド

```cmake
find_package(Boost REQUIRED COMPONENTS system)
target_link_libraries(app PRIVATE Boost::system)
```

vcpkg: `"dependencies": ["boost-asio"]`
