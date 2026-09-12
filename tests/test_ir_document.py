"""`document` 型（ir-type-vocabulary.md §2.8）: schema.json の宣言・content の検証・エスケープ・
テンプレートに渡す形。材料は `packages/club-meeting-log/examples/`（issue #30）。"""

from __future__ import annotations

import copy
from typing import Any

import pytest
from pydantic import ValidationError

from entex.errors import EnvelopeError, IRValidationError
from entex.ir.loader import load_and_validate
from entex.ir.schema import FieldDef, Schema
from entex.ir.validate import validate_content
from entex.packages import load_package
from entex.renderer import build_context, shape_documents
from entex.tex.escape import escape_content, escape_href
from tests.conftest import CLUB_LOG_EXAMPLES_DIR, PACKAGES_DIR, load_club_log_example

VALID_NAMES = sorted(p.name for p in (CLUB_LOG_EXAMPLES_DIR / "valid").glob("*.json"))
INVALID_NAMES = sorted(p.name for p in (CLUB_LOG_EXAMPLES_DIR / "invalid").glob("*.json"))


def _document_field(**overrides: Any) -> dict[str, Any]:
    fdef: dict[str, Any] = {
        "type": "document",
        "label": "本文",
        "sections": [
            {"key": "a", "heading": "A", "required": False},
            {"key": "b", "heading": "B", "required": False},
        ],
        "blocks": ["heading", "paragraph", "list", "quote", "code", "image"],
    }
    fdef.update(overrides)
    return fdef


def _schema(**overrides: Any) -> Schema:
    return Schema.model_validate(
        {
            "doc_type": "t-doc",
            "schema_version": 1,
            "title": "T",
            "fields": {"body": _document_field(**overrides)},
        }
    )


def _issues(content: dict[str, Any], schema: Schema) -> list[str]:
    _, issues = validate_content(content, schema)
    return [i.message for i in issues]


def _para(text: str) -> dict[str, Any]:
    return {"type": "paragraph", "spans": [{"text": text}]}


# --- schema.json 側（パッケージ作者の誤り） ------------------------------------------------


def test_club_meeting_log_package_loads() -> None:
    pkg = load_package(PACKAGES_DIR, "club-meeting-log")
    body = pkg.schema.fields["body"]
    assert body.type == "document"
    assert body.section_keys == ["activity_report", "announcement", "next_notice"]
    assert body.extra_sections == "allow"
    assert body.max_heading_level == 2
    assert pkg.schema.fields["meeting_date"].source == {"notion_property": "開催日"}


def test_document_defaults() -> None:
    fdef = FieldDef.model_validate(_document_field())
    assert fdef.extra_sections == "forbid"
    assert fdef.max_heading_level == 2
    assert fdef.sections is not None and fdef.sections[0].required is False
    assert fdef.source is None


def test_source_is_allowed_on_any_field() -> None:
    fdef = FieldDef.model_validate({"type": "date", "label": "d", "source": {"x": "y"}})
    assert fdef.source == {"x": "y"}


@pytest.mark.parametrize(
    ("fdef", "match"),
    [
        ({"type": "document", "label": "b", "blocks": ["paragraph"]}, "sections"),
        (_document_field(sections=[]), "sections"),
        (_document_field(blocks=None), "blocks"),
        (_document_field(blocks=[]), "blocks"),
        (_document_field(blocks=["paragraph", "table"]), "table"),
        (_document_field(blocks=["paragraph", "paragraph"]), "2 回"),
        (
            _document_field(sections=[{"key": "a", "heading": "A"}, {"key": "a", "heading": "B"}]),
            "重複",
        ),
        (_document_field(sections=[{"key": "Bad-Key", "heading": "A"}]), "pattern"),
        (_document_field(sections=[{"key": "a", "heading": "A", "extra": 1}]), "extra"),
        (_document_field(extra_sections="maybe"), "extra_sections"),
        (_document_field(max_heading_level=0), "max_heading_level"),
        ({"type": "text", "label": "t", "sections": [{"key": "a", "heading": "A"}]}, "document"),
        ({"type": "text", "label": "t", "blocks": ["paragraph"]}, "document"),
        ({"type": "text", "label": "t", "extra_sections": "allow"}, "document"),
        ({"type": "text", "label": "t", "max_heading_level": 3}, "document"),
        ({"type": "text", "label": "t", "source": {}}, "source"),
        (_document_field(default="x"), "default"),
        (_document_field(required=False, derived=True, expr={"count": "x"}), "integer"),
    ],
)
def test_document_schema_shape_is_checked(fdef: dict[str, Any], match: str) -> None:
    with pytest.raises(ValidationError, match=match):
        FieldDef.model_validate(fdef)


