"""Tests for Card to_html() composition."""

from __future__ import annotations

from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.components.card import Card
from marimo_utils.ui.styles import BadgeVariant


def test_card_to_html_includes_title_and_badge_child() -> None:
    html = Card(
        title="Metrics",
        description="Run summary",
        content=Badge(label="ok", variant=BadgeVariant.SECONDARY),
    ).to_html()
    assert "<h3" in html
    assert "Metrics" in html
    assert "Run summary" in html
    assert 'data-component="card"' in html
    assert 'data-component="badge"' in html
    assert ">ok</div>" in html


def test_card_to_html_does_not_include_dr_scope_wrapper() -> None:
    card = Card(title="Title", content="Body")
    to_html = card.to_html()
    assert "Title" in to_html
    assert "Body" in to_html
    assert "dr-scope" not in to_html
