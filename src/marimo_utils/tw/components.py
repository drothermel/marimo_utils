from __future__ import annotations

from datetime import datetime

import marimo as mo
from dr_widget.inline import ActiveHtml
from lucide import lucide_icon  # type: ignore[import-untyped]
from mohtml import div, h3, p, span  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.tw._rendering import auto_render, html_block
from marimo_utils.tw.variants import BADGE_BASE, BADGE_VARIANT_CLASSES, BadgeVariant


class Badge(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    variant: BadgeVariant = BadgeVariant.DEFAULT
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        parts = [BADGE_BASE, BADGE_VARIANT_CLASSES[self.variant]]
        if self.klass:
            parts.append(self.klass)
        classes = " ".join(parts)
        return html_block(span(self.label, klass=classes))


class CardTitle(BaseModel):
    """Shadcn `CardTitle`: `<h3>` with `text-2xl font-semibold leading-none`."""

    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        base = "text-2xl font-semibold leading-none tracking-tight"
        classes = f"{base} {self.klass}" if self.klass else base
        return html_block(h3(self.text, klass=classes))


class CardDescription(BaseModel):
    """Shadcn `CardDescription`: `<p>` with `text-sm text-muted-foreground`."""

    model_config = ConfigDict(frozen=True)

    text: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        base = "text-sm text-muted-foreground"
        classes = f"{base} {self.klass}" if self.klass else base
        return html_block(p(self.text, klass=classes))


class DataItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: str
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        container = "flex items-baseline gap-3"
        if self.klass:
            container = f"{container} {self.klass}"
        return html_block(
            div(
                span(
                    self.label,
                    klass=(
                        "inline-block min-w-28 text-xs font-medium "
                        "uppercase tracking-wide text-muted-foreground"
                    ),
                ),
                span(
                    self.value,
                    klass="text-sm font-semibold text-foreground",
                ),
                klass=container,
            )
        )


class LucideIcon(BaseModel):
    """Lucide icon rendered as an SVG inside an `inline-flex` span.

    `size` carries Tailwind height/width utilities (default `h-4 w-4`); the
    SVG fills the span at `100%` so resizing is driven by the utility class,
    not pixel attributes. `stroke="currentColor"` makes the icon color
    inherit from any `text-*` utility on an ancestor — a Badge tone, a
    muted meta row, etc. — without an explicit color prop here.

    Designed as the standalone primitive that other icon-bearing components
    (`DateStamp`, `ProjectStamp`, future icon-aware Badges) compose.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    size: str = "h-4 w-4"
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        svg = lucide_icon(
            self.name,
            width="100%",
            height="100%",
            stroke_width="2",
            stroke="currentColor",
        )
        wrapper = f"inline-flex flex-shrink-0 {self.size}"
        if self.klass:
            wrapper = f"{wrapper} {self.klass}"
        return html_block(span(svg, klass=wrapper))


class DateStamp(BaseModel):
    """Inline icon + date meta row — shadcn's `flex items-center gap-2 muted` idiom."""

    model_config = ConfigDict(frozen=True)

    value: datetime | None
    icon_name: str = "calendar"
    klass: str | None = None

    def _text(self) -> str:
        if self.value is None:
            return "--- --"
        return self.value.strftime("%b %d")

    def render(self) -> mo.Html | ActiveHtml:
        container = "inline-flex items-center gap-2 text-sm text-muted-foreground"
        if self.klass:
            container = f"{container} {self.klass}"
        return html_block(
            div(
                LucideIcon(name=self.icon_name).render(),
                span(self._text()),
                klass=container,
            )
        )


class ProjectStamp(BaseModel):
    """Inline icon + project-name meta row — sibling of `DateStamp`."""

    model_config = ConfigDict(frozen=True)

    project_name: str
    icon_name: str = "folder"
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        container = "inline-flex items-center gap-2 text-sm text-muted-foreground"
        if self.klass:
            container = f"{container} {self.klass}"
        return html_block(
            div(
                LucideIcon(name=self.icon_name).render(),
                span(self.project_name),
                klass=container,
            )
        )


class LabeledList(BaseModel):
    """Section label prefix + flex-wrapping list of rendered items.

    Label uses shadcn's muted inline-label style (`text-sm font-medium
    text-muted-foreground`) rather than the form-coupled `Label` primitive.
    Items are auto-rendered (any component with `.render()`) or passed
    through for string coercion by mohtml.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    label: str
    items: list[object]
    klass: str | None = None

    def render(self) -> mo.Html | ActiveHtml:
        container = "inline-flex flex-wrap items-center gap-2"
        if self.klass:
            container = f"{container} {self.klass}"
        rendered_items = [auto_render(item) for item in self.items]
        return html_block(
            div(
                span(
                    f"{self.label}:",
                    klass="text-sm font-medium text-muted-foreground",
                ),
                *rendered_items,
                klass=container,
            )
        )


__all__ = [
    "Badge",
    "CardDescription",
    "CardTitle",
    "DataItem",
    "DateStamp",
    "LabeledList",
    "LucideIcon",
    "ProjectStamp",
]
