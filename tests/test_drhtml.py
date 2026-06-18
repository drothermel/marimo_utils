"""Tests for drhtml tag builders."""

from __future__ import annotations

import marimo as mo

from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.components.labeled_list import LabeledList
from marimo_utils.ui.drhtml import br, cn, div, p, span
from marimo_utils.ui.rendering import render_inline
from marimo_utils.ui.styles import DivLayouts


def test_basic_div_p() -> None:
    assert str(div(p("hello"))) == "<div><p>hello</p></div>"


def test_basic_div_p_br() -> None:
    assert str(div(p("hello"), br())) == "<div><p>hello</p><br/></div>"


def test_klass_maps_to_class() -> None:
    assert (
        str(div(p("hello"), klass="foo bar"))
        == '<div class="foo bar"><p>hello</p></div>'
    )


def test_klass_merges_conflicting_tailwind_utilities() -> None:
    rendered = str(span("x", klass="text-sm text-muted-foreground text-lg"))
    assert 'class="text-muted-foreground text-lg"' in rendered
    assert "text-sm" not in rendered


def test_klass_then_class_prefers_class_for_conflicts() -> None:
    rendered = str(
        span(
            "x",
            klass="text-sm font-medium",
            **{"class": "text-lg font-semibold"},
        )
    )
    assert 'class="text-lg font-semibold"' in rendered
    assert "text-sm" not in rendered
    assert "font-medium" not in rendered


def test_cn_merges_layout_enum_with_override() -> None:
    merged = cn(DivLayouts.COL, "pt-0")
    assert "p-6" in merged
    assert "pt-0" in merged


def test_nested_mo_html_child() -> None:
    badge_html = Badge(label="X").render()
    rendered = str(div(span("Tags:"), badge_html, klass="container"))
    assert "Html()" not in rendered
    assert ">X</div>" in rendered


def test_labeled_list_composes_badges() -> None:
    rendered = LabeledList(
        label="Tags",
        items=[Badge(label="A"), Badge(label="B")],
    ).render()
    assert isinstance(rendered, mo.Html)
    assert ">A</div>" in rendered.text
    assert ">B</div>" in rendered.text


def test_render_inline_bold_and_breaks() -> None:
    nodes = render_inline("line one\n**bold** tail")
    rendered = str(p(*nodes))
    assert "<br/>" in rendered
    assert "<strong>bold</strong>" in rendered
