"""Tests for Badge to_html() and legacy render()."""

from __future__ import annotations

import marimo as mo

from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.host import show
from marimo_utils.ui.styles import BadgeVariant


def test_badge_to_html_emits_dr_badge_with_verification_hooks() -> None:
    html = Badge(label="Active", variant=BadgeVariant.DEFAULT).to_html()
    assert "<dr-badge" in html
    assert 'data-component="dr-badge"' in html
    assert "data-props=" in html
    assert '"label":"Active"' in html
    assert "bg-primary" in html


def test_badge_render_still_uses_legacy_div_markup() -> None:
    rendered = Badge(label="Active", variant=BadgeVariant.DEFAULT).render()
    assert isinstance(rendered, mo.Html)
    assert "<div" in rendered.text
    assert "dr-badge" not in rendered.text
    assert "Active" in rendered.text


def test_show_badge_wraps_custom_element_in_dr_scope() -> None:
    rendered = show(Badge(label="Active", variant=BadgeVariant.OUTLINE))
    assert isinstance(rendered, mo.Html)
    assert rendered.text.startswith('<div class="dr-scope"><dr-badge')
    assert rendered.text.endswith("</dr-badge></div>")
