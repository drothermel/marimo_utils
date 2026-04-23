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


def auto_render(obj: object) -> object:
    """Call `.render()` if present; otherwise pass through.

    Mohtml concatenates children via `__str__`, so `mo.Html` / `ActiveHtml` /
    raw strings all work as-is once rendered.
    """
    render_fn = getattr(obj, "render", None)
    if callable(render_fn):
        return render_fn()
    return obj


__all__ = ["HtmlRenderable", "auto_render", "html_block"]
