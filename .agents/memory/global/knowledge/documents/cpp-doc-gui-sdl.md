---
cpp_doc_id: cpp.topic.gui_sdl
cpp_doc_topic: cpp
cpp_doc_kind: topic
cpp_doc_tags: [sdl, gui, window]
cpp_doc_regex_file: ^cpp-doc-gui\-sdl\.md$
---

<!-- CPP_DOC_ID: cpp.topic.gui_sdl -->
<!-- CPP_DOC_KIND: topic -->
<!-- CPP_DOC_TOPIC: cpp -->

# C++ GUI プログラミング（SDL2）

**出典**: SDL2 公式ドキュメント

---

## 1. SDL2 とは

**Simple DirectMedia Layer** — クロスプラットフォームのマルチメディア・ウィンドウ・入力ライブラリ。OpenGL/Vulkan サーフェス作成にも使用。

---

## 2. 初期化とウィンドウ

```cpp
#include <SDL.h>

int main() {
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* window = SDL_CreateWindow(
        "App", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        800, 600, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    bool running = true;
    while (running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT) running = false;
        }
        SDL_SetRenderDrawColor(renderer, 30, 30, 40, 255);
        SDL_RenderClear(renderer);
        // 描画 ...
        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}
```

---

## 3. イベントループ

| イベント | 意味 |
|----------|------|
| `SDL_QUIT` | ウィンドウ閉じる |
| `SDL_KEYDOWN` / `SDL_KEYUP` | キー入力 |
| `SDL_MOUSEBUTTONDOWN` | マウスクリック |
| `SDL_WINDOWEVENT` | リサイズ等 |

`SDL_PollEvent` は非ブロック — 毎フレームキューを空にする。

---

## 4. 2D 描画

```cpp
SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
SDL_Rect rect{100, 100, 200, 150};
SDL_RenderFillRect(renderer, &rect);
SDL_RenderDrawLine(renderer, 0, 0, 800, 600);
```

テクスチャ:

```cpp
SDL_Surface* surface = SDL_LoadBMP("sprite.bmp");
SDL_Texture* tex = SDL_CreateTextureFromSurface(renderer, surface);
SDL_RenderCopy(renderer, tex, nullptr, &dest_rect);
```

---

## 5. 時間管理

```cpp
Uint32 last = SDL_GetTicks();
// フレーム内
Uint32 now = SDL_GetTicks();
float dt = (now - last) / 1000.0f;
last = now;
```

`SDL_GetPerformanceCounter()` で高精度タイマーも可。

---

## 6. CMake 連携

```cmake
find_package(SDL2 CONFIG REQUIRED)
target_link_libraries(app PRIVATE SDL2::SDL2 SDL2::SDL2main)
```

---

## 7. 設計パターン

| パターン | 内容 |
|----------|------|
| ゲームループ | input → update → render |
| 固定タイムステップ | 物理 `dt` 固定 · 描画は補間 |
| 状態マシン | メニュー / ゲーム / ポーズ |
| RAII ラッパ | `SDL_Window*` を unique_ptr + deleter で管理 |

```cpp
struct SDL_Deleter {
    void operator()(SDL_Window* w) const { SDL_DestroyWindow(w); }
};
using WindowPtr = std::unique_ptr<SDL_Window, SDL_Deleter>;
```

---

## 8. Vulkan / OpenGL との接続

```cpp
SDL_Window* window = SDL_CreateWindow(..., SDL_WINDOW_VULKAN);
// または SDL_WINDOW_OPENGL
```

SDL はウィンドウとイベントのみ担当 — 描画 API は Vulkan / OpenGL / Metal 等が担当。
