from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import tailwind_css  # type: ignore[import-untyped]


def bootstrap_tailwind() -> mo.Html | ActiveHtml:
    """Inject the Tailwind Play CDN into the notebook.

    Returns an `ActiveHtml` (not plain `mo.Html`) because the CDN delivery is
    a `<script src=...>` tag and marimo's default HTML path strips script
    nodes. `ActiveHtml` appends external scripts to `document.head` and
    deduplicates by src across widget instances, so evaluating this in
    multiple cells is safe.
    """
    return ActiveHtml(html=str(tailwind_css()))


__all__ = ["bootstrap_tailwind"]
