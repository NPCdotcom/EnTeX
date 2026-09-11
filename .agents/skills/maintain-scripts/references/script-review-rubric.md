# Script review rubric

正本: [`../../_SCRIPT_POLICY.md`](../../_SCRIPT_POLICY.md)

## 必須（.py）

| # | チェック | fail 例 |
|---|----------|---------|
| 1 | `argparse` または明確な `main()` | トップレベルだけのスクリプト |
| 2 | `if __name__ == "__main__"` | import 時に副作用 |
| 3 | `SKILL.md` に stem 記載 | inventory が UNDOCUMENTED |
| 4 | 終了コード 0 / 非0 意味あり | 常に 0 |
| 5 | 書込パスが skill `references/` に明記 | 任意パスへ write |

## 推奨

| # | チェック |
|---|----------|
| 6 | `--dry-run`（変更を伴う script） |
| 7 | 250 行未満 — 超えたら `env/python/lib/` |
| 8 | Windows 正本 `.py` · `.sh` はラッパー |

## 禁止パターン

- `.env` · `password=` · `api_key=` 等のハードコード
- `python -c` を生成する script
- プロジェクト `node_modules` / `.venv` への import

## hooks/（別系統）

| 項目 | 要件 |
|------|------|
| 依存 | **stdlib のみ** |
| 起動 | Cursor `.cursor/hooks.json` — `agents-run` 非経由 |
| メンテ | `maintain-scripts` では review 対象外（inventory に一覧のみ） |

## 共通化の判断

| 状況 | 行動 |
|------|------|
| 2 skill で同一 stem | 名前を分けるか lib へ |
| 正規化ハッシュ一致 | `dedupe-report` → lib 抽出案 |
| 3 回目のコピペ | 必ず lib 化を検討 |
