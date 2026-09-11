---
cpp_doc_id: cpp.topic.vulkan
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [vulkan, graphics, rendering]
cpp_doc_regex_file: ^cpp-doc-vulkan\-graphics\.md$
---

<!-- CPP_DOC_ID: cpp.topic.vulkan -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# Vulkan グラフィックス API

**出典**: Khronos Vulkan Tutorial · Vulkan Specification

---

## 1. Vulkan の設計思想

旧 API（OpenGL 等）はドライバ推測が多く CPU ボトルネックが残った。Vulkan は **明示的** · **低オーバーヘッド** · **マルチスレッド対応** を目標に再設計。

| 特性 | 内容 |
|------|------|
| 明示性 | ほぼ全状態をアプリが宣言 |
| 並列 | 複数スレッドからコマンド記録 |
| シェーダ | SPIR-V バイトコード |
| 統合 | Graphics + Compute 同一 API |
| 代償 | 初期ボイラープレート多 · Validation Layers 必須（開発時） |

---

## 2. 三角形までの 8 ステップ

```text
1. Instance + PhysicalDevice 選択
2. Logical Device + Queue families
3. Window · Surface · Swapchain
4. ImageView
5. Dynamic rendering（beginRendering）
6. Graphics pipeline + ShaderModule
7. Command pool / Command buffer
8. Main loop（acquire · submit · present + sync）
```

---

## 3. 主要オブジェクト

| オブジェクト | 役割 |
|--------------|------|
| `vk::Instance` | API エントリ · 拡張列挙 |
| `vk::PhysicalDevice` | GPU ハードウェア |
| `vk::Device` | 論理デバイス |
| `vk::Queue` | コマンド実行（graphics/compute/transfer） |
| `vk::SurfaceKHR` | WSI · ウィンドウ接続 |
| `vk::SwapchainKHR` | ダブル/トリプルバッファ |
| `vk::Image` / `vk::ImageView` | GPU 画像リソース |
| `vk::Pipeline` | 描画パイプライン状態 |
| `vk::ShaderModule` | SPIR-V モジュール |
| `vk::CommandBuffer` | コマンド記録 |
| `vk::Semaphore` | GPU-GPU 同期 |
| `vk::Fence` | CPU-GPU 同期 |

---

## 4. Dynamic Rendering（Vulkan 1.3+）

| 旧方式 | Dynamic rendering |
|--------|-------------------|
| `RenderPass` + `Framebuffer` 事前作成 | `beginRendering` / `endRendering` |
| attachment 構成がパイプラインと密結合 | `RenderingInfo` で実行時指定 |

```cpp
vk::RenderingInfo renderingInfo{};
renderingInfo.renderArea = {{0, 0}, {width, height}};
renderingInfo.layerCount = 1;
renderingInfo.colorAttachmentCount = 1;
renderingInfo.pColorAttachments = &colorAttachment;
commandBuffer.beginRendering(renderingInfo);
// draw calls
commandBuffer.endRendering();
```

---

## 5. グラフィックスパイプライン

固定機能ステージ + プログラマブルシェーダ:

```text
Input Assembler → Vertex Shader → Rasterization → Fragment Shader → Output Merger
```

| 状態 | 例 |
|------|-----|
| 入力レイアウト | 頂点属性のフォーマット |
| シェーダステージ | vert + frag（+ geom 等） |
| ビューポート/シザー | 描画領域 |
| ラスタライズ | カリング · ポリゴンモード |
| 深度/ステンシル | テスト · 書き込み |
| ブレンド | アルファ合成 |
| 動的状態 | viewport, scissor, lineWidth 等 |

**パイプラインはほぼ全て事前確定** — 実行時変更は限定的（dynamic state）。

---

## 6. フレームループ

```text
acquireNextImageKHR ──► commandBuffer 記録 ──► queue.submit
       ▲                                            │
       │         semaphore / fence                  ▼
       └──────── presentKHR ◄────────────── render 完了
```

| 同期 | 用途 |
|------|------|
| Semaphore | GPU 間の順序（acquire → render → present） |
| Fence | CPU が GPU 完了を待つ |
| Pipeline barrier | リソースの可用性/レイアウト遷移 |

---

## 7. バッファとメモリ

```cpp
vk::BufferCreateInfo bufferInfo{};
bufferInfo.size = size;
bufferInfo.usage = vk::BufferUsageFlagBits::eVertexBuffer;
auto buffer = device.createBuffer(bufferInfo);

// メモリ割当
auto memReq = device.getBufferMemoryRequirements(buffer);
vk::MemoryAllocateInfo allocInfo{memReq.size, findMemoryType(...)};
auto memory = device.allocateMemory(allocInfo);
device.bindBufferMemory(buffer, memory, 0);
```

| メモリプロパティ | 用途 |
|------------------|------|
| `eDeviceLocal` | GPU 専用（頂点/テクスチャ） |
| `eHostVisible` | CPU からマップ可能（ステージング） |
| `eHostCoherent` | キャッシュフラッシュ不要 |

---

## 8. 3D 数学（最小セット）

| 概念 | 用途 |
|------|------|
| ベクトル | 位置 · 方向 |
| 行列（4×4） | 変換（model/view/projection） |
| 同次座標 | 射影変換 |
| 法線変換 | 法線行列（モデル行列の逆転置） |
| 右手/左手系 | Vulkan は Y 下向きクリップ空間等に注意 |

```text
clip_pos = projection * view * model * local_pos
```

---

## 9. Vulkan-Hpp パターン

```cpp
vk::Instance instance = vk::createInstance(createInfo);
// RAII: UniqueHandle が自動 destroy
```

`VULKAN_HPP_NO_EXCEPTIONS` で `Result` チェックスタイルも可。

---

## 10. デバッグ

**Validation Layers** を有効化:

```cpp
createInfo.enabledLayerCount = 1;
createInfo.ppEnabledLayerNames = &validationLayerName;
```

エラーメッセージが具体的 — 本番ビルドでは無効化。
