"""Tests for the precompiled dr.css stylesheet and bootstrap."""

from __future__ import annotations

from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.components.card import Card
from marimo_utils.ui.setup.bootstrap import bootstrap_tailwind
from marimo_utils.ui.setup.stylesheet import DR_CSS, DR_STYLE_BLOCK, stylesheet_path


def test_dr_css_scopes_design_tokens_to_dr_scope() -> None:
    assert ":root {" not in DR_CSS
    assert ":root{" not in DR_CSS
    assert ".dr-scope {\n  --background:" in DR_CSS
    assert ":where(.dr-scope" in DR_CSS
    assert "box-sizing:border-box" in DR_CSS
    assert ".dr-scope .w-100{width:25rem}" in DR_CSS
    assert ".dr-scope .w-160{width:40rem}" in DR_CSS
    assert ".dr-scope .border-border" in DR_CSS
    assert ".dr-scope .border{border-width:1px}" in DR_CSS
    assert "--tone-good-soft:" in DR_CSS
    assert ".dr-scope .bg-tone-good-soft" in DR_CSS
    assert ".dr-scope .border-tone-neutral-solid" in DR_CSS


def test_dr_css_does_not_emit_global_utility_selectors() -> None:
    """Utilities must not match marimo chrome that shares class names."""
    import re

    assert re.search(r"(?<!\.dr-scope )\.flex\{", DR_CSS) is None
    assert re.search(r"(?<!\.dr-scope )\.bg-popover\{", DR_CSS) is None
    assert re.search(r"(?<!\.dr-scope )\.bg-secondary\{", DR_CSS) is None
    assert ".dr-scope .flex{" in DR_CSS
    assert ".dr-scope .bg-popover" in DR_CSS


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
        border_color = page.locator(".dr-scope .border-border").first.evaluate(
            "el => getComputedStyle(el).borderTopColor"
        )
        browser.close()

    assert border_width == "1px"
    assert border_color == "rgb(228, 228, 231)"


def test_badge_has_no_hover_background_change() -> None:
    from playwright.sync_api import sync_playwright

    from marimo_utils.ui.styles import BadgeVariant

    badge_html = Badge(label="Active", variant=BadgeVariant.DEFAULT).render().text
    page_html = f"<!DOCTYPE html><html><head>{DR_STYLE_BLOCK}</head><body>{badge_html}</body></html>"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content(page_html)
        locator = page.locator(".dr-scope div").first
        before = locator.evaluate("el => getComputedStyle(el).backgroundColor")
        locator.hover()
        during = locator.evaluate("el => getComputedStyle(el).backgroundColor")
        browser.close()

    assert before == during


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


def test_badge_to_html_renders_with_precompiled_styles() -> None:
    from playwright.sync_api import sync_playwright

    from marimo_utils.ui.host import plain_html_page
    from marimo_utils.ui.styles import BadgeVariant

    page_html = plain_html_page(
        Badge(label="Active", variant=BadgeVariant.DEFAULT),
        title="badge probe",
        include_runtime=False,
    )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content(page_html)
        page.wait_for_selector('[data-tw-ready="true"]', state="attached")
        page.wait_for_selector('[data-component="badge"]', state="attached")
        locator = page.locator('[data-component="badge"]').first
        border_width = locator.evaluate("el => getComputedStyle(el).borderTopWidth")
        before = locator.evaluate("el => getComputedStyle(el).backgroundColor")
        locator.hover()
        during = locator.evaluate("el => getComputedStyle(el).backgroundColor")
        browser.close()

    assert border_width == "1px"
    assert before == during


def test_utilities_do_not_apply_outside_dr_scope() -> None:
    """Simulate marimo chrome sharing Tailwind-like class names."""
    from playwright.sync_api import sync_playwright

    page_html = f"""<!DOCTYPE html><html><head>{DR_STYLE_BLOCK}
<style>:root {{ --popover: light-dark(#fff, #252927); }}</style>
</head><body>
<div class="flex bg-popover border" id="marimo-chrome">menu</div>
</body></html>"""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content(page_html)
        border_width = page.locator("#marimo-chrome").evaluate(
            "el => getComputedStyle(el).borderTopWidth"
        )
        background = page.locator("#marimo-chrome").evaluate(
            "el => getComputedStyle(el).backgroundColor"
        )
        browser.close()

    assert border_width == "0px"
    assert background in {"rgba(0, 0, 0, 0)", "transparent"}


def test_plotly_card_renders_under_setup_host_styles() -> None:
    from playwright.sync_api import sync_playwright

    from marimo_utils.ui.charts.bar import BarChart, BarItem
    from marimo_utils.ui.setup.bootstrap import bootstrap_tailwind
    from marimo_utils.ui.setup.stylesheet import DR_STYLE_BLOCK

    plotly_card = Card(
        title="Chart",
        content=BarChart(
            items=[BarItem(label="A", value=1), BarItem(label="B", value=2)],
            height=120,
        ),
    ).render()
    page_html = (
        f"<!DOCTYPE html><html><head>{DR_STYLE_BLOCK}</head><body>"
        f"{bootstrap_tailwind()}{plotly_card}</body></html>"
    )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.set_content(page_html)
        page.wait_for_selector(".js-plotly-plot")
        plot = page.locator(".js-plotly-plot").first
        box = plot.bounding_box()
        plotly_scripts = page.locator('script[src*="plotly"]').count()
        border_width = page.locator(".dr-scope .border").first.evaluate(
            "el => getComputedStyle(el).borderTopWidth"
        )
        browser.close()

    assert box is not None
    assert box["width"] > 0
    assert box["height"] > 0
    assert plotly_scripts == 1
    assert border_width == "1px"


_LUMINANCE_JS = """
(el) => {
  const cs = getComputedStyle(el);
  function luminance(color) {
    const parts = color.match(/[\\d.]+/g);
    if (!parts || parts.length < 3) return 0;
    const channels = parts.slice(0, 3).map((value) => {
      const channel = parseFloat(value) / 255;
      return channel <= 0.03928
        ? channel / 12.92
        : Math.pow((channel + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
  }
  return {
    bgLum: luminance(cs.backgroundColor),
    fgLum: luminance(cs.color),
  };
}
"""


def test_tone_surface_renders_with_expected_contrast() -> None:
    from playwright.sync_api import sync_playwright

    from marimo_utils.ui.core.drhtml import div, html_block
    from marimo_utils.ui.styles import ToneEmphasis, ToneSurface

    cases = [
        (ToneSurface.GOOD_SOFT, ToneEmphasis.SOFT),
        (ToneSurface.GOOD_SOLID, ToneEmphasis.SOLID),
        (ToneSurface.BAD_SOFT, ToneEmphasis.SOFT),
        (ToneSurface.BAD_SOLID, ToneEmphasis.SOLID),
        (ToneSurface.NEUTRAL_SOFT, ToneEmphasis.SOFT),
        (ToneSurface.NEUTRAL_SOLID, ToneEmphasis.SOLID),
    ]

    for surface, emphasis in cases:
        swatch = html_block(div("tone", klass=surface)).text
        page_html = (
            f"<!DOCTYPE html><html><head>{DR_STYLE_BLOCK}</head>"
            f"<body>{swatch}</body></html>"
        )

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            page.set_content(page_html)
            locator = page.locator(".dr-scope div").first
            lums = locator.evaluate(_LUMINANCE_JS)
            browser.close()

        assert lums["bgLum"] > 0, surface
        assert lums["fgLum"] < lums["bgLum"], surface
