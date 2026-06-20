"""Marimo host adapter: light-DOM rendering via ``mo.Html``."""

from __future__ import annotations

from typing import TYPE_CHECKING

import marimo as mo

from marimo_utils.ui.core.component import wrap_dr_scope

if TYPE_CHECKING:
    from marimo_utils.ui.core.component import HtmlComponent


def show(component: HtmlComponent | str) -> mo.Html:
    """Render component markup into marimo's light DOM.

    Wraps output in ``.dr-scope`` so precompiled styles match the plain-HTML
    host and legacy ``html_block()`` behavior.
    """
    markup = component if isinstance(component, str) else component.to_html()
    return mo.Html(wrap_dr_scope(markup))
