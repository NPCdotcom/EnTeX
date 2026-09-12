"""利用者向けメッセージを持つ例外の階層。

renderer.md「エラー分類と FR7 の写像方針」に対応する。どの層（CLI・将来の API）でも
`EnTeXError.user_message` をそのまま利用者へ返してよい。TeX のログや Python の
トレースバックをこの属性に入れてはならない（charter §4）。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class EnTeXError(Exception):
    """すべての利用者向けエラーの基底。`user_message` は日本語の完成文。"""

    def __init__(self, user_message: str) -> None:
        super().__init__(user_message)
        self.user_message = user_message


class PackageError(EnTeXError):
    """doc-package（`packages/<slug>/`）が見つからない、または壊れている。

    利用者ではなくテンプレート作者・管理者向けの問題だが、メッセージは同じ規約で日本語にする。
    """


class EnvelopeError(EnTeXError):
    """封筒（`doc_type` / `schema_version`）が期待と一致しない（FR1）。"""


@dataclass(frozen=True, slots=True)
class FieldIssue:
    """`content` の検証で見つかった 1 件の問題。

    `path` は機械向け（`finance[1].amount`）、`message` は利用者向けの完成文で
    フィールドの `label` を含む。
    """

    path: str
    message: str


class IRValidationError(EnTeXError):
    """`content` の型・属性違反。見つかった分をまとめて持つ（FR2）。"""

    def __init__(self, issues: list[FieldIssue]) -> None:
        if not issues:
            raise ValueError("IRValidationError には 1 件以上の issue が必要")
        self.issues = list(issues)
        lines = [f"入力に{len(self.issues)}件の問題があります。"]
        lines.extend(f"- {issue.message}" for issue in self.issues)
        super().__init__("\n".join(lines))


class DerivationError(EnTeXError):
    """導出値の計算に失敗した。schema.json の `expr` の誤り（パッケージ作者向け）。"""


class RenderError(EnTeXError):
    """`.tex` の組み立て、または latexmk が失敗した（FR7）。

    `log_path` はサーバ側にだけ残す生ログの場所、`detail` は運用者向けの短い原因メモ。
    どちらも利用者向けメッセージには含めない。
    """

    GENERIC_MESSAGE = (
        "PDFの生成に失敗しました。入力内容をご確認のうえ、"
        "解決しない場合は管理者へお問い合わせください。"
    )

    def __init__(
        self,
        user_message: str | None = None,
        *,
        log_path: Path | None = None,
        detail: str | None = None,
    ) -> None:
        super().__init__(user_message or self.GENERIC_MESSAGE)
        self.log_path = log_path
        self.detail = detail


class RenderTimeoutError(RenderError):
    """latexmk が制限時間内に終わらなかった。

    組版失敗（`RenderError`）の一種として扱えるが、利用者には「やり直せば通るかもしれない」
    と伝えたいので文言と API の `type` を分ける（api.md §9）。
    """

    GENERIC_MESSAGE = (
        "PDFの生成が時間内に終わりませんでした。しばらくしてからやり直してください。"
        "繰り返し起きる場合は管理者へお問い合わせください。"
    )
