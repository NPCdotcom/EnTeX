"""FR5: TeX 特殊文字のエスケープ。"""

from __future__ import annotations

from pathlib import Path

import pytest

from entex.ir.loader import load_and_validate
from entex.tex.escape import TEX_ESCAPES, escape_content, escape_text
from tests.conftest import load_example

SPECIALS = "& % $ # _ { } ~ ^ \\ < > ' \" ` |"


@pytest.mark.parametrize("ch", sorted(TEX_ESCAPES))
def test_each_special_char_is_replaced(ch: str) -> None:
    out = escape_text(f"a{ch}b")
    assert out.startswith("a") and out.endswith("b")
    assert out != f"a{ch}b"
    # 置換結果に生の特殊文字が（制御綴りの一部以外で）残らない
    body = out[1:-1]
    assert body == TEX_ESCAPES[ch]


def test_escape_is_single_pass() -> None:
    # `\` → `\textbackslash{}` の `{}` が再度 `\{\}` にならないこと
    assert escape_text("\\") == r"\textbackslash{}"
    assert escape_text("{}") == r"\{\}"
    assert escape_text("100%") == r"100\%"
    assert escape_text("R&B #2") == r"R\&B \#2"


def test_plain_and_japanese_text_pass_through() -> None:
    s = "青葉大学 軽音楽サークル（8/3–8/5、長野）2026-08"
    assert escape_text(s) == s
    assert escape_text("") == ""


def test_escape_content_touches_only_text_and_rich_text(packages_dir: Path) -> None:
    ir = load_and_validate(load_example("valid/06-tex-special-chars.json"), packages_dir)
    escaped = escape_content(ir.content, ir.package.schema)

    # text（トップ・object・row_list のセル・list<text>）
    assert escaped["organization"] == r"青葉大学 R\&B研究会 \#2"
    assert escaped["representative"]["name"] == r"O\textquotesingle{}Brien 花子"
    assert escaped["author"]["role"] == r"副代表 \& 会計"
    assert escaped["activities"][0]["title"] == r"セッション \#12（Tom \& Jerry 編）"
    assert escaped["activities"][0]["place"] == r"練習室 \textless{}B\textgreater{}"
    assert escaped["next_month_plan"] == [r"7月: 100\%出席を目標に"]

    # rich_text
    blocks = escaped["summary"]["blocks"]
    assert (
        blocks[0]["text"] == r"予算消化率は約 85\% で、目標の \$10,000 相当（円換算）を下回った。"
    )
    assert blocks[1]["items"][0] == r"曲目: 「A\_B」「C\textasciicircum{}D」「\{E\}」の3曲"
    assert (
        blocks[1]["items"][1]
        == r"備考: \textbackslash{} や \textasciitilde{} を含む文字列も崩れないこと"
    )

    # 触らないもの: enum / date / integer / money / boolean
    assert escaped["activities"][0]["category"] == "regular"
    assert escaped["activities"][0]["date"] == "2026-06-14"
    assert escaped["finance"][0]["amount"] == 1250
    assert escaped["audited"] is False

    # 元の dict は変更されない
    assert ir.content["organization"] == "青葉大学 R&B研究会 #2"