def test_document_cannot_nest_inside_object_or_row_list() -> None:
    for outer in ("object", "row_list"):
        with pytest.raises(ValidationError):
            FieldDef.model_validate(
                {"type": outer, "label": "o", "fields": {"d": _document_field()}}
            )


# --- content 側: examples/ を全件 ----------------------------------------------------------


@pytest.mark.parametrize("name", VALID_NAMES)
def test_valid_examples_pass(name: str) -> None:
    ir = load_and_validate(load_club_log_example(f"valid/{name}"), PACKAGES_DIR)
    assert ir.doc_type == "club-meeting-log"
    body = ir.content["body"]
    assert set(body) == {"sections", "extra_sections"}
    # 節のキーの並びはスキーマの宣言順に揃う
    order = ir.package.schema.fields["body"].section_keys
    assert list(body["sections"]) == [k for k in order if k in body["sections"]]


@pytest.mark.parametrize(
    ("name", "error", "match"),
    [
        ("01-unknown-section-key.json", IRValidationError, "free_talk"),
        ("02-unknown-block-type.json", IRValidationError, "'table'"),
        ("03-heading-too-deep.json", IRValidationError, "1から2まで"),
        ("04-missing-meeting-date.json", IRValidationError, "開催日は必須"),
        ("05-envelope-mismatch.json", EnvelopeError, "schema_version"),
        ("06-list-nested-too-deep.json", IRValidationError, "3段まで"),
    ],
)
def test_invalid_examples_are_rejected(name: str, error: type[Exception], match: str) -> None:
    assert name in INVALID_NAMES
    with pytest.raises(error, match=match):
        load_and_validate(load_club_log_example(f"invalid/{name}"), PACKAGES_DIR)


def test_unknown_section_hint_points_to_extra_sections() -> None:
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(
            load_club_log_example("invalid/01-unknown-section-key.json"), PACKAGES_DIR
        )
    assert len(ei.value.issues) == 1
    assert ei.value.issues[0].path == "body.sections.free_talk"
    assert "extra_sections" in ei.value.issues[0].message


def test_error_messages_use_labels_not_tex() -> None:
    with pytest.raises(IRValidationError) as ei:
        load_and_validate(load_club_log_example("invalid/03-heading-too-deep.json"), PACKAGES_DIR)
    msg = ei.value.user_message
    assert "本文のアナウンス" in msg
    assert "\\" not in msg and "tex" not in msg.lower()


# --- content 側: 個別の規則 ------------------------------------------------------------------


def test_forbid_rejects_extra_sections_but_allows_empty_list() -> None:
    schema = _schema(extra_sections="forbid")
    body = {"sections": {"a": {"blocks": [_para("x")]}}, "extra_sections": []}
    assert _issues({"body": body}, schema) == []
    body["extra_sections"] = [{"heading": "臨時", "blocks": [_para("y")]}]
    msgs = _issues({"body": body}, schema)
    assert len(msgs) == 1 and "宣言外の節" in msgs[0]


def test_extra_sections_key_may_be_omitted() -> None:
    normalized, issues = validate_content(
        {"body": {"sections": {"a": {"blocks": [_para("x")]}}}}, _schema()
    )
    assert issues == []
    assert normalized["body"]["extra_sections"] == []


def test_required_section_is_enforced() -> None:
    schema = _schema(sections=[{"key": "a", "heading": "議題"}, {"key": "b", "heading": "B"}])
    msgs = _issues({"body": {"sections": {"b": {"blocks": [_para("x")]}}}}, schema)
    assert msgs == ["本文の議題は必須です"]


