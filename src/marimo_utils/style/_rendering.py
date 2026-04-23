from __future__ import annotations

import marimo as mo

from marimo_utils.style.protocols import HtmlRenderable


def html_block(fragment: HtmlRenderable) -> mo.Html:
    return mo.Html(str(fragment))


def rem_to_float(value: str) -> float:
    normalized = value.strip()
    if normalized.endswith("rem"):
        normalized = normalized.removesuffix("rem")
    return float(normalized)


__all__ = ["html_block", "rem_to_float"]
