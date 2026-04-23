from __future__ import annotations

import marimo as mo
import plotly.graph_objects as go
import plotly.io as pio

from marimo_utils.style._active_html import ActiveHtml
from marimo_utils.style.protocols import HtmlRenderable


def html_block(fragment: HtmlRenderable) -> mo.Html | ActiveHtml:
    html = str(fragment)
    if "<script" in html.lower():
        return ActiveHtml(html=html)
    return mo.Html(html)


def rem_to_float(value: str) -> float:
    normalized = value.strip()
    if normalized.endswith("rem"):
        normalized = normalized.removesuffix("rem")
    return float(normalized)


def as_html(obj: object) -> HtmlRenderable:
    """Coerce a supported renderable into an HtmlRenderable.

    Bare plotly ``go.Figure`` instances are wrapped explicitly via
    ``pio.to_html(..., include_plotlyjs='cdn')`` so Cards get the CDN
    bootstrap even though ``Figure`` itself already satisfies the
    ``HtmlRenderable`` protocol. Other ``HtmlRenderable`` values pass
    through unchanged.
    """
    if isinstance(obj, go.Figure):
        return mo.Html(pio.to_html(obj, include_plotlyjs="cdn", full_html=False))
    if isinstance(obj, HtmlRenderable):
        return obj
    raise TypeError(f"Cannot convert {type(obj).__name__} to HTML")


__all__ = ["as_html", "html_block", "rem_to_float"]