def test_empty_or_null_section_must_be_omitted() -> None:
    schema = _schema()
    msgs = _issues({"body": {"sections": {"a": {"blocks": []}}}}, schema)
    assert msgs == ["本文のAが空です。節ごと省いてください"]
    msgs = _issues({"body": {"sections": {"a": None}}}, schema)
    assert len(msgs) == 1 and "null" in msgs[0]


def test_undeclared_block_type_is_rejected_even_if_in_vocabulary() -> None:
    schema = _schema(blocks=["paragraph"])
    body = {"sections": {"a": {"blocks": [{"type": "heading", "level": 1, "text": "h"}]}}}
    msgs = _issues({"body": body}, schema)
    assert len(msgs) == 1 and "paragraph のいずれか" in msgs[0]


@pytest.mark.parametrize("level", [0, -1, 3, None, "1", 1.5])
def test_heading_level_is_bounded(level: Any) -> None:
    body = {"sections": {"a": {"blocks": [{"type": "heading", "level": level, "text": "h"}]}}}
    msgs = _issues({"body": body}, _schema(max_heading_level=2))
    assert len(msgs) == 1 and "level" in msgs[0]


def test_heading_level_upper_bound_follows_schema() -> None:
    body = {"sections": {"a": {"blocks": [{"type": "heading", "level": 3, "text": "h"}]}}}
    assert _issues({"body": body}, _schema(max_heading_level=3)) == []


def test_list_nesting_limit_is_three() -> None:
    def nested(depth: int) -> dict[str, Any]:
        item: dict[str, Any] = {"spans": [{"text": f"{depth}"}]}
        if depth > 1:
            item["items"] = [nested(depth - 1)]
        return item

    def body(depth: int) -> dict[str, Any]:
        return {"sections": {"a": {"blocks": [{"type": "list", "items": [nested(depth)]}]}}}

    assert _issues({"body": body(3)}, _schema()) == []
    msgs = _issues({"body": body(4)}, _schema())
    assert len(msgs) == 1 and "3段まで" in msgs[0]


def test_code_text_keeps_newlines_and_is_not_normalized() -> None:
    raw = "a\n  b\t\\n %"
    body = {"sections": {"a": {"blocks": [{"type": "code", "text": raw, "lang": "sh"}]}}}
    normalized, issues = validate_content({"body": body}, _schema())
    assert issues == []
    assert normalized["body"]["sections"]["a"]["blocks"][0] == {
        "type": "code",
        "text": raw,
        "lang": "sh",
    }


def test_span_text_follows_text_rules() -> None:
    body = {"sections": {"a": {"blocks": [_para("1行目\n2行目")]}}}
    msgs = _issues({"body": body}, _schema())
    assert msgs == ["本文のAの1番目のブロックの1番目の文は1行で入力してください"]


@pytest.mark.parametrize(
    ("block", "match"),
    [
        ({"type": "paragraph", "spans": "x"}, "spans は配列"),
        ({"type": "paragraph", "spans": [{"href": "https://e.com"}]}, "text は文字列"),
        ({"type": "paragraph", "spans": [{"text": "x", "href": ""}]}, "href"),
        ({"type": "paragraph", "spans": [{"text": "x", "bold": True}]}, "bold"),
        ({"type": "paragraph", "spans": [{"text": "x"}], "extra": 1}, "extra"),
        ({"type": "list", "items": [{"text": "x"}]}, "text"),
        ({"type": "list", "items": [{"spans": [{"text": "x"}], "level": 1}]}, "level"),
        ({"type": "image"}, "src"),
        ({"type": "image", "src": "a b.png"}, "使えない文字"),
        ({"type": "image", "src": "../x.png"}, "使えない文字"),
        ({"type": "image", "src": "a{b}.png"}, "使えない文字"),
        ({"type": "image", "src": "/etc/x.png"}, "使えない文字"),
        ({"type": "image", "src": "x.png", "alt": 1}, "alt"),
        ({"type": "code"}, "text は文字列"),
        ({"type": "code", "text": "x", "lang": 1}, "lang"),
        ({"type": "heading", "level": 1}, "text は文字列"),
        ("not a block", "オブジェクト"),
    ],
)
def test_block_shape_is_checked(block: Any, match: str) -> None:
    body = {"sections": {"a": {"blocks": [block]}}}
    msgs = _issues({"body": body}, _schema())
    assert msgs, block
    assert any(match in m for m in msgs), msgs


