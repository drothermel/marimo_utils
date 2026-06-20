"""Host adapters for marimo and plain-HTML verification surfaces."""

from __future__ import annotations

from dr_widget.inline import ActiveHtml, load_dr_runtime

from marimo_utils.ui.core.component import HtmlComponent, MarkupComponent
from marimo_utils.ui.host.marimo import show
from marimo_utils.ui.host.tw_ready import DATA_TW_READY, TW_READY_SELECTOR
from marimo_utils.ui.host.verification import COMPONENT_SELECTOR, selectors_for_dump
from marimo_utils.ui.host.web import (
    dr_css_text,
    plain_html_page,
    plain_html_page_with_link,
)


def setup_host() -> tuple[ActiveHtml, ActiveHtml]:
    """One-time notebook bootstrap: dr_widget runtime plus scoped styles."""
    from marimo_utils.ui.setup.bootstrap import bootstrap_tailwind  # noqa: PLC0415

    return (load_dr_runtime(), bootstrap_tailwind())


__all__ = [
    "COMPONENT_SELECTOR",
    "DATA_TW_READY",
    "TW_READY_SELECTOR",
    "HtmlComponent",
    "MarkupComponent",
    "dr_css_text",
    "load_dr_runtime",
    "plain_html_page",
    "plain_html_page_with_link",
    "selectors_for_dump",
    "setup_host",
    "show",
]
