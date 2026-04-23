from __future__ import annotations

import marimo as mo
from dr_widget.inline import ActiveHtml
from mohtml import div, h3, p, span  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict

from marimo_utils.tw._rendering import html_block
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
    """Shadcn `CardDescription` — `<p>` with `text-sm text-muted-foreground`."""

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


__all__ = ["Badge", "CardDescription", "CardTitle", "DataItem"]
