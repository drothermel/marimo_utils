"""Tests for styles.py layout enums and component threading."""

from __future__ import annotations

import marimo as mo

from marimo_utils.ui.card import Card
from marimo_utils.ui.components.badge import Badge
from marimo_utils.ui.components.data_item import DataItem
from marimo_utils.ui.components.lucide_icon import LucideIcon
from marimo_utils.ui.drhtml import cn
from marimo_utils.ui.styles import (
    Background,
    BadgeVariant,
    BORDER,
    CardWidth,
    DivLayouts,
    IconSize,
    Padding,
    SpanLayouts,
)


def test_div_layout_values() -> None:
    assert DivLayouts.COL_SHELL == "self-start flex flex-col gap-1.5"
    assert DivLayouts.COL == "flex flex-col p-6 gap-1.5"
    assert (
        DivLayouts.INLINE_ROW
        == "self-start inline-flex items-center gap-2 flex-wrap"
    )
    assert DivLayouts.KEY_VAL_ROW == "flex items-baseline gap-3"


def test_span_layout_values() -> None:
    assert SpanLayouts.KEY_VAL_LABEL == "inline-block min-w-28"
    assert SpanLayouts.ICON_FRAME == "inline-flex flex-shrink-0"


def test_icon_size_values() -> None:
    assert IconSize.SMALL == "h-4 w-4"
    assert IconSize.MEDIUM == "h-6 w-6"
    assert IconSize.LARGE == "h-8 w-8"


def test_card_width_values() -> None:
    assert CardWidth.NARROW == "w-80"
    assert CardWidth.DEFAULT == "w-100"
    assert CardWidth.WIDE == "w-160"


def test_card_default_width() -> None:
    rendered = Card(content="Body").render()
    assert isinstance(rendered, mo.Html)
    assert CardWidth.DEFAULT in rendered.text


def test_cn_col_pt0_merge() -> None:
    merged = cn(DivLayouts.COL, "pt-0")
    assert "flex flex-col" in merged
    assert "p-6" in merged
    assert "pt-0" in merged
    assert "gap-1.5" in merged


def test_card_col_shell_structure() -> None:
    rendered = Card(
        title="Title",
        description="Desc",
        content="Body",
    ).render()
    assert isinstance(rendered, mo.Html)
    html = rendered.text
    assert "self-start flex flex-col gap-1.5" in html
    assert "flex flex-col p-6 gap-1.5" in html
    assert "pt-0" in html


def test_card_content_only_uses_col_without_pt0() -> None:
    rendered = Card(content="Body").render()
    assert isinstance(rendered, mo.Html)
    html = rendered.text
    assert "flex flex-col p-6 gap-1.5" in html
    assert "pt-0" not in html


def test_badge_variant_values() -> None:
    assert "bg-primary" in BadgeVariant.DEFAULT
    assert "bg-secondary" in BadgeVariant.SECONDARY
    assert "bg-destructive" in BadgeVariant.DESTRUCTIVE
    assert "text-foreground" in Background.OUTLINE
    assert "hover:bg-accent" in Background.OUTLINE
    assert "border-border" in BORDER
    assert "shadow-sm" in BORDER
    assert Padding.BADGE == "px-2.5 py-0.5"


def test_badge_renders_div_with_inline_row() -> None:
    rendered = Badge(label="Active").render()
    assert isinstance(rendered, mo.Html)
    html = rendered.text
    assert "<div" in html
    assert "inline-flex items-center gap-2 flex-wrap" in html
    assert "border-border" in html
    assert "text-sm" in html
    assert "font-semibold" in html
    assert ">Active</div>" in html


def test_data_item_key_val_layouts() -> None:
    rendered = DataItem(label="Status", value="Active").render()
    assert isinstance(rendered, mo.Html)
    html = rendered.text
    assert "items-baseline gap-3" in html
    assert "min-w-28" in html


def test_lucide_icon_frame_and_size() -> None:
    rendered = LucideIcon(name="calendar").render()
    assert isinstance(rendered, mo.Html)
    html = rendered.text
    assert "inline-flex flex-shrink-0" in html
    assert "h-4 w-4" in html
