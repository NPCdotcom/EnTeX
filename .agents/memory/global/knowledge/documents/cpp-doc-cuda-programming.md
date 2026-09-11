---
cpp_doc_id: cpp.topic.cuda
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [gpu, cuda, kernels]
cpp_doc_regex_file: ^cpp-doc-cuda\-programming\.md$
---

<!-- CPP_DOC_ID: cpp.topic.cuda -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# CUDA GPU プログラミング

**出典**: NVIDIA CUDA Programming Guide

---

## 1. ヘテロジニアスモデル

```text
[ Host ]  CPU + システムメモリ（DRAM）
    │  cudaMemcpy / kernel launch / sync
    ▼
[ Device ] GPU + デバイスメモリ（global memory）
```

| 用語 | 意味 |
|------|------|
| **host** | CPU とそのメモリ |
| **device** | GPU とそのメモリ |
| **kernel** | GPU 上で実行される関数（`__global__`） |
| **kernel launch** | 多数の GPU スレッドで kernel を並列起動 |

アプリは CPU から開始。CUDA API で転送 · 起動 · 同期を行う。

---

## 2. スレッド階層

```text
Grid（1〜3 次元）
 └─ Thread Block（1〜3 次元）
      └─ Thread
           └─ Warp（32 スレッド · ハードウェア実行単位）
```

| 組み込み変数 | 意味 |
|--------------|------|
| `threadIdx` | ブロック内のスレッド ID |
| `blockIdx` | グリッド内のブロック ID |
| `blockDim` | ブロックの次元 |
| `gridDim` | グリッドの次元 |

```cpp
int i = blockIdx.x * blockDim.x + threadIdx.x;
```

**ブロックサイズ**は 32 の倍数が望ましい（warp 未使用レーン回避）。

---

## 3. 最小 kernel 例

```cpp
__global__ void add(int n, float* x, float* y) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = x[i] + y[i];
}

// host
int blockSize = 256;
int numBlocks = (n + blockSize - 1) / blockSize;
add<<<numBlocks, blockSize>>>(n, d_x, d_y);
cudaDeviceSynchronize();
```

| 修飾子 | 実行場所 | 呼び出し元 |
|--------|----------|------------|
| `__global__` | device | host から launch |
| `__device__` | device | device から |
| `__host__` | host | host から（既定） |

---

## 4. メモリ階層

| 種類 | スコープ | 速度 | 寿命 |
|------|----------|------|------|
| **Register** | スレッド | 最速 | スレッド |
| **Shared memory** | ブロック | 速い | ブロック |
| **Global memory** | 全 SM | 遅い（帯域制限） | アプリ |
| **Constant memory** | 全 SM | キャッシュ付き | アプリ |
| **L1/L2 cache** | — | 自動 | — |

```cpp
__shared__ float tile[TILE_SIZE];  // ブロック共有
```

**Coalescing**: 隣接スレッドが隣接アドレスにアクセスすると帯域効率が良い。

---

## 5. ホスト・デバイス間転送

```cpp
float *d_x;
cudaMalloc(&d_x, n * sizeof(float));
cudaMemcpy(d_x, h_x, n * sizeof(float), cudaMemcpyHostToDevice);
// kernel ...
cudaMemcpy(h_y, d_y, n * sizeof(float), cudaMemcpyDeviceToHost);
cudaFree(d_x);
```

**Unified Memory** (`cudaMallocManaged`): CPU/GPU 共有仮想アドレス — 簡便だが性能は明示転送より劣ることが多い。

---

## 6. SIMT と Warp divergence

- **Warp** = 32 スレッドが同一命令を SIMT で実行
- 分岐が warp 内で割れる → 片方マスクオフ → 利用率低下
- 対策: 分岐を warp 境界で揃える · データをソートしてから処理

---

## 7. ストリームと並列実行

```cpp
cudaStream_t stream;
cudaStreamCreate(&stream);
kernel<<<blocks, threads, 0, stream>>>(...);
cudaMemcpyAsync(..., stream);
cudaStreamSynchronize(stream);
```

複数ストリームで **転送と計算のオーバーラップ** が可能。

---

## 8. 最適化の観点

| ボトルネック | 対策 |
|--------------|------|
| メモリ帯域 | coalescing · shared memory で再利用 |
| 低利用率 | ブロック/グリッドサイズ調整 |
| 分岐 | divergence 削減 |
| 転送 | ピン留めメモリ · ストリーム · 転送削減 |
| ライブラリ | cuBLAS · cuDNN · Thrust / CCCL |

---

## 9. エラーチェック

```cpp
#define CUDA_CHECK(call) do { \
    cudaError_t err = call; \
    if (err != cudaSuccess) { /* ログ */ } \
} while(0)
```

---

## 10. CMake 例

```cmake
enable_language(CUDA)
add_executable(cuda_app main.cu)
set_property(TARGET cuda_app PROPERTY CUDA_STANDARD 17)
```