@pytest.mark.parametrize("src", ["47-01.png", "a_b.png", "img/2026-07/x.jpg", "x"])
def test_image_src_accepts_plain_filenames(src: str) -> None:
    body = {"sections": {"a": {"blocks": [{"type": "image", "src": src}]}}}
    assert _issues({"body": body}, _schema()) == []


def test_extra_section_needs_a_heading_and_blocks() -> None:
    schema = _schema(extra_sections="allow")
    body = {"sections": {}, "extra_sections": [{"blocks": [_para("x")]}]}
    msgs = _issues({"body": body}, schema)
    assert msgs == ["本文の1番目の臨時の節には見出し（heading）が必要です"]
    body = {"sections": {}, "extra_sections": [{"heading": "h", "blocks": [], "note": 1}]}
    msgs = _issues({"body": body}, schema)
    assert any("'note'" in m for m in msgs) and any("空です" in m for m in msgs)


def test_document_shape_errors_are_collected_together() -> None:
    body = {
        "sections": {"a": {"blocks": [_para("x")]}, "zzz": {"blocks": []}},
        "extra_sections": "no",
        "junk": 1,
    }
    msgs = _issues({"body": body}, _schema())
    assert len(msgs) == 3
    assert any("'zzz'" in m for m in msgs)
    assert any("extra_sections は配列" in m for m in msgs)
    assert any("'junk'" in m for m in msgs)


def test_document_type_mismatch_uses_type_word() -> None:
    assert _issues({"body": "text"}, _schema()) == [
        '本文はオブジェクト（{ "sections": { ... } }）で入力してください'
    ]


# --- エスケープ -------------------------------------------------------------------------------


def _escaped_body(name: str) -> dict[str, Any]:
    ir = load_and_validate(load_club_log_example(f"valid/{name}"), PACKAGES_DIR)
    return escape_content(ir.content, ir.package.schema)["body"]


def test_spans_and_headings_are_escaped_but_code_is_not() -> None:
    blocks = _escaped_body("05-tex-special-chars.json")["sections"]["announcement"]["blocks"]
    assert blocks[0]["text"] == r"予算 \& 会計（100\% 確定）"
    spans = blocks[1]["spans"]
    assert spans[0]["text"] == r"集計用の式は \#\{total\} \textasciitilde{} \$amount で、"
    assert spans[1]["text"] == r"詳細は \textless{}共有シート\textgreater{}"
    assert spans[2]["text"] == r" の C\_1 列にあります。"
    items = [i["spans"][0]["text"] for i in blocks[2]["items"]]
    assert items[0] == r"バックスラッシュ \textbackslash{} とチルダ \textasciitilde{} を含む名前"
    assert items[2] == (
        r"引用符 \textquotesingle{} \textquotedbl{} \textasciigrave{} "
        r"とパイプ \textbar{} を含む名前"
    )
    # code は書かれたとおり
    assert blocks[3]["text"] == "# ここはエスケープしない\nprintf '%s\\n' \"${HOME}\" | tr a-z A-Z"


def test_href_keeps_url_meaning() -> None:
    spans = _escaped_body("05-tex-special-chars.json")["sections"]["announcement"]["blocks"][1][
        "spans"
    ]
    assert spans[1]["href"] == r"https://example.com/sheet?a=1\&b=2"


def test_escape_href_rules() -> None:
    # URL の区切りは `\` を前置して意味を保つ（hyperref が元の文字に戻す）
    assert escape_href("https://e.com/p?a=1&b=2#frag") == r"https://e.com/p?a=1\&b=2\#frag"
    assert escape_href("https://e.com/x%20y") == r"https://e.com/x\%20y"
    # unreserved はパーセントエンコードしても同じ URL
    assert escape_href("https://e.com/~u/my_file") == r"https://e.com/\%7Eu/my\%5Ffile"
    out = escape_href("https://e.com/{}\\^<>'\"`| あ")
    assert out == (r"https://e.com/\%7B\%7D\%5C\%5E\%3C\%3E\%27\%22\%60\%7C\%20\%E3\%81\%82")
    # `\` は `\%` の一部としてしか現れない
    assert out.count("\\") == out.count(r"\%")
    assert escape_href("https://example.com/a/b") == "https://example.com/a/b"


