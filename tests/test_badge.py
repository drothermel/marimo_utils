"""Tests for Badge to_html() and legacy render()."""

from __future__ import annotations

import marimo as mo
import pytest

from marimo_utils.ui.components.badge import (
    Badge,
    bad_badge,
    bool_badge,
    good_badge,
    neutral_badge,
)
from marimo_utils.ui.host import show
from marimo_utils.ui.styles import BadgeVariant, SemanticTone, ToneEmphasis


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


@pytest.mark.parametrize(
    ("builder", "tone_class"),
    [
        (good_badge, "bg-tone-good-soft"),
        (bad_badge, "bg-tone-bad-soft"),
        (neutral_badge, "bg-tone-neutral-soft"),
    ],
)
def test_semantic_badge_builders_emit_tone_classes(
    builder,
    tone_class: str,
) -> None:
    html = builder("ok").to_html()
    assert 'data-component="badge"' in html
    assert tone_class in html
    assert "ok" in html
    assert "bg-primary" not in html
    assert "bg-secondary" not in html


def test_semantic_badge_solid_emphasis() -> None:
    html = good_badge("done", emphasis=ToneEmphasis.SOLID).to_html()
    assert "bg-tone-good-solid" in html


def test_bool_badge_good_when_true() -> None:
    assert "bg-tone-good-soft" in bool_badge(True, true_label="pass").to_html()
    assert "bg-tone-bad-soft" in bool_badge(False, false_label="fail").to_html()


def test_bool_badge_inverts_polarity_when_good_when_true_false() -> None:
    assert "bg-tone-bad-soft" in bool_badge(
        True, good_when_true=False, true_label="alert"
    ).to_html()
    assert "bg-tone-good-soft" in bool_badge(
        False, good_when_true=False, false_label="clear"
    ).to_html()


def test_bool_badge_skipped_false_neutral_pattern() -> None:
    html = bool_badge(
        False,
        good_when_true=True,
        true_label="done",
        false_label="skipped",
        false_tone=SemanticTone.NEUTRAL,
    ).to_html()
    assert "skipped" in html
    assert "bg-tone-neutral-soft" in html
