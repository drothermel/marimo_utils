"""Tests for Badge to_html() and legacy render()."""

from __future__ import annotations

import marimo as mo

from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.host import show
from marimo_utils.ui.styles import BadgeVariant


def test_badge_to_html_emits_static_div_with_verification_hook() -> None:
    html = Badge(label="Active", variant=BadgeVariant.DEFAULT).to_html()
    assert html.startswith("<div")
    assert 'data-component="badge"' in html
    assert "Active" in html
    assert "bg-primary" in html
    assert "dr-badge" not in html


def test_badge_render_still_uses_legacy_div_markup() -> None:
    rendered = Badge(label="Active", variant=BadgeVariant.DEFAULT).render()
    assert isinstance(rendered, mo.Html)
    assert "<div" in rendered.text
    assert "Active" in rendered.text
    assert "dr-scope" in rendered.text


def test_badge_to_html_omits_dr_scope_wrapper() -> None:
    html = Badge(label="Active", variant=BadgeVariant.DEFAULT).to_html()
    assert "dr-scope" not in html


def test_show_badge_wraps_static_markup_in_dr_scope() -> None:
    rendered = show(Badge(label="Active", variant=BadgeVariant.OUTLINE))
    assert isinstance(rendered, mo.Html)
    assert rendered.text.startswith('<div class="dr-scope"><div')
    assert 'data-component="badge"' in rendered.text
    assert rendered.text.endswith("Active</div></div>")
