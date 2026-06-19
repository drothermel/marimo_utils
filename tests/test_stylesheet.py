"""Tests for the precompiled dr.css stylesheet and bootstrap."""

from __future__ import annotations

from marimo_utils.ui.setup.bootstrap import bootstrap_tailwind
from marimo_utils.ui.setup.stylesheet import DR_CSS, DR_STYLE_BLOCK, stylesheet_path


def test_dr_css_contains_scope_reset_and_custom_widths() -> None:
    assert ".dr-scope" in DR_CSS
    assert "box-sizing:border-box" in DR_CSS
    assert ".w-100{width:25rem}" in DR_CSS
    assert ".w-160{width:40rem}" in DR_CSS
    assert ".border-border" in DR_CSS


def test_stylesheet_path_points_at_dr_css() -> None:
    assert stylesheet_path().name == "dr.css"
    assert stylesheet_path().is_file()


def test_dr_style_block_wraps_css() -> None:
    assert DR_STYLE_BLOCK.startswith('<style id="dr-styles">')
    assert DR_STYLE_BLOCK.endswith("</style>")


def test_bootstrap_does_not_load_play_cdn() -> None:
    rendered = bootstrap_tailwind()
    html = str(rendered)
    assert "cdn.tailwindcss.com" not in html
    assert "dr-styles" in html
