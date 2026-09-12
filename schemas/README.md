# Schemas

共有スキーマ置き場。

| パス | 内容 |
|------|------|
| `ir/envelope.schema.json` | IR の封筒（`doc_type` / `schema_version` / `content`）。正本は `src/entex/ir/loader.py` の `Envelope`（pydantic）で、`python -m entex.ir.loader` で再生成する。ズレはテストで検知する |
| `api/`（予定） | API の入出力（着手順 2 で OpenAPI を生成して置く） |

文書種ごとの `content` の形は `packages/<slug>/schema.json` 側にあり、その読み手は `src/entex/ir/schema.py`。

IR は「見た目を含まない中身」だけを表す（charter §10）。体裁の情報はここに入れない。

IR で使える型の語彙（`text` / `month` / `money` / `row_list` など）は [docs/design/elements/ir-type-vocabulary.md](../docs/design/elements/ir-type-vocabulary.md) で決める。`ir/` に置くファイルはその語彙から生成する。