def test_extra_section_heading_and_nested_items_are_escaped() -> None:
    ir = load_and_validate(load_club_log_example("valid/03-extra-sections.json"), PACKAGES_DIR)
    content = copy.deepcopy(ir.content)
    content["body"]["extra_sections"][0]["heading"] = "部費 & 会計"
    content["body"]["sections"]["announcement"]["blocks"][0]["items"][0]["items"] = [
        {"spans": [{"text": "50%"}]}
    ]
    body = escape_content(content, ir.package.schema)["body"]
    assert body["extra_sections"][0]["heading"] == r"部費 \& 会計"
    nested = body["sections"]["announcement"]["blocks"][0]["items"][0]["items"][0]
    assert nested["spans"][0]["text"] == r"50\%"
    # 元の dict は変更されない
    assert content["body"]["extra_sections"][0]["heading"] == "部費 & 会計"


def test_image_src_and_alt_are_escaped() -> None:
    blocks = _escaped_body("06-with-images.json")["sections"]["activity_report"]["blocks"]
    assert blocks[2] == {"type": "image", "src": "47-01.png", "alt": "会場の様子"}
    assert blocks[3]["alt"] == "発表スライド"


# --- テンプレートに渡す形（節の並べ替え） ---------------------------------------------------------


def test_sections_are_ordered_by_schema_then_extras_in_input_order() -> None:
    ir = load_and_validate(load_club_log_example("valid/03-extra-sections.json"), PACKAGES_DIR)
    shaped = shape_documents(ir.content, ir.package.schema)["body"]
    assert list(shaped) == ["sections"]
    headings = [s["heading"] for s in shaped["sections"]]
    assert headings == ["活動報告", "アナウンス", "次回予告", "成果物発表会", "部費回収"]
    assert [s.get("key") for s in shaped["sections"]] == [
        "activity_report",
        "announcement",
        "next_notice",
        None,
        None,
    ]
    # 無い節は blocks が空の要素として渡る（落とすかはテンプレートの判断）
    assert shaped["sections"][0]["blocks"] == []
    assert shaped["sections"][1]["blocks"] and shaped["sections"][3]["blocks"]
    # IR のキーの並びは見ない
    reordered = copy.deepcopy(ir.content)
    reordered["body"]["sections"] = dict(reversed(list(reordered["body"]["sections"].items())))
    assert shape_documents(reordered, ir.package.schema)["body"] == shaped


def test_build_context_exposes_sections_as_namespaces() -> None:
    ir = load_and_validate(load_club_log_example("valid/01-typical.json"), PACKAGES_DIR)
    ctx = build_context(ir.content, ir.package.schema)
    sections = ctx["doc"].body.sections
    assert [s.key for s in sections] == ["activity_report", "announcement", "next_notice"]
    link = sections[0].blocks[1].spans[1]
    assert link.text == "公開ページ" and link.href == "https://example.com/projects/1234"
    assert not hasattr(sections[0].blocks[1].spans[0], "href")
    # `items` が dict のメソッドに化けない（入れ子の箇条書き）
    first_item = sections[1].blocks[2].items[0]
    assert first_item.spans[0].text == "受付" and len(first_item.items) == 2
    # schema 側にも節の宣言が出る
    assert [s.key for s in ctx["schema"].fields.body.sections] == [
        "activity_report",
        "announcement",
        "next_notice",
    ]
    assert ctx["schema"].fields.body.sections[0].heading == "活動報告"


def test_shape_documents_leaves_other_fields_alone() -> None:
    ir = load_and_validate(load_club_log_example("valid/02-minimal.json"), PACKAGES_DIR)
    shaped = shape_documents(ir.content, ir.package.schema)
    assert shaped["meeting_date"] == "2024-04-24"
    assert "session_no_total" not in shaped
    assert ir.content["body"]["sections"]  # 元は dict のまま
