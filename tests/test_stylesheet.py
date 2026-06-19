"""Tests for the precompiled dr.css stylesheet and bootstrap."""

from __future__ import annotations

from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.components.card import Card
from marimo_utils.ui.setup.bootstrap import bootstrap_tailwind
from marimo_utils.ui.setup.stylesheet import DR_CSS, DR_STYLE_BLOCK, stylesheet_path


def test_dr_css_contains_scope_reset_and_custom_widths() -> None:
    assert ":where(.dr-scope" in DR_CSS
    assert "box-sizing:border-box" in DR_CSS
    assert ".w-100{width:25rem}" in DR_CSS
    assert ".w-160{width:40rem}" in DR_CSS
    assert ".border-border" in DR_CSS
    assert ".border{border-width:1px}" in DR_CSS


def test_stylesheet_path_points_at_dr_css() -> None:
    with stylesheet_path() as path:
        assert path.name == "dr.css"
        assert path.is_file()


def test_dr_style_block_wraps_css() -> None:
    assert DR_STYLE_BLOCK.startswith('<style id="dr-styles">')
    assert DR_STYLE_BLOCK.endswith("</style>")


def test_bootstrap_does_not_load_play_cdn() -> None:
    rendered = bootstrap_tailwind()
    html = str(rendered)
    assert "cdn.tailwindcss.com" not in html
    assert "dr-styles" in html


def test_dr_scope_reset_allows_border_utility() -> None:
    from playwright.sync_api import sync_playwright

    card_html = Card(content="Body").render().text
    page_html = f"<!DOCTYPE html><html><head>{DR_STYLE_BLOCK}</head><body>{card_html}</body></html>"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content(page_html)
        border_width = page.locator(".dr-scope .border").first.evaluate(
            "el => getComputedStyle(el).borderTopWidth"
        )
        browser.close()

    assert border_width == "1px"


def test_activehtml_route_includes_styles_for_plotly_card() -> None:
    from dr_widget.inline import ActiveHtml

    from marimo_utils.ui.charts.bar import BarChart, BarItem

    rendered = Card(
        title="Chart",
        content=BarChart(items=[BarItem(label="A", value=1)], height=120),
    ).render()
    assert isinstance(rendered, ActiveHtml)
    html = str(rendered)
    assert 'style id="dr-styles"' in html
    assert "dr-scope" in html
    assert Badge(label="X").render().text.count("dr-scope") == 1
