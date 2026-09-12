# Schemas

共有スキーマ置き場。

| パス | 内容 |
|------|------|
| `ir/envelope.schema.json` | IR の封筒（`doc_type` / `schema_version` / `content`）。正本は `src/entex/ir/loader.py` の `Envelope`（pydantic）で、`python -m entex.ir.loader` で再生成する。ズレはテストで検知する |
| `api/problem.schema.json` | API の失敗応答（RFC 9457 Problem Details + 拡張 `issues`）。正本は `src/entex/api/problems.py` の `Problem`（pydantic）。`python -m entex.api.app` で再生成。ズレは `tests/test_api.py` で検知 |
| `api/openapi.json` | API 全体の OpenAPI 3.1（`/v1/render` `/v1/health` `/v1/doc-types*`）。正本は FastAPI アプリ（`src/entex/api/app.py`）。同じコマンドで再生成、同じテストで検知。設計: [docs/design/programs/api.md](../docs/design/programs/api.md) §3 |

まとめて再生成するときは `make schemas`。

文書種ごとの `content` の形は `packages/<slug>/schema.json` 側にあり、その読み手は `src/entex/ir/schema.py`。

IR は「見た目を含まない中身」だけを表す（charter §10）。体裁の情報はここに入れない。

IR で使える型の語彙（`text` / `month` / `money` / `row_list` など）は [docs/design/elements/ir-type-vocabulary.md](../docs/design/elements/ir-type-vocabulary.md) で決める。`ir/` に置くファイルはその語彙から生成する。
