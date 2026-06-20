"""Plain-HTML page adapter for web reuse and Playwright verification."""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

from marimo_utils.ui.core.component import wrap_dr_scope
from marimo_utils.ui.host._runtime import runtime_script_tag
from marimo_utils.ui.host.tw_ready import (
    MARK_TW_READY_ON_STYLESHEET_JS,
    TW_SENTINEL_HTML,
)
from marimo_utils.ui.setup.stylesheet import DR_CSS, DR_STYLE_BLOCK

if TYPE_CHECKING:
    from marimo_utils.ui.core.component import HtmlComponent


def _render_markup(component: HtmlComponent | str) -> str:
    return component if isinstance(component, str) else component.to_html()


def _html_page_shell(*, title: str, head_content: str, body_markup: str) -> str:
    escaped_title = html.escape(title, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title}</title>
  {head_content}
</head>
<body>
  {TW_SENTINEL_HTML}
  {wrap_dr_scope(body_markup)}
  <script>{MARK_TW_READY_ON_STYLESHEET_JS}</script>
</body>
</html>
"""


def plain_html_page(
    *markup: HtmlComponent | str,
    title: str = "dr probe",
    include_runtime: bool = True,
) -> str:
    """Build a full HTML document shell for web hosts and verification.

    Includes the precompiled stylesheet, optional dr_widget runtime, a
    ``data-tw-ready`` sentinel, and a ``.dr-scope`` wrapper around component
    markup — the same seams marimo probes rely on after ``setup_host()``.
    """
    body = "".join(_render_markup(part) for part in markup)
    runtime = runtime_script_tag() if include_runtime else ""
    return _html_page_shell(
        title=title,
        head_content=f"{DR_STYLE_BLOCK}\n  {runtime}".strip(),
        body_markup=body,
    )


def plain_html_page_with_link(
    *markup: HtmlComponent | str,
    stylesheet_href: str,
    title: str = "dr probe",
    include_runtime: bool = True,
) -> str:
    """Like :func:`plain_html_page` but references an external ``dr.css`` URL."""
    body = "".join(_render_markup(part) for part in markup)
    escaped_href = html.escape(stylesheet_href, quote=True)
    runtime = runtime_script_tag() if include_runtime else ""
    return _html_page_shell(
        title=title,
        head_content=(
            f'<link rel="stylesheet" data-dr-stylesheet="true" href="{escaped_href}">\n'
            f"  {runtime}"
        ).strip(),
        body_markup=body,
    )


def dr_css_text() -> str:
    """Expose bundled stylesheet text for hosts that assemble pages manually."""
    return DR_CSS
