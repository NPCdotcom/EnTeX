# Schemas

共有スキーマ置き場。

| パス | 内容 |
|------|------|
| `ir/envelope.schema.json` | IR の封筒（`doc_type` / `schema_version` / `content`）。JSON Schema draft 2020-12。正本は `src/entex/ir/loader.py` の `Envelope`（pydantic）で、`python -m entex.ir.loader` で再生成する。ズレはテストで検知する |
| `api/problem.schema.json` | API の失敗応答（RFC 9457 Problem Details + 拡張 `issues`）。正本は `src/entex/api/problems.py` の `Problem`（pydantic）。`python -m entex.api.app` で再生成。ズレは `tests/test_api.py` で検知 |
| `api/openapi.json` | API 全体の OpenAPI 3.1（`/v1/render` `/v1/health` `/v1/doc-types*`）。正本は FastAPI アプリ（`src/entex/api/app.py`）。同じコマンドで再生成、同じテストで検知。設計: [docs/design/programs/api.md](../docs/design/programs/api.md) §3 |

まとめて再生成するときは `make schemas`。

## 封筒はどちらを見るか

封筒は `api/openapi.json` の `components.schemas.Envelope` にも同じ内容で出る。正本がどちらも同じ pydantic モデルなのでズレはしないが、**外から参照するなら `ir/envelope.schema.json` を見る**。`$schema` と `$id` が付いていて単独で `$ref` できるのはこちらだけで、OpenAPI 側は API の入力の説明として埋め込まれているにすぎない。

`$id` はファイルの属性なのでモデルではなく生成関数（`envelope_json_schema_text()`）が足している。モデル側に置くと OpenAPI の components にも `$id` が出て `$ref` の解決を乱すためである。

## 層の違い

封筒のスキーマが見るのは **封筒だけ**である。`content` は「オブジェクトであること」しか見ず、未知のキーと導出フィールドのキーの拒否、型の検証は `packages/<slug>/schema.json` の層（`src/entex/ir/validate.py`）が行う。`schema_version` も同様で、1 以上の整数であることしか見ない。実際の版が一致するかの照合は読み込み時（`src/entex/ir/loader.py`）である。この2層の分担は [ir-type-vocabulary.md §6.1](../docs/design/elements/ir-type-vocabulary.md#61-封筒envelope-ir-がどの文書種のものかを自己申告する) が決めている。

文書種ごとの `content` の形は `packages/<slug>/schema.json` 側にあり、その読み手は `src/entex/ir/schema.py`。

IR は「見た目を含まない中身」だけを表す（charter §10）。体裁の情報はここに入れない。

IR で使える型の語彙（`text` / `month` / `money` / `row_list` など）は [docs/design/elements/ir-type-vocabulary.md](../docs/design/elements/ir-type-vocabulary.md) で決める。`ir/` に置くファイルはその語彙から生成する。
