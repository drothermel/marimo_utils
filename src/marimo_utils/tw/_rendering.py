from __future__ import annotations

from typing import Protocol, runtime_checkable

import marimo as mo
from dr_widget.inline import ActiveHtml


@runtime_checkable
class HtmlRenderable(Protocol):
    def __str__(self) -> str: ...


def html_block(fragment: HtmlRenderable) -> mo.Html | ActiveHtml:
    """Render an HTML fragment; routes through ActiveHtml when it contains scripts.

    `mo.Html` silently drops inline `<script>` tags via its react html-parser,
    so anything with scripts (Tailwind Play CDN, plotly) must go through
    `ActiveHtml`, which re-executes script nodes after mount.
    """
    html = str(fragment)
    if "<script" in html.lower():
        return ActiveHtml(html=html)
    return mo.Html(html)


__all__ = ["HtmlRenderable", "html_block"]
